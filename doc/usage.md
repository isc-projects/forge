Usage
=====

This document assumes the Forge was installed as [documented in the installation guide](install.md).

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
----------------------------------

You can follow step-by-step guide to set up simple environment and run some tests.
It's located in [example.md](example.md).
