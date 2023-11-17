##########


This playbook runs a python script to generate a line by line for configuring WAPS. 



1. The python script reads a CSV of necessary info, and then created a line by line config to send to the switch

2. the ansible playbook pushes the config line by line to the targeted switch in the playbook