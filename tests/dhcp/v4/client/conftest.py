# Copyright (C) 2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Pytest fixtures and hooks for DHCPv4 client compliance tests."""

import time, logging

import pytest

from src.clientsupport.client_control import ClientController, validate_client_config
from src.clientsupport.mock_server import MockDHCP4Server
from src.forge_cfg import world

log = logging.getLogger('forge')
# ---------------------------------------------------------------------------
# CLI option: --run-timing
# ---------------------------------------------------------------------------

def pytest_addoption(parser):
    parser.addoption(
        '--run-timing',
        action='store_true',
        default=False,
        help='Run timing-sensitive client compliance tests (disabled by default for CI)',
    )


def pytest_collection_modifyitems(config, items):
    """Skip timing_sensitive tests unless --run-timing is given."""
    if not config.getoption('--run-timing'):
        skip_marker = pytest.mark.skip(
            reason='timing-sensitive; use --run-timing to enable'
        )
        for item in items:
            if 'timing_sensitive' in item.keywords:
                item.add_marker(skip_marker)


# ---------------------------------------------------------------------------
# Session-level validation
# ---------------------------------------------------------------------------

def pytest_configure(config):
    """Validate required CLIENT_* settings when client_compliance tests are collected."""
    # Only validate if we are actually running client_compliance tests.
    # We check for the marker expression or the test path.
    markexpr = config.option.markexpr if hasattr(config.option, 'markexpr') else ''
    args = config.args if hasattr(config, 'args') else []
    client_path = any('v4/client' in str(a) for a in args)
    client_mark = 'client_compliance' in markexpr
    if client_path or client_mark:
        validate_client_config()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_server():
    """Start a MockDHCP4Server for the duration of one test.

    Clears world.client_pkts before each test and stops the server on teardown.
    """
    world.client_pkts = []
    iface = world.f_cfg.iface
    server_ip = world.f_cfg.srv4_addr
    srv = MockDHCP4Server(iface=iface, server_ip=server_ip)
    srv.start()
    yield srv
    srv.stop()


@pytest.fixture
def dhcp_client():
    """Manage the remote DHCP client lifecycle for one test.

    Setup:  flush cached leases and interface IP, then start the client.
    Teardown: stop the client, then flush again for isolation.
    """
    from src.softwaresupport.multi_server_functions import fabric_sudo_command
    from src.forge_cfg import world
    
    ctrl = ClientController()
    ctrl.flush()
    time.sleep(0.5)
    # Remove any IP address from the client interface to ensure clean state
    fabric_sudo_command(f'ip addr flush scope global dev {world.f_cfg.client_iface}', ignore_errors=True)
    ctrl.start()
    yield ctrl
    ctrl.stop()
    time.sleep(0.5)
    ctrl.flush()
    # Clean up IP address after test too
    fabric_sudo_command(f'ip addr flush scope global dev {world.f_cfg.client_iface}', ignore_errors=True)
    

@pytest.fixture
def mock_server_short_lease():
    """Start a MockDHCP4Server with a very short lease for expiry tests.

    The short lease parameters are set BEFORE the server starts accepting
    packets, ensuring the first OFFER already carries the short lease time.
    Teardown stops the server.
    """
    world.client_pkts = []
    iface = world.f_cfg.iface
    server_ip = world.f_cfg.srv4_addr
    srv = MockDHCP4Server(iface=iface, server_ip=server_ip,
                          lease_time=30, t1=12, t2=24)
    srv.start()
    yield srv
    srv.stop()


@pytest.fixture
def mock_server_and_client(mock_server, dhcp_client):
    """Convenience fixture combining mock_server and dhcp_client."""
    yield mock_server, dhcp_client
