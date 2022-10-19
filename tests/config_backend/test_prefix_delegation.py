# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea config backend testing prefix delegation."""

import pytest

from src.protosupport.dhcp4_scen import get_address
from src.softwaresupport.cb_model import setup_server_for_config_backend_cmds


pytestmark = [pytest.mark.v6,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.cb]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_pd_pool(backend):
    cfg = setup_server_for_config_backend_cmds(backend_type=backend)

    # add subnet with prefix delegation
    subnet_cfg, _ = cfg.add_subnet(backend=backend,
                                   subnet='3000::/64',
                                   pools=[{'pool': '3000::2/128'}],
                                   pd_pools=[{
                                       "prefix": '2001:db8:1::',
                                       "prefix-len": 90,
                                       "delegated-len": 96}])

    # and get a PD
    get_address(mac_addr='00:00:00:00:00:01',
                req_ia='IA-PD',
                exp_ia_pd_iaprefix_prefix='2001:db8:1::',
                exp_ia_pd_iaprefix_plen=96)

    # change PD params (prefix itself, its len and delgated len)
    subnet_cfg.update(backend=backend, pd_pools=[{
        "prefix": '2001:db8:2::',
        "prefix-len": 80,
        "delegated-len": 104,
    }])

    # get again a PD
    get_address(mac_addr='00:00:00:00:00:02',
                req_ia='IA-PD',
                exp_ia_pd_iaprefix_prefix='2001:db8:2::',
                exp_ia_pd_iaprefix_plen=104)

    # add exlusion to PD
    subnet_cfg.update(backend=backend, pd_pools=[{
        "prefix": '2001:db8:2::',
        "prefix-len": 80,
        "delegated-len": 104,
        "excluded-prefix": "2001:db8:2::",
        "excluded-prefix-len": 108,
    }])

    # TODO: make proper check for exclusion
    get_address(mac_addr='00:00:00:00:00:03',
                req_ia='IA-PD',
                exp_ia_pd_iaprefix_prefix='2001:db8:2::100:0',
                exp_ia_pd_iaprefix_plen=104)
