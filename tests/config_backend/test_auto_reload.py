# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# pylint: disable=unused-argument

import time
import pytest

from src.forge_cfg import world
from src.softwaresupport.cb_model import setup_server_for_config_backend_cmds, get_config
from src.protosupport.dhcp4_scen import get_address, get_rejected

pytestmark = [pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.cb,
              pytest.mark.v4,
              pytest.mark.v6]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_auto_reload_1second(dhcp_version, backend):
    # prepare initial config with fetch wait time set to 1 second
    cfg = setup_server_for_config_backend_cmds(backend_type=backend, config_control={"config-fetch-wait-time": 1},
                                               force_reload=False)

    dhcp_key = f'Dhcp{world.proto[1]}'
    subnet_key = f'subnet{world.proto[1]}'

    # check config that there is no subnets and fetch time is 1
    new_cfg = get_config()
    assert len(new_cfg[dhcp_key][subnet_key]) == 0
    assert new_cfg[dhcp_key]['config-control']['config-fetch-wait-time'] == 1

    # add subnet and wait 2 seconds that config is reloaded automatically
    cfg.add_subnet(backend=backend)
    time.sleep(2)

    # now check if there is a subnet in config
    new_cfg = get_config()
    assert len(new_cfg[dhcp_key][subnet_key]) == 1
    assert new_cfg[dhcp_key][subnet_key][0]['subnet'] == list(cfg.subnets.keys())[0]

    # there is subnet so getting address should succeed
    get_address()


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_auto_reload_100seconds(dhcp_version, backend):
    # prepare initial config with fetch wait time set to 100 seconds
    cfg = setup_server_for_config_backend_cmds(backend_type=backend, config_control={"config-fetch-wait-time": 100},
                                               force_reload=False)

    dhcp_key = f'Dhcp{world.proto[1]}'
    subnet_key = f'subnet{world.proto[1]}'

    # check config that there is no subnets and fetch time is 100
    new_cfg = get_config()
    assert len(new_cfg[dhcp_key][subnet_key]) == 0
    assert new_cfg[dhcp_key]['config-control']['config-fetch-wait-time'] == 100

    # add subnet and wait 2 seconds that config is NOT reloaded automatically as it is done every 100 seconds
    cfg.add_subnet(backend=backend)
    time.sleep(2)

    # now check if there is NO subnets in config
    new_cfg = get_config()
    assert len(new_cfg[dhcp_key][subnet_key]) == 0

    # there is NO subnet so getting address should fail
    get_rejected()
