# Ansible for Proxmox Setup

This directory contains Ansible configuration files needed to install Proxmox VE 8 on a Debian 11 machine.

This step assumes the following:
+ Debian 11 has been freshly installed on the target systems
+ Key-based SSH access to each system is available

At completion of the Ansible playbooks, we will have:
+ Debian 12 with Proxmox VE 8 installed
+ Basic networking configured inside Proxmox

## Run it

First, edit `inventory.yaml` to match your servers and path to private SSH key.

Set the environment variable to skip the annoying SSH key verification dialogue.
```
export ANSIBLE_HOST_KEY_CHECKING=0
```

Test that each server is reachable by pinging them:
```
ansible all -m ping -i inventory.yaml
```

Then, run the playbooks. This will take around 10 minutes.

```
ansible-playbook -i inventory.yaml all-playbooks.yaml
```

## Specifics:

The ansible playbooks will install Proxmox using the recommended pathway:
+ Install Proxmox VE 7 (according to https://pve.proxmox.com/wiki/Install_Proxmox_VE_on_Debian_11_Bullseye)
+ Upgrade the Debian 11 & Proxmox VE 7 installation to Debian 12 & Proxmox VE 8 (according to https://pve.proxmox.com/wiki/Upgrade_from_7_to_8)
+ Automatically find each machine's public IP and configure the network interface as seen by proxmox. This allows us to immediately set up Proxmox clusters.
+ Prepare each system so that it is ready to be configured for SNAT (which provides internet access to VMs).



