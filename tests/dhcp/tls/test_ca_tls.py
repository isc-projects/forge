# Copyright (C) 2022 Internet Systems Consortium.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Marcin Godzina

"""Kea Control channel TLS connection tests"""

# pylint: disable=invalid-name,line-too-long,unused-argument

import os
import pytest
from src import misc
from src import srv_msg
from src import srv_control
from src.forge_cfg import world
from src.softwaresupport.multi_server_functions import fabric_sudo_command
import requests
import json


class _CreateCert:
    def __init__(self):
        self.ca_key = os.path.join(world.f_cfg.software_install_path, 'ca_key.pem')
        self.ca_cert = os.path.join(world.f_cfg.software_install_path, 'ca_cert.pem')
        self.server_cert = os.path.join(world.f_cfg.software_install_path, 'server_cert.pem')
        self.server_csr = os.path.join(world.f_cfg.software_install_path, 'server_csr.csr')
        self.server_key = os.path.join(world.f_cfg.software_install_path, 'server_key.pem')

        srv_msg.remove_file_from_server(self.ca_key)
        srv_msg.remove_file_from_server(self.ca_cert)
        srv_msg.remove_file_from_server(self.server_cert)
        srv_msg.remove_file_from_server(self.server_csr)
        srv_msg.remove_file_from_server(self.server_key)

        generate_ca = f'openssl req ' \
                      f'-x509 ' \
                      f'-nodes ' \
                      f'-days 3650 ' \
                      f'-newkey rsa:4096 ' \
                      f'-keyout {self.ca_key} ' \
                      f'-out {self.ca_cert} ' \
                      f'-subj "/C=US/ST=Acme State/L=Acme City/O=Acme Inc./CN={world.f_cfg.mgmt_address}"'

        generate_server_priv = f'openssl genrsa -out {self.server_key} 4096 ; ' \
                               f'openssl req ' \
                               f'-new ' \
                               f'-key {self.server_key} ' \
                               f'-out {self.server_csr} ' \
                               f'-subj "/C=US/ST=Acme State/L=Acme City/O=Acme Inc./CN={world.f_cfg.mgmt_address}"'

        generate_server = f'openssl x509 -req ' \
                          f'-days 1460 ' \
                          f'-in {self.server_csr} ' \
                          f'-CA {self.ca_cert} ' \
                          f'-CAkey {self.ca_key} ' \
                          f'-CAcreateserial -out {self.server_cert}'

        fabric_sudo_command(generate_ca)
        fabric_sudo_command(generate_server_priv)
        fabric_sudo_command(generate_server)

    def download(self):
        srv_msg.copy_remote(self.server_cert)


@pytest.mark.v4
# @pytest.mark.v6
@pytest.mark.ca
@pytest.mark.controlchannel
def test_ca_tls(dhcp_version):
    certificate = _CreateCert()
    certificate.download()

    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    world.ca_cfg["Control-agent"]["trust-anchor"] = certificate.ca_cert
    world.ca_cfg["Control-agent"]["cert-file"] = certificate.server_cert
    world.ca_cfg["Control-agent"]["key-file"] = certificate.server_key
    world.ca_cfg["Control-agent"]["cert-required"] = False
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = {"command": "status-get", "arguments": {}}
   # response = srv_msg.send_ctrl_cmd(cmd, http)

    cmd = json.dumps(cmd)
    response = requests.post("https://192.168.61.9:8000",
                  headers={"Content-Type": "application/json"},
                  data=cmd, verify="/home/mgodzina/forge/tests_results/test_ca_tls_v4_/downloaded_file")

    print(response.text)