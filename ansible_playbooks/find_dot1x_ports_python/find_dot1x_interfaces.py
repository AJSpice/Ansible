import os
from netmiko import ConnectHandler
import csv

# open the inventory csv file and assign keys,values to the dict
def define_inventory():

    #empty dict for all devices
    devices = {}

    # open the inventory csv
    with open("inventory.csv", "r", encoding="utf-8") as f:
        inventory = csv.DictReader(f)
        for row in inventory:
            hostname = row["hostname"]
            ip_address = row["ip_address"]
            devices[hostname] = ip_address

    return devices

# gets all physical interfaces on the switch
def get_all_interfaces(connection):

    # cli commands to run
    config_commands = ["sh run | incl interface"]
    # runs the cli commands
    output = connection.send_config_set(config_commands)

    # parse the cli output
    output_lines = output.split("\n")
    return output_lines[3:-2]

# gets the running config of every interface from previous function
def get_interface_configs(connection, interfaces_list):

    # empty dict of interface configs
    interface_configs_dict = {}

    # loop through every interface from previous function
    for interface in interfaces_list:
        # remove logical interfaces
        if "mgmt" not in interface and "vlan" not in interface and "interface" in interface:
            # cli commands to run
            config_commands = [f"sh run {interface}"]
            # send the commands
            output = connection.send_config_set(config_commands)

            # format/parse the output
            output_lines = output.split("\n")
            desired_lines = output_lines[3:-2]

            # appends the formatted output to the dict
            interface_configs_dict[interface] = desired_lines
    return interface_configs_dict

# parses dict from previous function to find dot1x ports
def find_all_dot1x_ports(interface_configs_dict):

    # empty dict
    dot1x_interfaces = {}

    for interface, config_list in interface_configs_dict.items():

        # format the dict from previous function
        config = "\n".join(config_list)
        # find the aaa or port-access ports
        if "aaa" in config and "port-access" in config:
            dot1x_interfaces[interface] = config
    return dot1x_interfaces

# writes all aaa or port-access ports from previous function to a csv file per device 
def write_ports_to_csv(hostname, ip_address, dot1x_interfaces):
    # define csv path
    csv_path = f"aaa_interfaces.csv"

    # open the csv
    with open(csv_path, "a", newline="", encoding="utf-8") as f:

        # define the rows of the csv
        rows = ["device", "ip_address", "interface", "config"]
        writer = csv.DictWriter(f, fieldnames=rows)
        writer.writeheader()

        # loop through dot1x interfaces from previous function
        for interface, config in dot1x_interfaces.items():
            row = {"interface": interface, "config": config}
            row["device"] = hostname
            row["ip_address"] = ip_address
            # write to the csv the above data
            writer.writerow(row)

# connect to each device from the inventory and run the functions
def main():

    # define the devices
    devices = define_inventory()

    # loop through the devices
    for hostname, ip_address in devices.items():

        # connection info
        aruba_6300 = {
            "device_type": "aruba_osswitch",
            "ip": ip_address,
            "username": "username", # <-- change this
            "password": "passsword", # <-- change this
            "session_log": "session.log",
            "fast_cli": False,
            "allow_auto_change": True,
        }
        connection = ConnectHandler(**aruba_6300)
        # timeout
        connection.global_delay_factor = 20


        # gets the interfaces from the switch
        interfaces_list = get_all_interfaces(connection)
        # gets the interface configs of the switch
        interface_configs_dict = get_interface_configs(connection, interfaces_list)

        # sorts through interface configs to find aaa or port-access ports
        dot1x_interfaces = find_all_dot1x_ports(interface_configs_dict)
        # writes those ports to a csv per device
        write_ports_to_csv(hostname, ip_address, dot1x_interfaces)

if __name__ == "__main__":
    main()
