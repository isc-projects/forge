# Copyright (C) 2022-2025 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Marcin Godzina

"""config-* commands tests"""

import json
import pytest

from src import srv_control
from src import srv_msg
from src import misc
from src.forge_cfg import world
from src.protosupport.multi_protocol_functions import sort_container
from src.protosupport.multi_protocol_functions import remove_file_from_server, copy_file_from_server
from src.softwaresupport.multi_server_functions import verify_file_permissions

# Configuration snippets used in tests
GLOBAL_CONFIG = {
    "ISC": {
        "relay-info": [
            {
                "hop": 0,
                "link": "2001:db8:2::1000",
                "options": "0x00120008706F727431323334",
                "peer": "fe80::1"
            }
        ]
    },
    "version": [{"number": 1, "rev": 2}, {"id": 1, "no": 2}],
    "class": "!@#$%^&*(`)'_+=-?|\"\\\b\f\n\r\t",
    "tre,e": {"bra,nch1": {"treehouse": 1}, "bra,nch2": 2,
              "bra,nch3": {"leaf1": 1,
                           "leaf2": ["vein1", "vein2"]}}
}

SHAREDNETWORK_V6_CONFIG = [
    {
        "user-context": {"tre,e": {"bra,nch1": {"treehouse": 1}, "bra,nch2": 2,
                                   "bra,nch3": {"leaf1": 1,
                                                "leaf2": ["vein1", "vein2"]}}},
        "allocator": "iterative",
        "calculate-tee-times": True,
        "interface-id": "interface-abc",
        "max-preferred-lifetime": 3000,
        "max-valid-lifetime": 4000,
        "min-preferred-lifetime": 3000,
        "min-valid-lifetime": 4000,
        "name": "name-abc",
        "option-data": [],
        "pd-allocator": "iterative",
        "preferred-lifetime": 3000,
        "rapid-commit": False,
        "rebind-timer": 2000,
        "relay": {
            "ip-addresses": []
        },
        "renew-timer": 1000,
        "store-extended-info": False,
        "subnet6": [],
        "t1-percent": 0.5,
        "t2-percent": 0.8,
        "valid-lifetime": 4000
    },
    {
        "allocator": "iterative",
        "calculate-tee-times": True,
        "interface-id": "interface-xyz",
        "max-preferred-lifetime": 3000,
        "max-valid-lifetime": 4000,
        "min-preferred-lifetime": 3000,
        "min-valid-lifetime": 4000,
        "name": "name-xyz",
        "option-data": [],
        "pd-allocator": "iterative",
        "preferred-lifetime": 3000,
        "rapid-commit": False,
        "rebind-timer": 2000,
        "relay": {
            "ip-addresses": []
        },
        "renew-timer": 1000,
        "store-extended-info": False,
        "subnet6": [
            {
                "user-context": {"version": [{"number": 1, "rev": 2}, {"id": 1, "no": 2}]},
                "allocator": "iterative",
                "calculate-tee-times": True,
                "id": 3,
                "max-preferred-lifetime": 3000,
                "max-valid-lifetime": 4000,
                "min-preferred-lifetime": 3000,
                "min-valid-lifetime": 4000,
                "option-data": [],
                "pd-allocator": "iterative",
                "pd-pools": [],
                "pools": [
                    {
                        "option-data": [],
                        "pool": "2001:db8:c::1/128"
                    }
                ],
                "preferred-lifetime": 3000,
                "rebind-timer": 2000,
                "relay": {
                    "ip-addresses": []
                },
                "renew-timer": 1000,
                "reservations": [],
                "store-extended-info": False,
                "subnet": "2001:db8:c::/64",
                "t1-percent": 0.5,
                "t2-percent": 0.8,
                "valid-lifetime": 4000
            },
            {
                "calculate-tee-times": True,
                "allocator": "iterative",
                "id": 4,
                "max-preferred-lifetime": 3000,
                "max-valid-lifetime": 4000,
                "min-preferred-lifetime": 3000,
                "min-valid-lifetime": 4000,
                "option-data": [],
                "pd-allocator": "iterative",
                "pd-pools": [],
                "pools": [
                    {
                        "option-data": [],
                        "pool": "2001:db8:d::1/128"
                    }
                ],
                "preferred-lifetime": 3000,
                "rebind-timer": 2000,
                "relay": {
                    "ip-addresses": []
                },
                "renew-timer": 1000,
                "reservations": [],
                "store-extended-info": False,
                "subnet": "2001:db8:d::/64",
                "t1-percent": 0.5,
                "t2-percent": 0.8,
                "valid-lifetime": 4000
            }
        ],
        "t1-percent": 0.5,
        "t2-percent": 0.8,
        "valid-lifetime": 4000
    }
]

SHAREDNETWORK_V4_CONFIG = [
    {
        "user-context": {"tre,e": {"bra,nch1": {"treehouse": 1}, "bra,nch2": 2,
                                   "bra,nch3": {"leaf1": 1,
                                                "leaf2": ["vein1", "vein2"]}}},
        "allocator": "iterative",
        "calculate-tee-times": False,
        "interface": world.f_cfg.server_iface,
        "max-valid-lifetime": 4000,
        "min-valid-lifetime": 4000,
        "name": "name-abc",
        "option-data": [],
        "rebind-timer": 2000,
        "relay": {
            "ip-addresses": []
        },
        "renew-timer": 1000,
        "store-extended-info": False,
        "subnet4": [
            {
                "user-context": {"version": [{"number": 1, "rev": 2}, {"id": 1, "no": 2}]},
                "allocator": "iterative",
                "4o6-interface": "",
                "4o6-interface-id": "",
                "4o6-subnet": "",
                "calculate-tee-times": False,
                "id": 1,
                "interface": world.f_cfg.server_iface,
                "max-valid-lifetime": 4000,
                "min-valid-lifetime": 4000,
                "option-data": [
                    {
                        "always-send": False,
                        "code": 4,
                        "csv-format": True,
                        "data": "199.199.199.10",
                        "name": "time-servers",
                        "never-send": False,
                        "space": "dhcp4"
                    }
                ],
                "pools": [
                    {
                        "option-data": [],
                        "pool": "192.168.50.1/32"
                    }
                ],
                "rebind-timer": 2000,
                "relay": {
                    "ip-addresses": []
                },
                "renew-timer": 1000,
                "reservations": [],
                "store-extended-info": False,
                "subnet": "192.168.50.0/24",
                "t1-percent": 0.5,
                "t2-percent": 0.875,
                "valid-lifetime": 4000
            },
            {
                "allocator": "iterative",
                "4o6-interface": "",
                "4o6-interface-id": "",
                "4o6-subnet": "",
                "calculate-tee-times": False,
                "id": 2,
                "interface": world.f_cfg.server_iface,
                "max-valid-lifetime": 4000,
                "min-valid-lifetime": 4000,
                "option-data": [],
                "pools": [
                    {
                        "option-data": [],
                        "pool": "192.168.51.1/32"
                    }
                ],
                "rebind-timer": 2000,
                "relay": {
                    "ip-addresses": []
                },
                "renew-timer": 1000,
                "reservations": [],
                "store-extended-info": False,
                "subnet": "192.168.51.0/24",
                "t1-percent": 0.5,
                "t2-percent": 0.875,
                "valid-lifetime": 4000
            }
        ],
        "t1-percent": 0.5,
        "t2-percent": 0.875,
        "valid-lifetime": 4000
    },
    {
        'allocator': 'iterative',
        "calculate-tee-times": False,
        "max-valid-lifetime": 4000,
        "min-valid-lifetime": 4000,
        "name": "name-xyz",
        "option-data": [],
        "rebind-timer": 2000,
        "relay": {
            "ip-addresses": [
                "192.168.50.3"
            ]
        },
        "renew-timer": 1000,
        "store-extended-info": False,
        "subnet4": [
            {
                'allocator': 'iterative',
                "4o6-interface": "",
                "4o6-interface-id": "",
                "4o6-subnet": "",
                "calculate-tee-times": False,
                "id": 3,
                "max-valid-lifetime": 4000,
                "min-valid-lifetime": 4000,
                "option-data": [
                    {
                        "always-send": False,
                        "code": 4,
                        "csv-format": True,
                        "data": "199.199.199.100",
                        "name": "time-servers",
                        "never-send": False,
                        "space": "dhcp4"
                    }
                ],
                "pools": [
                    {
                        "option-data": [],
                        "pool": "192.168.52.1/32"
                    }
                ],
                "rebind-timer": 2000,
                "relay": {
                    "ip-addresses": [
                        "192.168.50.3"
                    ]
                },
                "renew-timer": 1000,
                "reservations": [],
                "store-extended-info": False,
                "subnet": "192.168.52.0/24",
                "t1-percent": 0.5,
                "t2-percent": 0.875,
                "valid-lifetime": 4000
            },
            {
                'allocator': 'iterative',
                "4o6-interface": "",
                "4o6-interface-id": "",
                "4o6-subnet": "",
                "calculate-tee-times": False,
                "id": 4,
                "max-valid-lifetime": 4000,
                "min-valid-lifetime": 4000,
                "option-data": [
                    {
                        "always-send": False,
                        "code": 4,
                        "csv-format": True,
                        "data": "199.199.199.200",
                        "name": "time-servers",
                        "never-send": False,
                        "space": "dhcp4"
                    }
                ],
                "pools": [
                    {
                        "option-data": [],
                        "pool": "192.168.53.1/32"
                    }
                ],
                "rebind-timer": 2000,
                "relay": {
                    "ip-addresses": [
                        "192.168.50.3"
                    ]
                },
                "renew-timer": 1000,
                "reservations": [],
                "store-extended-info": False,
                "subnet": "192.168.53.0/24",
                "t1-percent": 0.5,
                "t2-percent": 0.875,
                "valid-lifetime": 4000
            }
        ],
        "t1-percent": 0.5,
        "t2-percent": 0.875,
        "valid-lifetime": 4000
    }
]

CLASS_v4_CONFIG = [
    {
        "boot-file-name": "",
        "name": "first-class",
        "next-server": "0.0.0.0",
        "option-data": [],
        "option-def": [],
        "server-hostname": "",
        "user-context": {"version": [{"number": 1, "rev": 2}, {"id": 1, "no": 2}]}
    },
    {
        "boot-file-name": "",
        "name": "economy-class",
        "next-server": "0.0.0.0",
        "option-data": [],
        "option-def": [],
        "server-hostname": "",
        "user-context": {"tre,e": {"bra,nch1": {"treehouse": 1}, "bra,nch2": 2,
                                   "bra,nch3": {"leaf1": 1,
                                                "leaf2": ["vein1", "vein2"]}}}
    }
]

CLASS_v6_CONFIG = [
    {
        "name": "first-class",
        "option-data": [],
        "user-context": {"version": [{"number": 1, "rev": 2}, {"id": 1, "no": 2}]}
    },
    {
        "name": "economy-class",
        "option-data": [],
        "user-context": {"tre,e": {"bra,nch1": {"treehouse": 1}, "bra,nch2": 2,
                                   "bra,nch3": {"leaf1": 1,
                                                "leaf2": ["vein1", "vein2"]}}}
    }
]

EMPTY_RESERVATIONS_V4_CONFIG = [
    {
        "boot-file-name": "",
        "client-classes": [],
        "hostname": "",
        "hw-address": "ff:01:02:03:ff:04",
        "next-server": "0.0.0.0",
        "option-data": [],
        "server-hostname": ""
    }
]

EMPTY_RESERVATIONS_V6_CONFIG = [
    {
        "client-classes": [],
        "duid": "00:03:00:01:f6:f5:f4:f3:f2:22",
        "hostname": "",
        "ip-addresses": [],
        "option-data": [],
        "prefixes": []

    }
]


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.ca
@pytest.mark.controlchannel
@pytest.mark.parametrize('scope', ['global', 'shared_network', 'class'])
def test_config_commands_usercontext(scope: str, dhcp_version: str):
    """
    Test check if user-context is properly handled by config commands.
    Global, subnet, shared networks and client class containers are tested by parametrization.
    Config snippets are added to result of "config-get" and sent to server by "config-set"
    Forge uses "config-get" and "config-write" to check if changes were applied.

    :type scope: str
    :param scope: Scope of the config
    :type dhcp_version: str
    :param dhcp_version: DHCP version
    """

    misc.test_setup()
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Get current config
    cmd = {"command": "config-get", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    config_set = response['arguments']
    hash1 = config_set['hash']
    del config_set['hash']

    # Add user context to configuration
    if scope == 'global':
        config_set[f"Dhcp{dhcp_version[1]}"]['user-context'] = GLOBAL_CONFIG
    if scope == 'shared_network' and dhcp_version == 'v4':
        config_set[f"Dhcp{dhcp_version[1]}"]['shared-networks'] = SHAREDNETWORK_V4_CONFIG
    if scope == 'shared_network' and dhcp_version == 'v6':
        config_set[f"Dhcp{dhcp_version[1]}"]['shared-networks'] = SHAREDNETWORK_V6_CONFIG
    if scope == 'class' and dhcp_version == 'v4':
        config_set[f"Dhcp{dhcp_version[1]}"]['client-classes'] = CLASS_v4_CONFIG
    if scope == 'class' and dhcp_version == 'v6':
        config_set[f"Dhcp{dhcp_version[1]}"]['client-classes'] = CLASS_v6_CONFIG

    # Sort config for easier comparison
    config_set = sort_container(config_set)

    # Test modified config on server
    cmd = {"command": "config-test", "arguments": config_set}
    srv_msg.send_ctrl_cmd(cmd, 'http')

    # Send modified config to server
    cmd = {"command": "config-set", "arguments": config_set}
    resp = srv_msg.send_ctrl_cmd(cmd, 'http')
    hash2 = resp['arguments']['hash']

    # Get new config from server
    cmd = {"command": "config-get", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    config_get = response['arguments']
    hash3 = config_get['hash']
    del config_get['hash']
    config_get = sort_container(config_get)

    # Compare what we send and what Kea returned.
    assert config_set == config_get, "Send and received configurations are different"

    # let's check all 3 hash values:
    assert hash1 != hash2 == hash3, "First hash should be different than two returned later in the test"

    # Write config to file and download it
    remote_path = world.f_cfg.data_join('config-export.json')
    remove_file_from_server(remote_path)
    cmd = {"command": "config-write", "arguments": {"filename": remote_path}}
    srv_msg.send_ctrl_cmd(cmd, 'http')
    verify_file_permissions(remote_path)
    local_path = copy_file_from_server(remote_path, 'config-export.json')

    # Open downloaded file and sort it for easier comparison
    with open(local_path, 'r', encoding="utf-8") as config_file:
        config_write = json.load(config_file)
    config_write = sort_container(config_write)

    # Compare downloaded file with send config.
    assert config_set == config_write, "Send and downloaded file configurations are different"


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.ca
@pytest.mark.controlchannel
def test_config_commands_empty_reservations(dhcp_version: str):
    """
    Test check if user-context is properly handled by config commands.
    Global, subnet, shared networks and client class containers are tested by parametrization.
    Config snippets are added to result of "config-get" and sent to server by "config-set"
    Forge uses "config-get" and "config-write" to check if changes were applied.

    :type dhcp_version: str
    :param dhcp_version: DHCP version
    """

    misc.test_setup()
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Get current config
    cmd = {"command": "config-get", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    config_set = response['arguments']
    hash1 = config_set['hash']
    del config_set['hash']

    # Add reservation to configuration
    if dhcp_version == 'v4':
        config_set[f"Dhcp{dhcp_version[1]}"]['reservations'] = [{"hw-address": "ff:01:02:03:ff:04"}]
    else:
        config_set[f"Dhcp{dhcp_version[1]}"]['reservations'] = [{"duid": "00:03:00:01:f6:f5:f4:f3:f2:22"}]

    # Sort config for easier comparison
    config_set = sort_container(config_set)

    # Test modified config on server
    cmd = {"command": "config-test", "arguments": config_set}
    srv_msg.send_ctrl_cmd(cmd, 'http')

    # Send modified config to server
    cmd = {"command": "config-set", "arguments": config_set}
    resp = srv_msg.send_ctrl_cmd(cmd, 'http')
    hash2 = resp['arguments']['hash']
    # Get new config from server
    cmd = {"command": "config-get", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    config_get = response['arguments']
    hash3 = config_get['hash']
    del config_get['hash']
    config_get = sort_container(config_get)

    # update local config with expected values
    if dhcp_version == 'v4':
        config_set[f"Dhcp{dhcp_version[1]}"]['reservations'] = EMPTY_RESERVATIONS_V4_CONFIG
    else:
        config_set[f"Dhcp{dhcp_version[1]}"]['reservations'] = EMPTY_RESERVATIONS_V6_CONFIG

    # Sort config for easier comparison
    config_set = sort_container(config_set)

    # Compare what we send and what Kea returned.
    assert config_set == config_get, "Send and received configurations are different"

    # let's check all 3 hash values:
    assert hash1 != hash2 == hash3, "First hash should be different than two returned later in the test"

    # Write config to file and download it
    remote_path = world.f_cfg.data_join('config-export.json')
    remove_file_from_server(remote_path)
    cmd = {"command": "config-write", "arguments": {"filename": remote_path}}
    srv_msg.send_ctrl_cmd(cmd, 'http')
    verify_file_permissions(remote_path)
    local_path = copy_file_from_server(remote_path, 'config-export.json')

    # Open downloaded file and sort it for easier comparison
    with open(local_path, 'r', encoding="utf-8") as config_file:
        config_write = json.load(config_file)
    config_write = sort_container(config_write)

    # Compare downloaded file with send config.
    assert config_set == config_write, "Send and downloaded file configurations are different"


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.ca
@pytest.mark.controlchannel
def test_config_hash_get(dhcp_version: str):
    """
    Test check if user-context is properly handled by config commands.
    Global, subnet, shared networks and client class containers are tested by parametrization.
    Config snippets are added to result of "config-get" and sent to server by "config-set"
    Forge uses "config-get" and "config-write" to check if changes were applied.

    :type dhcp_version: str
    :param dhcp_version: DHCP version
    """

    misc.test_setup()
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Get current config
    cmd = {"command": "config-hash-get", "arguments": {}}
    hash1 = srv_msg.send_ctrl_cmd(cmd, 'http')["arguments"]["hash"]
    hash2 = srv_msg.send_ctrl_cmd(cmd, 'http')["arguments"]["hash"]
    assert hash1 == hash2, "Got two different hashes without config change"

    cmd = {"command": "config-get", "arguments": {}}
    cfg_get = srv_msg.send_ctrl_cmd(cmd, 'http')["arguments"]
    hash3 = cfg_get['hash']
    assert hash2 == hash3, "Got two different hashes without config change"
    del cfg_get['hash']

    # let's set something different as a config and check if has changed
    cfg_get[f"Dhcp{dhcp_version[1]}"]["option-def"] = [{
        "array": False,
        "code": 122,
        "encapsulate": "opt",
        "name": "optionX",
        "record-types": "",
        "space": "option122",
        "type": "empty"
    }]

    cmd = {"command": "config-set", "arguments": cfg_get}
    cfg_set = srv_msg.send_ctrl_cmd(cmd, 'http')["arguments"]
    hash4 = cfg_set['hash']
    assert hash4 != hash1, "Config has changed but hash not!"

    cmd = {"command": "config-hash-get", "arguments": {}}
    hash5 = srv_msg.send_ctrl_cmd(cmd, 'http')["arguments"]["hash"]
    assert hash4 == hash5, "hash returned in config-get-hash and config-set are different!"

    # let's set config from the beginning
    cfg_get[f"Dhcp{dhcp_version[1]}"]["option-def"] = []

    cmd = {"command": "config-set", "arguments": cfg_get}
    cfg_set = srv_msg.send_ctrl_cmd(cmd, 'http')["arguments"]
    hash6 = cfg_set['hash']

    assert hash1 == hash2 == hash3 == hash6 != hash4, "Kea reconfigured with the same config, hash shouldn't change"
    cmd = {"command": "config-hash-get", "arguments": {}}
    hash7 = srv_msg.send_ctrl_cmd(cmd, 'http')["arguments"]["hash"]
    assert hash6 == hash7, "hash returned in config-get-hash and config-set are different!"


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_config_commands_config_write(dhcp_version: str, backend: str):
    """Test config-write command with different backends.

    :type backend: str
    :param backend: backend type
    :type dhcp_version: str
    :param dhcp_version: DHCP version
    """
    misc.test_setup()
    if backend != 'memfile':
        srv_control.define_lease_db_backend(backend,
                                            db_name=world.f_cfg.db_name,
                                            db_host=world.f_cfg.db_host,
                                            db_user=world.f_cfg.db_user,
                                            db_passwd=world.f_cfg.db_passwd,
                                            retry_on_startup=True,
                                            max_reconnect_tries=3,
                                            reconnect_wait_time=120,
                                            on_fail="stop-retry-exit")

    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')

    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    if dhcp_version == 'v4':
        srv_msg.DORA('192.168.50.1')
    else:
        srv_msg.SARR('2001:db8:1::50')
    srv_msg.check_leases(srv_msg.get_all_leases(), backend=backend)
    cmd = {"command": "config-write", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    verify_file_permissions(response['arguments']['filename'])

    srv_control.start_srv('DHCP', 'reconfigured')

    if world.proto == 'v4':
        srv_msg.DORA('192.168.50.1')
    else:
        srv_msg.SARR('2001:db8:1::50')
    srv_msg.check_leases(srv_msg.get_all_leases(), backend=backend)


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.controlchannel
def test_config_commands_config_write_path(dhcp_version: str):
    """Test config-write limitig output paths.

    :type dhcp_version: str
    :param dhcp_version: DHCP version
    """
    misc.test_setup()
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')

    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = {"command": "config-write", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    verify_file_permissions(response['arguments']['filename'])

    illegal_paths = [
        ['/tmp/config-write.json', 1, 'not allowed to write config into'],
        ['~/config-write.json', 1, 'not allowed to write config into'],
        ['/var/config-write.json', 1, 'not allowed to write config into'],
        ['/srv/config-write.json', 1, 'not allowed to write config into'],
        ['/etc/kea/config-write.json', 1, 'not allowed to write config into'],
    ]
    for path, exp_result, exp_text in illegal_paths:
        srv_msg.remove_file_from_server(path)
        cmd = {"command": "config-write", "arguments": {"filename": path}}
        response = srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=exp_result)
        assert exp_text in response['text']


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.controlchannel
def test_config_output_options(dhcp_version):
    """
    Test check if output-options is properly handled by config commands.
    Checks kea#3594

    :type dhcp_version: str
    :param dhcp_version: DHCP version
    """

    misc.test_setup()
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Get current config
    cmd = {"command": "config-get", "arguments": {}}
    cfg_get = srv_msg.send_ctrl_cmd(cmd, 'http')["arguments"]
    del cfg_get['hash']
    # let's set something different as a config and check if has changed
    cfg_get[f"Dhcp{dhcp_version[1]}"]["loggers"][0]["output_options"] = cfg_get[
        f"Dhcp{dhcp_version[1]}"
    ]["loggers"][0].pop("output-options")

    cmd = {"command": "config-set", "arguments": cfg_get}
    srv_msg.send_ctrl_cmd(cmd, 'http')

    cmd = {"command": "config-get", "arguments": {}}
    cfg_get2 = srv_msg.send_ctrl_cmd(cmd, 'http')["arguments"]
    del cfg_get2['hash']

    assert (
        "output_options" in cfg_get2[f"Dhcp{dhcp_version[1]}"]["loggers"][0]
        or "output-options" in cfg_get2[f"Dhcp{dhcp_version[1]}"]["loggers"][0]
    ), "output_options or output-options not found in config"
