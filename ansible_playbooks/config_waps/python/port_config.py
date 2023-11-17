#Reads a .csv file to change ports to wap configs

#!/usr/bin/env python
import csv
import os

#define the current working dir
cwd = os.getcwd()
#define the path to the wap_ports csv
wap_info_csv_path = os.path.join(cwd , "python" , "wap_info.csv")
#config_path = os.path.join (cwd, "config.txt")

def clear_config_file():

    folder_path = os.path.join(cwd, "python")

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path , file)
        if "config.txt" in file_path:
            os.remove(file_path)
        

def make_config_file():

    #open the text file and add the conf t line
    with open(os.path.join(cwd, "python" , "config.txt"), 'a') as f:
        f.write("conf t\n")

    #opens the csv with the DictReader class to go through each row
    with open(wap_info_csv_path , newline='', encoding='utf-8') as f:
        wap_ports_csv_reader = csv.DictReader(f)
        for row in wap_ports_csv_reader:
            port=row["port"]
            wap=row["wap"]
            native_vlan=row['native_vlan']

            #list of the ios commands to run on the switch per row in the csv
            config_commands = [
                               f'default int {port}',
                               f'int {port}', 
                                f'description {wap}',
                                'no routing',
                                f'vlan trunk native {native_vlan}',
                                'vlan trunk allowed all',
                                'qos trust dscp',
                                'rate-limit multicast 2000 kbps\n']
            
            config_commands_joined = "\n".join(config_commands)
            
            #open the config.txt file and write the config commands to it
            with open(os.path.join(cwd, "python" , "config.txt"), 'a') as f:
                f.write(config_commands_joined)


clear_config_file()

make_config_file()