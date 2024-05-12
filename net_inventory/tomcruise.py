from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException, NetMikoAuthenticationException

def ConnectAndExtract(device_ip, username, password):
    # Define device parameters for SSH connection
    device = {
        "device_type": "cisco_ios",
        "ip": device_ip,
        "username": username,
        "password": password,
    }

    net_connect = None  # Initialize net_connect outside try block

    try:
        net_connect = ConnectHandler(**device)  # Establish SSH connection

        # Send commands to retrieve outputs
        cdp_output = net_connect.send_command("show cdp neighbor detail")
        int_brief_output = net_connect.send_command("show ip interface brief")
        show_version_output = net_connect.send_command("show version")
        
        return cdp_output, int_brief_output, show_version_output

    except NetMikoTimeoutException as e:
        print(f"Connection to {device_ip} timed out: {e}")
    except NetMikoAuthenticationException as e:
        print(f"Authentication failed for {device_ip}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if net_connect:
            net_connect.disconnect()

# Initial connection
device_ip = "192.168.30.31"
username = "gmedina"
password = "cisco"