"""Complex msg exchange scenarios"""

import misc
import srv_msg
from forge_cfg import world

#########################################################################
# DHCPv4

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


def send_decline4(requested_addr):
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
        assert rcvd_yiaddr == exp_yiaddr
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


def get_address4(chaddr=None, client_id=None,
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

#########################################################################
# DHCPv6

DHCPv6_STATUS_CODES = {
    'Success': '0',
    'UnspecFail': '1',
    'NoAddrsAvail': '2',
    'NoBinding': '3',
    'NotOnLink': '4',
    'UseMulticast': '5'
}

def send_solicit_and_check_advertise(duid=None, exp_ia_na_iaaddr_addr=None, exp_ia_na_status_code=None,
                                     exp_ia_na_t1=None, exp_ia_na_t2=None):
    # send SOLICIT
    misc.test_procedure()
    srv_msg.client_requests_option('1')
    if duid is not None:
        srv_msg.client_sets_value('Client', 'DUID', duid)
    #if client_id is not None:
    #    srv_msg.client_does_include_with_value('client_id', client_id)
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    # check ADVERTISE
    msgs = srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    # srv_msg.response_check_include_option('Response', None, '1')
    # srv_msg.response_check_include_option('Response', None, '54')
    # srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    # srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    # if exp_client_id is not None:
    #     if exp_client_id == 'missing':
    #         srv_msg.response_check_include_option('Response', 'NOT ', '61')
    #     else:
    #         srv_msg.response_check_include_option('Response', None, '61')
    #         srv_msg.response_check_option_content('Response', '61', None, 'value', exp_client_id)
    # if exp_next_server is not None:
    #     srv_msg.response_check_content('Response', None, 'siaddr', exp_next_server)
    # if exp_server_hostname is not None:
    #     srv_msg.response_check_content('Response', None, 'sname', exp_server_hostname)
    # if exp_boot_file_name is not None:
    #     srv_msg.response_check_content('Response', None, 'file', exp_boot_file_name)
    srv_msg.response_check_include_option('Response', None, '3')
    if exp_ia_na_status_code is not None:
        if exp_ia_na_status_code in DHCPv6_STATUS_CODES:
            exp_ia_na_status_code = DHCPv6_STATUS_CODES[exp_ia_na_status_code]
        elif not exp_ia_na_status_code.isdigit():
            raise Exception("exp_ia_na_status_code value '%s' should be a digit or status code name" % exp_ia_na_status_code)

        srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '13')
        srv_msg.response_check_suboption_content('Response', '13', '3', None, 'statuscode', exp_ia_na_status_code)

    if exp_ia_na_iaaddr_addr is not None:
        srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
        srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', exp_ia_na_iaaddr_addr)

    if exp_ia_na_t1 is not None:
        srv_msg.response_check_option_content('Response', '3', None, 'T1', exp_ia_na_t1)

    if exp_ia_na_t2 is not None:
        srv_msg.response_check_option_content('Response', '3', None, 'T2', exp_ia_na_t2)

    #return rcvd_yiaddr
    return None


def send_request_and_check_reply(duid=None,
                                 exp_ia_na_t1=None, exp_ia_na_t2=None,
                                 exp_ia_na_iaaddr_addr=None,
                                 exp_ia_na_iaaddr_preflft=None, exp_ia_na_iaaddr_validlft=None):
    # send REQUEST
    misc.test_procedure()
    if duid is not None:
        srv_msg.client_sets_value('Client', 'DUID', duid)
    # if client_id is not None:
    #     srv_msg.client_does_include_with_value('client_id', client_id)
    # if server_id is not None:
    #     srv_msg.client_copy_option('server_id')
    # if requested_addr is not None:
    #     srv_msg.client_does_include_with_value('requested_addr', requested_addr)
    # if ciaddr is not None:
    #     srv_msg.client_sets_value('Client', 'ciaddr', ciaddr)
    # srv_msg.client_requests_option('1')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    #srv_msg.client_save_option('server-id')
    #srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', None, 'client-id')

    srv_msg.client_send_msg('REQUEST')

    # check REPLY
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    exp_addr = exp_ia_na_iaaddr_addr
    # if exp_yiaddr is not None:
    #     exp_addr = exp_yiaddr
    # elif requested_addr is not None:
    #     exp_addr = requested_addr
    # elif ciaddr is not None:
    #     exp_addr = ciaddr
    # else:
    #     exp_addr = None
    # if exp_addr is not None:
    if exp_addr is not None or exp_ia_na_iaaddr_validlft is not None or exp_ia_na_iaaddr_preflft is not None:
        srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    if exp_addr is not None:
        srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', exp_addr)
    if exp_ia_na_iaaddr_preflft is not None:
        srv_msg.response_check_suboption_content('Response', '5', '3', None, 'preflft', exp_ia_na_iaaddr_preflft)
    if exp_ia_na_iaaddr_validlft is not None:
        srv_msg.response_check_suboption_content('Response', '5', '3', None, 'validlft', exp_ia_na_iaaddr_validlft)

    # srv_msg.response_check_include_option('Response', None, '1')
    # srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    # srv_msg.response_check_include_option('Response', None, '54')
    # srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')
    # srv_msg.response_check_include_option('Response', None, '51')
    # if exp_renew_timer is not None:
    #     missing = 'NOT ' if exp_renew_timer == 'missing' else None
    #     srv_msg.response_check_include_option('Response', missing, '58')
    #     if not missing:
    #         srv_msg.response_check_option_content('Response', '58', None, 'value', exp_renew_timer)
    # if exp_rebind_timer is not None:
    #     missing = 'NOT ' if exp_rebind_timer == 'missing' else None
    #     srv_msg.response_check_include_option('Response', missing, '59')
    #     if not missing:
    #         srv_msg.response_check_option_content('Response', '59', None, 'value', exp_rebind_timer)

    if exp_ia_na_t1 is not None:
        srv_msg.response_check_option_content('Response', '3', None, 'T1', exp_ia_na_t1)

    if exp_ia_na_t2 is not None:
        srv_msg.response_check_option_content('Response', '3', None, 'T2', exp_ia_na_t2)

    # if exp_client_id is not None:
    #     if exp_client_id == 'missing':
    #         srv_msg.response_check_include_option('Response', 'NOT ', '61')
    #     else:
    #         srv_msg.response_check_include_option('Response', None, '61')
    #         srv_msg.response_check_option_content('Response', '61', None, 'value', exp_client_id)

    # if exp_next_server is not None:
    #     srv_msg.response_check_content('Response', None, 'siaddr', exp_next_server)
    # if exp_server_hostname is not None:
    #     srv_msg.response_check_content('Response', None, 'sname', exp_server_hostname)
    # if exp_boot_file_name is not None:
    #     srv_msg.response_check_content('Response', None, 'file', exp_boot_file_name)


def get_address6(duid=None,
                 exp_ia_na_t1=None, exp_ia_na_t2=None,
                 exp_ia_na_iaaddr_addr=None,
                 exp_ia_na_iaaddr_preflft=None, exp_ia_na_iaaddr_validlft=None):
    # send SOLICIT and check ADVERTISE
    rcvd_ia_na_iaaddr = send_solicit_and_check_advertise(duid=duid,
                                                         exp_ia_na_t1=exp_ia_na_t1,
                                                         exp_ia_na_t2=exp_ia_na_t2,
                                                         exp_ia_na_iaaddr_addr=exp_ia_na_iaaddr_addr)

    # send REQUEST and check REPLY
    send_request_and_check_reply(duid=duid,
                                 exp_ia_na_t1=exp_ia_na_t1,
                                 exp_ia_na_t2=exp_ia_na_t2,
                                 exp_ia_na_iaaddr_addr=exp_ia_na_iaaddr_addr,
                                 exp_ia_na_iaaddr_preflft=exp_ia_na_iaaddr_preflft,
                                 exp_ia_na_iaaddr_validlft=exp_ia_na_iaaddr_validlft)

    return rcvd_ia_na_iaaddr


def send_decline6():
    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('DECLINE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')


def get_address(**kwargs):
    new_kwargs = {}

    for k, v in kwargs.items():
        if k == 'exp_addr':
            if world.proto == 'v4':
                new_kwargs['exp_yiaddr'] = v
            else:
                new_kwargs['exp_ia_na_iaaddr_addr'] = v
        elif k == 'mac_addr':
            if world.proto == 'v4':
                new_kwargs['chaddr'] = v
            else:
                new_kwargs['duid'] = '00:03:00:01:' + v
        elif k == 'exp_renew_timer':
            if world.proto == 'v6':
                new_kwargs['exp_ia_na_t1'] = v
        elif k == 'exp_rebind_timer':
            if world.proto == 'v6':
                new_kwargs['exp_ia_na_t2'] = v
        elif k == 'exp_lease_time':
            if world.proto == 'v6':
                new_kwargs['exp_ia_na_iaaddr_validlft'] = v
        else:
            new_kwargs[k] = v

    if world.proto == 'v4':
        return get_address4(**new_kwargs)
    else:
        return get_address6(**new_kwargs)
