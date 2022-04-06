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


class _CreateCert:
    """
    This class creates TLS certificates for CA, server and client,
    mostly for testing Control Agent with TLS.
    class attributes return certificate files paths on server.
    eg. CreateCert.ca_key returns "/home/user/kea/ca_key.pem"

    download() function downloads selected certificate to test result directory on forge machine
    and returns full path of the file.
    """
    def __init__(self):
        # Assign certificate files paths to attributes.
        self.ca_key = os.path.join(world.f_cfg.software_install_path, 'ca_key.pem')
        self.ca_cert = os.path.join(world.f_cfg.software_install_path, 'ca_cert.pem')
        self.server_cert = os.path.join(world.f_cfg.software_install_path, 'server_cert.pem')
        self.server_csr = os.path.join(world.f_cfg.software_install_path, 'server_csr.csr')
        self.server_key = os.path.join(world.f_cfg.software_install_path, 'server_key.pem')
        self.client_cert = os.path.join(world.f_cfg.software_install_path, 'client_cert.pem')
        self.client_csr = os.path.join(world.f_cfg.software_install_path, 'client_csr.csr')
        self.client_key = os.path.join(world.f_cfg.software_install_path, 'client_key.pem')

        # Delete leftover certificates.
        srv_msg.remove_file_from_server(self.ca_key)
        srv_msg.remove_file_from_server(self.ca_cert)
        srv_msg.remove_file_from_server(self.server_cert)
        srv_msg.remove_file_from_server(self.server_csr)
        srv_msg.remove_file_from_server(self.server_key)
        srv_msg.remove_file_from_server(self.client_cert)
        srv_msg.remove_file_from_server(self.client_csr)
        srv_msg.remove_file_from_server(self.client_key)

        # Generate CA cert and key
        generate_ca = f'openssl req ' \
                      f'-x509 ' \
                      f'-nodes ' \
                      f'-days 3650 ' \
                      f'-newkey rsa:4096 ' \
                      f'-keyout {self.ca_key} ' \
                      f'-out {self.ca_cert} ' \
                      f'-subj "/C=US/ST=Acme State/L=Acme City/O=Acme Inc./CN={world.f_cfg.mgmt_address}"'

        # Generate server cert and key
        generate_server_priv = f'openssl genrsa -out {self.server_key} 4096 ; ' \
                               f'openssl req ' \
                               f'-new ' \
                               f'-key {self.server_key} ' \
                               f'-out {self.server_csr} ' \
                               f'-subj "/C=US/ST=Acme State/L=Acme City/O=Acme Inc./CN={world.f_cfg.mgmt_address}"'
        # Sign server cert
        generate_server = f'openssl x509 -req ' \
                          f'-days 1460 ' \
                          f'-in {self.server_csr} ' \
                          f'-CA {self.ca_cert} ' \
                          f'-CAkey {self.ca_key} ' \
                          f'-CAcreateserial -out {self.server_cert} ' \
                          f'-extensions SAN ' \
                          f'-extfile <(cat /etc/ssl/openssl.cnf' \
                          f' <(printf "\n[SAN]\nsubjectAltName=IP:{world.f_cfg.mgmt_address}"))'

        # Generate client cert and key
        generate_client_priv = f'openssl genrsa -out {self.client_key} 4096 ; ' \
                               f'openssl req ' \
                               f'-new ' \
                               f'-key {self.client_key} ' \
                               f'-out {self.client_csr} ' \
                               f'-subj "/C=US/ST=Acme State/L=Acme City/O=Acme Inc./CN=client"'

        # Sign client cert
        generate_client = f'openssl x509 -req ' \
                          f'-days 1460 ' \
                          f'-in {self.client_csr} ' \
                          f'-CA {self.ca_cert} ' \
                          f'-CAkey {self.ca_key} ' \
                          f'-CAcreateserial -out {self.client_cert} ' \

        fabric_sudo_command(generate_ca)
        fabric_sudo_command(generate_server_priv)
        fabric_sudo_command(generate_server)
        fabric_sudo_command(generate_client_priv)
        fabric_sudo_command(generate_client)

    def download(self, cert_type: str):
        """ This function downloads selected certificate to test result directory on forge machine
    and returns full path of the file.
        :param cert_type: select from: server_cert, server_key, client_cert, client_key, ca_cert, ca_key
        :return: Full path of the downloaded file on Forge machine.
        """
        if cert_type == 'server_cert':
            srv_msg.copy_remote(self.server_cert, 'server_cert.pem')
            return f'{world.cfg["test_result_dir"]}/server_cert.pem'
        if cert_type == 'server_key':
            fabric_sudo_command(f'chmod 644 {self.server_key}')
            srv_msg.copy_remote(self.server_cert, 'server_key.pem')
            return f'{world.cfg["test_result_dir"]}/server_key.pem'
        if cert_type == 'client_key':
            fabric_sudo_command(f'chmod 644 {self.client_key}')
            srv_msg.copy_remote(self.client_key, 'client_key.pem')
            return f'{world.cfg["test_result_dir"]}/client_key.pem'
        if cert_type == 'client_cert':
            srv_msg.copy_remote(self.client_cert, 'client_cert.pem')
            return f'{world.cfg["test_result_dir"]}/client_cert.pem'
        if cert_type == 'ca_cert':
            srv_msg.copy_remote(self.server_cert, 'ca_cert.pem')
            return f'{world.cfg["test_result_dir"]}/ca_cert.pem'
        if cert_type == 'ca_key':
            fabric_sudo_command(f'chmod 644 {self.server_key}')
            srv_msg.copy_remote(self.server_cert, 'ca_key.pem')
            return f'{world.cfg["test_result_dir"]}/ca_key.pem'
        assert False, 'Wrong Certificate type to download.'


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.ca
@pytest.mark.controlchannel
@pytest.mark.parametrize('client_cert_required', [True, False])
def test_ca_tls_basic(dhcp_version, client_cert_required):
    """
    Basic test of Control Agent with TLS connectivity.
    Parametrization sets requirement of client certificate.

    Test creates all required certificates on server(ca, server, client),
    downloads those required for connection to Forge machine and sends command to Kea.
    """
    # Create certificates.
    certificate = _CreateCert()
    # Download required certificates.
    server_cert = certificate.download('server_cert')
    ca_cert = certificate.download('ca_cert')
    if client_cert_required:
        client_cert = certificate.download('client_cert')
        client_key = certificate.download('client_key')

    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    # Configure Control Agent to use TLS.
    world.ca_cfg["Control-agent"]["trust-anchor"] = certificate.ca_cert
    world.ca_cfg["Control-agent"]["cert-file"] = certificate.server_cert
    world.ca_cfg["Control-agent"]["key-file"] = certificate.server_key
    world.ca_cfg["Control-agent"]["cert-required"] = client_cert_required
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = {"command": "status-get", "arguments": {}}

    if client_cert_required:
        # Send command using server_cert  and ca_cert to verify Kea server,
        # and client_cert+client_key to authorize message.
        response = srv_msg.send_ctrl_cmd(cmd, 'https', verify=server_cert, cert=(client_cert, client_key))
        response2 = srv_msg.send_ctrl_cmd(cmd, 'https', verify=ca_cert, cert=(client_cert, client_key))
        assert response == response2
    else:
        # Send command using server_cert and ca_cert to verify Kea server.
        response = srv_msg.send_ctrl_cmd(cmd, 'https', verify=server_cert)
        response2 = srv_msg.send_ctrl_cmd(cmd, 'https', verify=ca_cert)
        assert response == response2

    # Check the response.
    for option in ["pid",
                   "reload",
                   "uptime",
                   "multi-threading-enabled"]:
        assert option in response['arguments']


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.ca
@pytest.mark.controlchannel
@pytest.mark.parametrize('client_cert_required', [True, False])
def test_ca_tls_basic_negative(dhcp_version, client_cert_required):
    """
    Basic negative test of Control Agent with TLS connectivity.
    Parametrization sets requirement of client certificate.

    Test creates all required certificates on server(ca, server, client),
    downloads those required for connection to Forge machine and sends command to Kea
    using incomplete or wrong certificate set.
    """
    # Create certificates.
    certificate = _CreateCert()
    # Download required certificates.
    server_cert = certificate.download('server_cert')
    ca_cert = certificate.download('ca_cert')
    client_cert = certificate.download('client_cert')
    if client_cert_required:
        client_key = certificate.download('client_key')

    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    # Configure Control Agent to use TLS.
    world.ca_cfg["Control-agent"]["trust-anchor"] = certificate.ca_cert
    world.ca_cfg["Control-agent"]["cert-file"] = certificate.server_cert
    world.ca_cfg["Control-agent"]["key-file"] = certificate.server_key
    world.ca_cfg["Control-agent"]["cert-required"] = client_cert_required
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = {"command": "status-get", "arguments": {}}

    if client_cert_required:
        # Send command using missing verification and client certs.
        srv_msg.send_ctrl_cmd(cmd, 'https', exp_failed=True)
        # Send command using wrong verification and missing client certs.
        srv_msg.send_ctrl_cmd(cmd, 'https', verify=client_cert, exp_failed=True)
        # Send command using wrong verification and correct client certs.
        srv_msg.send_ctrl_cmd(cmd, 'https', verify=client_cert, cert=(client_cert, client_key), exp_failed=True)
        # Send command using correct verification and missing client certs.
        srv_msg.send_ctrl_cmd(cmd, 'https', verify=server_cert, exp_failed=True)
        # Send command using correct verification, wrong client cert and correct client key.
        srv_msg.send_ctrl_cmd(cmd, 'https', verify=server_cert, cert=(server_cert, client_key), exp_failed=True)
        # Send command using correct verification, correct client cert and wrong client key.
        srv_msg.send_ctrl_cmd(cmd, 'https', verify=server_cert, cert=(client_cert, ca_cert), exp_failed=True)
    else:
        # Send command using missing verification.
        srv_msg.send_ctrl_cmd(cmd, 'https', exp_failed=True)
        # Send command using wrong verification.
        srv_msg.send_ctrl_cmd(cmd, 'https', verify=client_cert, exp_failed=True)
