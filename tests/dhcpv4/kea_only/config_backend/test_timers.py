"""Kea config backend testing timers in global params, subnets and shared networks."""

import time
import logging

import pytest

from cb_model import setup_server_for_config_backend_cmds, get_cfg_default
from dhcp4_scen import get_address, get_rejected


log = logging.getLogger('forge')


pytestmark = [pytest.mark.kea_only,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.config_backend]


@pytest.mark.v4
@pytest.mark.v6
def test_subnet_and_renew_timer(dhcp_version):
    # change renew timer on different levels (global and subnet)
    # and check if these changes are properly reflected in received ACKs

    cfg = setup_server_for_config_backend_cmds()

    dhcp_key = 'Dhcp%s' % dhcp_version[1]
    subnet_key = 'subnet%s' % dhcp_version[1]

    # define one, default subnet
    _, config = cfg.add_subnet()
    assert 'renew-timer' not in config[dhcp_key][subnet_key][0]

    # check getting address from this subnet
    get_address()

    # change global renew_timer to 1sec and now check
    # if received lease has renew_timer accordingly set
    cfg.set_global_parameter(renew_timer=1)
    get_address(exp_renew_timer=1)

    # change renew_timer on subnet level to 1000sec
    # and now check if received lease has renew_timer accordingly set
    cfg.update_subnet(renew_timer=1000)
    get_address(exp_renew_timer=1000)

    # change again renew_timer on subnet level to 1sec
    # and now check if received lease has renew_timer accordingly set
    cfg.update_subnet(renew_timer=1)
    get_address(exp_renew_timer=1)

    # change again renew_timer on global level to 500sec
    # and now check if it is ignored ans it still should be taken
    # from subnet level
    cfg.set_global_parameter(renew_timer=500)
    get_address(exp_renew_timer=1)


@pytest.mark.v4
@pytest.mark.v6
def test_subnet_and_rebind_timer(dhcp_version):  # pylint: disable=unused-argument
    # change rebind timer on different levels (global and subnet)
    # and check if these changes are properly reflected in received ACKs

    cfg = setup_server_for_config_backend_cmds()

    # define one, default subnet
    cfg.add_subnet()

    # check getting address from this subnet
    get_address()

    # change global renew_timer to 1sec and now check
    # if received lease has renew_timer accordingly set
    cfg.set_global_parameter(rebind_timer=1)
    get_address(exp_rebind_timer=1)

    # change rebind_timer on subnet level to 1000sec
    # and now check if received lease has rebind_timer accordingly set
    cfg.update_subnet(rebind_timer=1000)
    get_address(exp_rebind_timer=1000)

    # change again rebind_timer on subnet level to 1sec
    # and now check if received lease has rebind_timer accordingly set
    cfg.update_subnet(rebind_timer=1)
    get_address(exp_rebind_timer=1)

    # change again rebind_timer on global level to 500sec
    # and now check if it is ignored ans it still should be taken
    # from subnet level
    cfg.set_global_parameter(rebind_timer=500)
    get_address(exp_rebind_timer=1)


@pytest.mark.v4
@pytest.mark.v6
def test_subnet_and_timers_renew_less(dhcp_version):  # pylint: disable=unused-argument
    # change both renew and rebind timers on different levels (global and subnet)
    # and check if these changes are properly reflected in received ACKs
    # in this case renew is always less than rebind time so both should
    # be present in responses

    cfg = setup_server_for_config_backend_cmds()

    # define one, default subnet
    cfg.add_subnet()

    # check getting address from this subnet
    get_address()

    # set renew and rebind timers on global level
    # and check if they are present in ACK packet
    cfg.set_global_parameter(renew_timer=100, rebind_timer=1000)
    get_address(exp_renew_timer=100, exp_rebind_timer=1000)

    # set renew and rebind timers on subnet level
    # and check if they are present in ACK packet
    cfg.update_subnet(renew_timer=200, rebind_timer=2000)
    get_address(exp_renew_timer=200, exp_rebind_timer=2000)

    # change renew and rebind timers on subnet level
    # and check if they are present in ACK packet
    cfg.update_subnet(renew_timer=300, rebind_timer=3000)
    get_address(exp_renew_timer=300, exp_rebind_timer=3000)

    # change renew and rebind timers on global level
    # and check if they are not reflected in ACK packet,
    # they still should be taken from subnet
    cfg.set_global_parameter(renew_timer=400, rebind_timer=4000)
    get_address(exp_renew_timer=300, exp_rebind_timer=3000)


@pytest.mark.v4
@pytest.mark.v6
def test_subnet_and_timers_renew_greater(dhcp_version):
    # change both renew and rebind timers on different levels (global and subnet)
    # and check if these changes are properly reflected in received ACKs
    # in this case renew is always greater than rebind time,
    # ie. renew should be ignored and not present in responses

    cfg = setup_server_for_config_backend_cmds()

    # define one, default subnet
    cfg.add_subnet()

    # check getting address from this subnet
    get_address()

    # TODO: add test for bug #505, renew_timer < rebind_timer

    # set renew and rebind timers on global level
    # and as renew is greater rebind check if only rebind is present in ACK packet
    cfg.set_global_parameter(renew_timer=100, rebind_timer=10)
    get_address(exp_renew_timer='missing' if dhcp_version == 'v4' else 0, exp_rebind_timer=10)

    # set renew and rebind timers on subnet level
    # and as renew is greater rebind check if only rebind is present in ACK packet
    cfg.update_subnet(renew_timer=100, rebind_timer=10)
    get_address(exp_renew_timer='missing' if dhcp_version == 'v4' else 0, exp_rebind_timer=10)

    # change renew and rebind timers on subnet level
    # and as renew is greater rebind check if only rebind is present in ACK packet
    cfg.update_subnet(renew_timer=200, rebind_timer=20)
    get_address(exp_renew_timer='missing' if dhcp_version == 'v4' else 0, exp_rebind_timer=20)

    # change renew and rebind timers on global level
    # and check if they are not reflected in ACK packet,
    # they still should be taken from subnet
    cfg.set_global_parameter(renew_timer=300, rebind_timer=30)
    get_address(exp_renew_timer='missing' if dhcp_version == 'v4' else 0, exp_rebind_timer=20)


@pytest.mark.v4
@pytest.mark.v6
def test_subnet_and_timers_equal(dhcp_version):
    # change both renew and rebind timers on different levels (global and subnet)
    # and check if these changes are properly reflected in received ACKs
    # in this case renew is always equal to rebind time,
    # ie. renew should be ignored and not present in responses

    cfg = setup_server_for_config_backend_cmds()

    # define one, default subnet
    cfg.add_subnet()

    # check getting address from this subnet
    get_address()

    # set renew and rebind timers on global level
    # and as renew equals rebind check if only rebind is present in ACK packet
    cfg.set_global_parameter(renew_timer=1, rebind_timer=1)
    get_address(exp_renew_timer='missing' if dhcp_version == 'v4' else 0, exp_rebind_timer=1)

    # set renew and rebind timers on subnet level
    # and as renew equals rebind check if only rebind is present in ACK packet
    cfg.update_subnet(renew_timer=1000, rebind_timer=1000)
    get_address(exp_renew_timer='missing' if dhcp_version == 'v4' else 0, exp_rebind_timer=1000)

    # change renew and rebind timers on subnet level
    # and as renew equals rebind check if only rebind is present in ACK packet
    cfg.update_subnet(renew_timer=2, rebind_timer=2)
    get_address(exp_renew_timer='missing' if dhcp_version == 'v4' else 0, exp_rebind_timer=2)

    # change renew and rebind timers on global level
    # and check if they are not reflected in ACK packet,
    # they still should be taken from subnet
    cfg.set_global_parameter(renew_timer=5, rebind_timer=5)
    get_address(exp_renew_timer='missing' if dhcp_version == 'v4' else 0, exp_rebind_timer=2)


@pytest.mark.v4
@pytest.mark.v6
def test_subnet_and_timers_mix(dhcp_version):
    # change both renew and rebind timers on different levels (global and subnet)
    # and check if these changes are properly reflected in received ACKs
    # in this case they are in different relations to each other

    cfg = setup_server_for_config_backend_cmds()

    # define one, default subnet
    cfg.add_subnet()

    # check getting address from this subnet
    get_address()

    # change renew and rebind timers that they are either greater
    # less or equal to each other, do it on global level
    cfg.set_global_parameter(renew_timer=1500, rebind_timer=1000)
    get_address(exp_renew_timer='missing' if dhcp_version == 'v4' else 0, exp_rebind_timer=1000)

    cfg.set_global_parameter(renew_timer=1500, rebind_timer=1500)
    get_address(exp_renew_timer='missing' if dhcp_version == 'v4' else 0, exp_rebind_timer=1500)

    cfg.set_global_parameter(renew_timer=1000, rebind_timer=1500)
    get_address(exp_renew_timer=1000, exp_rebind_timer=1500)

    cfg.set_global_parameter(renew_timer=1000, rebind_timer=1000)
    get_address(exp_renew_timer='missing' if dhcp_version == 'v4' else 0, exp_rebind_timer=1000)

    # now change on subnet level in all directions
    cfg.update_subnet(renew_timer=1500, rebind_timer=1000)
    get_address(exp_renew_timer='missing' if dhcp_version == 'v4' else 0, exp_rebind_timer=1000)

    cfg.update_subnet(renew_timer=1500, rebind_timer=1500)
    get_address(exp_renew_timer='missing' if dhcp_version == 'v4' else 0, exp_rebind_timer=1500)

    cfg.update_subnet(renew_timer=1000, rebind_timer=1500)
    get_address(exp_renew_timer=1000, exp_rebind_timer=1500)

    cfg.update_subnet(renew_timer=1000, rebind_timer=1000)
    get_address(exp_renew_timer='missing' if dhcp_version == 'v4' else 0, exp_rebind_timer=1000)


@pytest.mark.v4
@pytest.mark.v6
def test_shared_networks_and_timers_renew_less(dhcp_version):  # pylint: disable=unused-argument
    # change both renew and rebind timers on different levels (global, shared network and subnet)
    # and check if these changes are properly reflected in received ACKs
    # in this case renew is always less than rebind time so both should be present in responses

    cfg = setup_server_for_config_backend_cmds()

    # define a shared network with one subnet
    network_cfg, _ = cfg.add_network()
    subnet_cfg, _ = cfg.add_subnet(network=network_cfg)

    # check getting address from this subnet
    get_address()

    # set renew and rebind timers on global level
    # and check if they are present in ACK packet
    cfg.set_global_parameter(renew_timer=10, rebind_timer=100)
    get_address(exp_renew_timer=10, exp_rebind_timer=100)

    # set renew and rebind timers on network level
    # and check if they are present in ACK packet
    network_cfg.update(renew_timer=20, rebind_timer=200)
    get_address(exp_renew_timer=20, exp_rebind_timer=200)

    # change renew and rebind timers on global level
    # and check if they are not reflected in ACK packet,
    # they still should be taken from subnet
    cfg.set_global_parameter(renew_timer=30, rebind_timer=300)
    get_address(exp_renew_timer=20, exp_rebind_timer=200)

    # change renew and rebind timers on network level
    # and check if they are present in ACK packet
    network_cfg.update(renew_timer=40, rebind_timer=400)
    get_address(exp_renew_timer=40, exp_rebind_timer=400)

    # set renew and rebind timers on subnet level
    # and check if they are present in ACK packet
    subnet_cfg.update(renew_timer=50, rebind_timer=500)
    get_address(exp_renew_timer=50, exp_rebind_timer=500)

    # change renew and rebind timers on subnet level
    # and check if they are present in ACK packet
    subnet_cfg.update(renew_timer=60, rebind_timer=600)
    get_address(exp_renew_timer=60, exp_rebind_timer=600)

    # change renew and rebind timers on global level
    # and check if they are not reflected in ACK packet,
    # they still should be taken from subnet
    network_cfg.update(renew_timer=70, rebind_timer=700)
    get_address(exp_renew_timer=60, exp_rebind_timer=600)

    # change renew and rebind timers on global level
    # and check if they are not reflected in ACK packet,
    # they still should be taken from subnet
    cfg.set_global_parameter(renew_timer=80, rebind_timer=800)
    get_address(exp_renew_timer=60, exp_rebind_timer=600)


@pytest.mark.v4
@pytest.mark.v6
def test_subnet_and_valid_lifetime(dhcp_version):
    # change valid-lifetime on different levels (global and subnet)
    # and check if behavior is as expected ie leases after lifetime
    # are available for other clients

    cfg = setup_server_for_config_backend_cmds()

    # define one, default subnet with 1 IP address
    cfg.add_subnet(pool="192.168.50.2/32" if dhcp_version == 'v4' else '2001:db8:1::2/128')

    # check getting address from this subnet by client 1
    get_address(mac_addr='00:00:00:00:00:01', exp_addr='192.168.50.2' if dhcp_version == 'v4' else '2001:db8:1::2')
    # after 2 seconds check if another client 2 can get address - as default lifetime is big
    # it should fail because there is no more IP addresses (there is only 1 taken)
    time.sleep(2)
    get_rejected(mac_addr='00:00:00:00:00:02')

    # change lease lifetime on global level to be small ie. 1sec
    # and 1) extend address pool by 1 IP for new client 3 as previous IP address is taken for long time
    # and 2) check getting address by this new client 3
    cfg.set_global_parameter(valid_lifetime=1)
    cfg.update_subnet(pool="192.168.50.2/31" if dhcp_version == 'v4' else '2001:db8:1::2/127')
    get_address(mac_addr='00:00:00:00:00:03', exp_lease_time=1,
                exp_addr='192.168.50.3' if dhcp_version == 'v4' else '2001:db8:1::3')
    # as lease time is 1 sec after 2secs this just taken IP address should
    # be available for other clients ie. client 4
    time.sleep(2)
    get_address(mac_addr='00:00:00:00:00:04',
                exp_addr='192.168.50.3' if dhcp_version == 'v4' else '2001:db8:1::3')
    # wait for lease expiration for next test steps
    time.sleep(2)

    # change lease lifetime on subnet level to be big ie. 1000sec
    # and check getting address by client 5
    cfg.update_subnet(valid_lifetime=1000)
    get_address(mac_addr='00:00:00:00:00:05', exp_lease_time=1000,
                exp_addr='192.168.50.3' if dhcp_version == 'v4' else '2001:db8:1::3')
    # after 2 seconds check if another client 6 can get address - as new lifetime is big
    # it should fail because there is no more IP addresses (there is only 2 taken)
    time.sleep(2)
    get_rejected(mac_addr='00:00:00:00:00:06')

    # change lease lifetime on subnet level to be small ie. 1sec
    # and check getting address by client 7 but first extent pool by one address
    # as previous IP addresses are taken for long time
    cfg.update_subnet(valid_lifetime=1,
                      pool="192.168.50.2-192.168.50.4" if dhcp_version == 'v4' else '2001:db8:1::2-2001:db8:1::4')
    get_address(mac_addr='00:00:00:00:00:07', exp_lease_time=1,
                exp_addr='192.168.50.4' if dhcp_version == 'v4' else '2001:db8:1::4')
    # as lease time is 1 sec after 2secs this just taken IP address should
    # be available for other clients ie. client 8
    time.sleep(2)
    get_address(mac_addr='00:00:00:00:00:08', exp_addr='192.168.50.4' if dhcp_version == 'v4' else '2001:db8:1::4')


@pytest.mark.v4
@pytest.mark.v6
def test_shared_networks_and_valid_lifetime(dhcp_version):
    # change valid-lifetime on different levels (global, shared network and subnet)
    # and check if behavior is as expected ie leases after lifetime
    # are not available for rebinding

    cfg = setup_server_for_config_backend_cmds()

    # define a shared network with one subnet
    network_cfg, _ = cfg.add_network()
    subnet_cfg, _ = cfg.add_subnet(network=network_cfg,
                                   pool="192.168.50.2/32" if dhcp_version == 'v4' else '2001:db8:1::2/128')

    # check getting address from this subnet by client 1
    get_address(mac_addr='00:00:00:00:00:01', exp_addr='192.168.50.2' if dhcp_version == 'v4' else '2001:db8:1::2')
    # after 2 seconds check if another client 2 can get address - as default lifetime is big
    # it should fail because there is no more IP addresses (there is only 1 that is taken)
    time.sleep(2)
    get_rejected(mac_addr='00:00:00:00:00:02')

    # change lease lifetime on global level to be small ie. 1sec
    # and 1) extend address pool by 1 IP for new client 3 as previous IP address is taken for long time
    # and 2) check getting address by this new client 3
    cfg.set_global_parameter(valid_lifetime=1)
    subnet_cfg.update(pool="192.168.50.2/31" if dhcp_version == 'v4' else '2001:db8:1::2/127')
    get_address(mac_addr='00:00:00:00:00:03', exp_lease_time=1,
                exp_addr='192.168.50.3' if dhcp_version == 'v4' else '2001:db8:1::3')
    # as lease time is 1 sec after 2secs this just taken IP address should
    # be available for other clients ie. client 4
    time.sleep(2)
    get_address(mac_addr='00:00:00:00:00:04', exp_addr='192.168.50.3' if dhcp_version == 'v4' else '2001:db8:1::3')
    # wait for lease expiration for next test steps
    time.sleep(2)

    # change lease lifetime on network level to be big ie. 1000sec
    # and check getting address by client 5
    network_cfg.update(valid_lifetime=1000)
    get_address(mac_addr='00:00:00:00:00:05',
                exp_lease_time=1000, exp_addr='192.168.50.3' if dhcp_version == 'v4' else '2001:db8:1::3')
    # after 2 seconds check if another client 6 can get address - as new lifetime is big
    # it should fail because there is no more IP addresses (there are only 2 that are taken)
    time.sleep(2)
    get_rejected(mac_addr='00:00:00:00:00:06')

    # change lease lifetime on network level to be small ie. 1sec
    # and check getting address by client 7 but first extent pool by one address
    # as previous IP addresses are taken for long time
    network_cfg.update(valid_lifetime=1)
    subnet_cfg.update(pool="192.168.50.2-192.168.50.4" if dhcp_version == 'v4' else '2001:db8:1::2-2001:db8:1::4')
    get_address(mac_addr='00:00:00:00:00:07', exp_lease_time=1,
                exp_addr='192.168.50.4' if dhcp_version == 'v4' else '2001:db8:1::4')
    # as lease time is 1 sec after 2secs this just taken IP address should
    # be available for other clients ie. client 8
    time.sleep(2)
    get_address(mac_addr='00:00:00:00:00:08', exp_addr='192.168.50.4' if dhcp_version == 'v4' else '2001:db8:1::4')
    # wait for lease expiration for next test steps
    time.sleep(2)

    # change lease lifetime on subnet level to be big ie. 1000sec
    # and check getting address by client 9
    subnet_cfg.update(valid_lifetime=1000)
    get_address(mac_addr='00:00:00:00:00:09', exp_lease_time=1000,
                exp_addr='192.168.50.4' if dhcp_version == 'v4' else '2001:db8:1::4')
    # after 2 seconds check if another client 10 can get address - as new lifetime is big
    # it should fail because there is no more IP addresses (there are only 4 that are taken)
    time.sleep(2)
    get_rejected(mac_addr='00:00:00:00:00:10')

    # change lease lifetime on subnet level to be small ie. 1sec
    # and check getting address by client 11 but first extent pool by one address
    # as previous IP addresses are taken for long time
    subnet_cfg.update(valid_lifetime=1,
                      pool="192.168.50.2-192.168.50.5" if dhcp_version == 'v4' else '2001:db8:1::2-2001:db8:1::5')
    get_address(mac_addr='00:00:00:00:00:11', exp_lease_time=1,
                exp_addr='192.168.50.5' if dhcp_version == 'v4' else '2001:db8:1::5')
    # as lease time is 1 sec after 2secs this just taken IP address should
    # be available for other clients ie. client 12
    time.sleep(2)
    get_address(mac_addr='00:00:00:00:00:12', exp_addr='192.168.50.5' if dhcp_version == 'v4' else '2001:db8:1::5')


@pytest.mark.v4
@pytest.mark.parametrize("initial_calculate_tee_times,initial_t1_percent,initial_t2_percent,initial_valid_lifetime",
                         [(None, None, None, None),
                          (False, 0.2, 0.6, 5000),
                          (True, None, None, None),
                          (True, 0.1, 0.9, None),
                          (True, None, None, 5000),
                          (True, 0.3, 0.7, 5000)])
def test_calculate_timers_init_v4(initial_calculate_tee_times,
                                  initial_t1_percent,
                                  initial_t2_percent,
                                  initial_valid_lifetime):
    # check initial values of different timers in config file

    cfg = setup_server_for_config_backend_cmds(calculate_tee_times=initial_calculate_tee_times,
                                               t1_percent=initial_t1_percent,
                                               t2_percent=initial_t2_percent,
                                               valid_lifetime=initial_valid_lifetime)

    # define one, default subnet
    cfg.add_subnet()

    calculate_tee_times = initial_calculate_tee_times if initial_calculate_tee_times is not None else False
    valid_lifetime = initial_valid_lifetime if initial_valid_lifetime is not None else get_cfg_default('valid-lifetime')

    if calculate_tee_times:
        t1_percent = initial_t1_percent if initial_t1_percent is not None else get_cfg_default('t1-percent')
        t2_percent = initial_t2_percent if initial_t2_percent is not None else get_cfg_default('t2-percent')
        renew_timer = int(t1_percent * valid_lifetime)
        rebind_timer = int(t2_percent * valid_lifetime)
    else:
        renew_timer = None
        rebind_timer = None

    # check getting address from this subnet
    get_address(exp_renew_timer=renew_timer, exp_rebind_timer=rebind_timer, exp_lease_time=valid_lifetime)


@pytest.mark.v6
@pytest.mark.parametrize("initial_calculate_tee_times,initial_t1_percent,"
                         "initial_t2_percent,initial_preferred_lifetime,initial_valid_lifetime",
                         [(None, None, None, None, None),
                          (False, 0.2, 0.6, 5000, 10000),
                          (True, None, None, None, None),
                          (True, 0.1, 0.9, None, None),
                          (True, None, None, 5000, 10000),
                          (True, 0.3, 0.7, 5000, 10000)])
def test_calculate_timers_init_v6(initial_calculate_tee_times,
                                  initial_t1_percent,
                                  initial_t2_percent,
                                  initial_preferred_lifetime,
                                  initial_valid_lifetime):
    # check initial values of different timers in config file

    cfg = setup_server_for_config_backend_cmds(calculate_tee_times=initial_calculate_tee_times,
                                               t1_percent=initial_t1_percent,
                                               t2_percent=initial_t2_percent,
                                               preferred_lifetime=initial_preferred_lifetime,
                                               valid_lifetime=initial_valid_lifetime)

    # define one, default subnet
    cfg.add_subnet()

    calculate_tee_times = initial_calculate_tee_times if initial_calculate_tee_times is not None else False
    if initial_preferred_lifetime is not None:
        preferred_lifetime = initial_preferred_lifetime
    else:
        preferred_lifetime = get_cfg_default('preferred-lifetime')
    valid_lifetime = initial_valid_lifetime if initial_valid_lifetime is not None else get_cfg_default('valid-lifetime')

    if calculate_tee_times:
        t1_percent = initial_t1_percent if initial_t1_percent is not None else get_cfg_default('t1-percent')
        t2_percent = initial_t2_percent if initial_t2_percent is not None else get_cfg_default('t2-percent')
        renew_timer = int(t1_percent * preferred_lifetime)
        rebind_timer = int(t2_percent * preferred_lifetime)
    else:
        renew_timer = None
        rebind_timer = None

    # check getting address from this subnet
    get_address(exp_renew_timer=renew_timer, exp_rebind_timer=rebind_timer,
                exp_ia_na_iaaddr_preflft=preferred_lifetime, exp_lease_time=valid_lifetime)


@pytest.mark.v4
@pytest.mark.v6
def test_subnet_and_calculate_timers(dhcp_version):
    # change renew timer on different levels (global and subnet)
    # and check if these changes are properly reflected in received ACKs

    cfg = setup_server_for_config_backend_cmds()

    # define one, default subnet
    cfg.add_subnet()

    if dhcp_version == 'v4':
        base_lifetime = get_cfg_default('valid-lifetime')
    else:
        base_lifetime = get_cfg_default('preferred-lifetime')

    # change global renew_timer to 1sec and now check
    # if received lease has renew_timer accordingly set
    cfg.set_global_parameter(calculate_tee_times=True)

    t1_percent = get_cfg_default('t1-percent')
    t2_percent = get_cfg_default('t2-percent')
    get_address(exp_renew_timer=int(t1_percent * base_lifetime),
                exp_rebind_timer=int(t2_percent * base_lifetime))

    # change t1 and t2 and check new renew/rebind-timers
    t1_percent = 0.1
    t2_percent = 0.9
    cfg.set_global_parameter(t1_percent=t1_percent, t2_percent=t2_percent)
    get_address(exp_renew_timer=int(t1_percent * base_lifetime),
                exp_rebind_timer=int(t2_percent * base_lifetime))

    # change again but only t1 and check new renew/rebind-timers
    t1_percent = 0.3
    cfg.set_global_parameter(t1_percent=t1_percent)
    get_address(exp_renew_timer=int(t1_percent * base_lifetime),
                exp_rebind_timer=int(t2_percent * base_lifetime))

    # switch off calculate_tee_times and check if renew/rebind-timers
    # are not present in responses anymore
    cfg.set_global_parameter(calculate_tee_times=False)
    get_address(exp_renew_timer=None, exp_rebind_timer=None)
