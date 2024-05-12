def IntBriefToDict(int_brief_output):
    """
    Returns a dictionary where the keys are interface names and the values are their corresponding IP addresses.
    """
    interface_ip_pairs = {}
    
    try:
        # Split the input text into lines and iterate over each line
        for line in int_brief_output.strip().splitlines()[1:]:
            # Split each line into words
            words = line.split()
            if len(words) >= 2:  # Ensure there are at least two words in the line
                # Extract interface and IP address and add them to the dictionary
                interface_ip_pairs[words[0]] = words[1]
    except Exception as e:
        print(f"Error: {e}")
        
    return interface_ip_pairs

def CdpToDict(cdp_output):
    """
    Returns a dictionary where the keys are local interface names and the values are arrays containing neighboring interface names and their corresponding IP addresses.
    """
    neighbors = {} # Initialize a list to store neighborhood information
    
    try:
        output_lines = cdp_output.splitlines() # Split the output into lines

        for line in output_lines:
            if "IP address" in line:
                neighbor_info = []  # Initialize list to store neighbor information
                neighbor_ip = line.split(":")[1].strip()
            elif "Interface" in line:
                interface_data = line.split(",")
                home_port = interface_data[0].split(":")[1].strip()
                away_port = interface_data[1].split(":")[1].strip()
                neighbor_info = [away_port, neighbor_ip]  # Store neighbor interface and IP as a tuple
                neighbors[home_port] = neighbor_info  # Store the neighbor information under the home port
    except Exception as e:
        print(f"Error: {e}")
            
    return neighbors

def ExtractHostname(show_version_output):
    """
    Extracts and returns the device hostname from the output of the 'show version' command.
    """
    hostname = None
    
    try:
        lines = show_version_output.splitlines()
        for line in lines:
            if 'hostname' in line.lower():
                hostname = line.split(":")[-1].strip()
                break
    except Exception as e:
        print(f"Error: {e}")
    
    return hostname
       
def ExtractDeviceType(int_brief_output):
    """
    Extracts and returns hostname if it exists from output of int brief command.
    """
    device_type = "Unknown"
    
    try: 
        lines = int_brief_output.strip().splitlines()

        # Check if the number of lines in the output is greater than 10
        if len(lines) > 10:
            device_type = "Switch"
        else:
            device_type = "Router"
            
        return device_type
    except Exception as e:
        print(f"Error: {e}")
    
    return device_type
            
def ExtractIpsForHistory(history, device_data, entry_ip):
    try:  
        interfaces = device_data.get("Interfaces", {})
        for interface, ip_address in interfaces.items():
            if ip_address != "unassigned":
                history.append(ip_address)
    except Exception as e:
        print(f"Error: {e}")
        history.append(entry_ip)
        
    return history

def ExtractNeighborIps(neighbor_ips, device_data):
    try:
        neighbors = device_data.get("Neighbors", {})
        for neighbor_interface, neighbor_info in neighbors.items():
            neighbor_ip = neighbor_info[1]  # Neighbor IP address is the second item in the neighbor_info list
            neighbor_ips.append(neighbor_ip)
    except Exception as e:
        print(f"Error: {e}")
        
    return neighbor_ips