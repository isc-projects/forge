import pytest

import srv_msg
import srv_control
import misc

from forge_cfg import world


@pytest.mark.v4
@pytest.mark.flex_options
def test_flex_options_add():
    misc.test_setup()
    # first exchange of DORA with hostname should result with adding option boot-file-name (67) with hostname + .boot
    # second exchange of DORA without hostname should result with adding option boot-file-name with value 'no-boot-file'
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.2')
    srv_control.add_hooks('libdhcp_flex_option.so')

    world.dhcp_cfg["hooks-libraries"][0].update(
        {
            "parameters": {
                "options": [
                    {
                        "code": 67,
                        "add": "ifelse(option[host-name].exists,concat(option[host-name].text,'.boot'),'no-boot-file')"
                    }
                ]
            }
        }
    )
    srv_control.build_and_send_config_files('SSH', 'configfile')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:01')
    srv_msg.client_does_include_with_value('hostname', 'myuniquehostname')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', 67, None, 'value', 'myuniquehostname.boot')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:01')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('hostname', 'myuniquehostname')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', 67, None, 'value', 'myuniquehostname.boot')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:02')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.2')
    srv_msg.response_check_option_content('Response', 67, None, 'value', 'no-boot-file')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:01')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.2')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.2')
    srv_msg.response_check_option_content('Response', 67, None, 'value', 'no-boot-file')


@pytest.mark.v4
@pytest.mark.flex_options
def test_flex_options_remove():
    misc.test_setup()
    # First DORA without hostname, responses from server will include option name-servers
    # second DORA exchange with hostname should NOT include name-servers option
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.2')
    srv_control.config_srv_opt('name-servers', '199.199.199.1')
    srv_control.add_hooks('libdhcp_flex_option.so')

    world.dhcp_cfg["hooks-libraries"][0].update(
        {
            "parameters": {
                "options": [
                    {
                        "code": 5,
                        "remove": "option[host-name].exists"
                    }
                ]
            }
        }
    )
    srv_control.build_and_send_config_files('SSH', 'configfile')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:02')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', 5, None, 'value', '199.199.199.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:02')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_requests_option(5)
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', 5, None, 'value', '199.199.199.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:03')
    srv_msg.client_does_include_with_value('hostname', 'myuniquehostname')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.2')
    srv_msg.response_check_include_option('Response', 'NOT ', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:03')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('hostname', 'myuniquehostname')
    srv_msg.client_requests_option(5)
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.2')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.2')
    srv_msg.response_check_include_option('Response', 'NOT ', 5)


@pytest.mark.v4
@pytest.mark.flex_options
def test_flex_options_remove_non_existing():
    misc.test_setup()
    # Kea will try to remove non existing option, let's check if it survives
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.2')
    srv_control.add_hooks('libdhcp_flex_option.so')

    world.dhcp_cfg["hooks-libraries"][0].update(
        {
            "parameters": {
                "options": [
                    {
                        "code": 5,
                        "remove": "option[host-name].exists"
                    }
                ]
            }
        }
    )
    srv_control.build_and_send_config_files('SSH', 'configfile')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:03')
    srv_msg.client_does_include_with_value('hostname', 'myuniquehostname')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.2')
    srv_msg.response_check_include_option('Response', 'NOT ', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:03')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('hostname', 'myuniquehostname')
    srv_msg.client_requests_option(5)
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.2')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.2')
    srv_msg.response_check_include_option('Response', 'NOT ', 5)


@pytest.mark.v4
@pytest.mark.flex_options
def test_flex_options_supersede():
    misc.test_setup()
    # first DORA exchange with hostname should include configured name-servers option
    # second DORA without hostname, responses from server will include changed option name-servers
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.2')
    srv_control.config_srv_opt('name-servers', '199.199.199.1')
    srv_control.add_hooks('libdhcp_flex_option.so')

    world.dhcp_cfg["hooks-libraries"][0].update(
        {
            "parameters": {
                "options": [
                    {
                        "code": 5,
                        "supersede": "ifelse(option[host-name].text == 'myuniquehostname', 0x0a000001,'')"
                    }
                ]
            }
        }
    )
    srv_control.build_and_send_config_files('SSH', 'configfile')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:02')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, 5)
    srv_msg.response_check_option_content('Response', 5, None, 'value', '199.199.199.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:02')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_requests_option(5)
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option('Response', None, 5)
    srv_msg.response_check_option_content('Response', 5, None, 'value', '199.199.199.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:03')
    srv_msg.client_does_include_with_value('hostname', 'myuniquehostname')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.2')
    srv_msg.response_check_include_option('Response', None, 5)
    srv_msg.response_check_option_content('Response', 5, None, 'value', '10.0.0.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:03')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('hostname', 'myuniquehostname')
    srv_msg.client_requests_option(5)
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.2')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.2')
    srv_msg.response_check_include_option('Response', None, 5)
    srv_msg.response_check_option_content('Response', 5, None, 'value', '10.0.0.1')


@pytest.mark.v4
@pytest.mark.flex_options
def test_flex_options_all_actions():
    misc.test_setup()
    # First DORA should activate all 3 actions, changed option 5, removed option 6, add option 67 with concat hostname
    # Second DORA should just activate 1 action, add option 67 with value no-boot-file
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.2')
    srv_control.config_srv_opt('name-servers', '199.199.199.1')
    srv_control.config_srv_opt('domain-name-servers', '100.100.100.1')
    srv_control.add_hooks('libdhcp_flex_option.so')

    world.dhcp_cfg["hooks-libraries"][0].update(
        {
            "parameters": {
                "options": [
                    {
                        # change option 5 to 10.0.0.1 if hostname is myuniquehostname
                        "code": 5,
                        "supersede": "ifelse(option[host-name].text == 'myuniquehostname', 0x0a000001,'')"
                    },
                    {
                        # remove option 6 domain-name-servers if client has a reservation
                        "code": 6,
                        "remove": "member('KNOWN')"
                    },
                    {
                        # if hostname provided add option 67 hostname+'.boot' if hostname not provided
                        # add option 67 'no-boot-file'
                        "code": 67,
                        "add": "ifelse(option[host-name].exists,concat(option[host-name].text,'.boot'),'no-boot-file')"
                    }
                ]
            }
        }
    )
    world.dhcp_cfg["subnet4"][0].update(
        {
            "reservations": [
                {
                    "ip-address": "192.168.50.200",
                    "hw-address": "01:02:03:04:05:06"
                }
            ]
        }
    )

    srv_control.build_and_send_config_files('SSH', 'configfile')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '01:02:03:04:05:06')
    srv_msg.client_does_include_with_value('hostname', 'myuniquehostname')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.200')
    srv_msg.response_check_include_option('Response', 'NOT ', 6)
    srv_msg.response_check_option_content('Response', 5, None, 'value', '10.0.0.1')
    srv_msg.response_check_option_content('Response', 67, None, 'value', 'myuniquehostname.boot')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '01:02:03:04:05:06')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('hostname', 'myuniquehostname')
    srv_msg.client_requests_option(5)
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.200')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.200')
    srv_msg.response_check_include_option('Response', 'NOT ', 6)
    srv_msg.response_check_option_content('Response', 5, None, 'value', '10.0.0.1')
    srv_msg.response_check_option_content('Response', 67, None, 'value', 'myuniquehostname.boot')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '01:01:01:01:05:06')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', 6, None, 'value', '100.100.100.1')
    srv_msg.response_check_option_content('Response', 5, None, 'value', '199.199.199.1')
    srv_msg.response_check_option_content('Response', 67, None, 'value', 'no-boot-file')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '01:01:01:04:05:06')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_requests_option(5)
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content('Response', 5, None, 'value', '199.199.199.1')
    srv_msg.response_check_option_content('Response', 67, None, 'value', 'no-boot-file')
