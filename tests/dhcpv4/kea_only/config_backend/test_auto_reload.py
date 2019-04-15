import time
import pytest

from cb_model import setup_server_for_config_backend_cmds, get_config
from dhcp4_scen import get_address, send_discover_with_no_answer

pytestmark = [pytest.mark.kea_only,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.config_backend,
              pytest.mark.kea_only,
              pytest.mark.v4]


def test_auto_reload_1second():
    # prepare initial config with fetch wait time set to 1 second
    cfg = setup_server_for_config_backend_cmds(config_control={"config-fetch-wait-time": 1}, force_reload=False)

    # check config that there is no subnets and fetch time is 1
    new_cfg = get_config()
    assert len(new_cfg['Dhcp4']['subnet4']) == 0
    assert new_cfg['Dhcp4']['config-control']['config-fetch-wait-time'] == 1

    # add subnet and wait 2 seconds that config is reloaded automatically
    cfg.add_subnet()
    time.sleep(2)

    # now check if there is a subnet in config
    new_cfg = get_config()
    assert len(new_cfg['Dhcp4']['subnet4']) == 1
    assert new_cfg['Dhcp4']['subnet4'][0]['subnet'] == cfg.subnet4.keys()[0]

    # there is subnet so getting address should succeed
    get_address()


def test_auto_reload_100seconds():
    # prepare initial config with fetch wait time set to 100 seconds
    cfg = setup_server_for_config_backend_cmds(config_control={"config-fetch-wait-time": 100}, force_reload=False)

    # check config that there is no subnets and fetch time is 100
    new_cfg = get_config()
    assert len(new_cfg['Dhcp4']['subnet4']) == 0
    assert new_cfg['Dhcp4']['config-control']['config-fetch-wait-time'] == 100

    # add subnet and wait 2 seconds that config is NOT reloaded automatically as it is done every 100 seconds
    cfg.add_subnet()
    time.sleep(2)

    # now check if there is NO subnets in config
    new_cfg = get_config()
    assert len(new_cfg['Dhcp4']['subnet4']) == 0

    # there is NO subnet so getting address should fail
    send_discover_with_no_answer()
