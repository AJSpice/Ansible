import os
from jinja2 import Template
import csv
import yaml

# defines the current working directory
cwd = os.getcwd()
# defines the path to the csv files
csvs = os.path.join(cwd, "csv_files")
# defines the path to the js files
j2s = os.path.join(cwd, "jinja_templates")
# defines the path to the generated_configs dir
generated_configs_path = os.path.join(cwd, "generated_configs")
# defines the path to the applied_configs dir
applied_configs_path = os.path.join(cwd, "applied_configs")


# define function to create a base config for a 6300 model
def prov_base_config_6300(output_dir):

    # define the j2 and csv file
    base_config_j2 = os.path.join(cwd, j2s, "prov_6300-template.j2")
    base_config_csv = os.path.join(cwd, csvs, "base_config.csv")

    # open the js template file to modify it
    with open(base_config_j2) as f:
        # use the jinja module to template the file
        config_template = Template(f.read(), keep_trailing_newline=True)

    # open the csv
    with open(base_config_csv) as f:
        # use the csv module to read the info
        base_config_csv_opened = csv.DictReader(f)
        # create a dictionary to store the base config of each device
        device_configs = {}
        for row in base_config_csv_opened:
            
            device = row["switch_hostname"]

            #create a new entry in the dictionary for each device, if it doesn't exist already
            if device not in device_configs:
                device_configs[device] = ""

            # generate the base configuration for this device using the Jinja template
            base_config = config_template.render(
                switch_hostname=row["switch_hostname"],
                mgmt_vlan=row["mgmt_vlan"],
                mgmt_vlan_name=row["mgmt_vlan_name"],
                mgmt_ip=row["mgmt_ip"],
                mgmt_ip_cidr=row["mgmt_ip_cidr"],
                gateway_ip=row["gateway_ip"],            
                system_location=row["system_location"]
            )

            # append this interface configuration to the configuration for this device
            device_configs[device] += base_config

        # save the base configurations for each device to a separate file
        for device, config in device_configs.items():
            output_path = os.path.join(output_dir, f"{device}_base_config.aos")
            with open(output_path, "w") as f:
                f.write(config)

def clean_slate():
    
    # loop through the applied_configs dir 
    for file in os.listdir(applied_configs_path):
        file_path = os.path.join(applied_configs_path, file)

        # remove each file in the dir
        if os.path.isfile(file_path):
            os.remove(file_path)

    # see notes above, but for generated_configs
    for file in os.listdir(generated_configs_path):
        file_path = os.path.join(generated_configs_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

def get_device_info():

    # create empty dict for device info
    device_info = {}

    # define the path the base config csv
    base_config_csv = os.path.join(cwd, csvs, "base_config.csv")


    # open the csv 
    with open(base_config_csv) as f:
        device_info_csv = csv.DictReader(f)
        for row in device_info_csv:

            # store info about each device into the device_info dictionary
            switch_hostname = row["switch_hostname"]
            prov_ip = row["prov_ip"]
            device_info[switch_hostname] = {"ansible_host": prov_ip}

    return device_info

def generate_ansible_inventory():
    
    ansible_inventory = {
        'PROV_NET': {
            'hosts': {},
        }
    }

    device_info = get_device_info()

    for device, info in device_info.items():

        # generated_configs_path = os.path.join(cwd, "generated_configs")
        for file in os.listdir(generated_configs_path):
            # grab the filename of each file
            filename = os.path.basename(file)

            if device in filename:  # check if device name is in the filename
                config_file_path = os.path.join(generated_configs_path, file)
                info['config_file'] = config_file_path

                # adding global variables to each device
                ansible_inventory.setdefault('PROV_NET', {}).setdefault('vars', {})['ansible_connection'] = 'network_cli'
                ansible_inventory.setdefault('PROV_NET', {}).setdefault('vars', {})['ansible_network_os'] = 'arubanetworks.aoscx.aoscx'

                ansible_inventory.setdefault('PROV_NET', {}).setdefault('hosts', {})[device] = info
                ansible_inventory['PROV_NET']['hosts'][device] = info
                break  # exit loop once the file is found for the device
        else:
            print(f"ERROR: no config file found for {device}")

    return ansible_inventory

def create_ansible_inventory(ansible_inventory):
    with open('hosts.yml', 'w') as file:
        file.write ('---\n')
        yaml.dump(ansible_inventory, file, default_flow_style=False)
        file.write ('...\n')
        
        ## a finished ansible config file generates like this: ##
        # PROV_NET:
        #     hosts:
        #         S0117SWT005:
        #             ansible_host: 192.168.1.10
        #             config_file: /home/ansible/ansible_playbooks/base_config/generated_configs/S0117SWT005_base_config.aos
        #         S0117SWT011:
        #             ansible_host: 192.168.1.11
        #             config_file: /home/ansible/ansible_playbooks/base_config/generated_configs/S0117SWT011_base_config.aos
        #         S0117SWT021:
        #             ansible_host: 192.168.1.12
        #             config_file: /home/ansible/ansible_playbooks/base_config/generated_configs/S0117SWT021_base_config.aos
        #         S0117SWT031:
        #             ansible_host: 192.168.1.13
        #             config_file: /home/ansible/ansible_playbooks/base_config/generated_configs/S0117SWT031_base_config.aos
        #     vars:
        #         ansible_connection: network_cli
        #         ansible_network_os: arubanetworks.aoscx.aoscx

def main():

    clean_slate()
    prov_base_config_6300(generated_configs_path)


main()

#generate the ansible inventory
inventory_data = generate_ansible_inventory()

#write the inventory to a file in YAML format
create_ansible_inventory(inventory_data)


####
####