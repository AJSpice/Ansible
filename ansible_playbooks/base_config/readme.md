######



This ansible script has a lot of moving parts, here are the main sections:



General Setup
PROV_NET: My OOB network 192.168.1.0/24

1. each switch gets put onto the PROV_NET with a unique IP address using the prov_switch.j2 file as a template
2. the CSV is modifed targeting each switch on the PROV_NET with the details that the switch will need for its base_config
3. the ansible playbook is run
4. the ansible playbook will first run the python script
5. python script generates the ansible hosts file in the current dir using the csv as info, and the PROV_NET ip'
6. python scruot generates a config file for each host on the PROV_NET according to the csv info and the corresponding .j2 file / _base_config.aos
7. the ansible playbook will push the base config to each device according to the CSV info and the corresponding .j2 file / _base_config.aos
      The ansible playbook sends a crypto key cert seperately
      The ansible playbook copies the running config and save to the applied_configs dir for review


Pre-Req's:
Setup a management network that the switches can get provisioned on. I setup an OOB network with ip 192.168.1.0/24 and statically assign the ips to the switches to get them on the "PROV_NET" (provision network)

Copy paste the prov_switch.j2 into each switch with a unique PROV-NET ip address


csv_files:
1. fill out the bae config csv with device specific info for the base config.
2. fill out the PROV_NET ip in the csv with the ip of the corresponding device on the PROV_NET


jinja_templates:
1. all empty varibles (marked as empty curly brackets {{NULL}} ) are entered to anonymize the base config of my PROD network. But these can be filled out, or even entered using the CSV with new columns as variable data!
2. there is a j2 file for two models of switches, in this branch they are duplicates, but in our PROD network there were slight differences. Feel free to create new template configs to send out and use a new playbook to use it!
3. there are two "prov_switch" j2s, one to get a switch on the PROV_NET and one to undo those changes before sending the switch out to PROD

create_base_config.py's:
1. there are two scripts here, both are the same, in my environment, they were slighty different
2. the script(s) perform a few crucial functions
3. script(s) generate an ansible hosts file using the CSV info, mainly using the prov_ip column
4. script(s) take the j2 template files and modify them with the CSV info, then saving it to the generated_configs dir

hosts.yml:
1. g
2. enerated by the python scripts
