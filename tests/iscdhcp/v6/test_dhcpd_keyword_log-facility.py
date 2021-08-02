"""ISC_DHCP DHCPv6 Keywords"""


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
@pytest.mark.v6
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.log_facility
def test_v6_dhcpd_keyword_log_facility_success(step):
    """new-v6.dhcpd.keyword.log-facility.success"""
    # # Testing log-facility server option
    # #
    # # Verifies that log-facility option (there by forge default setup)
    # # succeeds in capturing dhcpd logging.
    # #
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # No steps required
    misc.test_procedure(step)

    misc.pass_criteria(step)
    srv_msg.log_contains_line(step, 'DHCP', None, 'dhcpd: Server starting service.')



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.log_facility
def test_v6_dhcpd_keyword_log_facility_fail(step):
    """new-v6.dhcpd.keyword.log-facility.fail"""
    # # Testing log-facility server option
    # #
    # # Verifies that by setting log-facility to an invalid
    # # value, causes dhcpd logging to not be directed to log file.
    # #
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::2')
    srv_control.run_command(step, 'log-facility bogus;')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv_during_process(step, 'DHCP', 'configuration')

    # No steps required
    misc.test_procedure(step)

    misc.pass_criteria(step)
    # @todo - pre-startup errors only go to syslog, we need to look at
    # console output captured by Forge.  Don't yet have a step in Forge
    # for looking at console output.
    # DHCP log contains 1 of line: server.cfg_processed line 6: unknown value


