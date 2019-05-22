"""Kea config backend testing subnets."""

import time

import pytest

from dhcp4_scen import get_address, get_rejected
from dhcp4_scen import get_address4, get_address6
from dhcp4_scen import send_decline4, send_decline6
from dhcp4_scen import send_request_and_check_ack, rebind_with_nak_answer
from cb_model import setup_server_for_config_backend_cmds


pytestmark = [pytest.mark.kea_only,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.config_backend]


@pytest.mark.v4
@pytest.mark.parametrize("initial_echo_client_id", [None, True, False])
def test_echo_client_id(initial_echo_client_id):
    # Set initial value of echo-client-id in config file and then change it
    # using cb-cmds. Observe if client-id is included in responses according to settings.

    # Different initial settings for echo-client-id: default (=True), True and False.
    cfg = setup_server_for_config_backend_cmds(echo_client_id=initial_echo_client_id)

    cfg.add_subnet()

    # Request address and check if client-id is returned according to initial setting.
    get_address(client_id='00010203040506',
                exp_client_id='00010203040506' if initial_echo_client_id in [None, True] else 'missing')

    # Change setting to NOT return client-id. It should be missing in responses.
    cfg.set_global_parameter(echo_client_id=False)
    get_address(client_id='10010203040506', exp_client_id='missing')

    # Change again setting to return client-id. It should be missing in responses.
    cfg.set_global_parameter(echo_client_id=True)
    get_address(client_id='20010203040506', exp_client_id='20010203040506')

    # Change setting to NOT return client-id. It should be missing in responses.
    cfg.set_global_parameter(echo_client_id=False)
    get_address(client_id='30010203040506', exp_client_id='missing')


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.parametrize("initial_decline_probation_period", [None, 1, 1000])
def test_decline_and_probation_period(initial_decline_probation_period, dhcp_version):
    # Set initial value of decline-probation-period in config file and then change it
    # using cb-cmds. Observe if the setting is honored in case of sending DECLINE messages.

    # Different initial settings for decline-probation-period: default (=24h), 1 second and 1000 seconds.
    cfg = setup_server_for_config_backend_cmds(decline_probation_period=initial_decline_probation_period)

    # Prepare subnet with only 1 IP address in a pool. This way when the second DISCOVER is send
    # no response should be expected from server.
    cfg.add_subnet(pool='192.168.50.1/32' if dhcp_version == 'v4' else '2001:db8:1::1/128')

    # Get address and decline it.
    if dhcp_version == 'v4':
        addr = get_address4(exp_yiaddr='192.168.50.1')
        send_decline4(addr)
    else:
        get_address6(exp_ia_na_iaaddr_addr='2001:db8:1::1')
        send_decline6()

    # Wait a moment.
    time.sleep(2)

    # If initial decline-probation-period was 1 second then it should
    # be possible to acquire the same IP again, ie. after 1 second it should have been
    # returned to pool from probation space.
    if initial_decline_probation_period == 1:
        get_address(exp_addr='192.168.50.1' if dhcp_version == 'v4' else '2001:db8:1::1')
    else:
        # If initial value was other than 1 second then server should still keep
        # the IP in probation and no response should be sent by server.
        get_rejected()

    # Delete subnet. This will delete IP in probation. Ie. start from scratch.
    cfg.del_subnet()
    # Change decline-probation-period from initial to 1000 seconds.
    cfg.set_global_parameter(decline_probation_period=1000)
    # Create new subnet with different pool but still with 1 IP address.
    cfg.add_subnet(pool='192.168.50.2/32' if dhcp_version == 'v4' else '2001:db8:1::2/128')

    # Now after decline and sleeping 2 seconds the declined address still should
    # be in probation and server should not send any response for discover.
    if dhcp_version == 'v4':
        addr = get_address4(exp_yiaddr='192.168.50.2')
        send_decline4(addr)
    else:
        get_address6(exp_ia_na_iaaddr_addr='2001:db8:1::2')
        send_decline6()
    time.sleep(2)
    get_rejected()

    # Start from scratch again. New pool with 1 IP address.
    # Probation period is changed now to 1 second.
    cfg.del_subnet()
    cfg.set_global_parameter(decline_probation_period=1)
    cfg.add_subnet(pool='192.168.50.3/32' if dhcp_version == 'v4' else '2001:db8:1::3/128')

    # This time after decline and sleeping the address should be available
    # for the following request.
    if dhcp_version == 'v4':
        addr1 = get_address4(exp_yiaddr='192.168.50.3')
        send_decline4(addr1)
        time.sleep(2)
        addr2 = get_address4()
        assert addr2 == addr1
    else:
        get_address6(exp_ia_na_iaaddr_addr='2001:db8:1::3')
        send_decline6()
        time.sleep(2)
        get_address6(exp_ia_na_iaaddr_addr='2001:db8:1::3')


def _check_matching_client_id_when_false():
    rcvd_addr = get_address(chaddr='11:11:11:11:11:11', client_id='11111111111111')

    # HW addr and client ID are equal to original ones so the request is accepted
    send_request_and_check_ack(chaddr='11:11:11:11:11:11', client_id='11111111111111', ciaddr=rcvd_addr)

    # HW addr is different than original one so the request is rejected.
    # Client ID is equal to original one but it is ignored as match_client_id is False.
    rebind_with_nak_answer(chaddr='12:12:12:12:12:12', client_id='11111111111111', ciaddr=rcvd_addr)

    # HW addr and client ID are different than original ones so the request is rejected
    rebind_with_nak_answer(chaddr='12:12:12:12:12:12', client_id='12121212121212', ciaddr=rcvd_addr)

    # HW addr is equal to original one so the request is accepted.
    # Client ID is different but it is ignored as match_client_id is False
    send_request_and_check_ack(chaddr='11:11:11:11:11:11', client_id='12121212121212', ciaddr=rcvd_addr)


def _check_matching_client_id_when_true():
    rcvd_addr = get_address(chaddr='11:11:11:11:11:11', client_id='11111111111111')

    # HW addr and client ID are equal to original ones so the request is accepted
    send_request_and_check_ack(chaddr='11:11:11:11:11:11', client_id='11111111111111', ciaddr=rcvd_addr)

    # Client ID is equal to original one so the request is accepted.
    # HW addr is different but it is ignored as match_client_id is True.
    send_request_and_check_ack(chaddr='12:12:12:12:12:12', client_id='11111111111111', ciaddr=rcvd_addr)

    # HW addr and client ID are different than original ones so the request is rejected
    rebind_with_nak_answer(chaddr='12:12:12:12:12:12', client_id='12121212121212', ciaddr=rcvd_addr)

    # client ID is different than original one so the request is rejected
    rebind_with_nak_answer(chaddr='11:11:11:11:11:11', client_id='12121212121212', ciaddr=rcvd_addr)


@pytest.mark.v4
@pytest.mark.parametrize("initial_match_client_id", [None, True, False])
def test_match_client_id_override_init(initial_match_client_id):
    cfg, _ = setup_server_for_config_backend_cmds(match_client_id=initial_match_client_id,
                                                  check_config=True)

    cfg.add_subnet()

    # check initial situation
    if initial_match_client_id in [None, True]:
        _check_matching_client_id_when_true()
    else:
        _check_matching_client_id_when_false()

    # client id is used on global level
    cfg.set_global_parameter(match_client_id=True)
    _check_matching_client_id_when_true()


@pytest.mark.v4
def test_subnet_and_match_client_id():
    cfg, _ = setup_server_for_config_backend_cmds(check_config=True)

    cfg.add_subnet()
    _check_matching_client_id_when_true()

    # client id is used on global level
    cfg.set_global_parameter(match_client_id=True)
    _check_matching_client_id_when_true()

    # client id is ignored on global level
    cfg.set_global_parameter(match_client_id=False)
    _check_matching_client_id_when_false()

    # client id is used on subnet level
    cfg.update_subnet(match_client_id=True)
    _check_matching_client_id_when_true()

    # client id is ignored on subnet level
    cfg.update_subnet(match_client_id=False)
    _check_matching_client_id_when_false()


@pytest.mark.v4
def test_network_and_match_client_id():
    cfg, _ = setup_server_for_config_backend_cmds(check_config=True)

    network_cfg, _ = cfg.add_network()
    subnet_cfg, _ = cfg.add_subnet(network=network_cfg)
    _check_matching_client_id_when_true()

    # client id is ignored on global level
    cfg.set_global_parameter(match_client_id=False)
    _check_matching_client_id_when_false()

    # client id is used on network level
    network_cfg.update(match_client_id=True)
    _check_matching_client_id_when_true()

    # client id is ignored on network level
    network_cfg.update(match_client_id=False)
    _check_matching_client_id_when_false()

    # client id is used on subnet level
    subnet_cfg.update(match_client_id=True)
    _check_matching_client_id_when_true()

    # client id is ignored on subnet level
    subnet_cfg.update(match_client_id=False)
    _check_matching_client_id_when_false()

    # client id is still ignored on subnet level but used on network level
    network_cfg.update(match_client_id=True)
    _check_matching_client_id_when_false()

    # client id is used on subnet level
    subnet_cfg.update(match_client_id=True)
    _check_matching_client_id_when_true()

    # match-client-id is reset on subnet level
    # and should be used due to network leve setting
    subnet_cfg.update(match_client_id=None)
    _check_matching_client_id_when_true()


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.parametrize("initial_dhcp4o6_port", [None, 1234])
def test_dhcp4o6_port(initial_dhcp4o6_port, dhcp_version):  # pylint: disable=unused-argument
    cfg, config = setup_server_for_config_backend_cmds(dhcp4o6_port=initial_dhcp4o6_port,
                                                       check_config=True)

    dhcp_key = 'Dhcp%s' % dhcp_version[1]

    if initial_dhcp4o6_port is None:
        assert config[dhcp_key]['dhcp4o6-port'] == 0
    else:
        assert config[dhcp_key]['dhcp4o6-port'] == 1234

    cfg.set_global_parameter(dhcp4o6_port=4321)
