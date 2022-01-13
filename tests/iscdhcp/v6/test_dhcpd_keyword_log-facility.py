"""ISC_DHCP DHCPv6 Keywords"""

# pylint: disable=invalid-name,line-too-long

import pytest
import misc
import srv_control
import srv_msg
from softwaresupport.isc_dhcp6_server.functions import build_log_path, add_line_in_global


@pytest.mark.v6
@pytest.mark.dhcpd
def test_v6_dhcpd_keyword_log_facility_success():
    """new-v6.dhcpd.keyword.log-facility.success"""
    # # Testing log-facility server option
    # #
    # # Verifies that log-facility option (there by forge default setup)
    # # succeeds in capturing dhcpd logging.
    # #
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::2')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # No steps required
    misc.test_procedure()

    misc.pass_criteria()
    srv_msg.log_contains('dhcpd: Server starting service.',
                         log_file=build_log_path())


@pytest.mark.v6
@pytest.mark.dhcpd
def test_v6_dhcpd_keyword_log_facility_fail():
    """new-v6.dhcpd.keyword.log-facility.fail"""
    # # Testing log-facility server option
    # #
    # # Verifies that by setting log-facility to an invalid
    # # value, causes dhcpd logging to not be directed to log file.
    # #
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::2')
    add_line_in_global('log-facility bogus;')
    srv_control.build_and_send_config_files()
    srv_control.start_srv_during_process('DHCP', 'configuration')

    # No steps required
    misc.test_procedure()

    misc.pass_criteria()
    # @todo - pre-startup errors only go to syslog, we need to look at
    # console output captured by Forge.  Don't yet have a step in Forge
    # for looking at console output.
    # DHCP log contains 1 of line: server.cfg_processed line 6: unknown value
