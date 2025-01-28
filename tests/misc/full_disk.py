# Copyright (C) 2022-2025 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Testing how kea behaves when available disk space run out.

THIS IS NOT DESIGNED FOR AUTOMATED TESTING! Only manual!
Tests are explained in test code
"""

import os
import pytest

from src import srv_control
from src import misc
from src import srv_msg
from src.forge_cfg import world
from tests.HA.steps import generate_leases, send_command


def _check_disk(dest=world.f_cfg.mgmt_address):
    return srv_msg.execute_shell_cmd('df -l', dest=dest).stdout


def _create_ramdisk(location='/tmp/kea_ram_disk', size='10M', dest=world.f_cfg.mgmt_address):
    """Create new ramdisk, clear it if already exists.

    :param location: where new ramdisk should be mounted
    :param size: size of new disk
    :param dest: IP address of a system on which we want to allocate disk space
    :return: result of executed command
    """
    cmd = f'sudo mkdir -p {location} && sudo mount -t tmpfs -o size={size} tmpfs {location} && chmod 777 {location}'
    return srv_msg.execute_shell_cmd(cmd, dest=dest)


def _destroy_ramdisk(location='/tmp/kea_ram_disk', dest=world.f_cfg.mgmt_address):
    """Destroy previously created ramdisk. If disk will be busy it will be just cleared.

    :param location: location of previously mounted ramdisk
    :param dest: IP address of a system on which we want to allocate disk space
    :return: result of executed command
    """
    cmd = f'sudo rm -rf {location}/* && sudo umount -f {location}'
    return srv_msg.execute_shell_cmd(cmd, dest=dest)


def _allocate_disk_space(size="full",
                         location='/tmp/kea_ram_disk/allocate_disk',
                         dest=world.f_cfg.mgmt_address):
    """Quickly allocate space on ramdisk or anywhere you want ;).

    On some systems it may be required
    to execute this function twice to get entire disk allocated

    :param size: string parameter to define how much space should be allocated,
        by default it will take full space on disk that include "kea_ram_disk"
        in its path
    :param location: path to file that will be generated
    :param dest: IP address of a system on which we want to allocate disk space
    :return: result of executed command
    :rtype:
    """
    if size == "full":
        cmd = 'df -l | grep kea_ram_disk'
        size = int(srv_msg.execute_shell_cmd(cmd, dest=dest).stdout.split()[3]) * 1024
        # output of df -l, we want just Avail parameter,
        # wlodek@debian9-64-2:~ $ df -lh
        # Filesystem      Size  Used Avail Use% Mounted on
        # tmpfs              10240        0     10240   0% /tmp/kea_ram_disk

    cmd = f'fallocate -l {size} {location}'
    return srv_msg.execute_shell_cmd(cmd, dest=dest)


def _move_pgsql_to_ram_disk(location='/tmp/kea_ram_disk_pgsql', dest=world.f_cfg.mgmt_address):
    """Backup postgres data and config, new ramdisk, copy postgres data there and reconfigure postgres to use ramdisk.

    THIS FUNCTION MAY DAMAGE YOUR SETUP!

    :param location: location for new ram disk where pgsql will save all the data
    :param dest: destination host
    :return: two strings, location from where we moved postgres and path to configuration file
        required to reverse changes
    :rtype: tuple[str, str]
    """
    cmd = 'sudo systemctl start postgresql'
    srv_msg.execute_shell_cmd(cmd, dest=dest, save_results=False)

    # check where current location is, it should be similar to "/var/lib/postgresql/9.6/main"
    cmd = 'echo "SHOW data_directory;" | sudo -u postgres psql'
    pgsql_output = srv_msg.execute_shell_cmd(cmd, dest=dest).stdout
    for line in pgsql_output.split("\n"):
        if "postgresql" in line:
            full_current_location = line.strip()
            # this is correct only if pgsql is installed in default path
            current_location = "/".join(line.split("/")[:4])
            pgsql_location = "/".join(line.split("/")[4:])
            pgsql_version = pgsql_location.split("/", maxsplit=1)[0]
            break
    else:
        print("location not found")
        return 0

    cmd = 'sudo systemctl stop postgresql'
    srv_msg.execute_shell_cmd(cmd, dest=dest, save_results=False)

    # create ramdisk and copy data
    _create_ramdisk(location=location, size='300M')
    cmd = f'sudo rsync -av {current_location} {location}'
    srv_msg.execute_shell_cmd(cmd, dest=dest, save_results=False)

    # move content to different location
    cmd = f'sudo mv {full_current_location} {full_current_location}.back'
    srv_msg.execute_shell_cmd(cmd, dest=dest, save_results=False)

    # backup config
    pgsql_conf = f'/etc/postgresql/{pgsql_version}/main/postgresql.conf'
    cmd = f'sudo cp {pgsql_conf} {pgsql_conf}_backup'
    srv_msg.execute_shell_cmd(cmd, dest=dest, save_results=False)

    # change config, it have to point to new location
    new_location = os.path.join(location, 'postgresql', pgsql_version, "main")
    print(f'new location: {new_location}')
    cmd = "sudo sed -i 's/%s/%s/g' %s" % (full_current_location.replace("/", "\\/"),
                                          new_location.replace("/", "\\/"), pgsql_conf)
    srv_msg.execute_shell_cmd(cmd, dest=dest, save_results=False)

    cmd = 'sudo systemctl start postgresql'
    srv_msg.execute_shell_cmd(cmd, dest=dest, save_results=False)

    cmd = 'echo "SHOW data_directory;" | sudo -u postgres psql'
    srv_msg.execute_shell_cmd(cmd, dest=dest)

    # all data from ramdisk will be dumped, so we need just copy backup files
    print("\n\n---IMPORTANT DATA FOR MANUAL RECOVERY----")
    print("STOP PGSQL:     sudo systemctl stop postgresql")
    print(f"RESTORE DATA:   sudo mv {full_current_location}.back {full_current_location}")
    print(f"RESTORE CONFIG: sudo cp {pgsql_conf}_backup {pgsql_conf}")
    print("RESTART PGSQL:  sudo systemctl start postgresql")
    print("-----------------------------------------\n\n")
    return full_current_location, pgsql_conf


def _move_pgsql_back_to_default(previous_location, pgsql_cfg,
                                dest=world.f_cfg.mgmt_address):
    """Reverse all changes made in _move_pgsql_to_ram_disk.

    :param previous_location: previous pgsql data folder
    :param pgsql_cfg:
    :param dest:
    :return:
    """
    cmd = 'sudo systemctl stop postgresql'
    srv_msg.execute_shell_cmd(cmd, dest=dest, save_results=False)

    # restore data from backup
    cmd = f'sudo mv {previous_location}.back {previous_location}'
    srv_msg.execute_shell_cmd(cmd, dest=dest, save_results=False)

    # restore config
    cmd = f'sudo cp {pgsql_cfg}_backup {pgsql_cfg}'
    srv_msg.execute_shell_cmd(cmd, dest=dest, save_results=False)

    cmd = 'sudo systemctl start postgresql'
    srv_msg.execute_shell_cmd(cmd, dest=dest, save_results=False)

    cmd = 'echo "SHOW data_directory;" | sudo -u postgres psql'
    srv_msg.execute_shell_cmd(cmd, dest=dest)


@pytest.mark.v6
@pytest.mark.disabled
def test_v6_recover_pgsql():
    """In case if test_v6_full_disk_testing_pgsql will fail and not recover settings."""
    # I made static recovery just for my particular setup
    assert False, "this test may destroy your setup, remove this line if you really want to run it"
    _move_pgsql_back_to_default('/var/lib/postgresql/9.6/main', '/etc/postgresql/9.6/main/postgresql.conf')


@pytest.mark.v6
@pytest.mark.disabled
def test_v6_full_disk_testing_pgsql():
    """Create new ramdisk."""
    assert False, "this test may destroy your setup, remove this line if you really want to run it"
    full_current_location, pgsql_conf = _move_pgsql_to_ram_disk()
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::500')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel(world.f_cfg.mgmt_address)
    # decide what you want to do:
    # set memfile and log location to created ramdisk
    # world.dhcp_cfg["lease-database"] = {"type": "memfile", "name": "/tmp/kea_ram_disk/dhcp.leases"}
    # or set pgsql as lease backend
    # srv_control.define_temporary_lease_db_backend("postgresql")
    world.dhcp_cfg["hooks-libraries"][0].update({"parameters": {"path": "/tmp/kea_ram_disk_pgsql",
                                                                "base-name": "kea-forensic",
                                                                'name': '$(DB_NAME)',
                                                                'password': '$(DB_PASSWD)',
                                                                'type': 'postgresql',
                                                                'user': '$(DB_USER)'}})

    srv_control.add_hooks('libdhcp_lease_cmds.so')
    # srv_control.print_cfg()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _allocate_disk_space(location='/tmp/kea_ram_disk_pgsql/allocate_disk')
    print(_check_disk())

    # we expected that kea will keep working properly, assigning addresses in memory,
    # turned out that when it can't save lease to memfile/db it return NAK/NoAddrAvail code
    # even if disk is reported with no empty space left kea is able to save multiple leases
    # mostly it's 36.
    # Kea will keep working when it can't write main logs
    # Kea will keep working when it can't write forensic logs, and log error about this event in main logs
    generate_leases(leases_count=100, dhcp_version='v6', iapd=0, mac="01:02:0c:03:0a:00")

    _move_pgsql_back_to_default(full_current_location, pgsql_conf)


@pytest.mark.v6
@pytest.mark.disabled
def test_v6_full_disk_testing_memfile():
    """Check how kea6 behave when disk is full, using memfile and logs to file."""
    assert False, "this test may destroy your setup, remove this line if you really want to run it"
    misc.test_setup()
    _create_ramdisk()

    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::500')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel(world.f_cfg.mgmt_address)
    # set memfile and log location to created ramdisk
    world.dhcp_cfg["lease-database"] = {"type": "memfile", "name": "/tmp/kea_ram_disk/dhcp.leases"}
    world.dhcp_cfg["loggers"] = [{"debuglevel": 99,
                                  "name": "kea-dhcp6",
                                  "output-options": [{"output": "/tmp/kea_ram_disk/kea.log"}],
                                  "severity": "DEBUG"}]
    world.dhcp_cfg["hooks-libraries"][0].update({"parameters": {"path": "/tmp/kea_ram_disk/",
                                                                "base-name": "kea-forensic"}})

    srv_control.add_hooks('libdhcp_lease_cmds.so')
    # srv_control.print_cfg()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    _allocate_disk_space()
    print(_check_disk())

    # we expected that kea will keep working properly, assigning addresses in memory,
    # turned out that when it can't save lease to memfile/db it return NAK/NoAddrAvail code
    # even if disk is reported with no empty space left kea is able to save multiple leases
    # mostly it's 36.
    # Kea will keep working when it can't write main logs
    # Kea will keep working when it can't write forensic logs, and log error about this event in main logs
    generate_leases(leases_count=100, dhcp_version='v6', iapd=0, mac="01:02:0c:03:0a:00")

    send_command(cmd={"command": "lease6-get-all"})
    # srv_msg.test_pause()


@pytest.mark.v4
@pytest.mark.disabled
def test_v4_full_disk_testing():
    """Check how kea4 behave when disk is full, using memfile and logs to file."""
    assert False, "this test may destroy your setup, remove this line if you really want to run it"
    misc.test_setup()
    _create_ramdisk()

    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.150')
    srv_control.add_hooks('libdhcp_legal_log.so')
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel(world.f_cfg.mgmt_address)
    # set memfile and log location to created ramdisk
    world.dhcp_cfg["lease-database"] = {"type": "memfile", "name": "/tmp/kea_ram_disk/dhcp.leases"}
    world.dhcp_cfg["loggers"] = [{"debuglevel": 99,
                                  "name": "kea-dhcp4",
                                  "output-options": [{"output": "/tmp/kea_ram_disk/kea.log"}],
                                  "severity": "DEBUG"}]
    world.dhcp_cfg["hooks-libraries"][0].update({"parameters": {"path": "/tmp/kea_ram_disk/",
                                                                "base-name": "kea-forensic"}})

    srv_control.add_hooks('libdhcp_lease_cmds.so')
    # srv_control.print_cfg()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    _allocate_disk_space()
    print(_check_disk())

    # we expected that kea will keep working properly, assigning addresses in memory,
    # turned out that when it can't save lease to memfile/db it return NAK/NoAddrAvail code
    # even if disk is reported with no empty space left kea is able to save multiple leases
    # mostly it's 36.
    # Kea will keep working when it can't write main logs
    # Kea will keep working when it can't write forensic logs, and log error about this event in main logs
    generate_leases(leases_count=100, dhcp_version='v4', iapd=0, mac="01:02:0c:03:0a:00")

    send_command(cmd={"command": "lease4-get-all"})
