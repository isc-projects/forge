# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import copy
import pytest

from src import misc
from src import srv_control
from src import srv_msg

from src.protosupport.dhcp4_scen import DHCPv6_STATUS_CODES
from src.protosupport.multi_protocol_functions import log_contains
from src.forge_cfg import world


def _bump_subnets(shared_networks: bool = False):
    """
    Increase subnet ID, subnet, pools and pd-pools for either usual subnets or shared networks so
    that they don't come in conflict with other subnets/pools.
    :param shared_networks: whether to act on shared networks; if not action is taken on usual subnets
    """
    subnetx = f'subnet{world.proto[-1]}'
    subnet_list = world.dhcp_cfg['shared-networks'][0][subnetx] if shared_networks else world.dhcp_cfg[subnetx]
    for i, _ in enumerate(world.dhcp_cfg[subnetx]):
        subnet_list[i]['id'] += 1000
        if world.proto == 'v4':
            subnet_list[i]['subnet'] = subnet_list[i]['subnet'].replace('192', '202')
            if 'pools' in subnet_list[i]:
                for j, _ in enumerate(subnet_list[i]['pools']):
                    pool = subnet_list[i]['pools'][j]['pool']
                    subnet_list[i]['pools'][j]['pool'] = pool.replace('192', '202')
            if 'pd-pools' in subnet_list[i]:
                for j, _ in enumerate(subnet_list[i]['pd-pools']):
                    prefix = subnet_list[i]['pd-pools'][j]['prefix']
                    subnet_list[i]['pd-pools'][j]['prefix'] = prefix.replace('192', '202')
        else:
            subnet_list[i]['subnet'] = subnet_list[i]['subnet'].replace('2001', '3001')
            if 'pools' in subnet_list[i]:
                for j, _ in enumerate(subnet_list[i]['pools']):
                    pool = subnet_list[i]['pools'][j]['pool']
                    subnet_list[i]['pools'][j]['pool'] = pool.replace('2001', '3001')
            if 'pd-pools' in subnet_list[i]:
                for j, _ in enumerate(subnet_list[i]['pd-pools']):
                    prefix = subnet_list[i]['pd-pools'][j]['prefix']
                    subnet_list[i]['pd-pools'][j]['prefix'] = prefix.replace('2001', '3001')


@pytest.mark.v4
@pytest.mark.v4_bootp
@pytest.mark.parametrize('subnet_scope', ['subnet', 'shared-network'])
def test_overlapping_pools(subnet_scope: str):
    """
    Check that overlapping pools belonging to the same subnet result in a configuration error.
    :param subnet_scope: subnet-level pools or shared-network-level pools
    """
    misc.test_setup()

    subnets = [
        {
            'id': 1,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '192.168.0.1 - 192.168.0.3'
                },
                {
                    'pool': '192.168.0.2 - 192.168.0.4'
                }
            ],
            'subnet': '192.168.0.0/24'
        }
    ]

    if subnet_scope == 'subnet':
        world.dhcp_cfg.update({'subnet4': copy.deepcopy(subnets)})
    if subnet_scope == 'shared-network':
        world.dhcp_cfg.update({
            'shared-networks': [
                {
                    'name': 'network',
                    'interface': world.f_cfg.server_iface,
                    'subnet4': copy.deepcopy(subnets)
                }
            ]
        })

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started', should_succeed=False)
    log_contains(
        'DHCP4_PARSER_FAIL failed to create or run parser for configuration element '
        + ('shared-networks' if 'shared-network' == subnet_scope else 'subnet4') + ': '
        'subnet configuration failed: a pool of type V4, with the following address range: '
        '192.168.0.2-192.168.0.4 overlaps with an existing pool in the subnet: '
        '192.168.0.0/24 to which it is being added')


@pytest.mark.v6
@pytest.mark.parametrize('subnet_scope', ['subnet', 'shared-network'])
def test_overlapping_ia_na_pools(subnet_scope: str):
    """
    Check that overlapping pools belonging to the same subnet result in a configuration error.
    :param subnet_scope: subnet-level pools or shared-network-level pools
    """
    misc.test_setup()

    subnets = [
        {
            'id': 1,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '2001:db8:1::1 - 2001:db8:1::3'
                },
                {
                    'pool': '2001:db8:1::2 - 2001:db8:1::4'
                }
            ],
            'subnet': '2001:db8:1::/64'
        }
    ]

    if subnet_scope == 'subnet':
        world.dhcp_cfg.update({'subnet6': copy.deepcopy(subnets)})
    if subnet_scope == 'shared-network':
        world.dhcp_cfg.update({
            'shared-networks': [
                {
                    'name': 'network',
                    'interface': world.f_cfg.server_iface,
                    'subnet6': copy.deepcopy(subnets)
                }
            ]
        })

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started', should_succeed=False)
    log_contains(
        'DHCP6_PARSER_FAIL failed to create or run parser for configuration element '
        + ('shared-networks' if 'shared-network' == subnet_scope else 'subnet6') + ': '
        'subnet configuration failed: a pool of type IA_NA, with the following address range: '
        '2001:db8:1::2-2001:db8:1::4 overlaps with an existing pool in the subnet: '
        '2001:db8:1::/64 to which it is being added')


@pytest.mark.v6
@pytest.mark.parametrize('subnet_scope', ['subnet', 'shared-network'])
def test_overlapping_ia_pd_pools(subnet_scope: str):
    """
    Check that overlapping PD pools belonging to the same subnet result in a configuration error.
    :param subnet_scope: subnet-level pools or shared-network-level pools
    """
    misc.test_setup()

    subnets = [
        {
            'id': 1,
            'interface': world.f_cfg.server_iface,
            'pd-pools': [
                {
                    "delegated-len": 96,
                    "prefix": "2001:db8:1::",
                    "prefix-len": 80
                },
                {
                    "delegated-len": 98,
                    "prefix": "2001:db8:1::",
                    "prefix-len": 82
                }
            ],
            'subnet': '2001:db8:1::/64'
        }
    ]

    if subnet_scope == 'subnet':
        world.dhcp_cfg.update({'subnet6': copy.deepcopy(subnets)})
    if subnet_scope == 'shared-network':
        world.dhcp_cfg.update({
            'shared-networks': [
                {
                    'name': 'network',
                    'interface': world.f_cfg.server_iface,
                    'subnet6': copy.deepcopy(subnets)
                }
            ]
        })

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started', should_succeed=False)
    log_contains(
        'DHCP6_PARSER_FAIL failed to create or run parser for configuration element '
        + ('shared-networks' if 'shared-network' == subnet_scope else 'subnet6') + ': '
        'subnet configuration failed: a pool of type IA_PD, with the following address range: '
        '2001:db8:1::-2001:db8:1::3fff:ffff:ffff overlaps with an existing pool in the subnet: '
        '2001:db8:1::/64 to which it is being added')


@pytest.mark.v4
@pytest.mark.v4_bootp
@pytest.mark.parametrize('subnet_scope', [['subnet'], ['shared-network'], ['subnet', 'shared-network']])
def test_overlapping_pools_in_different_subnets(subnet_scope):
    """
    Check the behavior of overlapping pools belonging to different subnets. Currently, at subnet
    level, leases are only given from one subnet. At shared network level, all pools from all
    subnets are exhausted.
    :param subnet_scope: subnet-level pools or shared-network-level pools or both
    """
    misc.test_setup()

    subnets = [
        {
            'id': 22,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '192.168.0.1 - 192.168.0.8'
                }
            ],
            'subnet': '192.168.0.0/24'
        },
        {
            'id': 111,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '192.168.0.7 - 192.168.0.9'
                }
            ],
            'subnet': '192.168.0.0/26'
        },
        {
            'id': 3,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '192.168.0.2 - 192.168.0.4'
                }
            ],
            'subnet': '192.168.0.0/25'
        },
        {
            'id': 4,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '192.168.0.1 - 192.168.0.5'
                }
            ],
            'subnet': '192.168.0.0/27'
        },
        {
            'id': 5,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '192.168.1.1 - 192.168.1.2'
                }
            ],
            'subnet': '192.168.1.0/30'
        }
    ]

    if 'subnet' in subnet_scope:
        world.dhcp_cfg.update({'subnet4': copy.deepcopy(subnets)})
        if len(subnet_scope) == 2:
            _bump_subnets()
    if 'shared-network' in subnet_scope:
        world.dhcp_cfg.update({
            'shared-networks': [
                {
                    'name': 'network',
                    'interface': world.f_cfg.server_iface,
                    'subnet4': copy.deepcopy(subnets)
                }
            ]
        })

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Leases are provided from the subnet with the lowest ID: subnet 3.
    for i in [2, 3, 4]:
        srv_msg.DORA(f'192.168.0.{i}', chaddr=f'ff:01:02:03:ff:0{i}',
                     subnet_mask='255.255.255.128')

    if 'shared-network' in subnet_scope:
        # Subnet 4
        for i in [1, 5]:
            srv_msg.DORA(f'192.168.0.{i}', chaddr=f'ff:11:12:13:ff:0{i}',
                         subnet_mask='255.255.255.224')

        # Subnet 5
        for i in [1, 2]:
            srv_msg.DORA(f'192.168.1.{i}', chaddr=f'ff:21:22:23:ff:0{i}',
                         subnet_mask='255.255.255.252')

        # Subnet 22
        for i in [6, 7, 8]:
            srv_msg.DORA(f'192.168.0.{i}', chaddr=f'ff:31:32:33:ff:0{i}',
                         subnet_mask='255.255.255.0')

        # Subnet 111
        for i in [9]:
            srv_msg.DORA(f'192.168.0.{i}', chaddr=f'ff:41:42:43:ff:0{i}',
                         subnet_mask='255.255.255.192')

    # For common subnets, the remaining subnets do not provide any lease.
    # For shared networks, all the pools have been exhausted.
    srv_msg.DORA(None, chaddr='ff:f1:f2:f3:ff:ff', response_type='NAK')


@pytest.mark.v6
@pytest.mark.parametrize('subnet_scope', [['subnet'], ['shared-network'], ['subnet', 'shared-network']])
def test_overlapping_ia_na_pools_in_different_subnets(subnet_scope):
    """
    Check the behavior of overlapping pools belonging to different subnets. Currently, at subnet
    level, leases are only given from one subnet. At shared network level, all pools from all
    subnets are exhausted.
    :param subnet_scope: subnet-level pools or shared-network-level pools or both
    """
    misc.test_setup()

    subnets = [
        {
            'id': 22,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '2001:db8:1::1 - 2001:db8:1::8'
                }
            ],
            'subnet': '2001:db8:1::/64'
        },
        {
            'id': 111,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '2001:db8:1::7 - 2001:db8:1::9'
                }
            ],
            'subnet': '2001:db8:1::/66'
        },
        {
            'id': 3,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '2001:db8:1::2 - 2001:db8:1::4'
                }
            ],
            'subnet': '2001:db8:1::/65'
        },
        {
            'id': 4,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '2001:db8:1::1 - 2001:db8:1::5'
                }
            ],
            'subnet': '2001:db8:1::/67'
        },
        {
            'id': 5,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '2001:db8:2::1 - 2001:db8:2::2'
                }
            ],
            'subnet': '2001:db8:2::/70'
        }
    ]

    if 'subnet' in subnet_scope:
        world.dhcp_cfg.update({'subnet6': copy.deepcopy(subnets)})
        if len(subnet_scope) == 2:
            _bump_subnets()
    if 'shared-network' in subnet_scope:
        world.dhcp_cfg.update({
            'shared-networks': [
                {
                    'name': 'network',
                    'interface': world.f_cfg.server_iface,
                    'subnet6': copy.deepcopy(subnets)
                }
            ]
        })

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Leases are provided from the subnet with the lowest ID: subnet 3.
    for i in [2, 3, 4]:
        srv_msg.SARR(f'2001:db8:1::{i}', duid=f'00:03:00:01:f6:f5:f4:f3:f2:0{i}')

    if 'shared-network' in subnet_scope:
        # Subnet 4
        for i in [1, 5]:
            srv_msg.SARR(f'2001:db8:1::{i}', duid=f'00:03:00:01:f6:f5:f4:f3:f2:1{i}')

        # Subnet 5
        for i in [1, 2]:
            srv_msg.SARR(f'2001:db8:2::{i}', duid=f'00:03:00:01:f6:f5:f4:f3:f2:2{i}')

        # Subnet 22
        for i in [6, 7, 8]:
            srv_msg.SARR(f'2001:db8:1::{i}', duid=f'00:03:00:01:f6:f5:f4:f3:f2:3{i}')

        # Subnet 111
        for i in [9]:
            srv_msg.SARR(f'2001:db8:1::{i}', duid=f'00:03:00:01:f6:f5:f4:f3:f2:4{i}')

    # For common subnets, the remaining subnets do not provide any lease.
    # For shared networks, all the pools have been exhausted.
    srv_msg.SARR(duid='00:03:00:01:f6:f5:f4:f3:f2:ff',
                 status_code=DHCPv6_STATUS_CODES['NoAddrsAvail'])


@pytest.mark.v6
@pytest.mark.parametrize('subnet_scope', [['subnet'], ['shared-network'], ['subnet', 'shared-network']])
def test_overlapping_ia_pd_pools_in_different_subnets(subnet_scope):
    """
    Check the behavior of overlapping PD pools belonging to different subnets. Currently, at subnet
    level, leases are only given from one subnet. At shared network level, all pools from all
    subnets are exhausted.
    :param subnet_scope: subnet-level pools or shared-network-level pools or both
    """
    misc.test_setup()

    subnets = [
        {
            'id': 22,
            'interface': world.f_cfg.server_iface,
            'pd-pools': [
                {
                    "delegated-len": 128,
                    "prefix": "2001:db8:1::",
                    "prefix-len": 127
                }
            ],
            'subnet': '2001:db8:1::/64'
        },
        {
            'id': 111,
            'interface': world.f_cfg.server_iface,
            'pd-pools': [
                {
                    "delegated-len": 128,
                    "prefix": "2001:db8:1::",
                    "prefix-len": 127
                }
            ],
            'subnet': '2001:db8:1::/66'
        },
        {
            'id': 3,
            'interface': world.f_cfg.server_iface,
            'pd-pools': [
                {
                    "delegated-len": 128,
                    "prefix": "2001:db8:1::",
                    "prefix-len": 127
                }
            ],
            'subnet': '2001:db8:1::/65'
        },
        {
            'id': 4,
            'interface': world.f_cfg.server_iface,
            'pd-pools': [
                {
                    "delegated-len": 128,
                    "prefix": "2001:db8:1::",
                    "prefix-len": 127
                }
            ],
            'subnet': '2001:db8:1::/67'
        },
        {
            'id': 5,
            'interface': world.f_cfg.server_iface,
            'pd-pools': [
                {
                    "delegated-len": 128,
                    "prefix": "2001:db8:2::",
                    "prefix-len": 127
                }
            ],
            'subnet': '2001:db8:2::/70'
        }
    ]

    if 'subnet' in subnet_scope:
        world.dhcp_cfg.update({'subnet6': copy.deepcopy(subnets)})
        if len(subnet_scope) == 2:
            _bump_subnets()
    if 'shared-network' in subnet_scope:
        world.dhcp_cfg.update({
            'shared-networks': [
                {
                    'name': 'network',
                    'interface': world.f_cfg.server_iface,
                    'subnet6': copy.deepcopy(subnets)
                }
            ]
        })

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Leases are provided from the subnet with the lowest ID: subnet 3.
    for i, prefix in enumerate(['2001:db8:1::', '2001:db8:1::1']):
        srv_msg.SARR(delegated_prefix=prefix, duid=f'00:03:00:01:f6:f5:f4:f3:f2:0{i}')

    if 'shared-network' in subnet_scope:
        # Subnet 4
        for i, prefix in enumerate(['2001:db8:2::', '2001:db8:2::1']):
            srv_msg.SARR(delegated_prefix=prefix, duid=f'00:03:00:01:f6:f5:f4:f3:f2:1{i}')

    # For common subnets, the remaining subnets do not provide any lease.
    # For shared networks, all the pools have been exhausted.
    srv_msg.SARR(duid='00:03:00:01:f6:f5:f4:f3:f2:ff',
                 status_code=DHCPv6_STATUS_CODES['NoAddrsAvail'])


@pytest.mark.v4
@pytest.mark.v4_bootp
@pytest.mark.parametrize('subnet_scope', [['subnet'], ['shared-network'], ['subnet', 'shared-network']])
def test_overlapping_pools_outside_subnets(subnet_scope):
    """
    Check the behavior of overlapping pools belonging to different subnets. The pools are outside
    the network range of the subnet they belong to. Currently, at subnet level, leases are only
    given from one subnet. At shared network level, all pools from all subnets are exhausted.
    :param subnet_scope: subnet-level pools or shared-network-level pools or both
    """
    misc.test_setup()

    subnets = [
        {
            'id': 22,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '192.168.2.1 - 192.168.2.8'
                }
            ],
            'subnet': '192.168.0.0/24'
        },
        {
            'id': 111,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '192.168.2.7 - 192.168.2.9'
                }
            ],
            'subnet': '192.168.0.0/26'
        },
        {
            'id': 3,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '192.168.2.2 - 192.168.2.4'
                }
            ],
            'subnet': '192.168.0.0/25'
        },
        {
            'id': 4,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '192.168.2.1 - 192.168.2.5'
                }
            ],
            'subnet': '192.168.0.0/27'
        },
        {
            'id': 5,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '192.168.3.1 - 192.168.3.2'
                }
            ],
            'subnet': '192.168.1.0/30'
        }
    ]

    if 'subnet' in subnet_scope:
        world.dhcp_cfg.update({'subnet4': copy.deepcopy(subnets)})
        if len(subnet_scope) == 2:
            _bump_subnets()
    if 'shared-network' in subnet_scope:
        world.dhcp_cfg.update({
            'shared-networks': [
                {
                    'name': 'network',
                    'interface': world.f_cfg.server_iface,
                    'subnet4': copy.deepcopy(subnets)
                }
            ]
        })

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started', should_succeed=False)
    log_contains(
        'DHCP4_PARSER_FAIL failed to create or run parser for configuration element '
        + ('shared-networks' if 'shared-network' in subnet_scope else 'subnet4') + ': '
        'subnet configuration failed: a pool of type V4, with the following address range: '
        '19[02].168.2.1-19[02].168.2.8 does not match the prefix of a subnet: '
        '19[02].168.0.0/24 to which it is being added')


@pytest.mark.v6
@pytest.mark.parametrize('subnet_scope', [['subnet'], ['shared-network'], ['subnet', 'shared-network']])
def test_overlapping_ia_na_pools_outside_subnets(subnet_scope):
    """
    Check the behavior of overlapping pools belonging to different subnets. Currently, at subnet
    level, leases are only given from one subnet. At shared network level, all pools from all
    subnets are exhausted.
    :param subnet_scope: subnet-level pools or shared-network-level pools or both
    """
    misc.test_setup()

    subnets = [
        {
            'id': 22,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '2001:db8:2::1 - 2001:db8:2::8'
                }
            ],
            'subnet': '2001:db8:1::/64'
        },
        {
            'id': 111,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '2001:db8:2::7 - 2001:db8:2::9'
                }
            ],
            'subnet': '2001:db8:1::/66'
        },
        {
            'id': 3,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '2001:db8:2::2 - 2001:db8:2::4'
                }
            ],
            'subnet': '2001:db8:1::/65'
        },
        {
            'id': 4,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '2001:db8:2::1 - 2001:db8:2::5'
                }
            ],
            'subnet': '2001:db8:1::/67'
        },
        {
            'id': 5,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '2001:db8:3::1 - 2001:db8:3::2'
                }
            ],
            'subnet': '2001:db8:2::/70'
        }
    ]

    if 'subnet' in subnet_scope:
        world.dhcp_cfg.update({'subnet6': copy.deepcopy(subnets)})
        if len(subnet_scope) == 2:
            _bump_subnets()
    if 'shared-network' in subnet_scope:
        world.dhcp_cfg.update({
            'shared-networks': [
                {
                    'name': 'network',
                    'interface': world.f_cfg.server_iface,
                    'subnet6': copy.deepcopy(subnets)
                }
            ]
        })

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started', should_succeed=False)
    log_contains(
        'DHCP6_PARSER_FAIL failed to create or run parser for configuration element '
        + ('shared-networks' if 'shared-network' in subnet_scope else 'subnet6') + ': '
        'subnet configuration failed: a pool of type IA_NA, with the following address range: '
        '[23]001:db8:2::1-[23]001:db8:2::8 does not match the prefix of a subnet: '
        '[23]001:db8:1::/64 to which it is being added')


@pytest.mark.v6
@pytest.mark.parametrize('subnet_scope', [['subnet'], ['shared-network'], ['subnet', 'shared-network']])
def test_overlapping_ia_pd_pools_outside_subnets(subnet_scope):
    """
    Check the behavior of overlapping PD pools belonging to different subnets.
    delegated-len == prefix-len is used to make clients jump faster from one pd-pool to the next.
    Currently, at subnet level, leases are only given from one subnet.
    At shared network level, all pools from all subnets are exhausted.
    :param subnet_scope: subnet-level pools or shared-network-level pools or both
    """
    misc.test_setup()

    subnets = [
        {
            'id': 22,
            'interface': world.f_cfg.server_iface,
            'pd-pools': [
                {
                    "delegated-len": 80,
                    "prefix": "2001:db8:2::",
                    "prefix-len": 80
                },
                {
                    "delegated-len": 96,
                    "prefix": "2001:db8:3::",
                    "prefix-len": 96
                }
            ],
            'subnet': '2001:db8:1::/64'
        },
        {
            'id': 111,
            'interface': world.f_cfg.server_iface,
            'pd-pools': [
                {
                    "delegated-len": 80,
                    "prefix": "2001:db8:4::",
                    "prefix-len": 80
                },
                {
                    "delegated-len": 96,
                    "prefix": "2001:db8:5::",
                    "prefix-len": 96
                }
            ],
            'subnet': '2001:db8:1::/66'
        },
        {
            'id': 3,
            'interface': world.f_cfg.server_iface,
            'pd-pools': [
                {
                    "delegated-len": 80,
                    "prefix": "2001:db8:6::",
                    "prefix-len": 80
                },
                {
                    "delegated-len": 96,
                    "prefix": "2001:db8:7::",
                    "prefix-len": 96
                }
            ],
            'subnet': '2001:db8:1::/65'
        },
        {
            'id': 4,
            'interface': world.f_cfg.server_iface,
            'pd-pools': [
                {
                    "delegated-len": 80,
                    "prefix": "2001:db8:8::",
                    "prefix-len": 80
                },
                {
                    "delegated-len": 96,
                    "prefix": "2001:db8:9::",
                    "prefix-len": 96
                }
            ],
            'subnet': '2001:db8:1::/67'
        },
        {
            'id': 5,
            'interface': world.f_cfg.server_iface,
            'pd-pools': [
                {
                    "delegated-len": 80,
                    "prefix": "2001:db8:a::",
                    "prefix-len": 80
                },
                {
                    "delegated-len": 96,
                    "prefix": "2001:db8:b::",
                    "prefix-len": 96
                }
            ],
            'subnet': '2001:db8:2::/70'
        }
    ]

    if 'subnet' in subnet_scope:
        world.dhcp_cfg.update({'subnet6': copy.deepcopy(subnets)})
        if len(subnet_scope) == 2:
            _bump_subnets()
    if 'shared-network' in subnet_scope:
        world.dhcp_cfg.update({
            'shared-networks': [
                {
                    'name': 'network',
                    'interface': world.f_cfg.server_iface,
                    'subnet6': copy.deepcopy(subnets)
                }
            ]
        })

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Leases are provided from the subnet with the lowest ID: subnet 3.
    for i in [6, 7]:
        srv_msg.SARR(delegated_prefix=f'2001:db8:{i}::', duid=f'00:03:00:01:f6:f5:f4:f3:f2:0{i}')

    if 'shared-network' in subnet_scope:
        # Subnet 4
        for i in [8, 9]:
            srv_msg.SARR(delegated_prefix=f'2001:db8:{i}::', duid=f'00:03:00:01:f6:f5:f4:f3:f2:1{i}')

        # Subnet 5
        for i in ['a', 'b']:
            srv_msg.SARR(delegated_prefix=f'2001:db8:{i}::', duid=f'00:03:00:01:f6:f5:f4:f3:f2:2{i}')

        # Subnet 22
        for i in [2, 3]:
            srv_msg.SARR(delegated_prefix=f'2001:db8:{i}::', duid=f'00:03:00:01:f6:f5:f4:f3:f2:3{i}')

        # Subnet 111
        for i in [4, 5]:
            srv_msg.SARR(delegated_prefix=f'2001:db8:{i}::', duid=f'00:03:00:01:f6:f5:f4:f3:f2:4{i}')

    # For common subnets, the remaining subnets do not provide any lease.
    # For shared networks, all the pools have been exhausted.
    srv_msg.SARR(duid='00:03:00:01:f6:f5:f4:f3:f2:ff',
                 status_code=DHCPv6_STATUS_CODES['NoAddrsAvail'])
