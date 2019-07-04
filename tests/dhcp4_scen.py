"""Complex msg exchange scenarios"""

import misc
import srv_msg
from forge_cfg import world


def _to_list(val):
    if val is not None:
        if not isinstance(val, list):
            return [val]
    return val

#########################################################################
# DHCPv4

def _send_discover(chaddr=None, client_id=None, giaddr=None, req_opts=None):
    if chaddr is not None:
        srv_msg.client_sets_value('Client', 'chaddr', chaddr)
    if client_id is not None:
        srv_msg.client_does_include_with_value('client_id', client_id)
    if giaddr is not None:
        srv_msg.network_variable('source_port', '67')
        srv_msg.network_variable('source_address', giaddr)
        srv_msg.network_variable('destination_address', '$(SRV4_ADDR)')
        srv_msg.client_sets_value('Client', 'giaddr', giaddr)
    if req_opts:
        for opt in req_opts:
            srv_msg.client_requests_option(opt)
    srv_msg.client_send_msg('DISCOVER')


def send_discover_with_no_answer(chaddr=None, client_id=None, giaddr=None):
    misc.test_procedure()
    _send_discover(chaddr=chaddr, client_id=client_id, giaddr=giaddr)
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
        chaddr=None, client_id=None, giaddr=None, req_opts=None,
        exp_yiaddr=None, exp_client_id=None,
        exp_next_server=None, exp_server_hostname=None, exp_boot_file_name=None, exp_option=None, no_exp_option=None,
        no_exp_boot_file_name=None):
    # send DISCOVER
    misc.test_procedure()
    _send_discover(chaddr=chaddr, client_id=client_id, giaddr=giaddr, req_opts=req_opts)

    # check OFFER
    msgs = srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    rcvd_yiaddr = msgs[0].yiaddr
    if exp_yiaddr is not None:
        assert rcvd_yiaddr == exp_yiaddr
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '54')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content('Response', '54', None, 'value', '$(SRV4_ADDR)')

    if exp_option:
        for opt in exp_option:
            srv_msg.response_check_option_content('Response', opt.get("code"), None, 'value', opt.get("data"))

    if no_exp_option:
        for opt in no_exp_option:
            srv_msg.response_check_include_option('Response', 'NOT ', opt.get("code"))

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
    if no_exp_boot_file_name is not None:
        srv_msg.response_check_content('Response', 'NOT ', 'file', no_exp_boot_file_name)
    return rcvd_yiaddr


def send_request_and_check_ack(
        chaddr=None, client_id=None, requested_addr=None, ciaddr=None, server_id=None, req_opts=None,
        exp_lease_time=None, exp_renew_timer=None, exp_rebind_timer=None,
        exp_yiaddr=None, exp_client_id=None,
        exp_next_server=None, exp_server_hostname=None, exp_boot_file_name=None,
        exp_option=None, no_exp_option=None, no_exp_boot_file_name=None):
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
    if req_opts:
        for opt in req_opts:
            srv_msg.client_requests_option(opt)
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

    if no_exp_boot_file_name is not None:
        srv_msg.response_check_content('Response', 'NOT ', 'file', no_exp_boot_file_name)
    if exp_next_server is not None:
        srv_msg.response_check_content('Response', None, 'siaddr', exp_next_server)
    if exp_server_hostname is not None:
        srv_msg.response_check_content('Response', None, 'sname', exp_server_hostname)
    if exp_boot_file_name is not None:
        srv_msg.response_check_content('Response', None, 'file', exp_boot_file_name)
    if exp_option:
        for opt in exp_option:
            srv_msg.response_check_option_content('Response', opt.get("code"), None, 'value', opt.get("data"))
    if no_exp_option:
        for opt in no_exp_option:
            srv_msg.response_check_include_option('Response', 'NOT ', opt.get("code"))


def get_address4(chaddr=None, client_id=None, giaddr=None, req_opts=None,
                 exp_yiaddr=None, exp_lease_time=None, exp_renew_timer=None, exp_rebind_timer=None,
                 exp_client_id=None,
                 exp_next_server=None, exp_server_hostname=None, exp_boot_file_name=None, exp_option=None,
                 no_exp_option=None, no_exp_boot_file_name=None):
    # send DISCOVER and check OFFER
    rcvd_yiaddr = send_discover_and_check_offer(
        chaddr=chaddr, client_id=client_id, giaddr=giaddr, req_opts=_to_list(req_opts),
        exp_yiaddr=exp_yiaddr, exp_client_id=exp_client_id,
        exp_next_server=exp_next_server, exp_server_hostname=exp_server_hostname, exp_boot_file_name=exp_boot_file_name,
        exp_option=_to_list(exp_option), no_exp_option=_to_list(no_exp_option),
        no_exp_boot_file_name=no_exp_boot_file_name)

    # send REQUEST and check ACK
    send_request_and_check_ack(
        chaddr=chaddr, client_id=client_id, requested_addr=rcvd_yiaddr, server_id=True, req_opts=_to_list(req_opts),
        exp_lease_time=exp_lease_time, exp_renew_timer=exp_renew_timer, exp_rebind_timer=exp_rebind_timer,
        exp_client_id=exp_client_id,
        exp_next_server=exp_next_server, exp_server_hostname=exp_server_hostname, exp_boot_file_name=exp_boot_file_name,
        exp_option=_to_list(exp_option), no_exp_option=_to_list(no_exp_option),
        no_exp_boot_file_name=no_exp_boot_file_name)

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

def _check_ia_na_options(exp_ia_na_t1,
                         exp_ia_na_t2,
                         exp_ia_na_status_code,
                         exp_ia_na_iaaddr_addr,
                         exp_ia_na_iaaddr_preflft,
                         exp_ia_na_iaaddr_validlft):
    srv_msg.response_check_include_option('Response', None, 'IA_NA')

    # check IA_NA
    if exp_ia_na_t1 is not None:
        srv_msg.response_check_option_content('Response', 'IA_NA', None, 'T1', exp_ia_na_t1)

    if exp_ia_na_t2 is not None:
        srv_msg.response_check_option_content('Response', 'IA_NA', None, 'T2', exp_ia_na_t2)

    # check IA_NA/status_code
    if exp_ia_na_status_code is not None:
        if exp_ia_na_status_code in DHCPv6_STATUS_CODES:
            exp_ia_na_status_code = DHCPv6_STATUS_CODES[exp_ia_na_status_code]
        elif not exp_ia_na_status_code.isdigit():
            raise Exception("exp_ia_na_status_code value '%s' should be a digit or status code name" % exp_ia_na_status_code)

        srv_msg.response_check_option_content('Response', 'IA_NA', None, 'sub-option', 'status-code')
        srv_msg.response_check_suboption_content('Response', 'status-code', 'IA_NA', None, 'statuscode', exp_ia_na_status_code)

    # check IA_NA/IA_address
    if exp_ia_na_iaaddr_addr is not None or exp_ia_na_iaaddr_validlft is not None or exp_ia_na_iaaddr_preflft is not None:
        srv_msg.response_check_option_content('Response', 'IA_NA', None, 'sub-option', 'IA_address')

    if exp_ia_na_iaaddr_addr is not None:
        srv_msg.response_check_suboption_content('Response', 'IA_address', 'IA_NA', None, 'addr', exp_ia_na_iaaddr_addr)
    if exp_ia_na_iaaddr_preflft is not None:
        srv_msg.response_check_suboption_content('Response', 'IA_address', 'IA_NA', None, 'preflft', exp_ia_na_iaaddr_preflft)
    if exp_ia_na_iaaddr_validlft is not None:
        srv_msg.response_check_suboption_content('Response', 'IA_address', 'IA_NA', None, 'validlft', exp_ia_na_iaaddr_validlft)


def _check_ia_pd_options(exp_ia_pd_iaprefix_prefix=None,
                         exp_ia_pd_iaprefix_plen=None):
    # IA-PD checks
    srv_msg.response_check_include_option('Response', None, 'IA_PD')

    if exp_ia_pd_iaprefix_prefix is not None:
        srv_msg.response_check_option_content('Response', 'IA_PD', None, 'sub-option', 'IA-Prefix')
        srv_msg.response_check_suboption_content('Response', 'IA-Prefix', 'IA_PD', None, 'prefix', exp_ia_pd_iaprefix_prefix)

    if exp_ia_pd_iaprefix_plen is not None:
        srv_msg.response_check_option_content('Response', 'IA_PD', None, 'sub-option', 'IA-Prefix')
        srv_msg.response_check_suboption_content('Response', 'IA-Prefix', 'IA_PD', None, 'plen', exp_ia_pd_iaprefix_plen)


def _send_and_check_response(req_ia,
                             exp_msg_type,
                             exp_ia_na_t1,
                             exp_ia_na_t2,
                             exp_ia_na_status_code,
                             exp_ia_na_iaaddr_addr,
                             exp_ia_na_iaaddr_preflft,
                             exp_ia_na_iaaddr_validlft,
                             exp_ia_pd_iaprefix_prefix,
                             exp_ia_pd_iaprefix_plen,
                             exp_rapid_commit,
                             exp_option,
                             no_exp_option):
    msgs = srv_msg.send_wait_for_message('MUST', None, exp_msg_type)

    if exp_msg_type == 'RELAYREPLY':
        srv_msg.response_check_include_option('Response', None, 'relay-msg')
        srv_msg.response_check_option_content('Response', 'relay-msg', None, 'Relayed', 'Message')

    if req_ia == 'IA-NA':
        _check_ia_na_options(exp_ia_na_t1,
                             exp_ia_na_t2,
                             exp_ia_na_status_code,
                             exp_ia_na_iaaddr_addr,
                             exp_ia_na_iaaddr_preflft,
                             exp_ia_na_iaaddr_validlft)

    if req_ia == 'IA-PD':
        _check_ia_pd_options(exp_ia_pd_iaprefix_prefix,
                             exp_ia_pd_iaprefix_plen)

    if exp_rapid_commit:
        srv_msg.response_check_include_option('Response', None, 'rapid_commit')

    if exp_option:
        for opt in exp_option:
            srv_msg.response_check_option_content('Response', opt.get("code"), None, 'value', opt.get("data"))

    if no_exp_option:
        for opt in no_exp_option:
            srv_msg.response_check_include_option('Response', 'NOT ', opt.get("code"))


def send_solicit_and_check_response(duid=None, relay_addr=None, req_ia='IA-NA', rapid_commit=False,
                                    interface_id=None,
                                    exp_ia_na_t1=None,
                                    exp_ia_na_t2=None,
                                    exp_ia_na_status_code=None,
                                    exp_ia_na_iaaddr_addr=None,
                                    exp_ia_na_iaaddr_preflft=None,
                                    exp_ia_na_iaaddr_validlft=None,
                                    exp_ia_pd_iaprefix_prefix=None,
                                    exp_ia_pd_iaprefix_plen=None,
                                    req_opts=None,
                                    exp_option=None,
                                    no_exp_option=None):
    # send SOLICIT
    misc.test_procedure()
    srv_msg.client_requests_option('1')
    if duid is not None:
        srv_msg.client_sets_value('Client', 'DUID', duid)
    #if client_id is not None:
    #    srv_msg.client_does_include_with_value('client_id', client_id)
    srv_msg.client_does_include('Client', None, 'client-id')
    if req_ia is not None:
        srv_msg.client_does_include('Client', None, req_ia)
    if req_opts is not None:
        for opt in req_opts:
            srv_msg.client_requests_option(opt)

    if rapid_commit:
        srv_msg.client_does_include('Client', None, 'rapid-commit')

    srv_msg.client_send_msg('SOLICIT')

    # add relay agent stuff
    if relay_addr is not None:
        srv_msg.client_sets_value('RelayAgent', 'linkaddr', relay_addr)

    if interface_id is not None:
        srv_msg.client_sets_value('RelayAgent', 'ifaceid', interface_id)
        srv_msg.client_does_include('RelayAgent', None, 'interface-id')

    if relay_addr is not None or interface_id is not None:
        srv_msg.create_relay_forward()

    # check response
    if relay_addr is not None or interface_id is not None:
        exp_msg_type = 'RELAYREPLY'
    elif rapid_commit:
        exp_msg_type = 'REPLY'
    else:
        exp_msg_type = 'ADVERTISE'

    _send_and_check_response(req_ia,
                             exp_msg_type,
                             exp_ia_na_t1,
                             exp_ia_na_t2,
                             exp_ia_na_status_code,
                             exp_ia_na_iaaddr_addr,
                             exp_ia_na_iaaddr_preflft,
                             exp_ia_na_iaaddr_validlft,
                             exp_ia_pd_iaprefix_prefix,
                             exp_ia_pd_iaprefix_plen,
                             rapid_commit,
                             exp_option,
                             no_exp_option)

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

    #return rcvd_yiaddr
    return None


def send_request_and_check_reply(duid=None,
                                 req_ia=None,
                                 interface_id=None,
                                 exp_ia_na_t1=None,
                                 exp_ia_na_t2=None,
                                 exp_ia_na_status_code=None,
                                 exp_ia_na_iaaddr_addr=None,
                                 exp_ia_na_iaaddr_preflft=None,
                                 exp_ia_na_iaaddr_validlft=None,
                                 exp_ia_pd_iaprefix_prefix=None,
                                 exp_ia_pd_iaprefix_plen=None,
                                 req_opts=None,
                                 exp_option=None,
                                 no_exp_option=None):
    # send REQUEST
    misc.test_procedure()
    world.sender_type = "Client"
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
    if req_ia == 'IA-NA':
        srv_msg.client_copy_option('IA_NA')
    if req_ia == 'IA-PD':
        srv_msg.client_copy_option('IA_PD')
    srv_msg.client_copy_option('server-id')
    #srv_msg.client_save_option('server-id')
    #srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', None, 'client-id')
    if req_opts is not None:
        for opt in req_opts:
            srv_msg.client_requests_option(opt)

    srv_msg.client_send_msg('REQUEST')

    if interface_id is not None:
        srv_msg.client_sets_value('RelayAgent', 'ifaceid', interface_id)
        srv_msg.client_does_include('RelayAgent', None, 'interface-id')
        srv_msg.create_relay_forward()

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

    if interface_id is not None:
        exp_msg_type = 'RELAYREPLY'
    else:
        exp_msg_type = 'REPLY'

    _send_and_check_response(req_ia,
                             exp_msg_type,
                             exp_ia_na_t1,
                             exp_ia_na_t2,
                             exp_ia_na_status_code,
                             exp_ia_na_iaaddr_addr,
                             exp_ia_na_iaaddr_preflft,
                             exp_ia_na_iaaddr_validlft,
                             exp_ia_pd_iaprefix_prefix,
                             exp_ia_pd_iaprefix_plen,
                             False,  # exp_rapid_commit=False
                             exp_option,
                             no_exp_option)


def get_address6(duid=None, relay_addr=None, req_ia='IA-NA', rapid_commit=False,
                 interface_id=None,
                 exp_ia_na_t1=None,
                 exp_ia_na_t2=None,
                 exp_ia_na_iaaddr_addr=None,
                 exp_ia_na_iaaddr_preflft=None,
                 exp_ia_na_iaaddr_validlft=None,
                 exp_ia_pd_iaprefix_prefix=None,
                 exp_ia_pd_iaprefix_plen=None,
                 req_opts=None,
                 exp_option=None,
                 no_exp_option=None):

    send_solicit_and_check_response(duid=duid,
                                    relay_addr=relay_addr,
                                    req_ia=req_ia,
                                    rapid_commit=rapid_commit,
                                    interface_id=interface_id,
                                    exp_ia_na_t1=exp_ia_na_t1,
                                    exp_ia_na_t2=exp_ia_na_t2,
                                    exp_ia_na_iaaddr_addr=exp_ia_na_iaaddr_addr,
                                    exp_ia_pd_iaprefix_prefix=exp_ia_pd_iaprefix_prefix,
                                    exp_ia_pd_iaprefix_plen=exp_ia_pd_iaprefix_plen,
                                    req_opts=_to_list(req_opts),
                                    exp_option=_to_list(exp_option),
                                    no_exp_option=_to_list(no_exp_option))

    if not rapid_commit:
        send_request_and_check_reply(duid=duid,
                                     req_ia=req_ia,
                                     interface_id=interface_id,
                                     exp_ia_na_t1=exp_ia_na_t1,
                                     exp_ia_na_t2=exp_ia_na_t2,
                                     exp_ia_na_iaaddr_addr=exp_ia_na_iaaddr_addr,
                                     exp_ia_na_iaaddr_preflft=exp_ia_na_iaaddr_preflft,
                                     exp_ia_na_iaaddr_validlft=exp_ia_na_iaaddr_validlft,
                                     exp_ia_pd_iaprefix_prefix=exp_ia_pd_iaprefix_prefix,
                                     exp_ia_pd_iaprefix_plen=exp_ia_pd_iaprefix_plen,
                                     req_opts=_to_list(req_opts),
                                     exp_option=_to_list(exp_option),
                                     no_exp_option=_to_list(no_exp_option))


def send_decline6():
    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('DECLINE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')


#########################################################################
# common functions

def _common_keys_to_specific(kwargs):
    new_kwargs = {}
    key_map = {
        'exp_addr': {'v4': 'exp_yiaddr', 'v6': 'exp_ia_na_iaaddr_addr'},
        'exp_renew_timer': {'v4': 'exp_renew_timer', 'v6': 'exp_ia_na_t1'},
        'exp_rebind_timer': {'v4': 'exp_rebind_timer', 'v6': 'exp_ia_na_t2'},
        'exp_lease_time': {'v4': 'exp_lease_time', 'v6': 'exp_ia_na_iaaddr_validlft'},
        'relay_addr': {'v4': 'giaddr', 'v6': 'relay_addr'},
    }

    for k, v in kwargs.items():
        if k in key_map:
            new_key = key_map[k][world.proto]
            new_kwargs[new_key] = v
        elif k == 'mac_addr':
            if world.proto == 'v4':
                new_kwargs['chaddr'] = v
            else:
                new_kwargs['duid'] = '00:03:00:01:' + v
        else:
            new_kwargs[k] = v

    return new_kwargs


def get_address(**kwargs):
    new_kwargs = _common_keys_to_specific(kwargs)

    if world.proto == 'v4':
        return get_address4(**new_kwargs)
    else:
        return get_address6(**new_kwargs)


def get_rejected(**kwargs):
    new_kwargs = _common_keys_to_specific(kwargs)

    if world.proto == 'v4':
        return send_discover_with_no_answer(**new_kwargs)
    else:
        if 'exp_ia_na_status_code' not in new_kwargs:
            new_kwargs['exp_ia_na_status_code'] = 'NoAddrsAvail'
        return send_solicit_and_check_response(**new_kwargs)
