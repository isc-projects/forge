# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""ISC_DHCP DHCPv6 Keywords"""

# pylint: disable=line-too-long

import pytest
from src import misc
from src import srv_control
from src import srv_msg

from src.protosupport.multi_protocol_functions import log_contains, log_doesnt_contain
from src.softwaresupport.isc_dhcp6_server.functions import build_log_path, add_line_in_global


@pytest.mark.v6
@pytest.mark.dhcpd
@pytest.mark.ddns
def test_v6_dhcpd_keyword_ddns_reverse_add():
    """new-v6.dhcpd.keyword.ddns.reverse.add"""
    # #
    # Testing: Checks that a reverse add is attempted when the configuration
    # is valid but minimal and client sends a request with valid fqdn
    # #
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::2-2001:db8:1::2')
    add_line_in_global('ddns-updates true;')
    add_line_in_global('ddns-update-style interim;')
    add_line_in_global('do-reverse-updates true;')
    add_line_in_global('zone 0.0.0.3.ip6.arpa. {primary 127.0.0.1;}')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # #
    # Grab a lease
    # #
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'N')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'myhost.bubba.com')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::2')
    log_contains('DDNS_STATE_ADD_PTR myhost.bubba.com for 2.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.3.ip6.arpa.',
                 log_file=build_log_path())


@pytest.mark.v6
@pytest.mark.dhcpd
@pytest.mark.ddns
def test_v6_dhcpd_keyword_ddns_reverse_do_reverse_updates_false():
    """new-v6.dhcpd.keyword.ddns.reverse.do-reverse-updates.false"""
    # #
    # Testing: Checks that a reverse add is not attempted when the
    # when do-reverse-updates is set to false.
    # #
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::2-2001:db8:1::2')
    add_line_in_global('ddns-updates true;')
    add_line_in_global('ddns-update-style interim;')
    add_line_in_global('do-reverse-updates false;')
    add_line_in_global('zone 0.0.0.3.ip6.arpa. {primary 127.0.0.1;}')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # #
    # Grab a lease
    # #
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'N')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'myhost.bubba.com')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::2')
    log_doesnt_contain('DDNS_STATE_ADD_PTR reverse myhost.bubba.com for 2.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.3.ip6.arpa.',
                       log_file=build_log_path())


@pytest.mark.v6
@pytest.mark.dhcpd
@pytest.mark.ddns
def test_v6_dhcpd_keyword_ddns_reverse_no_client_fqdn():
    """new-v6.dhcpd.keyword.ddns.reverse.no-client-fqdn"""
    # #
    # Testing: Checks that reverse ddns updates are not attempted when
    # no client FQDN option is supplied.
    # #
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::2-2001:db8:1::2')
    add_line_in_global('ddns-updates true;')
    add_line_in_global('ddns-update-style interim;')
    add_line_in_global('do-reverse-updates true;')
    add_line_in_global('zone 0.0.0.3.ip6.arpa. {primary 127.0.0.1;}')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # #
    # Grab a lease
    # #
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::2')
    log_doesnt_contain('DDNS_STATE_ADD_PTR reverse.', log_file=build_log_path())


@pytest.mark.v6
@pytest.mark.dhcpd
@pytest.mark.ddns
def test_v6_dhcpd_keyword_ddns_reverse_ddns_ttl():
    """new-v6.dhcpd.keyword.ddns.reverse.ddns-ttl"""
    # #
    # Testing: Checks that TTL sent with the reverse add can be specified
    # using ddns-ttl.
    # #
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::2-2001:db8:1::2')
    add_line_in_global('ddns-updates true;')
    add_line_in_global('ddns-update-style interim;')
    add_line_in_global('do-reverse-updates true;')
    add_line_in_global('zone 0.0.0.3.ip6.arpa. {primary 127.0.0.1;}')
    add_line_in_global('ddns-ttl 7701;')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # #
    # Grab a lease
    # #
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'N')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'myhost.bubba.com')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::2')
    log_contains('ttl: 7701', log_file=build_log_path())


@pytest.mark.v6
@pytest.mark.dhcpd
@pytest.mark.ddns
def test_v6_dhcpd_keyword_ddns_reverse_ddns_hostname():
    """new-v6.dhcpd.keyword.ddns.reverse.ddns-hostname"""
    # #
    # Testing: Checks that hostname used as the FQDN in the reverse add
    # can be specified using ddns-hostname.
    # #
    # This test currently FAILS.  Unlike for forward v6 updates which
    # use ddns-hostname for the AAAA record, they do not use it for
    # the PTR record.  This seems inconsistent.
    # #
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::2-2001:db8:1::2')
    add_line_in_global('ddns-updates true;')
    add_line_in_global('ddns-domainname "six.example.com";')
    add_line_in_global('ddns-hostname "cfg_host";')
    add_line_in_global('ddns-update-style interim;')
    add_line_in_global('do-reverse-updates true;')
    add_line_in_global('zone 0.0.0.3.ip6.arpa. {primary 127.0.0.1;}')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # #
    # Grab a lease
    # #
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('client-id')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'N')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'myhost.bubba.com')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::2')
    log_contains('DDNS_STATE_ADD_PTR reverse cfg_host.bubba.com for 2.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.3.ip6.arpa.',
                 log_file=build_log_path())
