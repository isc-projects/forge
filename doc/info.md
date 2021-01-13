  ISC Forge info
 ----------------

ISC Forge is an automated DHCP validation framework. It uses Scapy, Pytest and
Fabric to run various DHCP tests.

For questions, ideas bug reports please contact us via kea-dev@lists.isc.org

 Dependencies Installation
---------------------------
Forge requires python 2.7.x, the latest Scapy (from git) and pytest (4.6.5 or newer).
Please see [requirements.txt](../requirements.txt) for details.

You basically only need to do this:

```
cd forge-source-code-path
python -m virtualenv venv
source ./venv/bin/activate
./venv/bin/pip install -r requirements.txt
```

Also you may want to install tcpdump for saving captures of every test.
This step is optional and tcpdump usage is controlled via init_all.py

```
$ sudo apt-get install tcpdump

```

 DUT dependencies requirements and configuration
-------------------------------------------------
On Device Under Test (DUT) on which will be running your server you need:

* be able to connect via ssh
* have access to bash shell from /bin/bash
* install sudo - if you are using non-root account grand rights to use 'sudo'
  without password to your user account by adding to sudoers file:

    %<group_name> ALL=(ALL) NOPASSWD: ALL
* installed DHCP/DNS server

 Configuration
---------------
Configuration management is not well designed yet. The default configuration
is stored in forge/tests/init_all.py_default. Please copy this file
to forge/tests/init_all.py and edit relevant values in this file.
Without init_all.py Forge will not start at all. init_all.py is added
to gitignore, so any local changes you make to this file will be ignored by git.

Also make sure that your ssh server is configured. Make sure that SSH connection between
used vms can be executed using generated keys.

Environment example:
To use Forge you will need two PC's. In this configuration author used two virtual
machines using VM VirtualBox. Those machines needs to be connected with internal network
(without any other access to interfaces) in VirtualBox this is called Host-Only network.
You can establish internet connection on other interface if you want. Two different networks
should be used for:
	vboxnet0 - configuration server via ssh
	vboxnet1 - testing.

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

To run tests using virtualenv created previously
```
source ./venv/bin/activate
sudo ./venv/bin/pytest
```

To run just subset of tests from one file
```
sudo ./venv/bin/pytest tests/dhcpv4/kea_only/control_channel/test_command_control_socket.py
```
Additional useful options are:

using tests tags:
```
sudo ./venv/bin/pytest -m ddns
```
Increased verbosity for debugging tests results

```
sudo ./venv/bin/pytest -vv
```

Forge system tests require root privileges to open DHCP ports, mange DHCP servers and
capturing traffic via tcpdump.

 Writing new tests
-------------------

Since forge moved from lettuce to pytest, writing new tests it's just python programming.
Functions available in tests/srv_control.py are used to operate remote DHCP/DNS servers.
Functions available in tests/srv_msg.py are used to generate and parse traffic.

 Additional info
-----------------
https://docs.pytest.org/en/latest/ - Pytest homepage
http://www.secdev.org/projects/scapy/ - Scapy homepage
