  ISC Forge info
 ----------------

ISC Forge is an automated DHCP validation framework. It uses Scapy, Pytest and
Fabric to run various DHCP tests.

For questions, ideas bug reports please contact us via kea-dev@lists.isc.org

 Dependencies Installation
---------------------------
Forge requires python 3.9.x, the latest Scapy and pytest. We also recommend venv.
We recommend newest versions, if not specified otherwise in [requirements.txt](../requirements.txt).

You basically only need to do this:

```shell
cd forge-source-code-path
python3 -m venv venv
source ./venv/bin/activate
./venv/bin/pip install -r requirements.txt
```

Also, you may want to install tcpdump for saving captures of every test.
This step is optional and tcpdump usage is controlled via init_all.py

```shell
sudo apt-get install tcpdump
```



 DUT dependencies requirements and configuration
-------------------------------------------------
On Device Under Test (DUT) on which will be running your server you need:

* be able to connect via ssh
* have access to bash shell from /bin/bash
* install `sudo` - if you are using non-root account grand rights to use 'sudo'
  without password to your user account by adding to sudoers file:

    `%<group_name> ALL=(ALL) NOPASSWD: ALL`
* install `socat` for testing Socket connections
* installed DHCP/DNS server

 Manual Configuration
----------------------
Configuration management is not well-designed yet. The default configuration
is stored in forge/tests/init_all.py_default. Please copy this file
to forge/tests/init_all.py and edit relevant values in this file.
Without init_all.py Forge will not start at all. init_all.py is added
to gitignore, so any local changes you make to this file will be ignored by git.

Also make sure that your ssh server is configured. Make sure that SSH connection between
used vms can be executed using generated keys or provided password.

Environment example:
To use Forge you will need two PC's. In this configuration author used two virtual
machines using VM VirtualBox. Those machines need to be connected with internal network
(without any other access to interfaces). In VirtualBox this is called Host-Only network.
You can establish internet connection on other interface if you want. Two different networks
should be used for:

	vboxnet0 - configuration server via ssh, you can use this network to ssh to forge machine
	vboxnet1 - testing, ip needs to be set manualy on both machines

Author used this configuration:
```
 ______                                            ______
|      | <----vboxnet0: configuration via ssh---> |      |
| VM 1 |                                          | VM 2 |
|______| <----vboxnet1: testing DHCP        ----> |______|
```

That's the only example, other architectures not tested. If you set up other configuration please
report it on https://github.com/isc-projects/forge to update documentation.

 Usage
-------
First enter virtualenv created previously

```shell
source ./venv/bin/activate
```
To run all tests using virtualenv created previously
```shell
sudo ./venv/bin/pytest
```

To run just subset of tests from one file
```shell
sudo ./venv/bin/pytest tests/dhcpv4/kea_only/control_channel/test_command_control_socket.py
```
Additional useful options are:

using tests tags:
```shell
sudo ./venv/bin/pytest -m ddns
sudo ./venv/bin/pytest -m v4
sudo ./venv/bin/pytest -m 'v4 and v6'
```

using test keywords:
```shell
sudo ./venv/bin/pytest -k 'test_status_get'
```
Increased verbosity for debugging tests results

```shell
sudo ./venv/bin/pytest -vv
```

Forge system tests require root privileges to open DHCP ports, mange DHCP servers and
capturing traffic via tcpdump.

 Step-by-step working setup example
------------------------------------
You can follow step-by-step guide to set up simple environment and run some tests.
It's located in [example.md](example.md).

 Writing new tests
-------------------
Since forge moved from lettuce to pytest, writing new tests it's just python programming.
Functions available in tests/srv_control.py are used to operate remote DHCP/DNS servers.
Functions available in tests/srv_msg.py are used to generate and parse traffic.

 Additional info
-----------------
https://docs.pytest.org/en/latest/ - Pytest homepage
http://www.secdev.org/projects/scapy/ - Scapy homepage
