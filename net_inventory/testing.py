devices = {0: {'Parent ID': None, 'Device Type': 'Router', 'Hostname': None, 'Neighbors': {'GigabitEthernet0/0/0': ['GigabitEthernet0/1', '192.168.1.2'], 'GigabitEthernet0/4/3': ['GigabitEthernet0/1', '192.168.1.2'], 'GigabitEthernet0/0/1': ['GigabitEthernet0/1', '192.168.1.2']}, 'Interfaces': {'GigabitEthernet0/0/0': '192.168.1.1', 'GigabitEthernet0/0/1': 'unassigned', 'GigabitEthernet0/0/2': 'unassigned', 'GigabitEthernet0/0/3': 'unassigned'}}, 1: {'Parent ID': 0, 'Device Type': 'Switch', 'Hostname': None, 'Neighbors': {'GigabitEthernet0/1': ['GigabitEthernet0/4/3', '192.168.1.1']}, 'Interfaces': {'Vlan1': '192.168.1.2', 'FastEthernet0/1': 'unassigned', 'FastEthernet0/2': 'unassigned', 'FastEthernet0/3': 'unassigned', 'FastEthernet0/4': 'unassigned', 'FastEthernet0/5': 'unassigned', 'FastEthernet0/6': 'unassigned', 'FastEthernet0/7': 'unassigned', 'FastEthernet0/8': 'unassigned', 'FastEthernet0/9': 'unassigned', 'FastEthernet0/10': 'unassigned', 'FastEthernet0/11': 'unassigned', 'FastEthernet0/12': 'unassigned', 'FastEthernet0/13': 'unassigned', 'FastEthernet0/14': 'unassigned', 'FastEthernet0/15': 'unassigned', 'FastEthernet0/16': 'unassigned', 'FastEthernet0/17': 'unassigned', 'FastEthernet0/18': 'unassigned', 'FastEthernet0/19': 'unassigned', 'FastEthernet0/20': 'unassigned', 'FastEthernet0/21': 'unassigned', 'FastEthernet0/22': 'unassigned', 'FastEthernet0/23': 'unassigned', 'FastEthernet0/24': 'unassigned', 'GigabitEthernet0/1': 'unassigned', 'GigabitEthernet0/2': 'unassigned'}}}

def extract_neighbors_values(devices):
    neighbors_values = {}
    for device_number, device_info in devices.items():
        neighbors = device_info.get('Neighbors', {})
        neighbors_values[device_number] = [[key, value[0]] for key, value in neighbors.items()]
    return neighbors_values

def extract_id_parent_pairs(devices):
    id_parent_pairs = {}
    for device_id, device_info in devices.items():
        parent_id = device_info.get('Parent ID')
        if parent_id is not None:
            id_parent_pairs[device_id] = parent_id
    return id_parent_pairs

id_parent_pairs = extract_id_parent_pairs(devices)
neighbors_values = extract_neighbors_values(devices)
print(id_parent_pairs)
print(neighbors_values)

def compare_neighbors_with_parent(id_parent_pairs, neighbors_values):
    flipped_pairs = {}
    for device_id, parent_id in id_parent_pairs.items():
        flipped_pairs[device_id] = []
        if device_id in neighbors_values:
            device_neighbors = neighbors_values[device_id]
            for neighbor_pair in device_neighbors:
                flipped_pair = neighbor_pair[::-1]  # Reversing the order of items in the pair
                if flipped_pair in neighbors_values.get(parent_id, []):
                    flipped_pairs[device_id].append(flipped_pair)
    return flipped_pairs

flipped_pairs = compare_neighbors_with_parent(id_parent_pairs, neighbors_values)
print(flipped_pairs)

def fill_connection_dict(id_parent_pairs, flipped_pairs):
    connection_list = []
    for device_id, parent_id in id_parent_pairs.items():
        if device_id in flipped_pairs:
            flipped_neighbor = flipped_pairs[device_id][0]  # Taking the first flipped neighbor pair
            connection_dict = {
                'from': parent_id,
                'to': device_id,
                'fromLabel': flipped_neighbor[0],
                'toLabel': flipped_neighbor[1]
            }
            connection_list.append(connection_dict)
    return connection_list

connection_dict = fill_connection_dict(id_parent_pairs, flipped_pairs)
print(connection_dict)