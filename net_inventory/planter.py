
"""
devices = {
    0: {
        'Parent ID': None,
        'Device Type': 'Router',
        'Hostname': None,
        'Neighbors': {
            'GigabitEthernet0/0/0': ['GigabitEthernet0/1', '192.168.1.2'],
            'GigabitEthernet0/4/3': ['GigabitEthernet0/1', '192.168.1.2'],
            'GigabitEthernet0/0/1': ['GigabitEthernet0/1', '192.168.1.2']
        },
        'Interfaces': {
            'GigabitEthernet0/0/0': '192.168.1.1',
            'GigabitEthernet0/0/1': 'unassigned',
            'GigabitEthernet0/0/2': 'unassigned',
            'GigabitEthernet0/0/3': 'unassigned'
        }
    },
    1: {
        'Parent ID': 0,
        'Device Type': 'Switch',
        'Hostname': None,
        'Neighbors': {
            'GigabitEthernet0/1': ['GigabitEthernet0/4/3', '192.168.1.1']
        },
        'Interfaces': {
            'Vlan1': '192.168.1.2',
            'FastEthernet0/1': 'unassigned',
            'FastEthernet0/2': 'unassigned',
            'FastEthernet0/3': 'unassigned',
            'FastEthernet0/4': 'unassigned',
            'FastEthernet0/5': 'unassigned',
            'FastEthernet0/6': 'unassigned',
            'FastEthernet0/7': 'unassigned',
            'FastEthernet0/8': 'unassigned',
            'FastEthernet0/9': 'unassigned',
            'FastEthernet0/10': 'unassigned',
            'FastEthernet0/11': 'unassigned',
            'FastEthernet0/12': 'unassigned',
            'FastEthernet0/13': 'unassigned',
            'FastEthernet0/14': 'unassigned',
            'FastEthernet0/15': 'unassigned',
            'FastEthernet0/16': 'unassigned',
            'FastEthernet0/17': 'unassigned',
            'FastEthernet0/18': 'unassigned',
            'FastEthernet0/19': 'unassigned',
            'FastEthernet0/20': 'unassigned',
            'FastEthernet0/21': 'unassigned',
            'FastEthernet0/22': 'unassigned',
            'FastEthernet0/23': 'unassigned',
            'FastEthernet0/24': 'unassigned',
            'GigabitEthernet0/1': 'unassigned',
            'GigabitEthernet0/2': 'unassigned'
        }
    },
    2: {  # New device with ID 2
        'Parent ID': 0,
        'Device Type': 'Switch',
        'Hostname': None,
        'Neighbors': {
            'GigabitEthernet0/1': ['GigabitEthernet0/4/3', '192.168.1.1']
        },
        'Interfaces': {
            'Vlan1': '192.168.1.2',
            'FastEthernet0/1': 'unassigned',
            'FastEthernet0/2': 'unassigned',
            # Add more interfaces if needed
        }
    },
    3: {  # New device with ID 3
        'Parent ID': 2,  # Assigning Parent ID to an existing device
        'Device Type': 'Router',
        'Hostname': None,
        'Neighbors': {
            'GigabitEthernet0/1': ['GigabitEthernet0/4/3', '192.168.1.1']
        },
        'Interfaces': {
            'GigabitEthernet0/0/0': '192.168.1.1',
            'GigabitEthernet0/0/1': 'unassigned',
            # Add more interfaces if needed
        }
    }
}

"""

def extract_neighbors_values(devices):
    return {device_number: [[key, value[0]] for key, value in device_info.get('Neighbors', {}).items()] for device_number, device_info in devices.items()}

def extract_id_parent_pairs(devices):
    return {device_id: device_info.get('Parent ID') for device_id, device_info in devices.items() if device_info.get('Parent ID') is not None}

def compare_neighbors_with_parent(id_parent_pairs, neighbors_values):
    flipped_pairs = {}
    for device_id, parent_id in id_parent_pairs.items():
        flipped_pairs[device_id] = []
        if device_id in neighbors_values:
            device_neighbors = neighbors_values[device_id]
            flipped_pairs[device_id] = [neighbor_pair for neighbor_pair in device_neighbors if neighbor_pair[::-1] in neighbors_values.get(parent_id, [])]
    return flipped_pairs

def fill_connection_dict(id_parent_pairs, flipped_pairs):
    return [{'id': -(index + 1), 'from': parent_id, 'to': device_id, 'fromLabel': flipped_pairs[device_id][0][1], 'toLabel': flipped_pairs[device_id][0][0]} for index, (device_id, parent_id) in enumerate(id_parent_pairs.items()) if device_id in flipped_pairs and flipped_pairs[device_id]]
