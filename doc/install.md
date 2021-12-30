ISC Forge Installation
======================

The following document covers installation and configuration. For usage, see [usage](usage.md).

Dependencies Installation
-------------------------

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

The author used this configuration:

```
 ______                                            ______
|      | <----vboxnet0: configuration via ssh---> |      |
| VM 1 |                                          | VM 2 |
|______| <----vboxnet1: testing DHCP        ----> |______|
```

That's the only example, other architectures not tested. If you set up other configuration,
please report it on <https://github.com/isc-projects/forge> to update documentation.
