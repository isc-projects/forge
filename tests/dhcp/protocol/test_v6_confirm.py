# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""DHCPv6 Confirm"""

import pytest

from src import misc
from src import references
from src import srv_control
from src import srv_msg


@pytest.mark.v6
@pytest.mark.status_code
@pytest.mark.confirm
def test_v6_statuscode_success_confirm():
    #  Testing server ability perform CONFIRM - REPLY message exchange.
    #  Message details 		Client		Server
    #  						SOLICIT -->
    #  		   						<--	ADVERTISE
    #  						REQUEST -->
    #  		   						<--	REPLY
    #  correct message 		CONFIRM -->
    # 					  		    <--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					client-id
    # 					server-id
    # 					status-code with code 0
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('CONFIRM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'status-code', 0)

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.status_code
@pytest.mark.confirm
def test_v6_statuscode_notonlink_confirm():
    #  Testing server ability perform CONFIRM - REPLY message exchange,
    #  with unsuccessful confirmation process.
    #  Message details 		Client		Server
    #  						SOLICIT -->
    #  		   						<--	ADVERTISE
    #  						REQUEST -->
    #  	Save IA_NA with IA_Address	<--	REPLY
    #  						Server Reconfiguration
    #  						SOLICIT -->
    #  Make at least				<--	ADVERTISE
    #   one leases			REQUEST -->
    #  								<--	REPLY
    #  with saved IA_NA		CONFIRM -->
    #  NotOnLink error	  		    <--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					client-id
    # 					server-id
    # 					status-code with code 4
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1000')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    misc.test_procedure()
    srv_msg.client_save_option('IA_NA')

    misc.test_setup()
    srv_control.config_srv_subnet('3001::/64', '3001::2000-3001::3000')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')

    misc.test_procedure()
    srv_msg.client_add_saved_option(erase=True)
    # add IA NA from beginning of the test. makes it NotOnlink
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('CONFIRM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(13)
    srv_msg.response_check_option_content(13, 'statuscode', 4)

    references.references_check('RFC3315')
