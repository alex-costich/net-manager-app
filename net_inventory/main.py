import extractors
import tomcruise
import planter
import json

queue = []
history = []
devices = {}
id_count = 0

def CDParse(ip_address, parent):
    global queue
    global devices
    global history
    global id_count

    username = "gmedina"
    password = "cisco"
    
    cdp_output, int_brief_output, show_version_output = tomcruise.ConnectAndExtract(ip_address, username, password)

    device_data = {}
    neighbor_ips = []
    unique_id = id_count
    id_count += 1
    
    devices[unique_id] = device_data
    device_data["Parent ID"] = parent
    device_data["Device Type"] = extractors.ExtractDeviceType(int_brief_output)
    device_data["Hostname"] = extractors.ExtractHostname(show_version_output)
    device_data["Neighbors"] = extractors.CdpToDict(cdp_output)
    device_data["Interfaces"] = extractors.IntBriefToDict(int_brief_output)
    
    extractors.ExtractIpsForHistory(history, device_data, ip_address)

    extractors.ExtractNeighborIps(neighbor_ips, device_data)

    queue.extend(neighbor_ips)
    
    #print(f"Device data: {device_data}")
    
    while queue and queue[0] in history:
        queue.pop(0)
    if queue:
        CDParse(queue[0], unique_id)
    
ip_address = "192.168.30.31"
CDParse(ip_address, None)

#print(f"Queue: {queue}")
#print(f"History: {history}")
print(devices)

id_parent_pairs = planter.extract_id_parent_pairs(devices)
neighbors_values = planter.extract_neighbors_values(devices)
flipped_pairs = planter.compare_neighbors_with_parent(id_parent_pairs, neighbors_values)
connection_dict = planter.fill_connection_dict(id_parent_pairs, flipped_pairs)

# Convert Python dictionary to JSON string without single quotes
json_data = json.dumps(connection_dict)

print(json_data)