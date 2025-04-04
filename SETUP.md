# “Zero to Demo” - Limitless PC Proxmox Setup

# Create Developer SSH Key

On your Mac or Linux machine:

```bash
ssh-keygen -C "admin@aptero.co"
```

It will ask:

```bash
Generating public/private ed25519 key pair.
Enter file in which to save the key:
```

Name the key pair something memorable like `yundera-developer` 

Passphrase is optional but recommended.

This will create two files in `~/.ssh:`

```bash
yundera-developer
yundera-developer.pub
```

The *.pub file is the public key that you need to upload to Scaleway and attach to your server when you create the server.

The file without the *.pub extension is the private key.

# Rent Servers

Rent three Scaleway Dedibox START-2-L servers.

This section does not have an automated playbook because Scaleway Dedibox rental is a month-long commnitment and initial OS install can take up to 1 hour. These considerations made it infeasible to build and test automated scripts within the scope of this report.

Should that become a relevant goal, Scaleway offers its own APIs and the Terraform has a Scaleway provider already built-in, which will make the task straightforward.

Sign into [https://console.online.net/en/login](https://console.online.net/en/login)

![Screenshot 2025-03-27 at 14.12.54.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-03-27_at_14.12.54.png)

Since the latest version of Proxmox VE that Scaleway offers pre-installed is an outdated (7.x) one, we will install Proxmox VE 8.x ourselves from a Debian 11 base installation. In the process we’ll upgrade Debian from 11 to 12 also.

![Screenshot 2025-03-27 at 14.16.31.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-03-27_at_14.16.31.png)

![Screenshot 2025-03-29 at 00.21.44.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-03-29_at_00.21.44.png)

The default partitioning uses RAID1. We need to have one of the drives dedicated for Ceph storage. Therefore, change the partition to not use RAID. On the first drive, keep the Swap, /boot, and / partitions. On the second drive, replace everything with a single ext4 partition. For now we’ll mount that drive at /data but this path doesn’t matter since we will be wiping this drive later on.

![Screenshot 2025-03-30 at 02.33.30.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-03-30_at_02.33.30.png)

Change the hostname to something more meaningful. Pick a username and password and keep them somewhere safe.

![Screenshot 2025-03-29 at 00.25.44.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-03-29_at_00.25.44.png)

In addition, we need to set up SSH key access to the server. Click `or add a new one here` button. Copy the contents of the public SSH key (`yundera-developer.pub` in the previous step) here.

![Screenshot 2025-03-29 at 00.25.36.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-03-29_at_00.25.36.png)

Confirm in summary and wait until the servers boot up and installs the OS. The website says this can take up to an hour. Typically it takes around 15 to 30 minutes.

Repeat this for all servers.

# Install Proxmox VE 8

We use Ansible to automate the installation and upgrade of Proxmox VE 8.

We prefer starting from a Debian image instead of using the provided Proxmox VE 7 image because it allows us to use Ansible for more things.

This code for this section is:

[https://github.com/tensorturtle/yundera-limitless-pc](https://github.com/tensorturtle/yundera-limitless-pc)

Please read the ‘README.md’ inside the ‘ansible’ directory.

Ansible running on all three servers:

![Screenshot 2025-03-29 at 22.56.33.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-03-29_at_22.56.33.png)

Once Ansible is finished, navigate to the web interface, which is at port 8006 on each of the servers’ public IP addresses:

Proxmox uses self-signed certificates which web browsers don’t like - we can safely ignore this and it won’t bother us again.

![Screenshot 2025-03-29 at 02.27.15.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-03-29_at_02.27.15.png)

![Screenshot 2025-03-29 at 02.27.21.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-03-29_at_02.27.21.png)

Log in using the root password (which you defined when renting the server)

![Screenshot 2025-03-29 at 02.28.31.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-03-29_at_02.28.31.png)

Ignore warning for subscription.

![Screenshot 2025-03-29 at 02.29.36.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-03-29_at_02.29.36.png)

![Screenshot 2025-03-29 at 02.48.43.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-03-29_at_02.48.43.png)

At this point, we should be able to access all three Proxmox web UIs.

# Create Proxmox Cluster

This step cannot be automated via Ansible due to a quirk of the ‘pvecm’ command - specifically, it requires the root password to be entered (even when key-based SSH is set up between the servers) but it cannot be scripted with STDIN or even ‘expect’. More work is required to find a workaround.

Log into the first of the three hosts. We should see a single host in the ‘Datacenter’ list.

![Screenshot 2025-03-29 at 12.27.08.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-03-29_at_12.27.08.png)

Create a new cluster.

![Screenshot 2025-03-29 at 12.32.04.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-03-29_at_12.32.04.png)

Pick a cluster name of your choice.

![Screenshot 2025-03-29 at 12.34.00.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-03-29_at_12.34.00.png)

Copy the “Join Information” field.

![Screenshot 2025-03-29 at 12.34.06.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-03-29_at_12.34.06.png)

Now log into the Proxmox web UI of the other two hosts.

In the same Cluster settings, join the cluster by pasting in the ‘Join Information’ content.

![Screenshot 2025-04-04 at 18.06.39.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-04-04_at_18.06.39.png)

Enter the root password of the first host when prompted.

![Screenshot 2025-04-04 at 18.06.55.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-04-04_at_18.06.55.png)

## Using Command Line

The same process can be done through the command line.

SSH into the first node (node 0) as root.

Create a new cluster

```bash
pvecm create YUNDERACLUSTER
```

View status

```bash
pvecm status
```

Note the IP address of this ‘leader’.

SSH into the other hosts

```bash
pvecm add LEADER.IP.ADDRESS.HERE
```

Enter root password for the leader.

Go back to the leader node and run `pvecm status` to see the new node in the cluster.

The cluster should now look like this (the cluster is visible from all nodes)

![Screenshot 2025-03-30 at 00.00.52.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-03-30_at_00.00.52.png)

Equivalently, we can run

`pvecm status`:

```bash
root@proxmox-dev-cluster-0-node-0:~# pvecm status
Cluster information
-------------------
Name:             YUNDERACLUSTER
Config Version:   3
Transport:        knet
Secure auth:      on

Quorum information
------------------
Date:             Sat Mar 29 16:02:14 2025
Quorum provider:  corosync_votequorum
Nodes:            3
Node ID:          0x00000001
Ring ID:          1.d
Quorate:          Yes

Votequorum information
----------------------
Expected votes:   3
Highest expected: 3
Total votes:      3
Quorum:           2
Flags:            Quorate

Membership information
----------------------
    Nodeid      Votes Name
0x00000001          1 163.172.68.57 (local)
0x00000002          1 163.172.68.59
0x00000003          1 163.172.68.106
```

# Create Ceph Cluster on top of Proxmox Cluster

[Deploy Hyper-Converged Ceph Cluster - Proxmox VE](https://pve.proxmox.com/wiki/Deploy_Hyper-Converged_Ceph_Cluster)

## Wipe Second Drive

Our servers came installed with two SSDs. 

One is used by the host system, and the other will be dedicated to Ceph.

Since we had to format it to ext4 in the setup stage, we wipe it again to be used for Ceph.

Go to ‘Disks’ and select the drive that has just one partition. Then click ‘Wipe Disk’.

![Screenshot 2025-03-30 at 05.05.17.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-03-30_at_05.05.17.png)

## Install Ceph on all machines

![Screenshot 2025-03-30 at 05.06.16.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-03-30_at_05.06.16.png)

Select the latest version (squid) and No-subscription

![Screenshot 2025-03-30 at 05.06.40.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-03-30_at_05.06.40.png)

![Screenshot 2025-03-30 at 05.07.49.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-03-30_at_05.07.49.png)

Repeat for all servers.

# Create Ceph Cluster

We’ll have one monitor, three managers (one main, two standby), and three OSDs.

If you are unfamiliar with Ceph terms, please see the [documentation](https://docs.ceph.com/en/squid/start/)

Add another manager:

![Screenshot 2025-03-30 at 05.13.46.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-03-30_at_05.13.46.png)

Add OSD for each server:

![Screenshot 2025-03-30 at 05.11.16.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-03-30_at_05.11.16.png)

Create Metadata servers (one active, two standby). Then, create a CephFS storage. CephFS storage is a simple shared file system among the nodes. We will use it to store the VM image base ISOs.

![Screenshot 2025-03-30 at 05.30.36.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-03-30_at_05.30.36.png)

Create a new pool for RBD, which is where the VMs will store their state. 

Note: All Ceph related changes are shared across all nodes, so we can do these operations from any node’s Proxmox web UI.

Note that CephFS storage is different from the Ceph RBD storage we defined above. CephFS is just a convenient shared directory to keep metadata like OS ISOs, and RBD is where the actual VMs will store their content.

First, create a Ceph pool. Keep defaults.

![Screenshot 2025-03-30 at 14.23.29.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-03-30_at_14.23.29.png)

Go to Datacenter → Storage, and add a new “RBD” storage, using cephpool.

![Screenshot 2025-03-30 at 14.25.41.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-03-30_at_14.25.41.png)

## Configure network for VMs

Follow the directions given this Proxmox documentation, starting from the ‘**Configuration’** section.

[https://pve.proxmox.com/wiki/Setup_Simple_Zone_With_SNAT_and_DHCP](https://pve.proxmox.com/wiki/Setup_Simple_Zone_With_SNAT_and_DHCP)

Notes:

- The first part, installing `dnsmasq` , is not necessary because it is already done by the initial Ansible setup.
- When defining the subnet, consider using a larger subnet mask like /16 to allow for a bigger network, such as:
    
    ![Screenshot 2025-04-04 at 18.20.19.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-04-04_at_18.20.19.png)
    
    ![Screenshot 2025-04-04 at 18.21.15.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-04-04_at_18.21.15.png)
    
- IP forwarding is required, which is done by: `echo 1 > /proc/sys/net/ipv4/ip_forward`  This was already applied in the initial Ansible playbooks, so we don’t have to worry about it
- Remember to ‘Apply’ changes from the ‘SDN’ view.

# Create a VM

## Download OS ISOs

Upload a Ubuntu 24.04 LTS image to the CephFS storage. Since that storage is shared, it means that all hosts within this cluster will be able to launch VMs using that ISO.

From France, a convenient download URL mirror is: [https://mirror.bakertelekom.fr/Ubuntu/24.04/ubuntu-24.04.2-desktop-amd64.iso](https://mirror.bakertelekom.fr/Ubuntu/24.04/ubuntu-24.04.2-desktop-amd64.iso)

![Screenshot 2025-04-04 at 18.23.18.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-04-04_at_18.23.18.png)

Upload it to the CephFS. Since it’s a shared storage location, now all hosts will be able to create VMs based on this ISO without copying.

![Screenshot 2025-04-02 at 17.51.30.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-04-02_at_17.51.30.png)

## Create VM

Press ‘Create VM’ button

![Screenshot 2025-04-04 at 18.37.22.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-04-04_at_18.37.22.png)

Use the previously uploaded ISO in cephfs:

![Screenshot 2025-04-04 at 18.37.33.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-04-04_at_18.37.33.png)

In System, select ‘Qemu Agent’

![Screenshot 2025-04-02 at 17.56.34.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-04-02_at_17.56.34.png)

In Storage, select the Ceph RBD. The disk size is not meaningfully changeable after this, so pick carefully. (More accurately, we can change the disk size but we cannot change the boot partition without rebooting and complex steps)

![Screenshot 2025-04-02 at 17.58.02.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-04-02_at_17.58.02.png)

In CPU, enter the maximum number of cores that will ever be used by this VM at the top ‘Cores’. It cannot exceed the number of physical cores on the host.

 Enter the actually allocated number of cores in the bottom ‘VCPUs’.

Enable NUMA.

![Screenshot 2025-04-02 at 17.58.22.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-04-02_at_17.58.22.png)

In Memory, ensure Ballooning Device is selected.

![Screenshot 2025-04-02 at 17.59.56.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-04-02_at_17.59.56.png)

In Network, a vnet created in the above SDN (Software Defined Network) should show up. This can be thought of as an internal network for the VMs, with the Proxmox cluster providing an internet gateway and a DHCP server.

Enable Firewall to disable inter-VM traffic.

![Screenshot 2025-04-02 at 18.00.36.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-04-02_at_18.00.36.png)

Finish VM creation. Don’t start it yet.

Select the newly created VM in the Server View and open Options → Hotplug.

![Screenshot 2025-04-02 at 18.03.30.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-04-02_at_18.03.30.png)

Enable everything including Memory and CPU.

Now we are ready to install the OS. Press ‘Start’ on this VM and open the Console.

Keep sensible defaults for the OS.

Once the OS is installed, we need to make the following system modifications.

Install OpenSSH:

```bash
sudo apt install openssh-server
sudo systemctl start ssh.service
```

These are all just bash commands, so we can do it from the VM’s own terminal, or SSH into it from the host. At this point, the VM doesn’t have an IP address so we won’t be able to SSH into it from outside the cluster.

## Guest VM Modifications for Vertical Scaling

[https://pve.proxmox.com/pve-docs/chapter-qm.html#_vcpu_hot_plug](https://pve.proxmox.com/pve-docs/chapter-qm.html#_vcpu_hot_plug)

On ubuntu 24, only one “cpu” line is needed.

```bash
mkdir -p /lib/udev/rules.d/
echo 'SUBSYSTEM=="cpu", ACTION=="add", TEST=="online", ATTR{online}=="0", ATTR{online}="1"' > /lib/udev/rules.d/80-hotplug-cpu-mem.rules

```

On Debian 12, the additional line 

```bash
echo 'SUBSYSTEM=="memory", ACTION=="add", TEST=="state", ATTR{state}=="offline", ATTR{state}="online"' > /lib/udev/rules.d/80-hotplug-cpu-mem.rules
```

Is required. The [https://pve.proxmox.com/wiki/Hotplug_(qemu_disk,nic,cpu,memory)](https://pve.proxmox.com/wiki/Hotplug_(qemu_disk,nic,cpu,memory)) docs say that the memory line is only required for kernel older than 4.7, but on Debian 12 with Kernel 6.1, it was still necessary. If left out, the VM will only see 1GB of RAM.

Edit /etc/default/grub

```bash
vi /etc/default/grub
```

Find the **`GRUB_CMDLINE_LINUX_DEFAULT`** line and add `movable_node`

```bash
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash movable_node"
```

```bash
update-grub
```

Now, we are able to freely scale the CPU and RAM up and down using the Proxmox web GUI → Hardware.

Note that for most system monitoring programs, changes to the CPU count won’t be shown unless you re-open the program. Typically, changes in RAM capacity will show up instantly.

For convenience, install some commonly used packages that are used later

```bash
apt install -y htop vim iperf3 bc rclone
```

**Clean the image for use as template**

```bash
apt clean

# Delete temp files
rm -rf /tmp/*
rm -rf /var/tmp/*

# Reset machine-id
truncate -s 0 /etc/machine-id
rm -f /var/lib/dbus/machine-id

# Remove random seed files
rm -f /var/lib/systemd/random-seed
rm -f /loader/random-seed

# Remove system identity files
rm -f /var/lib/dbus/machine-id
rm -rf /var/lib/cloud/instances/*

# Remove credential secret
rm -f /var/lib/systemd/credential.secret

# Reset SSH host keys
rm -f /etc/ssh/ssh_host_*

```

**Shutdown** the VM.

Use the Proxmox GUI to create template using this VM.

To use this template, ‘Clone VM Template’ from the VM, instead of ‘Create VM’ at the top of the screen.

In the future, we should automate the OS installation process using something like cloud-init.

# Mount a Backblaze Bucket

We create a very slightly modified template, starting from the above Ubuntu desktop template. 

Since we deleted the SSH host keys in the previous step for a clean OS, we need to reconfigure it. This needs to be done for new VMs.

```
sudo dpkg-reconfigure openssh-server
```

We simply add a script in the user’s home directory, which can be run once to set up a backblaze mount.

[https://github.com/tensorturtle/yundera-limitless-pc/blob/main/backblaze-mount/setup-backblaze-mount.sh](https://github.com/tensorturtle/yundera-limitless-pc/blob/main/backblaze-mount/setup-backblaze-mount.sh)

The user should be directed to run this once at the beginning.

In Proxmox, a new VM template is created.

This VM template has full CPU and RAM vertical scalability, along with Backblaze mount setup script.

The Setup process for the POC is now complete. The next section will demonstrate starting up a VM based on the above template and run some experiments to verify the vertical scaling capabilities.

## CasaOS Installation

On top of the Ubuntu + Backblaze template, we install CasaOS to create the final template.

```bash
wget -qO- https://get.casaos.io | sudo bash
```

A demo VM is spun up using this template at

[https://yundera-limitless-pc-demo.tensorturtle.com](https://yundera-limitless-pc-demo.tensorturtle.com)

Some unique modifications were made to serve as a demo:

- A demo Backblaze bucket (from Jason Sohn’s Backblaze account) is mounted.
- This VM is connected to Jason Sohn’s personal Tailscale network and reverse proxy server. A similar VPN based setup is required for deployment.

![Screenshot 2025-04-05 at 01.22.06.png](%E2%80%9CZero%20to%20Demo%E2%80%9D%20-%20Limitless%20PC%20Proxmox%20Setup%201cbe0e1449bc8030a6bce8d080d4ce89/Screenshot_2025-04-05_at_01.22.06.png)