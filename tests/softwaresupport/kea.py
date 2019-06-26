# Copyright (C) 2013-2019 Internet Systems Consortium.
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND INTERNET SYSTEMS CONSORTIUM
# DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# INTERNET SYSTEMS CONSORTIUM BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
# FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
# WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import os
import sys
from time import sleep
import logging
import json

from forge_cfg import world
from softwaresupport.multi_server_functions import fabric_run_command, fabric_send_file, remove_local_file,\
    copy_configuration_file, fabric_sudo_command, fabric_download_file, locate_entry, fabric_remove_file_command

log = logging.getLogger('forge')


def set_kea_ctrl_config():
    if world.f_cfg.software_install_path.endswith('/'):
        path = world.f_cfg.software_install_path[:-1]
    else:
        path = world.f_cfg.software_install_path

    kea6 = 'no'
    kea4 = 'no'
    ddns = 'no'
    ctrl_agent = 'no'
    if "kea6" in world.cfg["dhcp_under_test"]:
        kea6 = 'yes'
    elif "kea4" in world.cfg["dhcp_under_test"]:
        kea4 = 'yes'
    if world.ddns_enable:
        ddns = 'yes'
    if world.ctrl_enable:
        ctrl_agent = 'yes'
    world.cfg["keactrl"] = '''kea_config_file={path}/etc/kea/kea.conf
    dhcp4_srv={path}/sbin/kea-dhcp4
    dhcp6_srv={path}/sbin/kea-dhcp6
    dhcp_ddns_srv={path}/sbin/kea-dhcp-ddns
    ctrl_agent_srv={path}/sbin/kea-ctrl-agent
    netconf_srv={path}/sbin/kea-netconf
    kea_dhcp4_config_file={path}/etc/kea/kea.conf
    kea_dhcp6_config_file={path}/etc/kea/kea.conf
    kea_dhcp_ddns_config_file={path}/etc/kea/kea.conf
    kea_ctrl_agent_config_file={path}/etc/kea/kea.conf
    kea_netconf_config_file={path}/etc/kea/kea.conf
    dhcp4={kea4}
    dhcp6={kea6}
    dhcp_ddns={ddns}
    kea_verbose=no
    netconf=no
    ctrl_agent={ctrl_agent}
    '''.format(**locals())


def _write_cfg2(cfg):
    # log.info('provisioned cfg:\n%s', cfg)
    with open(world.cfg["cfg_file"], 'w') as cfg_file:
        json.dump(cfg, cfg_file, sort_keys=True, indent=4, separators=(',', ': '))

    cfg_file = open(world.cfg["cfg_file_2"], 'w')
    cfg_file.write(world.cfg["keactrl"])
    cfg_file.close()


def build_and_send_config_files2(cfg, connection_type, configuration_type="config-file",
                                 destination_address=world.f_cfg.mgmt_address):
    if configuration_type == "config-file" and connection_type == "SSH":
        world.cfg['leases'] = os.path.join(world.f_cfg.software_install_path, 'etc/kea/kea-leases4.csv')
        set_kea_ctrl_config()
        _write_cfg2(cfg)
        fabric_send_file(world.cfg["cfg_file"],
                         os.path.join(world.f_cfg.software_install_path, "etc/kea/kea.conf"),
                         destination_host=destination_address)
        fabric_send_file(world.cfg["cfg_file_2"],
                         os.path.join(world.f_cfg.software_install_path, "etc/kea/keactrl.conf"),
                         destination_host=destination_address)
        copy_configuration_file(world.cfg["cfg_file"], destination_host=destination_address)
        copy_configuration_file(world.cfg["cfg_file_2"], "kea_ctrl_config", destination_host=destination_address)
        remove_local_file(world.cfg["cfg_file"])
        remove_local_file(world.cfg["cfg_file_2"])
    elif configuration_type == "config-file" and connection_type is None:
        world.cfg['leases'] = os.path.join(world.f_cfg.software_install_path, 'etc/kea/kea-leases4.csv')
        set_kea_ctrl_config()
        cfg_write()
        copy_configuration_file(world.cfg["cfg_file"], destination_host=destination_address)
        remove_local_file(world.cfg["cfg_file"])


def clear_logs(destination_address=world.f_cfg.mgmt_address):
    fabric_remove_file_command(os.path.join(world.f_cfg.software_install_path, 'etc/kea/kea.log*'),
                               destination_host=destination_address)


def clear_all(tmp_db_type=None, destination_address=world.f_cfg.mgmt_address):
    clear_logs(destination_address)

    fabric_remove_file_command(os.path.join(world.f_cfg.software_install_path, 'var/lib/kea/*'),
                               destination_host=world.f_cfg.mgmt_address)
    fabric_remove_file_command(os.path.join(world.f_cfg.software_install_path, 'var/run/kea/*'),
                               destination_host=world.f_cfg.mgmt_address)

    # use kea script for cleaning DB
    cmd = 'bash {software_install_path}/share/kea/scripts/mysql/wipe_data.sh `mysql -u{db_user} -p{db_passwd} {db_name} -N -B'
    cmd += ' -e "SELECT CONCAT_WS(\'.\', version, minor) FROM schema_version;" 2>/dev/null` -N -B'
    cmd += ' -u{db_user} -p{db_passwd} {db_name}'
    cmd = cmd.format(software_install_path=world.f_cfg.software_install_path,
                     db_user=world.f_cfg.db_user,
                     db_passwd=world.f_cfg.db_passwd,
                     db_name=world.f_cfg.db_name)
    fabric_run_command(cmd, destination_host=world.f_cfg.mgmt_address)
