# Copyright (C) 2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Generic DHCP client controller for client compliance testing.

Each operation maps to a shell command configured in init_all.py via
CLIENT_*_CMD settings.  Commands are executed on the remote client machine
via SSH (sudo).  If a command is an empty string the operation is unsupported
and the calling test is skipped automatically.
"""

import pytest
import logging

log = logging.getLogger(__name__)

from src.forge_cfg import world
from src.softwaresupport.multi_server_functions import fabric_sudo_command


def _host():
    """Return the client management address, falling back to MGMT_ADDRESS."""
    addr = world.f_cfg.client_mgmt_address
    return addr if addr else world.f_cfg.mgmt_address


def _user():
    """Return the client SSH username, falling back to MGMT_USERNAME."""
    u = world.f_cfg.client_mgmt_username
    return u if u else world.f_cfg.mgmt_username


def _password():
    """Return the client SSH password, falling back to MGMT_PASSWORD."""
    p = world.f_cfg.client_mgmt_password
    return p if p else world.f_cfg.mgmt_password


def _run(cmd, ignore_errors=False):
    """Execute *cmd* as sudo on the remote client machine."""
    return fabric_sudo_command(
        cmd,
        destination_host=_host(),
        user_loc=_user(),
        password_loc=_password(),
        ignore_errors=ignore_errors,
    )


def _run_setting(setting_name, skip_if_empty=True, ignore_errors=False):
    """Look up *setting_name* from forge_cfg and run it.

    :param setting_name: attribute name on world.f_cfg (lower-cased)
    :param skip_if_empty: if True and the command is empty, call pytest.skip()
    :param ignore_errors: if True, do not abort on non-zero exit code
    :raises pytest.skip.Exception: when the command is empty and skip_if_empty
    """
    cmd = getattr(world.f_cfg, setting_name.lower(), '')
    if not cmd:
        if setting_name.lower() == 'client_release_cmd':
            log.info(f'{setting_name.upper()} is not configured — '
                     f'operation not supported by this client under test')
        if skip_if_empty:
            pytest.skip(f'{setting_name.upper()} is not configured — '
                        f'operation not supported by this client under test')
        return None
    elif setting_name.lower() == 'client_release_cmd':
        log.info(f'release command: {cmd}')
    return _run(cmd, ignore_errors=ignore_errors)


class ClientController:
    """Thin wrapper that drives a remote DHCP client via configured commands."""

    def start(self):
        """Start the DHCP client (CLIENT_START_CMD)."""
        _run_setting('client_start_cmd')

    def stop(self):
        """Stop the DHCP client (CLIENT_STOP_CMD)."""
        _run_setting('client_stop_cmd', ignore_errors=True)

    def release(self):
        """Send DHCPRELEASE and deconfigure address (CLIENT_RELEASE_CMD).

        Skips the test if CLIENT_RELEASE_CMD is not configured.
        """
        _run_setting('client_release_cmd', skip_if_empty=True)

    def flush(self):
        """Erase all cached lease state (CLIENT_FLUSH_CMD)."""
        _run_setting('client_flush_cmd', ignore_errors=True)

    def renew(self):
        """Trigger unicast renewal (CLIENT_RENEW_CMD).

        Skips the test if not configured; caller should fall back to
        timer-wait and mark the test timing_sensitive.
        """
        _run_setting('client_renew_cmd', skip_if_empty=True)

    def rebind(self):
        """Trigger broadcast rebind (CLIENT_REBIND_CMD).

        Skips the test if not configured; caller should fall back to
        timer-wait and mark the test timing_sensitive.
        """
        _run_setting('client_rebind_cmd', skip_if_empty=True)

    def inform(self):
        """Send DHCPINFORM (CLIENT_INFORM_CMD).

        Skips the test if not configured.
        """
        _run_setting('client_inform_cmd', skip_if_empty=True)

    def has_renew_cmd(self):
        """Return True if CLIENT_RENEW_CMD is configured."""
        return bool(getattr(world.f_cfg, 'client_renew_cmd', ''))

    def has_rebind_cmd(self):
        """Return True if CLIENT_REBIND_CMD is configured."""
        return bool(getattr(world.f_cfg, 'client_rebind_cmd', ''))

    def has_inform_cmd(self):
        """Return True if CLIENT_INFORM_CMD is configured."""
        return bool(getattr(world.f_cfg, 'client_inform_cmd', ''))


def validate_client_config():
    """Raise SystemExit if required CLIENT_* settings are missing.

    Called from the client compliance conftest at collection time.
    """
    required = [
        ('client_mgmt_address', 'CLIENT_MGMT_ADDRESS'),
        ('client_iface', 'CLIENT_IFACE'),
        ('client_start_cmd', 'CLIENT_START_CMD'),
        ('client_stop_cmd', 'CLIENT_STOP_CMD'),
        ('client_flush_cmd', 'CLIENT_FLUSH_CMD'),
    ]
    missing = []
    for attr, label in required:
        val = getattr(world.f_cfg, attr, '')
        if not val:
            missing.append(label)
    if missing:
        import sys
        print(f'\nERROR: The following settings are required for client_compliance '
              f'tests but are not set in init_all.py:\n  ' +
              '\n  '.join(missing))
        sys.exit(1)
