"""Common functions for cb-cmds testing."""

import srv_msg
import srv_control
import misc


def setup_server_for_config_backend_cmds(echo_client_id=None, decline_probation_period=None,
                                         next_server=None, server_hostname=None, boot_file_name=None):
    misc.test_setup()
    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')

    if echo_client_id is not None:
        srv_control.set_conf_parameter_global('echo-client-id', 'true' if echo_client_id else 'false')
    if decline_probation_period is not None:
        srv_control.set_conf_parameter_global('decline-probation-period', decline_probation_period)
    if next_server is not None:
        srv_control.set_conf_parameter_global('next-server', '"%s"' % next_server)
    if server_hostname is not None:
        srv_control.set_conf_parameter_global('server-hostname', '"%s"' % server_hostname)
    if boot_file_name is not None:
        srv_control.set_conf_parameter_global('boot-file-name', '"%s"' % boot_file_name)

    srv_control.add_hooks('$(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_cb_cmds.so')
    srv_control.add_hooks('$(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_mysql_cb.so')
    srv_control.open_control_channel(
        'unix',
        '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel('$(SRV4_ADDR)',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.run_command(
        '"config-control":{"config-databases":[{"user":"$(DB_USER)",'
        '"password":"$(DB_PASSWD)","name":"$(DB_NAME)","type":"mysql"}]}')
    srv_control.run_command(',"server-tag": "abc"')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')


def send_discovery_with_no_answer():
    misc.test_procedure()
    srv_msg.client_send_msg('DISCOVER')
    srv_msg.send_wait_for_message("MUST", False, "None")


def rebind_with_ack_answer(ciaddr):
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'ciaddr', ciaddr)
    srv_msg.client_send_msg('REQUEST')

    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')
    # TODO: what else should be checked


def rebind_with_nak_answer(ciaddr):
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'ciaddr', ciaddr)
    srv_msg.client_send_msg('REQUEST')

    srv_msg.send_wait_for_message('MUST', None, 'NAK')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')


def send_decline(requested_addr):
    misc.test_procedure()
    # srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:22')
    # srv_msg.client_does_include_with_value('client_id', '00010203040122')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'ciaddr', '0.0.0.0')
    srv_msg.client_does_include_with_value('requested_addr', requested_addr)
    srv_msg.client_send_msg('DECLINE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()


def _compare_subnets(received_subnets, exp_subnet):
    found = False
    for sn in received_subnets:
        if sn['subnet'] == exp_subnet['subnet']:
            found = True
            for f in ['valid-lifetime', 'renew_timer', 'renew_timer']:
                if f in exp_subnet:
                    assert f in sn
                    assert sn[f] == exp_subnet[f]
            break
    assert found, 'Cannot find subnet with prefix %s' % exp_subnet['subnet']


def set_subnet(**kwargs):
    # prepare command
    subnet = {
        "subnet": "192.168.50.0/24",
        "interface": "$(SERVER_IFACE)",
        "pools": [{"pool": kwargs['pool'] if 'pool' in kwargs else "192.168.50.1-192.168.50.100"}]}

    for param, val in kwargs.items():
        subnet[param.replace('_', '-')] = val

    cmd = {"command": "remote-subnet4-set",
           "arguments": {"remote": {"type": "mysql"},
                         "server-tags": ["abc"],
                         "subnets": [subnet]}}

    # send command
    response = srv_msg.send_request('v4', cmd)
    assert response["result"] == 0

    # request config reloading
    # srv_control.start_srv('DHCP', 'restarted')
    cmd = {"command": "config-reload", "arguments": {}}
    response = srv_msg.send_request('v4', cmd)
    assert response == {'result': 0, 'text': 'Configuration successful.'}

    # check config seen by server
    cmd = {"command": "config-get", "arguments": {}}
    response = srv_msg.send_request('v4', cmd)
    _compare_subnets(response['arguments']['Dhcp4']['subnet4'], subnet)


def del_subnet(op_kind='by-prefix'):
    # prepare command
    if op_kind == 'by-id':
        cmd = {"command": "remote-subnet4-del-by-id",
               "arguments": {"remote": {"type": "mysql"},
                             "server-tags": ["all"],
                             "subnets": [{"id": 1}]}}
    else:
        cmd = {"command": "remote-subnet4-del-by-prefix",
               "arguments": {"remote": {"type": "mysql"},
                             "server-tags": ["all"],
                             "subnets": [{"subnet": "192.168.50.0/24"}]}}

    # send command
    response = srv_msg.send_request('v4', cmd)
    assert response["result"] == 0

    # request config reloading
    # srv_control.start_srv('DHCP', 'restarted')
    cmd = {"command": "config-reload", "arguments": {}}
    response = srv_msg.send_request('v4', cmd)
    assert response == {'result': 0, 'text': 'Configuration successful.'}

    # check config seen by server
    cmd = {"command": "config-get", "arguments": {}}
    response = srv_msg.send_request('v4', cmd)
    for sn in response['arguments']['Dhcp4']['subnet4']:
        assert sn['subnet'] != "192.168.50.0/24"


def set_network(**kwargs):
    # prepare command
    network = {
        "name": "floor13",
        "interface": "$(SERVER_IFACE)",
        "subnet4": [{
            "subnet": "192.168.50.0/24",
            "pools": [{"pool": "192.168.50.1-192.168.50.100"}]}]}

    for param, val in kwargs.items():
        level, param = param.split('_', 1)
        param = param.replace('_', '-')
        if level == 'network':
            network[param] = val
        else:
            network['subnet4'][0][param] = val

    cmd = {"command": "remote-network4-set",
           "arguments": {"remote": {"type": "mysql"},
                         "server-tags": ["abc"],
                         "shared-networks": [network]}}

    # send command
    response = srv_msg.send_request('v4', cmd)
    assert response["result"] == 0

    # request config reloading
    # srv_control.start_srv('DHCP', 'restarted')
    cmd = {"command": "config-reload", "arguments": {}}
    response = srv_msg.send_request('v4', cmd)
    assert response == {'result': 0, 'text': 'Configuration successful.'}

    # check config seen by server
    cmd = {"command": "config-get", "arguments": {}}
    response = srv_msg.send_request('v4', cmd)
    found = False
    for n in response['arguments']['Dhcp4']['shared-networks']:
        if n['name'] == network['name']:
            found = True
            for f in []:  # TODO: add fields to check
                if f in network:
                    assert f in n
                    assert n[f] == network[f]
            for subnet in network['subnet4']:
                _compare_subnets(n['subnet4'], subnet)
            break
    assert found, 'Cannot find shared network with name %s' % network['name']


def set_global_parameter(**kwargs):
    # prepare command
    parameters = []
    for param, val in kwargs.items():
        parameters.append({'name': param.replace('_', '-'), 'value': val})

    # TODO: later should be possible to set list of params in one shot
    for param in parameters:
        cmd = {"command": "remote-global-parameter4-set",
               "arguments": {"remote": {"type": "mysql"},
                             "server-tags": ["abc"],
                             "parameters": [param]}}

        response = srv_msg.send_request('v4', cmd)
        assert response["result"] == 0

    # request config reloading
    # srv_control.start_srv('DHCP', 'restarted')
    cmd = {"command": "config-reload", "arguments": {}}
    response = srv_msg.send_request('v4', cmd)
    assert response == {'result': 0, 'text': 'Configuration successful.'}

    # check config seen by server
    cmd = {"command": "config-get", "arguments": {}}
    response = srv_msg.send_request('v4', cmd)
    dhcp4_cfg = response['arguments']['Dhcp4']
    for param in parameters:
        assert param['name'] in dhcp4_cfg
        assert dhcp4_cfg[param['name']] == param['value']


def get_address(chaddr=None, client_id=None,
                exp_yiaddr=None, exp_lease_time=7200, exp_renew_timer=None, exp_rebind_timer=None,
                exp_client_id=None,
                exp_next_server=None, exp_server_hostname=None, exp_boot_file_name=None):
    # send DISCOVER
    misc.test_procedure()
    srv_msg.client_requests_option('1')
    if chaddr is not None:
        srv_msg.client_sets_value('Client', 'chaddr', chaddr)
    if client_id is not None:
        srv_msg.client_does_include_with_value('client_id', client_id)
    srv_msg.client_send_msg('DISCOVER')

    # check OFFER
    msgs = srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    if exp_yiaddr is not None:
        assert exp_yiaddr in msgs[0].yiaddr
    rcvd_yiaddr = msgs[0].yiaddr
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    if exp_client_id is not None:
        if exp_client_id == 'missing':
            srv_msg.response_check_include_option('Response', 'NOT ', '61')
        else:
            srv_msg.response_check_include_option('Response', None, '61')
            srv_msg.response_check_option_content('Response', '61', None, 'value', exp_client_id)
    if exp_next_server is not None:
        srv_msg.response_check_content('Response', None, 'siaddr', exp_next_server)

    # send REQUEST
    misc.test_procedure()
    if client_id is not None:
        srv_msg.client_does_include_with_value('client_id', client_id)
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', rcvd_yiaddr)
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    # check ACK
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', rcvd_yiaddr)
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_include_option('Response', None, '51')
    srv_msg.response_check_option_content('Response', '51', None, 'value', exp_lease_time)
    if exp_renew_timer is not None:
        missing = 'NOT ' if exp_renew_timer == 'missing' else None
        srv_msg.response_check_include_option('Response', missing, '58')
        if not missing:
            srv_msg.response_check_option_content('Response', '58', None, 'value', exp_renew_timer)
    if exp_rebind_timer is not None:
        missing = 'NOT ' if exp_rebind_timer == 'missing' else None
        srv_msg.response_check_include_option('Response', missing, '59')
        if not missing:
            srv_msg.response_check_option_content('Response', '59', None, 'value', exp_rebind_timer)
    if exp_client_id is not None:
        if exp_client_id == 'missing':
            srv_msg.response_check_include_option('Response', 'NOT ', '61')
        else:
            srv_msg.response_check_include_option('Response', None, '61')
            srv_msg.response_check_option_content('Response', '61', None, 'value', exp_client_id)

    if exp_next_server is not None:
        srv_msg.response_check_content('Response', None, 'siaddr', exp_next_server)
    if exp_server_hostname is not None:
        srv_msg.response_check_content('Response', None, 'sname', exp_server_hostname)
    if exp_boot_file_name is not None:
        srv_msg.response_check_content('Response', None, 'file', exp_boot_file_name)

    return rcvd_yiaddr
