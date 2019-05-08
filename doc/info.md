  ISC Forge info
 ----------------

ISC Forge is an automated DHCP validation framework. It uses Scapy, Pytest and
Fabric to run various DHCP tests.

For questions, ideas bug reports please contact us via kea-dev@lists.isc.org


 Dependencies Installation (OUTDATED)
---------------------------
Forge requires python 2.7.x, Scapy (2.2.0) and lettuce (0.2.17 or newer).
The following steps are necessary on Debian 7.0. If you use different operating system,
your steps may be slightly different:

(Note: may have to edit `/etc/apt/sources.list` and place new mirror entry:

```
   deb http://mirror.cse.iitk.ac.in/debian/ testing main contrib
```

then run "sudo apt-get update")

The folowing command will install pip (python package installer):

```
$ sudo apt-get install python-pip
```

Next move is to install Scapy
http://bb.secdev.org/scapy/wiki/Home

to get source from repo:
$ hg clone http://bb.secdev.org/scapy
or you can download by:
$ wget -O scapy.zip scapy.net

If you downloaded scapy.zip (scapy-2.2.0) please apply all scapy patches included
to Forge (forge/patches/scapy/). If you are using actual source code you need check
which changes needs to be applied. Forge developers are in contact with Scapy team
with goal of adding fixes to official code but not all fixes can eventually end up
in Scapy official source code.

$ cd scapy-2.2.0
$ sudo python setup.py install

As of Feb. 2013, Scapy is quite outdated. When starting it may produce
warnings similar to:

WARNING: No route found for IPv6 destination :: (no default route?)
/usr/local/lib/python2.6/dist-packages/scapy/crypto/cert.py:10:
DeprecationWarning: the sha module is deprecated; use the hashlib module instead
  import os, sys, math, socket, struct, sha, hmac, string, time
/usr/local/lib/python2.6/dist-packages/scapy/crypto/cert.py:11:
DeprecationWarning: The popen2 module is deprecated.  Use the subprocess module.
  import random, popen2, tempfile

Our understanding is that those can be safely ignored for now.

Also you may want to install tcpdump for saving captures of every test.
This step is optional and tcpdump usage is controlled via init_all.py

$ sudo apt-get install tcpdump

Forge uses fabric module to control DUT. It is mandatory. Use the latest
version available here: https://pypi.python.org/pypi/Fabric. You can also use
pip to install it:

$ sudo pip install fabric

Scapy uses crypto libraries that may be needed:

$ sudo apt-get install python-crypto
$ sudo pip install ecdsa

For http requests Forge needs requests module:

$ sudo pip install requests

 DUT dependencies requirements and configuration
-------------------------------------------------
On Device Under Test (DUT) on which will be running your server you need:

* be able to connect via ssh
* have access to bash shell from /bin/bash
* install sudo - if you are using non-root account grand rights to use 'sudo'
  without password to your user account by adding to sudoers file:

    %<group_name> ALL=(ALL) NOPASSWD: ALL
* installed DHCP/DNS server


 Scapy patches
---------------
After long time when Scapy project was on hold we are in contact with Scapy team
But if your scapy code does not include fixes that were developed with Forge
(scapy-2.2.0 has none of those) please use included patches.
The scapy code that needs to be patched is in scapy-2.2.0/scapy/layers.

Please apply each patch using the following (or similar) command:
patch -p0 < name-of-the-patch

For example, if Forge lives in ~/builds/forge, and the Scapy source
is in ~/builds/scapy-2.2.0, then you can patch the Scapy file
"dhcp6.py" with patch by performing the following:
cd ~/scapy-2.2.0
patch -p 0 <~/builds/forge/patches/scapy/scapy-2.2.0-dhcp6.patch


 Configuration
---------------
Configuration management is not well designed yet. The default configuration
is stored in forge/lettuce/features/init_all.py_default. Please copy this file
to features/init_all.py and edit relevant values in this file. The configuration
is not described here in detail example how you should fill it is stored in
forge/lettuce/features/init_all.py_example. Without init_all.py Forge will
not start at all. init_all.py is added to gitignore, so any local changes
you make to this file will be ignored by git.

Also make sure that your ssh server is configured.

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

That's only example, other architectures not tested. If you set up other configuration please
report it on https://github.com/isc-projects/forge to update documentation.

 Usage (OUTDATED)
-------

IMPORTANT:
	You can dynamically generate user help by running forge/lettuce/help.py. UserHelp.txt
	will contain all information about using and further developing Forge project.

cd forge/lettuce

The following command should be executed as root because these tests require
opening of privileged ports (DHCP client port):

./forge.py -6 -t basic


 Writing new tests
-------------------

TODO: Write this section from scratch. Lettuce example was useless.

 Additional info
-----------------
https://docs.pytest.org/en/latest/ - Pytest homepage
http://www.secdev.org/projects/scapy/ - Scapy homepage
