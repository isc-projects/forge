"""ISC_DHCP DHCPv4 Failover Configuration"""


import sys
if 'features' not in sys.path:
    sys.path.append('features')

if 'pytest' in sys.argv[0]:
    import pytest
else:
    import lettuce as pytest

import misc
import srv_control
import srv_msg


@pytest.mark.py_test
@pytest.mark.v4
@pytest.mark.dhcpd
@pytest.mark.failover
@pytest.mark.sanity_check
def test_v4_dhcpd_failover_sanity_check_good_config(step):
    """new-v4.dhcpd.failover.sanity_check.good_config"""
    # #
    # # Verifies that failover config for two peers passes
    # # sanity checking
    # #
    misc.test_setup(step)
    srv_control.run_command(step, ' failover peer "fonet" {')
    srv_control.run_command(step, '     primary;')
    srv_control.run_command(step, '     address 175.16.1.30;')
    srv_control.run_command(step, '     port 519;')
    srv_control.run_command(step, '     peer address 175.16.1.30;')
    srv_control.run_command(step, '     peer port 520;')
    srv_control.run_command(step, '     mclt 30;')
    srv_control.run_command(step, '     split 128;')
    srv_control.run_command(step, '     load balance max seconds 2;')
    srv_control.run_command(step, ' }')
    srv_control.run_command(step, ' failover peer "beebonet" {')
    srv_control.run_command(step, '     primary;')
    srv_control.run_command(step, '     address 175.16.1.30;')
    srv_control.run_command(step, '     port 521;')
    srv_control.run_command(step, '     peer address 175.16.1.30;')
    srv_control.run_command(step, '     peer port 522;')
    srv_control.run_command(step, '     mclt 30;')
    srv_control.run_command(step, '     split 128;')
    srv_control.run_command(step, '     load balance max seconds 2;')
    srv_control.run_command(step, ' }')
    srv_control.run_command(step, ' subnet 178.16.1.0 netmask 255.255.255.0 {')
    srv_control.run_command(step, '     pool {')
    srv_control.run_command(step, '       failover peer "fonet";')
    srv_control.run_command(step, '       range 178.16.1.50 178.16.1.50;')
    srv_control.run_command(step, '     }')
    srv_control.run_command(step, '     pool {')
    srv_control.run_command(step, '       failover peer "beebonet";')
    srv_control.run_command(step, '       range 178.16.1.150 178.16.1.200;')
    srv_control.run_command(step, '     }')
    srv_control.run_command(step, ' }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # No steps required
    misc.test_procedure(step)

    misc.pass_criteria(step)
    srv_msg.log_contains_line(step,
                              'DHCP',
                              None,
                              'failover peer fonet: I move from recover to startup')
    srv_msg.log_contains_line(step,
                              'DHCP',
                              None,
                              'failover peer beebonet: I move from recover to startup')




@pytest.mark.py_test
@pytest.mark.v4
@pytest.mark.dhcpd
@pytest.mark.failover
@pytest.mark.sanity_check
def test_v4_dhcpd_failover_sanity_check_no_pools(step):
    """new-v4.dhcpd.failover.sanity_check.no_pools"""
    # #
    # # Verifies that failover sanity checking detects when
    # # peers are not referenced in pools.
    # #
    misc.test_setup(step)
    srv_control.run_command(step, ' failover peer "fonet" {')
    srv_control.run_command(step, '     primary;')
    srv_control.run_command(step, '     address 175.16.1.30;')
    srv_control.run_command(step, '     port 519;')
    srv_control.run_command(step, '     peer address 175.16.1.30;')
    srv_control.run_command(step, '     peer port 520;')
    srv_control.run_command(step, '     mclt 30;')
    srv_control.run_command(step, '     split 128;')
    srv_control.run_command(step, '     load balance max seconds 2;')
    srv_control.run_command(step, ' }')
    srv_control.run_command(step, ' failover peer "beebonet" {')
    srv_control.run_command(step, '     primary;')
    srv_control.run_command(step, '     address 175.16.1.30;')
    srv_control.run_command(step, '     port 521;')
    srv_control.run_command(step, '     peer address 175.16.1.30;')
    srv_control.run_command(step, '     peer port 522;')
    srv_control.run_command(step, '     mclt 30;')
    srv_control.run_command(step, '     split 128;')
    srv_control.run_command(step, '     load balance max seconds 2;')
    srv_control.run_command(step, ' }')
    srv_control.run_command(step, ' subnet 178.16.1.0 netmask 255.255.255.0 {')
    srv_control.run_command(step, '     pool {')
    srv_control.run_command(step, '       range 178.16.1.50 178.16.1.50;')
    srv_control.run_command(step, '     }')
    srv_control.run_command(step, '     pool {')
    srv_control.run_command(step, '       range 178.16.1.150 178.16.1.200;')
    srv_control.run_command(step, '     }')
    srv_control.run_command(step, ' }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    misc.test_procedure(step)
    # No steps required

    misc.pass_criteria(step)
    # @todo Forge does not yet support searching console output.  Pre-startup
    # errors like these occur before logging is initted, so the console is the
    # only place to see them.
    # DHCP console MUST contain line: ERROR: Failover peer, fobonet, has no referring pools
    # DHCP console MUST contain line: ERROR: Failover peer, beebonet, has no referring pools


