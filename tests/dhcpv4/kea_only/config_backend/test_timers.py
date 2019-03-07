"""Kea config backend testing timers in global params, subnets and shared networks."""

import time

import pytest

from .cb_cmds import setup_server_for_config_backend_cmds
from .cb_cmds import rebind_with_ack_answer, rebind_with_nak_answer
from .cb_cmds import get_address, set_global_parameter, set_subnet, set_network


pytestmark = [pytest.mark.v4,
              pytest.mark.kea_only,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.config_backend]


def test_subnet_and_renew_timer():
    # change renew timer on different levels (global and subnet)
    # and check if these changes are properly reflected in received ACKs

    setup_server_for_config_backend_cmds()

    # define one, default subnet
    set_subnet()

    # check getting address from this subnet
    get_address()

    # change global renew_timer to 1sec and now check
    # if received lease has renew_timer accordingly set
    set_global_parameter(renew_timer=1)
    get_address(exp_renew_timer=1)

    # change renew_timer on subnet level to 1000sec
    # and now check if received lease has renew_timer accordingly set
    set_subnet(renew_timer=1000)
    get_address(exp_renew_timer=1000)

    # change again renew_timer on subnet level to 1sec
    # and now check if received lease has renew_timer accordingly set
    set_subnet(renew_timer=1)
    get_address(exp_renew_timer=1)

    # change again renew_timer on global level to 500sec
    # and now check if it is ignored ans it still should be taken
    # from subnet level
    set_global_parameter(renew_timer=500)
    get_address(exp_renew_timer=1)


def test_subnet_and_rebind_timer():
    # change rebind timer on different levels (global and subnet)
    # and check if these changes are properly reflected in received ACKs

    setup_server_for_config_backend_cmds()

    # define one, default subnet
    set_subnet()

    # check getting address from this subnet
    get_address()

    # change global renew_timer to 1sec and now check
    # if received lease has renew_timer accordingly set
    set_global_parameter(rebind_timer=1)
    get_address(exp_rebind_timer=1)

    # change rebind_timer on subnet level to 1000sec
    # and now check if received lease has rebind_timer accordingly set
    set_subnet(rebind_timer=1000)
    get_address(exp_rebind_timer=1000)

    # change again rebind_timer on subnet level to 1sec
    # and now check if received lease has rebind_timer accordingly set
    set_subnet(rebind_timer=1)
    get_address(exp_rebind_timer=1)

    # change again rebind_timer on global level to 500sec
    # and now check if it is ignored ans it still should be taken
    # from subnet level
    set_global_parameter(rebind_timer=500)
    get_address(exp_rebind_timer=1)


def test_subnet_and_timers_renew_less():
    # change both renew and rebind timers on different levels (global and subnet)
    # and check if these changes are properly reflected in received ACKs
    # in this case renew is always less than rebind time

    setup_server_for_config_backend_cmds()

    # define one, default subnet
    set_subnet()

    # check getting address from this subnet
    get_address()

    # set renew and rebind timers on global level
    # and check if they are present in ACK packet
    set_global_parameter(renew_timer=100, rebind_timer=1000)
    get_address(exp_renew_timer=100, exp_rebind_timer=1000)

    # set renew and rebind timers on subnet level
    # and check if they are present in ACK packet
    set_subnet(renew_timer=200, rebind_timer=2000)
    get_address(exp_renew_timer=200, exp_rebind_timer=2000)

    # change renew and rebind timers on subnet level
    # and check if they are present in ACK packet
    set_subnet(renew_timer=300, rebind_timer=3000)
    get_address(exp_renew_timer=300, exp_rebind_timer=3000)

    # change renew and rebind timers on global level
    # and check if they are not reflected in ACK packet,
    # they still should be taken from subnet
    set_global_parameter(renew_timer=400, rebind_timer=4000)
    get_address(exp_renew_timer=300, exp_rebind_timer=3000)


def test_subnet_and_timers_renew_greater():
    # change both renew and rebind timers on different levels (global and subnet)
    # and check if these changes are properly reflected in received ACKs
    # in this case renew is always greater than rebind time,
    # ie. renew should be ignored

    setup_server_for_config_backend_cmds()

    # define one, default subnet
    set_subnet()

    # check getting address from this subnet
    get_address()

    # TODO: bug #505, renew_timer < rebind_timer

    # set renew and rebind timers on global level
    # and as renew is greater rebind check if only rebind is present in ACK packet
    set_global_parameter(renew_timer=100, rebind_timer=10)
    get_address(exp_renew_timer='missing', exp_rebind_timer=10)

    # set renew and rebind timers on subnet level
    # and as renew is greater rebind check if only rebind is present in ACK packet
    set_subnet(renew_timer=100, rebind_timer=10)
    get_address(exp_renew_timer='missing', exp_rebind_timer=10)

    # change renew and rebind timers on subnet level
    # and as renew is greater rebind check if only rebind is present in ACK packet
    set_subnet(renew_timer=200, rebind_timer=20)
    get_address(exp_renew_timer='missing', exp_rebind_timer=20)

    # change renew and rebind timers on global level
    # and check if they are not reflected in ACK packet,
    # they still should be taken from subnet
    set_global_parameter(renew_timer=300, rebind_timer=30)
    get_address(exp_renew_timer='missing', exp_rebind_timer=20)


def test_subnet_and_timers_equal():
    # change both renew and rebind timers on different levels (global and subnet)
    # and check if these changes are properly reflected in received ACKs
    # in this case renew is always equal to rebind time,
    # ie. renew should be ignored

    setup_server_for_config_backend_cmds()

    # define one, default subnet
    set_subnet()

    # check getting address from this subnet
    get_address()

    # set renew and rebind timers on global level
    # and as renew equals rebind check if only rebind is present in ACK packet
    set_global_parameter(renew_timer=1, rebind_timer=1)
    get_address(exp_renew_timer='missing', exp_rebind_timer=1)

    # set renew and rebind timers on subnet level
    # and as renew equals rebind check if only rebind is present in ACK packet
    set_subnet(renew_timer=1000, rebind_timer=1000)
    get_address(exp_renew_timer='missing', exp_rebind_timer=1000)

    # change renew and rebind timers on subnet level
    # and as renew equals rebind check if only rebind is present in ACK packet
    set_subnet(renew_timer=2, rebind_timer=2)
    get_address(exp_renew_timer='missing', exp_rebind_timer=2)

    # change renew and rebind timers on global level
    # and check if they are not reflected in ACK packet,
    # they still should be taken from subnet
    set_global_parameter(renew_timer=5, rebind_timer=5)
    get_address(exp_renew_timer='missing', exp_rebind_timer=2)


def test_subnet_and_timers_mix():
    # change both renew and rebind timers on different levels (global and subnet)
    # and check if these changes are properly reflected in received ACKs
    # in this case they are in different relations to each other

    setup_server_for_config_backend_cmds()

    # define one, default subnet
    set_subnet()

    # check getting address from this subnet
    get_address()

    # change renew and rebind timers that they are either greater
    # less or equal to each other, do it on global level
    set_global_parameter(renew_timer=1500, rebind_timer=1000)
    get_address(exp_renew_timer='missing', exp_rebind_timer=1000)

    set_global_parameter(renew_timer=1500, rebind_timer=1500)
    get_address(exp_renew_timer='missing', exp_rebind_timer=1500)

    set_global_parameter(renew_timer=1000, rebind_timer=1500)
    get_address(exp_renew_timer=1000, exp_rebind_timer=1500)

    set_global_parameter(renew_timer=1000, rebind_timer=1000)
    get_address(exp_renew_timer='missing', exp_rebind_timer=1000)

    # now change on subnet level in all directions
    set_subnet(renew_timer=1500, rebind_timer=1000)
    get_address(exp_renew_timer='missing', exp_rebind_timer=1000)

    set_subnet(renew_timer=1500, rebind_timer=1500)
    get_address(exp_renew_timer='missing', exp_rebind_timer=1500)

    set_subnet(renew_timer=1000, rebind_timer=1500)
    get_address(exp_renew_timer=1000, exp_rebind_timer=1500)

    set_subnet(renew_timer=1000, rebind_timer=1000)
    get_address(exp_renew_timer='missing', exp_rebind_timer=1000)


def test_shared_networks_and_timers_renew_less():
    # change both renew and rebind timers on different levels (global, shared network and subnet)
    # and check if these changes are properly reflected in received ACKs
    # in this case renew is always less than rebind time

    setup_server_for_config_backend_cmds()

    # define a shared network with one subnet
    set_network()

    # check getting address from this subnet
    get_address()

    # set renew and rebind timers on global level
    # and check if they are present in ACK packet
    set_global_parameter(renew_timer=100, rebind_timer=1000)
    get_address(exp_renew_timer=100, exp_rebind_timer=1000)

    # set renew and rebind timers on network level
    # and check if they are present in ACK packet
    set_network(network_renew_timer=200, network_rebind_timer=2000)
    get_address(exp_renew_timer=200, exp_rebind_timer=2000)

    # change renew and rebind timers on global level
    # and check if they are not reflected in ACK packet,
    # they still should be taken from subnet
    set_global_parameter(renew_timer=300, rebind_timer=3000)
    get_address(exp_renew_timer=200, exp_rebind_timer=2000)

    # change renew and rebind timers on network level
    # and check if they are present in ACK packet
    set_network(network_renew_timer=400, network_rebind_timer=4000)
    get_address(exp_renew_timer=400, exp_rebind_timer=4000)

    # set renew and rebind timers on subnet level
    # and check if they are present in ACK packet
    set_network(subnet_renew_timer=500, subnet_rebind_timer=5000)
    get_address(exp_renew_timer=500, exp_rebind_timer=5000)

    # change renew and rebind timers on subnet level
    # and check if they are present in ACK packet
    set_network(subnet_renew_timer=600, subnet_rebind_timer=6000)
    get_address(exp_renew_timer=600, exp_rebind_timer=6000)

    # change renew and rebind timers on global level
    # and check if they are not reflected in ACK packet,
    # they still should be taken from subnet
    set_network(network_renew_timer=700, network_rebind_timer=7000)
    get_address(exp_renew_timer=600, exp_rebind_timer=6000)

    # change renew and rebind timers on global level
    # and check if they are not reflected in ACK packet,
    # they still should be taken from subnet
    set_global_parameter(renew_timer=800, rebind_timer=8000)
    get_address(exp_renew_timer=600, exp_rebind_timer=6000)


def test_subnet_and_valid_lifetime():
    # change valid-lifetime on different levels (global and subnet)
    # and check if behavior is as expected ie leases after lifetime
    # are not available for rebinding

    setup_server_for_config_backend_cmds()

    # define one, default subnet
    set_subnet()

    # check getting address from this subnet by client 1
    yiaddr1 = get_address(chaddr='00:00:00:00:00:01')
    time.sleep(2)
    # check rebinding after 2 seconds, as default lifetime is big it should succeed
    rebind_with_ack_answer(yiaddr1)

    # change lease lifetime on global level to be small ie. 1sec
    # and check getting address by client 2
    set_global_parameter(valid_lifetime=1)
    yiaddr2 = get_address(chaddr='00:00:00:00:00:02', exp_lease_time=1)
    # now rebinding after lifetime should fail
    time.sleep(2)
    rebind_with_nak_answer(yiaddr2)

    # change lease lifetime on subnet level to be big ie. 1000sec
    # and check getting address by client 3
    set_subnet(valid_lifetime=1000)
    yiaddr3 = get_address(chaddr='00:00:00:00:00:03', exp_lease_time=1000)
    time.sleep(2)
    # now rebinding after a few seconds, before lifetime should succeed
    rebind_with_ack_answer(yiaddr3)

    # change lease lifetime on subnet level to be small ie. 1sec
    # and check getting address by client 4
    set_subnet(valid_lifetime=1)
    yiaddr4 = get_address(chaddr='00:00:00:00:00:04', exp_lease_time=1)
    time.sleep(2)
    # now rebinding after lifetime should fail again
    rebind_with_nak_answer(yiaddr4)


def test_shared_networks_and_valid_lifetime():
    # change valid-lifetime on different levels (global, shared network and subnet)
    # and check if behavior is as expected ie leases after lifetime
    # are not available for rebinding

    setup_server_for_config_backend_cmds()

    # define a shared network with one subnet
    set_network()

    # change lease lifetime on global level to be small ie. 1sec
    # and check getting address by client 2
    set_global_parameter(valid_lifetime=1)
    yiaddr2 = get_address(chaddr='00:00:00:00:00:02', exp_lease_time=1)
    time.sleep(2)
    # now rebinding after lifetime should fail
    rebind_with_nak_answer(yiaddr2)

    # change lease lifetime on network level to be big ie. 1000sec
    # and check getting address by client 3
    set_network(network_valid_lifetime=1000)
    yiaddr3 = get_address(chaddr='00:00:00:00:00:03', exp_lease_time=1000)
    time.sleep(2)
    # now rebinding after a few seconds, before lifetime should succeed
    rebind_with_ack_answer(yiaddr3)

    # change lease lifetime on network level to be small ie. 1sec
    # and check getting address by client 4
    set_network(network_valid_lifetime=1)
    yiaddr4 = get_address(chaddr='00:00:00:00:00:04', exp_lease_time=1)
    time.sleep(2)
    # now rebinding after lifetime should fail
    rebind_with_nak_answer(yiaddr4)

    # change lease lifetime on subnet level to be big ie. 1000sec
    # and check getting address by client 5
    set_network(subnet_valid_lifetime=1000)
    yiaddr5 = get_address(chaddr='00:00:00:00:00:05', exp_lease_time=1000)
    time.sleep(2)
    # now rebinding after a few seconds, before lifetime should succeed
    rebind_with_ack_answer(yiaddr5)

    # change lease lifetime on subnet level to be small ie. 1sec
    # and check getting address by client 6
    set_network(subnet_valid_lifetime=1)
    yiaddr6 = get_address(chaddr='00:00:00:00:00:06', exp_lease_time=1)
    time.sleep(2)
    # now rebinding after lifetime should fail
    rebind_with_nak_answer(yiaddr6)
