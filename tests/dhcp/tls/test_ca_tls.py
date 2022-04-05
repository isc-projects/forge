# Copyright (C) 2022 Internet Systems Consortium.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Marcin Godzina

"""Kea Control channel TLS connection tests"""

# pylint: disable=invalid-name,line-too-long,unused-argument

import pytest
import os
import glob
from src import misc
from src import srv_msg
from src import srv_control
from src.forge_cfg import world
from src.softwaresupport.multi_server_functions import fabric_sudo_command


@pytest.mark.v4
# @pytest.mark.v6
@pytest.mark.ca
@pytest.mark.controlchannel
def test_ca_tls(dhcp_version):
    """
    """
    srv_msg.remove_file_from_server(os.path.join(world.f_cfg.software_install_path, 'ca_ca.crt'))
    srv_msg.remove_file_from_server(os.path.join(world.f_cfg.software_install_path, 'ca_server.crt'))
    srv_msg.remove_file_from_server(os.path.join(world.f_cfg.software_install_path, 'ca_server.key'))
    srv_msg.send_file_to_server(glob.glob("**/ca_ca.crt", recursive=True)[0],
                                os.path.join(world.f_cfg.software_install_path, 'ca_ca.crt'))
    srv_msg.send_file_to_server(glob.glob("**/ca_server.crt", recursive=True)[0],
                                os.path.join(world.f_cfg.software_install_path, 'ca_server.crt'))
    srv_msg.send_file_to_server(glob.glob("**/ca_server.key", recursive=True)[0],
                                os.path.join(world.f_cfg.software_install_path, 'ca_server.key'))

    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    world.ca_cfg["Control-agent"]["trust-anchor"] = os.path.join(world.f_cfg.software_install_path, 'ca_ca.crt')
    world.ca_cfg["Control-agent"]["cert-file"] = os.path.join(world.f_cfg.software_install_path, 'ca_server.crt')
    world.ca_cfg["Control-agent"]["key-file"] = os.path.join(world.f_cfg.software_install_path, 'ca_server.key')
    world.ca_cfg["Control-agent"]["cert-required"] = False
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
