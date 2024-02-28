#
#
Setup switch for SSH access on the PROV_NET:

    1. Plug switches into the Provision Network (PROV_NET) using the MGMT interface on the switch
    2. Plugin DAC cables as needed if they are being stacked
        a. Each switch in the stack needs to be configured on the PROV_NET with a unique IP address to be configured
    3. Configure local admin login on the switch(es)
    4. Configure the switch(es) for access from Ansible and on the PROV_NET using the PROV_SWITCH_CONFIG file relevant to your use case. Copy paste into each switch using a unique IP
    5. There are a few scripts to get a switch on the PROV_NET located on the ansible server ~/ansible/prov_switch_configs -- Below is one example for normal access layer switch
        
        !
        Conf t
        
        ssh server vrf mgmt
        aaa authentication login ssh local
        aaa authentication allow-fail-through
        !
        spanning-tree mode mstp
        spanning-tree
        spanning-tree priority 8
        !
        interface mgmt
            ip static 10.96.7.{{}}/24
            default-gateway 10.96.7.254
            no shut
        Exit
        
        Wr me
        
        
        
    6. Confirm switch(es) has SSH access with the local admin login and is reachable on its IP address


Firmware Updates:

Login to the Ansible Server and go into the ~/ansible/ansible_playbooks/firmware_updates directory  (File > Open Folder > /home/{ username }/ansible/ansible_playbooks/firmware_updates)

    1. Modify the hosts.yml file in this directory to target switch(es) on the PROV_NET for firmware update (See Ansible page for more details)  
    2. Save the hosts.yml file and its changes
    3. Inside a terminal window, and inside the ~/ansible/ansible_playbooks/firmware_updates directory run the firmware_update_{ model # of switch }.yml playbook:
        ansible-playbook firmware_update_{ model # of switch }.yml
    4. Wait for the playbook to finish running and confirm the new firmware is loaded onto the switch(es)


VSF Stacking:

Login to the Ansible Server and go into the ~/ansible/ansible_playbooks/vsf_stacking directory (File > Open Folder > /home/{ username }/ansible/ansible_playbooks/vsf_stacking)

    1. Open and modify the vsf_device_info.csv file to the information for the switch(es) being modified          
    2. Save the vsf_device_info.csv file and its changes
    3. Inside a terminal window, and inside the ~/ansible/ansible_playbooks/vsf_stacking directory run the push_vsf_config.yml playbook:
        ansible-playbook push_vsf_config.yml
    4. Wait for the playbook to finish running and confirm the new stacking configuration on the switch(es)


Base Config:

Login to the Ansible Server and go into the ~/ansible/ansible_playbooks/base_config directory (File > Open Folder > /home/{ username }/ansible/ansible_playbooks/base_config)

    1. Open and modify the base_config.csv under the ./csv_files dir   
    2. Save the base_config.csv and its changes
    3. Inside a terminal window, and inside the ~/ansible/ansible_playbooks_base_config directory run the push_{ model # of switch }_base_config.yml:
        ansible-playbook  push_{ model # of switch }_base_config.yml
    4. Wait for the playbook to finish running and confirm the new base configs are applied to the switches
        Confirm configs by comparing ./applied_configs to ./generated_configs
