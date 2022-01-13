"""ISC_DHCP DHCPv4 Failover Configuration"""

# pylint: disable=invalid-name,line-too-long

import pytest
import misc
import srv_control
import srv_msg

from softwaresupport.isc_dhcp6_server.functions import build_log_path, add_line_in_global


@pytest.mark.v4
@pytest.mark.dhcpd
def test_v4_dhcpd_failover_sanity_check_good_config():
    """new-v4.dhcpd.failover.sanity_check.good_config"""
    srv_msg.wait_for_message_in_log('Pool threshold reset', count=1, log_file=build_log_path())
    # Verifies that failover config for two peers passes
    srv_msg.wait_for_message_in_log('Pool threshold reset', count=1, log_file=build_log_path())
    # sanity checking
    srv_msg.wait_for_message_in_log('Pool threshold reset', count=1, log_file=build_log_path())
    # #
    misc.test_setup()
    add_line_in_global(' failover peer "fonet" {')
    add_line_in_global('     primary;')
    add_line_in_global('     address 175.16.1.30;')
    add_line_in_global('     port 519;')
    add_line_in_global('     peer address 175.16.1.30;')
    add_line_in_global('     peer port 520;')
    add_line_in_global('     mclt 30;')
    add_line_in_global('     split 128;')
    add_line_in_global('     load balance max seconds 2;')
    add_line_in_global(' }')
    add_line_in_global(' failover peer "beebonet" {')
    add_line_in_global('     primary;')
    add_line_in_global('     address 175.16.1.30;')
    add_line_in_global('     port 521;')
    add_line_in_global('     peer address 175.16.1.30;')
    add_line_in_global('     peer port 522;')
    add_line_in_global('     mclt 30;')
    add_line_in_global('     split 128;')
    add_line_in_global('     load balance max seconds 2;')
    add_line_in_global(' }')
    add_line_in_global(' subnet 178.16.1.0 netmask 255.255.255.0 {')
    add_line_in_global('     pool {')
    add_line_in_global('       failover peer "fonet";')
    add_line_in_global('       range 178.16.1.50 178.16.1.50;')
    add_line_in_global('     }')
    add_line_in_global('     pool {')
    add_line_in_global('       failover peer "beebonet";')
    add_line_in_global('       range 178.16.1.150 178.16.1.200;')
    add_line_in_global('     }')
    add_line_in_global(' }')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # No steps required
    misc.test_procedure()

    misc.pass_criteria()
    srv_msg.log_contains('failover peer fonet: I move from recover to startup',
                         log_file=build_log_path())
    srv_msg.log_contains('failover peer beebonet: I move from recover to startup',
                         log_file=build_log_path())


@pytest.mark.v4
@pytest.mark.dhcpd
def test_v4_dhcpd_failover_sanity_check_no_pools():
    """new-v4.dhcpd.failover.sanity_check.no_pools"""
    # #
    # # Verifies that failover sanity checking detects when
    # # peers are not referenced in pools.
    # #
    misc.test_setup()
    add_line_in_global(' failover peer "fonet" {')
    add_line_in_global('     primary;')
    add_line_in_global('     address 175.16.1.30;')
    add_line_in_global('     port 519;')
    add_line_in_global('     peer address 175.16.1.30;')
    add_line_in_global('     peer port 520;')
    add_line_in_global('     mclt 30;')
    add_line_in_global('     split 128;')
    add_line_in_global('     load balance max seconds 2;')
    add_line_in_global(' }')
    add_line_in_global(' failover peer "beebonet" {')
    add_line_in_global('     primary;')
    add_line_in_global('     address 175.16.1.30;')
    add_line_in_global('     port 521;')
    add_line_in_global('     peer address 175.16.1.30;')
    add_line_in_global('     peer port 522;')
    add_line_in_global('     mclt 30;')
    add_line_in_global('     split 128;')
    add_line_in_global('     load balance max seconds 2;')
    add_line_in_global(' }')
    add_line_in_global(' subnet 178.16.1.0 netmask 255.255.255.0 {')
    add_line_in_global('     pool {')
    add_line_in_global('       range 178.16.1.50 178.16.1.50;')
    add_line_in_global('     }')
    add_line_in_global('     pool {')
    add_line_in_global('       range 178.16.1.150 178.16.1.200;')
    add_line_in_global('     }')
    add_line_in_global(' }')
    srv_control.build_and_send_config_files()
    srv_control.start_srv_during_process('DHCP', 'configuration')

    misc.test_procedure()
    # No steps required

    misc.pass_criteria()
    # @todo Forge does not yet support searching console output.  Pre-startup
    # errors like these occur before logging is initted, so the console is the
    # only place to see them.
    # DHCP console MUST contain line: ERROR: Failover peer, fobonet, has no referring pools
    # DHCP console MUST contain line: ERROR: Failover peer, beebonet, has no referring pools
