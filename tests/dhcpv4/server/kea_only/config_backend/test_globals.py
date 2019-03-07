"""Kea config backend testing subnets. TODO """

import time

import pytest

from .cb_cmds import setup_server_for_config_backend_cmds
from .cb_cmds import send_discovery_with_no_answer, send_decline
from .cb_cmds import get_address, set_subnet, del_subnet, set_global_parameter


pytestmark = [pytest.mark.kea_only,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.config_backend]


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.parametrize("initial_echo_client_id", [None, True, False])
def test_echo_client_id(initial_echo_client_id):
    # Set initial value of echo-client-id in config file and then change it
    # using cb-cmds. Observe if client-id is included in responses according to settings.

    # Different initial settings for echo-client-id: default (=True), True and False.
    setup_server_for_config_backend_cmds(echo_client_id=initial_echo_client_id)

    set_subnet()

    # Request address and check if client-id is returned according to initial setting.
    get_address(client_id='00010203040506',
                exp_client_id='00010203040506' if initial_echo_client_id in [None, True] else 'missing')

    # Change setting to NOT return client-id. It should be missing in responses.
    set_global_parameter(echo_client_id=False)
    get_address(client_id='10010203040506', exp_client_id='missing')

    # Change again setting to return client-id. It should be missing in responses.
    set_global_parameter(echo_client_id=True)
    get_address(client_id='20010203040506', exp_client_id='20010203040506')

    # Change setting to NOT return client-id. It should be missing in responses.
    set_global_parameter(echo_client_id=False)
    get_address(client_id='30010203040506', exp_client_id='missing')


@pytest.mark.v4
@pytest.mark.kea_only
@pytest.mark.parametrize("initial_decline_probation_period", [None, 1, 1000])
def test_decline_and_probation_period(initial_decline_probation_period):
    # Set initial value of decline-probation-period in config file and then change it
    # using cb-cmds. Observe if the setting is honored in case of sending DECLINE messages.

    # Different initial settings for decline-probation-period: default (=24h), 1 second and 1000 seconds.
    setup_server_for_config_backend_cmds(decline_probation_period=initial_decline_probation_period)

    # Prepare subnet with only 1 IP address in a pool. This way when the second DISCOVER is send
    # no response should be expected from server.
    set_subnet(pool='192.168.50.1-192.168.50.1')

    # Get address and decline it.
    addr1 = get_address(exp_yiaddr='192.168.50.1')
    send_decline(addr1)

    # Wait a moment.
    time.sleep(2)

    # If initial decline-probation-period was 1 second then it should
    # be possible to acquire the same IP again, ie. after 1 second it should have been
    # returned to pool from probation space.
    if initial_decline_probation_period == 1:
        addr2 = get_address()
        assert addr2 == addr1
    else:
        # If initial value was other than 1 second then server should still keep
        # the IP in probabtion and no response should be sent by server.
        send_discovery_with_no_answer()

    # Delete subnet. This will delete IP in probabation. Ie. start from scratch.
    del_subnet()
    # Change decline-probabation-period from initial to 1000 seconds.
    set_global_parameter(decline_probation_period=1000)
    # Create new subnet with different pool but still with 1 IP address.
    set_subnet(pool='192.168.50.2-192.168.50.2')

    # Now after decline and sleeping 2 seconds the declined address still should
    # be in probation and server should not send any response for discover.
    addr = get_address(exp_yiaddr='192.168.50.2')
    send_decline(addr)
    time.sleep(2)
    send_discovery_with_no_answer()

    # Start from scratch again. New pool with 1 IP address.
    # Probabation period is changed now to 1 second.
    del_subnet()
    set_global_parameter(decline_probation_period=1)
    set_subnet(pool='192.168.50.3-192.168.50.3')

    # This time after decline and sleeping the address should be available
    # for the following request.
    addr1 = get_address(exp_yiaddr='192.168.50.3')
    send_decline(addr1)
    time.sleep(2)
    addr2 = get_address()
    assert addr2 == addr1


# TODO
# @pytest.mark.v4
# @pytest.mark.kea_only
# @pytest.mark.parametrize("initial_match_client_id", [None, True, False])
# def test_match_client_id(initial_echo_client_id):
#     pass


# TODO
# @pytest.mark.v4
# @pytest.mark.kea_only
# @pytest.mark.parametrize("initial_dhcp4o6_port", [None, True, False])
# def test_dhcp4o6_port(initial_echo_client_id):
#     pass
