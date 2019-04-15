"""Complex msg exchange scenarios"""

import misc
import srv_msg

def send_discover_with_no_answer(chaddr=None, client_id=None):
    misc.test_procedure()
    if chaddr is not None:
        srv_msg.client_sets_value('Client', 'chaddr', chaddr)
    if client_id is not None:
        srv_msg.client_does_include_with_value('client_id', client_id)
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


def rebind_with_nak_answer(chaddr=None, client_id=None, ciaddr=None):
    misc.test_procedure()
    if chaddr is not None:
        srv_msg.client_sets_value('Client', 'chaddr', chaddr)
    if client_id is not None:
        srv_msg.client_does_include_with_value('client_id', client_id)
    if ciaddr is not None:
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


def send_discover_and_check_offer(
        chaddr=None, client_id=None,
        exp_yiaddr=None, exp_client_id=None,
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
    rcvd_yiaddr = msgs[0].yiaddr
    if exp_yiaddr is not None:
        assert exp_yiaddr == rcvd_yiaddr
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
    if exp_server_hostname is not None:
        srv_msg.response_check_content('Response', None, 'sname', exp_server_hostname)
    if exp_boot_file_name is not None:
        srv_msg.response_check_content('Response', None, 'file', exp_boot_file_name)

    return rcvd_yiaddr


def send_request_and_check_ack(
        chaddr=None, client_id=None, requested_addr=None, ciaddr=None, server_id=None,
        exp_lease_time=None, exp_renew_timer=None, exp_rebind_timer=None,
        exp_yiaddr=None, exp_client_id=None,
        exp_next_server=None, exp_server_hostname=None, exp_boot_file_name=None):
    # send REQUEST
    misc.test_procedure()
    if chaddr is not None:
        srv_msg.client_sets_value('Client', 'chaddr', chaddr)
    if client_id is not None:
        srv_msg.client_does_include_with_value('client_id', client_id)
    if server_id is not None:
        srv_msg.client_copy_option('server_id')
    if requested_addr is not None:
        srv_msg.client_does_include_with_value('requested_addr', requested_addr)
    if ciaddr is not None:
        srv_msg.client_sets_value('Client', 'ciaddr', ciaddr)
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('REQUEST')

    # check ACK
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    if exp_yiaddr is not None:
        exp_addr = exp_yiaddr
    elif requested_addr is not None:
        exp_addr = requested_addr
    elif ciaddr is not None:
        exp_addr = ciaddr
    else:
        exp_addr = None
    if exp_addr is not None:
        srv_msg.response_check_content('Response', None, 'yiaddr', exp_addr)
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')
    srv_msg.response_check_include_option('Response', None, '51')
    if exp_lease_time is not None:
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


def get_address(chaddr=None, client_id=None,
                exp_yiaddr=None, exp_lease_time=None, exp_renew_timer=None, exp_rebind_timer=None,
                exp_client_id=None,
                exp_next_server=None, exp_server_hostname=None, exp_boot_file_name=None):
    # send DISCOVER and check OFFER
    rcvd_yiaddr = send_discover_and_check_offer(
        chaddr=chaddr, client_id=client_id,
        exp_yiaddr=exp_yiaddr, exp_client_id=exp_client_id,
        exp_next_server=exp_next_server, exp_server_hostname=exp_server_hostname, exp_boot_file_name=exp_boot_file_name)

    # send REQUEST and check ACK
    send_request_and_check_ack(
        chaddr=chaddr, client_id=client_id, requested_addr=rcvd_yiaddr, server_id=True,
        exp_lease_time=exp_lease_time, exp_renew_timer=exp_renew_timer, exp_rebind_timer=exp_rebind_timer,
        exp_client_id=exp_client_id,
        exp_next_server=exp_next_server, exp_server_hostname=exp_server_hostname, exp_boot_file_name=exp_boot_file_name)

    return rcvd_yiaddr
