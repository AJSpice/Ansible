##############


Welcome to my Ansible Branch!

This Branch showcases a copy of what the structure of my Ansible server looks like that I stood up at my most recent position.

I have anonymized all data on this Branch so that I do not reveal company information, but all scripts were used in production in one way or another

Note: There is a hidden file in this dir called .ansible.cfg, this is the standard for home dir ansible config files. My playbooks use this as their default ansible cfg files









Credentials:

This ansible server was setup to use a credentials.yaml file that is encrypted with Ansible-Vault. The data has been stripped in this branch but it would contain the TACACS login info for the PROD switches ansible_user account
There is a vault_password.txt file under /etc/ansible/ for this server that helps the plays open and use the credentials.yml file for TACACS login to network devices