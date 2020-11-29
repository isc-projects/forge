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

    h_param = {"options": [{"code": 67,
                            "add": "ifelse(option[host-name].exists,concat(option[host-name].text,'.boot'),'no-boot-file')",
                            "csv-format": True}]}

    world.dhcp_cfg["hooks-libraries"][0].update({"parameters": {}})
    world.dhcp_cfg["hooks-libraries"][0]["parameters"].update(h_param)

    srv_control.build_and_send_config_files('SSH', 'configfile')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:01')
    srv_msg.client_does_include_with_value('hostname', 'myuniquehostname')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(67, 'value', 'myuniquehostname.boot')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:01')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('hostname', 'myuniquehostname')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(67, 'value', 'myuniquehostname.boot')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:02')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.2')
    srv_msg.response_check_option_content(67, 'value', 'no-boot-file')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:01')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.2')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.2')
    srv_msg.response_check_option_content(67, 'value', 'no-boot-file')


@pytest.mark.v4
@pytest.mark.flex_options
def test_flex_options_remove():
    misc.test_setup()
    # First DORA without hostname, responses from server will include option name-servers
    # second DORA exchange with hostname should NOT include name-servers option
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.2')
    srv_control.config_srv_opt('name-servers', '199.199.199.1')
    srv_control.add_hooks('libdhcp_flex_option.so')

    h_param = {"options": [{"code": 5, "remove": "option[host-name].exists"}]}
    world.dhcp_cfg["hooks-libraries"][0].update({"parameters": {}})
    world.dhcp_cfg["hooks-libraries"][0]["parameters"].update(h_param)
    srv_control.build_and_send_config_files('SSH', 'configfile')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:02')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(5, 'value', '199.199.199.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:02')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_requests_option(5)
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(5, 'value', '199.199.199.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:03')
    srv_msg.client_does_include_with_value('hostname', 'myuniquehostname')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.2')
    srv_msg.response_check_include_option(5, expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:03')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('hostname', 'myuniquehostname')
    srv_msg.client_requests_option(5)
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.2')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.2')
    srv_msg.response_check_include_option(5, expect_include=False)


@pytest.mark.v4
@pytest.mark.flex_options
def test_flex_options_remove_non_existing():
    misc.test_setup()
    # Kea will try to remove non existing option, let's check if it survives
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.2')
    srv_control.add_hooks('libdhcp_flex_option.so')

    h_param = {"options": [{"code": 5, "remove": "option[host-name].exists"}]}
    world.dhcp_cfg["hooks-libraries"][0].update({"parameters": {}})
    world.dhcp_cfg["hooks-libraries"][0]["parameters"].update(h_param)
    srv_control.build_and_send_config_files('SSH', 'configfile')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:03')
    srv_msg.client_does_include_with_value('hostname', 'myuniquehostname')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(5, expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:03')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('hostname', 'myuniquehostname')
    srv_msg.client_requests_option(5)
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(5, expect_include=False)


@pytest.mark.v4
@pytest.mark.flex_options
def test_flex_options_supersede():
    misc.test_setup()
    # first DORA exchange with hostname should include configured name-servers option
    # second DORA without hostname, responses from server will include changed option name-servers
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.2')
    srv_control.config_srv_opt('name-servers', '199.199.199.1')
    srv_control.add_hooks('libdhcp_flex_option.so')

    h_param = {"options": [{"code": 5,
                            "supersede": "ifelse(option[host-name].text == 'myuniquehostname', '10.0.0.1','199.199.199.1')",
                            "csv-format": True}]}
    world.dhcp_cfg["hooks-libraries"][0].update({"parameters": {}})
    world.dhcp_cfg["hooks-libraries"][0]["parameters"].update(h_param)

    srv_control.build_and_send_config_files('SSH', 'configfile')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:02')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(5)
    srv_msg.response_check_option_content(5, 'value', '199.199.199.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:02')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_requests_option(5)
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(5)
    srv_msg.response_check_option_content(5, 'value', '199.199.199.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:03')
    srv_msg.client_does_include_with_value('hostname', 'myuniquehostname')
    srv_msg.client_requests_option(5)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.2')
    srv_msg.response_check_include_option(5)
    srv_msg.response_check_option_content(5, 'value', '10.0.0.1')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:03')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('hostname', 'myuniquehostname')
    srv_msg.client_requests_option(5)
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.2')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.2')
    srv_msg.response_check_include_option(5)
    srv_msg.response_check_option_content(5, 'value', '10.0.0.1')


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

    h_param = {"options": [{"code": 5, #  change option 5 to 10.0.0.1 if hostname is myuniquehostname
                            "supersede": "ifelse(option[host-name].text == 'myuniquehostname', '10.0.0.1', '199.199.199.1')",
                            "csv-format": True },
                           {"code": 6, #  remove option 6 domain-name-servers if client has a reservation
                            "remove": "member('KNOWN')"},
                           {"code": 67, #  if hostname provided add option 67 hostname+'.boot' if hostname not provided
                            # add option 67 'no-boot-file'
                            "add": "ifelse(option[host-name].exists,concat(option[host-name].text,'.boot'),'no-boot-file')",
                            "csv-format": True}]}

    world.dhcp_cfg["hooks-libraries"][0].update({"parameters": {}})
    world.dhcp_cfg["hooks-libraries"][0]["parameters"].update(h_param)
    reservation = {"reservations": [{"ip-address": "192.168.50.200", "hw-address": "01:02:03:04:05:06"}]}
    world.dhcp_cfg["subnet4"][0].update(reservation)

    srv_control.build_and_send_config_files('SSH', 'configfile')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '01:02:03:04:05:06')
    srv_msg.client_does_include_with_value('hostname', 'myuniquehostname')
    srv_msg.client_requests_option(5)
    srv_msg.client_requests_option(6)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.200')
    srv_msg.response_check_include_option(6, expect_include=False)
    srv_msg.response_check_include_option(5)
    srv_msg.response_check_option_content(5, 'value', '10.0.0.1')
    srv_msg.response_check_include_option(67)
    srv_msg.response_check_option_content(67, 'value', 'myuniquehostname.boot')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '01:02:03:04:05:06')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('hostname', 'myuniquehostname')
    srv_msg.client_requests_option(5)
    srv_msg.client_requests_option(6)
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.200')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.200')
    srv_msg.response_check_include_option(6, expect_include=False)
    srv_msg.response_check_option_content(5, 'value', '10.0.0.1')
    srv_msg.response_check_option_content(67, 'value', 'myuniquehostname.boot')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '01:01:01:01:05:06')
    srv_msg.client_requests_option(5)
    srv_msg.client_requests_option(6)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(6, 'value', '100.100.100.1')
    srv_msg.response_check_option_content(5, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(67, 'value', 'no-boot-file')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '01:01:01:04:05:06')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_requests_option(5)
    srv_msg.client_requests_option(6)
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_option_content(5, 'value', '199.199.199.1')
    srv_msg.response_check_option_content(67, 'value', 'no-boot-file')


@pytest.mark.v4
@pytest.mark.flex_options
def test_flex_options_complex():
    misc.test_setup()
    # first exchange of DORA with hostname should result with adding option boot-file-name (67) with hostname + .boot
    # second exchange of DORA without hostname should result with adding option boot-file-name with value 'no-boot-file'
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    srv_control.config_srv_opt('boot-file-name', 'somefilename')
    srv_control.add_hooks('libdhcp_flex_option.so')
    srv_control.host_reservation_in_subnet('ip-address',
                                           '192.168.50.110',
                                           0,
                                           'hw-address',
                                           'ff:01:02:03:ff:04')

    h_param = {"options": [{"code": 67,
                            "supersede": "ifelse(not option[77].exists and not option[60].exists, '', ifelse(not option[77].exists and option[60].exists, '/path/to/undionly.kpxe', ifelse(option[77].exists and option[60].exists and member('KNOWN'), concat('/path/to/host/specific/boot-', hexstring(pkt4.mac,'-')), '/path/to/default')))"}]}
    world.dhcp_cfg["hooks-libraries"][0].update({"parameters": {}})
    world.dhcp_cfg["hooks-libraries"][0]["parameters"].update(h_param)
    srv_control.build_and_send_config_files('SSH', 'configfile')
    srv_control.start_srv('DHCP', 'started')

    # if option 60 not present and option 77 not present, leave option as it is
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:01')
    srv_msg.client_requests_option(67)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(67)
    srv_msg.response_check_option_content(67, 'value', 'somefilename')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:01')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_requests_option(67)
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(67)
    srv_msg.response_check_option_content(67, 'value', 'somefilename')

    # if option 60 present and option 77 not present, use /path/to/undionly.kpxe
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:02')
    srv_msg.client_does_include_with_value('vendor_class_id', 'PXE')
    srv_msg.client_requests_option(67)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.2')
    srv_msg.response_check_include_option(67)
    srv_msg.response_check_option_content(67, 'value', '/path/to/undionly.kpxe')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:02')
    srv_msg.client_does_include_with_value('vendor_class_id', 'PXE')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.2')
    srv_msg.client_requests_option(67)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.2')
    srv_msg.response_check_include_option(67)
    srv_msg.response_check_option_content(67, 'value', '/path/to/undionly.kpxe')

    # if option 60 present and option 77 present and member of 'KNOWN', use /path/to/host/specific/boot-XX-XX-XX-XX-XX-XX
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('vendor_class_id', 'PXE')
    srv_msg.client_does_include_with_value('user-class', 'iPXE')
    srv_msg.client_requests_option(67)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.110')
    srv_msg.response_check_include_option(67)
    srv_msg.response_check_option_content(67, 'value', '/path/to/host/specific/boot-ff-01-02-03-ff-04')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('vendor_class_id', 'PXE')
    srv_msg.client_does_include_with_value("user-class", 'iPXE')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.110')
    srv_msg.client_requests_option(67)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.110')
    srv_msg.response_check_include_option(67)
    srv_msg.response_check_option_content(67, 'value', '/path/to/host/specific/boot-ff-01-02-03-ff-04')

    # else (if option 60 present and option 77 present and not member of 'reservation_class'), use /path/to/default

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:05')
    srv_msg.client_does_include_with_value('vendor_class_id', 'PXE')
    srv_msg.client_does_include_with_value('user-class', 'iPXE')
    srv_msg.client_requests_option(67)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.3')
    srv_msg.response_check_include_option(67)
    srv_msg.response_check_option_content(67, 'value', '/path/to/default')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:05')
    srv_msg.client_does_include_with_value('vendor_class_id', 'PXE')
    srv_msg.client_does_include_with_value("user-class", 'iPXE')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.3')
    srv_msg.client_requests_option(67)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.3')
    srv_msg.response_check_include_option(67)
    srv_msg.response_check_option_content(67, 'value', '/path/to/default')