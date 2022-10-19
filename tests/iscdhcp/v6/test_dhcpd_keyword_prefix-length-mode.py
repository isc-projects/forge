# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""ISC_DHCP DHCPv6 Keywords Prefix Length Mode"""

# pylint: disable=invalid-name,line-too-long

import pytest
from src import misc
from src import srv_control
from src import srv_msg

from src.softwaresupport.isc_dhcp6_server.functions import add_line_in_global


@pytest.mark.v6
@pytest.mark.dhcpd
def test_dhcpd_keyword_prefix_length_mode_default():
    """new-dhcpd.keyword.prefix-length-mode.default"""
    # Tests default setting for prefix_len_mode which should be match
    # prefix-length-mode = PLM_PREFER.
    # Uses a series of solicits with varying plens to check the offer
    # outcome.
    #
    # Solicit plen    Offer Outcome
    # --------------------------------------
    # /0              2001:db8:0:100::/56
    # /48             2001:db8:0:100::/56
    # /60             2001:db8:0:100::/56
    # /64             2001:db8:1:100::/64
    # /72             2001:db8:0:100::/56

    misc.test_setup()
    add_line_in_global('ddns-updates off;')
    add_line_in_global('authoritative;')
    add_line_in_global('subnet6 2001:db8::/32 {')
    add_line_in_global(' pool6 {')
    add_line_in_global('  prefix6 2001:db8:0:100:: 2001:db8:0:100:: /56;')
    add_line_in_global(' }')
    add_line_in_global(' pool6 {')
    add_line_in_global('  prefix6 2001:db8:1:100:: 2001:db8:1:100:: /64;')
    add_line_in_global(' }')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # /0              2001:db8:0:100::/56
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 0)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 56)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')

    # /48             2001:db8:0:100::/56
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 48)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 56)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')

    # /60             2001:db8:0:100::/56
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 60)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 56)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')

    # /64             2001:db8:1:100::/64
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 64)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 64)
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:1:100::')

    # /72             2001:db8:0:100::/56
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', '72')
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 56)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')


@pytest.mark.v6
@pytest.mark.dhcpd
def test_dhcpd_keyword_prefix_length_mode_ignore():
    """new-dhcpd.keyword.prefix-length-mode.ignore"""
    # Tests prefix-length-mode = ignore
    # Uses a series of solicits with varying plens to check the offer
    # outcome.
    #
    # Solicit plen    Offer Outcome
    # --------------------------------------
    # /0              2001:db8:0:100::/56
    # /48             2001:db8:0:100::/56
    # /60             2001:db8:0:100::/56
    # /64             2001:db8:0:100::/56
    # /72             2001:db8:0:100::/56

    misc.test_setup()
    add_line_in_global('ddns-updates off;')
    add_line_in_global('authoritative;')
    add_line_in_global('prefix-length-mode ignore;')
    add_line_in_global('subnet6 2001:db8::/32 {')
    add_line_in_global(' pool6 {')
    add_line_in_global('  prefix6 2001:db8:0:100:: 2001:db8:0:100:: /56;')
    add_line_in_global(' }')
    add_line_in_global(' pool6 {')
    add_line_in_global('  prefix6 2001:db8:1:100:: 2001:db8:1:100:: /64;')
    add_line_in_global(' }')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # /0              2001:db8:0:100::/56
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 0)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 56)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')

    # /48             2001:db8:0:100::/56
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 48)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 56)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')

    # /60             2001:db8:0:100::/56
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 60)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 56)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')

    # /64             2001:db8:1:100::/56
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 64)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 56)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')

    # /72             2001:db8:1:100::/56
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', '72')
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 56)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')


@pytest.mark.v6
@pytest.mark.dhcpd
def test_dhcpd_keyword_prefix_length_mode_prefer():
    """new-dhcpd.keyword.prefix-length-mode.prefer"""
    # Tests prefix-length-mode = prefer
    # Uses a series of solicits with varying plens to check the offer
    # outcome.
    #
    # Solicit plen    Offer Outcome
    # --------------------------------------
    # /0              2001:db8:0:100::/56
    # /48             2001:db8:0:100::/56
    # /60             2001:db8:0:100::/56
    # /64             2001:db8:1:100::/64
    # /72             2001:db8:0:100::/56

    misc.test_setup()
    add_line_in_global('ddns-updates off;')
    add_line_in_global('authoritative;')
    add_line_in_global('prefix-length-mode prefer;')
    add_line_in_global('subnet6 2001:db8::/32 {')
    add_line_in_global(' pool6 {')
    add_line_in_global('  prefix6 2001:db8:0:100:: 2001:db8:0:100:: /56;')
    add_line_in_global(' }')
    add_line_in_global(' pool6 {')
    add_line_in_global('  prefix6 2001:db8:1:100:: 2001:db8:1:100:: /64;')
    add_line_in_global(' }')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # /0              2001:db8:0:100::/56
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 0)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 56)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')

    # /48             2001:db8:0:100::/56
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 48)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 56)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')

    # /60             2001:db8:0:100::/56
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 60)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 56)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')

    # /64             2001:db8:1:100::/64
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 64)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 64)
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:1:100::')

    # /72             2001:db8:0:100::/56
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', '72')
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 56)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')


@pytest.mark.v6
@pytest.mark.dhcpd
def test_dhcpd_keyword_prefix_length_mode_exact():
    """new-dhcpd.keyword.prefix-length-mode.exact"""
    # Tests default setting for prefix-length-mode = exact.
    #
    # Uses a series of solicits with varying plens to check the offer
    # outcome.
    #
    # Solicit plen    Offer Outcome
    # --------------------------------------
    # /0              2001:db8:0:100::/56
    # /48             None available
    # /60             None available
    # /64             2001:db8:1:100::/64
    # /72             None available

    misc.test_setup()
    add_line_in_global('ddns-updates off;')
    add_line_in_global('authoritative;')
    add_line_in_global('prefix-length-mode exact;')
    add_line_in_global('subnet6 2001:db8::/32 {')
    add_line_in_global(' pool6 {')
    add_line_in_global('  prefix6 2001:db8:0:100:: 2001:db8:0:100:: /56;')
    add_line_in_global(' }')
    add_line_in_global(' pool6 {')
    add_line_in_global('  prefix6 2001:db8:1:100:: 2001:db8:1:100:: /64;')
    add_line_in_global(' }')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # /0              2001:db8:0:100::/56
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 0)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 56)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')

    # /48             None available
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 48)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 25, 'statuscode', 6)

    # /60             None available
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 60)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 25, 'statuscode', 6)

    # /64             2001:db8:1:100::/64
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 64)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 64)
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:1:100::')

    # /72             None available
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', '72')
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 25, 'statuscode', 6)


@pytest.mark.v6
@pytest.mark.dhcpd
def test_dhcpd_keyword_prefix_length_mode_minimum():
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
    # /0              2001:db8:0:100::/56
    # /48             2001:db8:0:100::/56
    # /60             2001:db8:1:100::/64
    # /64             2001:db8:1:100::/64
    # /72             None available

    misc.test_setup()
    add_line_in_global('ddns-updates off;')
    add_line_in_global('authoritative;')
    add_line_in_global('prefix-length-mode minimum;')
    add_line_in_global('subnet6 2001:db8::/32 {')
    add_line_in_global(' pool6 {')
    add_line_in_global('  prefix6 2001:db8:0:100:: 2001:db8:0:100:: /56;')
    add_line_in_global(' }')
    add_line_in_global(' pool6 {')
    add_line_in_global('  prefix6 2001:db8:1:100:: 2001:db8:1:100:: /64;')
    add_line_in_global(' }')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # /0              2001:db8:0:100::/56
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 0)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 56)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')

    # /48             2001:db8:0:100::/56
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 48)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 56)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')

    # /60             2001:db8:1:100::/64
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 60)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 64)
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:1:100::')

    # /64             2001:db8:1:100::/64
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 64)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 64)
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:1:100::')

    # /72             None available
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', '72')
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 25, 'statuscode', 6)


@pytest.mark.v6
@pytest.mark.dhcpd
def test_dhcpd_keyword_prefix_length_mode_maximum():
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
    # /0              2001:db8:0:100::/56
    # /48             None available
    # /60             2001:db8:1:100::/56
    # /64             2001:db8:1:100::/64
    # /72             2001:db8:0:100::/56

    misc.test_setup()
    add_line_in_global('ddns-updates off;')
    add_line_in_global('authoritative;')
    add_line_in_global('prefix-length-mode maximum;')
    add_line_in_global('subnet6 2001:db8::/32 {')
    add_line_in_global(' pool6 {')
    add_line_in_global('  prefix6 2001:db8:0:100:: 2001:db8:0:100:: /56;')
    add_line_in_global(' }')
    add_line_in_global(' pool6 {')
    add_line_in_global('  prefix6 2001:db8:1:100:: 2001:db8:1:100:: /64;')
    add_line_in_global(' }')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # /0              2001:db8:0:100::/56
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 0)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 56)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')

    # /48             None available
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 48)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 25, 'statuscode', 6)

    # /60            2001:db8:1:100::/56
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 60)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 56)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')

    # /64             2001:db8:1:100::/64
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 64)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 64)
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:1:100::')

    # /72             2001:db8:1:100::/56
    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', '72')
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 56)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')


@pytest.mark.v6
@pytest.mark.dhcpd
def test_dhcpd_keyword_prefix_length_mode_plen_0():
    """new-dhcpd.keyword.prefix-length-mode.plen_0"""
    # Tests that prefix selection is correct for clients soliciting with plen
    # of 0, as pools are exhausted.  With a plen of 0, prefix-length-mode is
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

    misc.test_setup()
    add_line_in_global('ddns-updates off;')
    add_line_in_global('authoritative;')
    add_line_in_global('subnet6 2001:db8::/32 {')
    add_line_in_global(' pool6 {')
    add_line_in_global('  prefix6 2001:db8:0:100:: 2001:db8:0:100:: /56;')
    add_line_in_global(' }')
    add_line_in_global(' pool6 {')
    add_line_in_global('  prefix6 2001:db8:1:100:: 2001:db8:1:100:: /64;')
    add_line_in_global(' }')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # ######################################################################
    # Case 1: Client 1 requests an address
    # - server should grant a lease from /56 pool (exhausts the /56 pool)
    # ######################################################################
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 0)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 56)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')

    misc.test_procedure()
    # Client copies IA-PD option from received message.
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 56)
    srv_msg.response_check_suboption_content(26,  25,  'prefix', '2001:db8:0:100::')

    # ######################################################################
    # Case 2: Client 2 requests an address
    # - server should grant a lease from /64 pool (exhausts the /64 pool)
    # ######################################################################
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 0)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 64)
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:1:100::')

    misc.test_procedure()
    # Client copies IA-PD option from received message.
    srv_msg.client_copy_option('IA_PD')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_option_content(25, 'sub-option', 26)
    srv_msg.response_check_suboption_content(26, 25, 'plen', 64)
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2001:db8:1:100::')

    # ######################################################################
    # Case 3: Client 3 requests an address
    # - server should respond with no addresses available
    # ######################################################################
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:03')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_sets_value('Client', 'plen', 0)
    srv_msg.client_sets_value('Client', 'prefix', '::')
    srv_msg.client_does_include('Client', 'IA_Prefix')
    srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(25)
    srv_msg.response_check_option_content(25, 'sub-option', 13)
    srv_msg.response_check_suboption_content(13, 25, 'statuscode', 6)
