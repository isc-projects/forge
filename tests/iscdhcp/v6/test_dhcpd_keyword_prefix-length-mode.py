"""ISC_DHCP DHCPv6 Keywords Prefix Length Mode"""


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
@pytest.mark.dhcp6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.keyword
@pytest.mark.prefix_length_mode
def test_dhcpd_keyword_prefix_length_mode_default(step):
    """new-dhcpd.keyword.prefix-length-mode.default"""
    # Tests default setting for prefix_len_mode which should be match
    # prefix-length-mode = PLM_PREFER.
    # Uses a series of solicits with varying plens to check the offer
    # outcome.
    # 
    # Solicit plen    Offer Outcome
    # --------------------------------------
    # /0              3000:db8:0:100::/56
    # /48             3000:db8:0:100::/56
    # /60             3000:db8:0:100::/56
    # /64             3000:db8:1:100::/64
    # /72             3000:db8:0:100::/56

    misc.test_setup(step)
    srv_control.run_command(step, 'ddns-updates off;')
    srv_control.run_command(step, 'authoritative;')
    srv_control.run_command(step, 'subnet6 3000::/16 {')
    srv_control.run_command(step, ' pool6 {')
    srv_control.run_command(step, '  prefix6 3000:db8:0:100:: 3000:db8:0:100:: /56;')
    srv_control.run_command(step, ' }')
    srv_control.run_command(step, ' pool6 {')
    srv_control.run_command(step, '  prefix6 3000:db8:1:100:: 3000:db8:1:100:: /64;')
    srv_control.run_command(step, ' }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # /0              3000:db8:0:100::/56
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '0')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '56')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')

    # /48             3000:db8:0:100::/56
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '48')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '56')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')

    # /60             3000:db8:0:100::/56
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '60')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '56')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')

    # /64             3000:db8:1:100::/64
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '64')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '64')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:1:100::')

    # /72             3000:db8:0:100::/56
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '72')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '56')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.keyword
@pytest.mark.prefix_length_mode
def test_dhcpd_keyword_prefix_length_mode_ignore(step):
    """new-dhcpd.keyword.prefix-length-mode.ignore"""
    # Tests prefix-length-mode = ignore
    # Uses a series of solicits with varying plens to check the offer
    # outcome.
    # 
    # Solicit plen    Offer Outcome
    # --------------------------------------
    # /0              3000:db8:0:100::/56
    # /48             3000:db8:0:100::/56
    # /60             3000:db8:0:100::/56
    # /64             3000:db8:0:100::/56
    # /72             3000:db8:0:100::/56

    misc.test_setup(step)
    srv_control.run_command(step, 'ddns-updates off;')
    srv_control.run_command(step, 'authoritative;')
    srv_control.run_command(step, 'prefix-length-mode ignore;')
    srv_control.run_command(step, 'subnet6 3000::/16 {')
    srv_control.run_command(step, ' pool6 {')
    srv_control.run_command(step, '  prefix6 3000:db8:0:100:: 3000:db8:0:100:: /56;')
    srv_control.run_command(step, ' }')
    srv_control.run_command(step, ' pool6 {')
    srv_control.run_command(step, '  prefix6 3000:db8:1:100:: 3000:db8:1:100:: /64;')
    srv_control.run_command(step, ' }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # /0              3000:db8:0:100::/56
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '0')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '56')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')

    # /48             3000:db8:0:100::/56
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '48')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '56')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')

    # /60             3000:db8:0:100::/56
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '60')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '56')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')

    # /64             3000:db8:1:100::/56
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '64')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '56')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')

    # /72             3000:db8:1:100::/56
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '72')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '56')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.keyword
@pytest.mark.prefix_length_mode
def test_dhcpd_keyword_prefix_length_mode_prefer(step):
    """new-dhcpd.keyword.prefix-length-mode.prefer"""
    # Tests prefix-length-mode = prefer
    # Uses a series of solicits with varying plens to check the offer
    # outcome.
    # 
    # Solicit plen    Offer Outcome
    # --------------------------------------
    # /0              3000:db8:0:100::/56
    # /48             3000:db8:0:100::/56
    # /60             3000:db8:0:100::/56
    # /64             3000:db8:1:100::/64
    # /72             3000:db8:0:100::/56

    misc.test_setup(step)
    srv_control.run_command(step, 'ddns-updates off;')
    srv_control.run_command(step, 'authoritative;')
    srv_control.run_command(step, 'prefix-length-mode prefer;')
    srv_control.run_command(step, 'subnet6 3000::/16 {')
    srv_control.run_command(step, ' pool6 {')
    srv_control.run_command(step, '  prefix6 3000:db8:0:100:: 3000:db8:0:100:: /56;')
    srv_control.run_command(step, ' }')
    srv_control.run_command(step, ' pool6 {')
    srv_control.run_command(step, '  prefix6 3000:db8:1:100:: 3000:db8:1:100:: /64;')
    srv_control.run_command(step, ' }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # /0              3000:db8:0:100::/56
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '0')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '56')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')

    # /48             3000:db8:0:100::/56
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '48')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '56')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')

    # /60             3000:db8:0:100::/56
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '60')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '56')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')

    # /64             3000:db8:1:100::/64
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '64')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '64')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:1:100::')

    # /72             3000:db8:0:100::/56
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '72')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '56')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.keyword
@pytest.mark.prefix_length_mode
def test_dhcpd_keyword_prefix_length_mode_exact(step):
    """new-dhcpd.keyword.prefix-length-mode.exact"""
    # Tests default setting for prefix-length-mode = exact.
    # 
    # Uses a series of solicits with varying plens to check the offer
    # outcome.
    # 
    # Solicit plen    Offer Outcome
    # --------------------------------------
    # /0              3000:db8:0:100::/56
    # /48             None available
    # /60             None available
    # /64             3000:db8:1:100::/64
    # /72             None available

    misc.test_setup(step)
    srv_control.run_command(step, 'ddns-updates off;')
    srv_control.run_command(step, 'authoritative;')
    srv_control.run_command(step, 'prefix-length-mode exact;')
    srv_control.run_command(step, 'subnet6 3000::/16 {')
    srv_control.run_command(step, ' pool6 {')
    srv_control.run_command(step, '  prefix6 3000:db8:0:100:: 3000:db8:0:100:: /56;')
    srv_control.run_command(step, ' }')
    srv_control.run_command(step, ' pool6 {')
    srv_control.run_command(step, '  prefix6 3000:db8:1:100:: 3000:db8:1:100:: /64;')
    srv_control.run_command(step, ' }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # /0              3000:db8:0:100::/56
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '0')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '56')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')

    # /48             None available
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '48')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '13',
                                             '25',
                                             None,
                                             'statuscode',
                                             '6')

    # /60             None available
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '60')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '13',
                                             '25',
                                             None,
                                             'statuscode',
                                             '6')

    # /64             3000:db8:1:100::/64
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '64')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '64')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:1:100::')

    # /72             None available
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '72')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '13',
                                             '25',
                                             None,
                                             'statuscode',
                                             '6')



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.keyword
@pytest.mark.prefix_length_mode
def test_dhcpd_keyword_prefix_length_mode_minimum(step):
    """new-dhcpd.keyword.prefix-length-mode.minimum"""
    # Tests default setting for prefix-length-mode = minimum, which should select:
    # an exact match if it exists, then the first available whose prefix
    # length is greater than preferred length, otherwise fail
    # 
    # Uses a series of solicits with varying plens to check the offer
    # outcome.
    # 
    # Solicit plen    Offer Outcome
    # --------------------------------------
    # /0              3000:db8:0:100::/56
    # /48             3000:db8:0:100::/56
    # /60             3000:db8:1:100::/64
    # /64             3000:db8:1:100::/64
    # /72             None available

    misc.test_setup(step)
    srv_control.run_command(step, 'ddns-updates off;')
    srv_control.run_command(step, 'authoritative;')
    srv_control.run_command(step, 'prefix-length-mode minimum;')
    srv_control.run_command(step, 'subnet6 3000::/16 {')
    srv_control.run_command(step, ' pool6 {')
    srv_control.run_command(step, '  prefix6 3000:db8:0:100:: 3000:db8:0:100:: /56;')
    srv_control.run_command(step, ' }')
    srv_control.run_command(step, ' pool6 {')
    srv_control.run_command(step, '  prefix6 3000:db8:1:100:: 3000:db8:1:100:: /64;')
    srv_control.run_command(step, ' }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # /0              3000:db8:0:100::/56
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '0')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '56')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')

    # /48             3000:db8:0:100::/56
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '48')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '56')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')

    # /60             3000:db8:1:100::/64
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '60')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '64')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:1:100::')

    # /64             3000:db8:1:100::/64
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '64')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '64')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:1:100::')

    # /72             None available
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '72')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '13',
                                             '25',
                                             None,
                                             'statuscode',
                                             '6')



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.keyword
@pytest.mark.prefix_length_mode
def test_dhcpd_keyword_prefix_length_mode_maximum(step):
    """new-dhcpd.keyword.prefix-length-mode.maximum"""
    # Tests default setting for prefix-length-mode = maximum, which should select:
    # an exact match if it exists, then the first available whose prefix
    # length is less than preferred length, otherwise fail
    # 
    # Uses a series of solicits with varying plens to check the offer
    # outcome.
    # 
    # Solicit plen    Offer Outcome
    # --------------------------------------
    # /0              3000:db8:0:100::/56
    # /48             None available
    # /60             3000:db8:1:100::/56
    # /64             3000:db8:1:100::/64
    # /72             3000:db8:0:100::/56

    misc.test_setup(step)
    srv_control.run_command(step, 'ddns-updates off;')
    srv_control.run_command(step, 'authoritative;')
    srv_control.run_command(step, 'prefix-length-mode maximum;')
    srv_control.run_command(step, 'subnet6 3000::/16 {')
    srv_control.run_command(step, ' pool6 {')
    srv_control.run_command(step, '  prefix6 3000:db8:0:100:: 3000:db8:0:100:: /56;')
    srv_control.run_command(step, ' }')
    srv_control.run_command(step, ' pool6 {')
    srv_control.run_command(step, '  prefix6 3000:db8:1:100:: 3000:db8:1:100:: /64;')
    srv_control.run_command(step, ' }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # /0              3000:db8:0:100::/56
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '0')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '56')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')


    # /48             None available
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '48')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '13',
                                             '25',
                                             None,
                                             'statuscode',
                                             '6')

    # /60            3000:db8:1:100::/56
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '60')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '56')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')

    # /64             3000:db8:1:100::/64
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '64')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '64')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:1:100::')

    # /72             3000:db8:1:100::/56
    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '72')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '56')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.PD
@pytest.mark.rfc3633
@pytest.mark.keyword
@pytest.mark.prefix_length_mode
def test_dhcpd_keyword_prefix_length_mode_plen_0(step):
    """new-dhcpd.keyword.prefix-length-mode.plen_0"""
    # Tests that prefix selection is correct for clients soliciting with plen
    # of 0, as pools are exhausted.  Witha plen of 0, prefix-length-mode is
    # ignored, so prefix consumption should proceed from first available.
    # 
    # Server is configured with two pools of 1 prefix each.  One pool with
    # a prefix length of /56, the second with a prefix length of /64. Then a
    # series of three SARRs, each using a different DUID are conducted:
    # 
    # Case 1: Client 1 requests an address
    # - server should grant a lease from /56 pool (exhausts the /56 pool)
    # Case 2: Client 2 requests an address
    # - server should grant a lease from /64 pool (exhausts the /64 pool)
    # Case 3: Client 3 requests an address
    # - server should respond with no addresses available

    misc.test_setup(step)
    srv_control.run_command(step, 'ddns-updates off;')
    srv_control.run_command(step, 'authoritative;')
    srv_control.run_command(step, 'subnet6 3000::/16 {')
    srv_control.run_command(step, ' pool6 {')
    srv_control.run_command(step, '  prefix6 3000:db8:0:100:: 3000:db8:0:100:: /56;')
    srv_control.run_command(step, ' }')
    srv_control.run_command(step, ' pool6 {')
    srv_control.run_command(step, '  prefix6 3000:db8:1:100:: 3000:db8:1:100:: /64;')
    srv_control.run_command(step, ' }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # ######################################################################
    # Case 1: Client 1 requests an address
    # - server should grant a lease from /56 pool (exhausts the /56 pool)
    # ######################################################################
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '0')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '56')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')

    misc.test_procedure(step)
    # Client copies IA-PD option from received message.
    srv_msg.client_copy_option(step, 'IA_PD')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '56')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:0:100::')

    # ######################################################################
    # Case 2: Client 2 requests an address
    # - server should grant a lease from /64 pool (exhausts the /64 pool)
    # ######################################################################
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '0')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '64')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:1:100::')

    misc.test_procedure(step)
    # Client copies IA-PD option from received message.
    srv_msg.client_copy_option(step, 'IA_PD')
    srv_msg.client_copy_option(step, 'client-id')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '26')
    srv_msg.response_check_suboption_content(step, 'Response', '26', '25', None, 'plen', '64')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '26',
                                             '25',
                                             None,
                                             'prefix',
                                             '3000:db8:1:100::')

    # ######################################################################
    # Case 3: Client 3 requests an address
    # - server should respond with no addresses available
    # ######################################################################
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:03')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'plen', '0')
    srv_msg.client_sets_value(step, 'Client', 'prefix', '::')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Prefix')
    srv_msg.client_does_include(step, 'Client', None, 'IA-PD')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '25')
    srv_msg.response_check_option_content(step, 'Response', '25', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '13',
                                             '25',
                                             None,
                                             'statuscode',
                                             '6')


