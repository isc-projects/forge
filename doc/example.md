  Working example
 -----------------
We present you step-by-step instructions to set up example testing environment and run some Forge tests on Kea server.
In this example we will use Ubuntu server 22.04.1 installed from ISO on two Virtual Machines.

We used this image: https://releases.ubuntu.com/22.04.1/ubuntu-22.04.1-live-server-amd64.iso

Other software used:
* Virtual Box installed on HOST machine

This guide was last tested on 10th November 2022.

  Setting up DUT (Device Under Test)
 ------------------------------------
### 1. Make VM for Kea Server
Kea will need at least 20 GB of disk space for build process.
(We recommend 80 GB to account for rebuilding without cleanup.)
We make new VM with network settings as follows:
* Adapter 1: NAT
* Adapter 2: Host-Only Adapter _(in our case it automatically made vboxnet0)_
* Adapter 3: Internal Network, write name you want to use for internal network

**(following instructions are meant to be executed on VM you choose to be Device Under Test)**

### 2. Install Ubuntu Server 22.04.1
Install Ubuntu from ISO using default settings and not installing additional services other than OpenSSH.

After installation check IP address acquired on Adapter 2 _(in our case interface: enp0s8 ip: 192.168.58.6)._

`ip address` will show you interfaces and ip addresses.

You can use this ip to connect by SSH from HOST machine for easier management.

### 3. Setup network interface for testing
Adapter 1 and 2 should get addresses from Virtual Box._(our machine got 10.0.2.15 for NAT and 192.168.58.6 for Host-Only)_

We use netplan on Ubuntu 22.04.1 to set static ip for Adapter 3.

Enter netplan directory and list files.
```shell
cd /etc/netplan
ls
```
If you didn't modify anything after install, you should see one file. _(00-installer-config.yaml in our case)_

Edit this file.

```shell
sudo nano your_filename.yaml
```

Change last interface options to static ip 192.168.50.252

Our file looks like this after modification.
```
network:
  ethernets:
    enp0s3:
      dhcp4: true
    enp0s8:
      dhcp4: true
    enp0s9:
      dhcp4: no
      addresses:
        - 192.168.50.252/24
  version: 2
```

Now you need to apply new configuration.

```shell
sudo netplan apply
```

### 4. Make sudo authenticate without password
We need to make sudo commands run without password, so Forge can execute them remotely.

```shell
sudo visudo
```

add line to the end replacing `<user_name>` with username you will use to gain ssh access to DUT machine from Forge

`%<user_name> ALL=(ALL) NOPASSWD: ALL`

now you won't be asked for password when using sudo

### 5. Clone Kea DHCP Server from Git Repository
You can use git clone to download Kea from repository.

```shell
git clone https://gitlab.isc.org/isc-projects/kea.git
```

### 6. Prepare environment for building Kea.
enter Kea directory

```shell
cd kea
```

run hammer.py script which will prepare all requirements for build process.
We use some predefined settings for basic server.

```shell
./hammer.py prepare-system -p local -s ubuntu -r 22.04 -w mysql pgsql radius gssapi netconf shell ccache
```

We need to make autoreconf of source.
```shell
autoreconf -if
```

Now we need to configure the building process, we included some preferred options for first install.

```shell
./configure --with-mysql --with-pgsql --with-gssapi --enable-shell
```

### 7. Building and installing Kea.
Next step is to build Kea from source. This step can take a while depending on speed of the machine. (it took about 20 minutes on our i5-4690K, 24GB RAM)

(If you have multicore machine you can use multiple threads. eg. for 4 threads use `make -j4` )

```shell
make
```

After you make, you need to install

This step uses sudo and **CAN NOT** be run with -j parameter.

```shell
sudo make install
```
And after install run:

```shell
sudo ldconfig
```
### 8. Install socat for socket testing

```shell
sudo apt install socat
```
**Now Server Machine is ready.**

  Setting up Forge Machine
 --------------------------
### 1. Make VM for Forge
We make new VM with network settings as follows:
* Adapter 1: NAT
* Adapter 2: Host-Only Adapter, choose the same as in DUT
* Adapter 3: Internal Network, write **exactly the same** name as in DUT

**(following instructions are meant to be executed on VM you choose to be Forge Machine)**
### 2. Install Ubuntu Server 22.04.1
Install Ubuntu from ISO on VM using default settings and not installing additional services other than OpenSSH.

After installation check IP address acquired on Adapter 2 _(in our case interface: enp0s8 ip: 192.168.58.5)._

`ip address` will show you interfaces and ip addresses.

You can use this ip to connect by SSH from HOST machine for easier management.

### 3. Setup network interface for testing
Adapter 1 and 2 should get addresses from Virtual Box. _(our machine got 10.0.2.15 for NAT and 192.168.58.5 for Host-Only)_

We use netplan on Ubuntu 22.04.01 to set static ip for Adapter 3.

Enter netplan directory and list files.
```shell
cd /etc/netplan
ls
```
If you didn't modify anything after install, you should see one file. _(00-installer-config.yaml in our case)_

Edit this file.

```shell
sudo nano your_filename.yaml
```

Change last interface options to static ip 192.168.50.3 and 2001:db9:1::2000

Our file looks like this after modification.
```
network:
  ethernets:
    enp0s3:
      dhcp4: true
    enp0s8:
      dhcp4: true
    enp0s9:
      dhcp4: no
      addresses:
        - 192.168.50.3/24
        - 2001:db9:1::2000/64
  version: 2
```

Now you need to apply new configuration.

```shell
sudo netplan apply
```

### 4. Clone Forge from Git Repository
You can use git clone to download Forge from repository.

```shell
git clone https://gitlab.isc.org/isc-projects/forge.git
```

### 5. Install Python virtual environment module (it should install also python pip)
```shell
sudo apt install python3.10-venv
```

### 6. pcapy package needs to have **build-essential** installed on Ubuntu 22.04.1
```shell
sudo apt install build-essential
```

### 7. Make virtual environment and install requirements.
We need to enter directory with cloned forge, make new virtual environment, activate it and run pip to install required python modules.
```shell
cd forge
python3 -m venv venv
source ./venv/bin/activate
```

Python 3.10 does not support `pcapy` package, so we need to use `pycap` instead by changing it in requirements file:
```shell
sed -i 's/pcapy/pycap/g' requirements.txt
```

Install requirements:
```shell
./venv/bin/pip install -r requirements.txt
```

### 8. Preparing config file
You need to copy default config file as a working one:

```shell
cp ./init_all.py_default ./init_all.py
```

And now edit this file:
```shell
nano ./init_all.py
```

Parameters that need to be set or uncommented, some of them will be empty:

`SOFTWARE_UNDER_TEST = ('kea6_server'),` (note the comma on the end)

`SRV4_ADDR = '192.168.50.252'` - this is the IP we set at Server

`CIADDR = '192.168.50.3'` - this is the IP we set at Forge Machine

`GIADDR4 = '192.168.50.3'` - this is the IP we set at Forge Machine

`IFACE = 'enp0s9'` - name of interface on Forge Machine which is connected to DUT for testing

`SERVER_IFACE = 'enp0s9'` - name of the interface on Server Machine which will be DHCP server

`SERVER2_IFACE = ''`

`MGMT_ADDRESS = '192.168.58.6'` - Server IP address on Host-Only network, so Forge can connect by SSH to manage Server

`MGMT_USERNAME = 'username'` - input your username on Server machine with sudo privileges

`MGMT_PASSWORD = 'password'` - input password to above username

`MGMT_ADDRESS_2 = ''`

`DNS_IFACE = ''`

`DNS4_ADDR = ''`

`DNS6_ADDR = ''`

**Your Forge Machine is ready for running tests**

  Running tests
 ---------------
You can run tests from Forge Machine by entering Virtual Environment and executing `pytest`
Following command performs a few known good test that should pass on this setup.

```shell
cd forge
source ./venv/bin/activate
sudo ./venv/bin/pytest -m 'v4 and v6' -k 'test_status_get'
```
**OR** You can run directly from normal command line by entering forge directory and using oneliner:

```shell
cd forge
```

and then:

```shell
sudo ./venv/bin/python ./venv/bin/pytest -m 'v4 and v6' -k 'test_status_get'
```

 Known problems
----------------
dnsmasq interferes with some testing. You can disable it temporary (until restart) using command on server:

```shell
sudo pkill -f dnsmasq
```
