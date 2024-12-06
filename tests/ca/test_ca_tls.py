# Copyright (C) 2022-2024 Internet Systems Consortium.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Marcin Godzina

"""Kea Control channel TLS connection tests"""

# pylint: disable=unused-argument

import pytest
from src import misc
from src import srv_msg
from src import srv_control

from src.forge_cfg import world


@pytest.fixture(autouse=True)
def skip_if_ca_disabled():
    if not world.f_cfg.control_agent:
        pytest.skip('This test requires CA to be enabled')


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
    certificate = srv_control.generate_certificate()
    # Download required certificates.
    ca_cert = certificate.download('ca_cert')
    if client_cert_required:
        client_cert = certificate.download('client_cert')
        client_key = certificate.download('client_key')

    misc.test_setup()
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.enable_https(
        certificate.ca_cert,
        certificate.server_cert,
        certificate.server_key,
        client_cert_required
    )
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = {"command": "status-get", "arguments": {}}

    if client_cert_required:
        # Send command using ca_cert to verify Kea server,
        # Use client_cert+client_key to authorize message.
        response = srv_msg.send_ctrl_cmd(cmd, 'https', verify=ca_cert, cert=(client_cert, client_key))
    else:
        # Send command using server_cert and ca_cert to verify Kea server.
        response = srv_msg.send_ctrl_cmd(cmd, 'https', verify=ca_cert)

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
    certificate = srv_control.generate_certificate()
    # Download required certificates.
    server_cert = certificate.download('server_cert')
    ca_cert = certificate.download('ca_cert')
    if client_cert_required:
        client_key = certificate.download('client_key')
        client_cert = certificate.download('client_cert')

    misc.test_setup()
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.enable_https(
        certificate.ca_cert,
        certificate.server_cert,
        certificate.server_key,
        client_cert_required
    )
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
