"""Kea config backend testing prefix delegation."""

import pytest

from dhcp4_scen import get_address
from cb_model import setup_server_for_config_backend_cmds


pytestmark = [pytest.mark.v6,
              pytest.mark.kea_only,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.config_backend]


def test_pd_pool():
    cfg = setup_server_for_config_backend_cmds()

    # add subnet with prefix delegation
    subnet_cfg, _ = cfg.add_subnet(
        subnet='3000::/64',
        pools=[{'pool': '3000::2/128'}],
        pd_pools=[{
            "prefix": '2001:db8:1::',
            "prefix-len": 90,
            "delegated-len": 96,
        }])

    # and get a PD
    get_address(mac_addr='00:00:00:00:00:01',
                req_ia='IA-PD',
                exp_ia_pd_iaprefix_prefix='2001:db8:1::',
                exp_ia_pd_iaprefix_plen=96)

    # change PD params (prefix itself, its len and delgated len)
    subnet_cfg.update(pd_pools=[{
        "prefix": '2001:db8:2::',
        "prefix-len": 80,
        "delegated-len": 104,
    }])

    # get again a PD
    get_address(mac_addr='00:00:00:00:00:02',
                req_ia='IA-PD',
                exp_ia_pd_iaprefix_prefix='2001:db8:2::',
                exp_ia_pd_iaprefix_plen=104)

    # TODO: exclude support on 1.6 final
    # add exlusion to PD
    subnet_cfg.update(pd_pools=[{
        "prefix": '2001:db8:2::',
        "prefix-len": 80,
        "delegated-len": 104,
        "excluded-prefix": "2001:db8:2::",
        "excluded-prefix-len": 108,
    }])

    # TODO: make proper check for exclusion
    get_address(mac_addr='00:00:00:00:00:03',
                req_ia='IA-PD',
                exp_ia_pd_iaprefix_prefix='2001:db8:2::',
                exp_ia_pd_iaprefix_plen=104)
