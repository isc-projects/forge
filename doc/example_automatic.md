  Working example.
 -----------------
We present step-by-step instructions for setting up a testing environment using the Incus script.

This script is prepared to work on a Debian system. (It may work on other `apt` based systems.)
It can be run on a bare-metal installation or on a virtual machine. (If running a VM, be sure to enable nested virtualization.)

In this example, we will use Debian 13.3.0 installed from an ISO.
We used this image: https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-13.3.0-amd64-netinst.iso

This guide was last tested on 17th February 2026.

> Warning:
>
> Incus script uses these networks internally, and they may conflict with your host:
>  - 192.168.100.0/24
>  - 192.168.50.0/24
>  - 192.168.51.0/24
>  - 2001:db0::0/32

  Installing OS and Incus.
 ------------------------------------
### 1. Install Debian.
Install Debian from ISO.
  - Select SSH Server if you need to connect remotely.
  - GUI is not required.
  - Set up a mirror server for the package repository.

### 2. Install prerequisites.
Debian does not come preinstalled with some packages required by the incus script. We need to install:
  - `sudo`
  - `git`
  - `python3`

To install packages, we need to switch the user to root by entering the command and then the root password when asked:
```shell
su -
```

Now we update the repository and install packages:
```shell
apt-get update
apt-get install sudo git python3
```

### 3. Configure sudo.
We need to make sudo commands run without a password, so the script can execute commands without asking for a password.
```shell
visudo
```

Add a line at the end, replacing `<username>` with your username.

`%<username> ALL=(ALL) NOPASSWD: ALL`

Now you won’t be asked for a password when using sudo.

Exit superuser so we can proceed using `sudo`:
```shell
exit
```

### 4. Clone Forge from the Git Repository.
Return to the home directory.
```shell
cd ~
```

You can use git clone to download Forge from the repository.
```shell
git clone https://gitlab.isc.org/isc-projects/forge.git
```

### 5. Install Incus using the script.
Enter the Forge directory and run the install script:
```shell
cd forge
sudo ./incus_install.sh
```

  Preparing containers.
 ------------------------------------
### 1. Prepare testing enviroment.
Incus script allows preparing various OSes for testing. We will start with Ubuntu 24.04 with 2 kea containers and 2 networks:
```shell
sudo ./incus.sh prepare-env ubuntu/24.04 2 2 master
```

We should now have 3 containers: kea-forge, kea-1, and kea-2 connected by two internal networks.

### 2. Installing Kea.
Incus script supports installing Kea from a tarball or packages.

### 2A. Installing Kea from tarball.
Kea can be obtained from the git repository or extracted from a tarball.

To download the latest master to the home directory:
```shell
git clone https://gitlab.isc.org/isc-projects/kea.git ~/kea
```
> You can also download a premium tarball into the kea directory.

Install Kea on the containers:
```shell
sudo ./incus.sh install-kea-tarball 2 ~/kea
```

### 2B. Installing Kea from packages.
This method supports only our internal repository (not publicly available)

Example command:
```shell
sudo ./incus.sh install-kea-pkgs ubuntu/24.04 2 2.7.3-isc20240903092214
```

  Running tests.
 ------------------------------------
### 1. Running pytest.
Running a full set of tests requires additional RADIUS and Windows installations.

More useful would be running a specific file:
```shell
sudo ./incus.sh run-pytest tests/dhcp/protocol/test_v6_basic.py
```

Or even a specific test:
```shell
sudo ./incus.sh run-pytest tests/dhcp/protocol/test_v6_basic.py::test_v6_basic_message_request_reply
```

### 2. Updating test files.
When you modify Forge files on the host machine, you can upload them to the Forge container using:
```shell
sudo ./incus.sh update-pytest
```

Or adding `--upload-pytest` option to `run-pytest`. For example:
```shell
sudo ./incus.sh run-pytest tests/dhcp/protocol/test_v6_basic.py --upload-pytest
```

### 3. Updating Kea.
There is no automatic way of reinstalling Kea at this time.
You need to delete containers and rebuild them.

To remove containers and networks, run:
```shell
sudo ./incus.sh clear-all 2 2
```

You can also log in to containers and update Kea manually. To log in to the first container run:
```shell
sudo incus exec kea-1 -- bash
```

  Additional settings.
 ------------------------------------

You can change `logFile="/dev/null"` line in `incus.sh` to log to file.
