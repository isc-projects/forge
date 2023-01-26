# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
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
        "interface": "enp0s9",
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
                "interface": "enp0s9",
                "max-valid-lifetime": 4000,
                "min-valid-lifetime": 4000,
                "option-data": [
                    {
                        "always-send": False,
                        "code": 4,
                        "csv-format": True,
                        "data": "199.199.199.10",
                        "name": "time-servers",
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
                "interface": "enp0s9",
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


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.ca
@pytest.mark.controlchannel
@pytest.mark.parametrize('scope', ['global', 'shared_network', 'class'])
def test_config_commands_usercontext(scope, dhcp_version):
    """
    Test check if user-context is properly handled by config commands.
    Global, subnet, shared networks and client class containers are tested by parametrization.
    Config snippets are added to result of "config-get" and sent to server by "config-set"
    Forge uses "config-get" and "config-write" to check if changes were applied.
    """

    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Get current config
    cmd = {"command": "config-get", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    config_set = response['arguments']

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

    # Send modified config to server
    cmd = {"command": "config-set", "arguments": config_set}
    srv_msg.send_ctrl_cmd(cmd, 'http')

    # Get new config from server
    cmd = {"command": "config-get", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    config_get = response['arguments']
    config_get = sort_container(config_get)

    # Compare what we send and what Kea returned.
    assert config_set == config_get, "Send and received configurations are different"

    # Write config to file and download it
    remote_path = world.f_cfg.data_join('config-export.json')
    remove_file_from_server(remote_path)
    cmd = {"command": "config-write", "arguments": {"filename": remote_path}}
    srv_msg.send_ctrl_cmd(cmd, 'http')
    local_path = copy_file_from_server(remote_path, 'config-export.json')

    # Open downloaded file and sort it for easier comparison
    with open(local_path, 'r', encoding="utf-8") as config_file:
        config_write = json.load(config_file)
    config_write = sort_container(config_write)

    # Compare downloaded file with send config.
    assert config_set == config_write, "Send and downloaded file configurations are different"
