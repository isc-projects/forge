# Copyright (C) 2013-2023 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Wlodzimierz Wencel

# pylint: disable=consider-using-f-string
# pylint: disable=empty-docstring
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=redefined-builtin
# pylint: disable=self-assigning-variable
# pylint: disable=simplifiable-if-expression
# pylint: disable=unbalanced-tuple-unpacking
# pylint: disable=unknown-option-value
# pylint: disable=unused-argument
# pylint: disable=useless-object-inheritance

import random
import json
import importlib
import ipaddress
import logging

from scapy.layers.dhcp6 import DUID_LLT, DUID_LL, DUID_EN
from .protosupport.dhcp4_scen import DHCPv6_STATUS_CODES
from .forge_cfg import world, step
from .protosupport import dns, multi_protocol_functions
from .protosupport.multi_protocol_functions import test_define_value, substitute_vars
from .softwaresupport.multi_server_functions import start_tcpdump, stop_tcpdump, download_tcpdump_capture

log = logging.getLogger('forge')


class Dispatcher(object):
    def __getattr__(self, attr_name):
        mod = importlib.import_module("src.protosupport.%s.srv_msg" % world.f_cfg.proto)
        return getattr(mod, attr_name)


dhcpmsg = Dispatcher()


# config values return
def get_interface():
    return world.f_cfg.iface


def get_proto_version():
    return world.f_cfg.proto


def get_server_interface():
    return world.f_cfg.server_iface


def get_server_path():
    return world.f_cfg.software_install_path


# building DHCP messages
@step(r'Client requests option (\d+).')
def client_requests_option(opt_type):
    """
    Add Option: Request Option with requested option code
    """
    dhcpmsg.client_requests_option(opt_type)


@step(r'(Client|RelayAgent) sets (\w+) value to (\S+).')
def client_sets_value(sender_type, value_name, new_value):
    """
    User can set values like: address, T1 or DUID to make test scenario
    more accurate.
    """
    # that is also used for DNS messages and RelayForward message but sender_type was
    # introduced just to keep tests cleaner - it's unused in the code.
    # if we pass DUID class do not check defined values
    if not isinstance(new_value, (DUID_LLT, DUID_LL, DUID_EN)):
        value_name, new_value = test_define_value(value_name, new_value)
    dhcpmsg.client_sets_value(value_name, new_value)


@step(r'Through (\S+) interface to address (\S+) client sends (\w+) message.')
def client_send_msg_via_interface(iface, addr, msgname):
    r"""
    This step actually build message (e.g. SOLICIT) with all details
    specified in steps like:
    Client sets (\w+) value to (\S+).
    Client does include (\S+).
    and others..
    Message builded here will be send in step: Server must response with...
    """
    msgname, iface, addr = test_define_value(msgname, iface, addr)
    dhcpmsg.client_send_msg(msgname, iface, addr)


@step(r'Client sends (\w+) message.')
def client_send_msg(msgname):
    r"""
    This step actually build message (e.g. SOLICIT) with all details
    specified in steps like:
    Client sets (\w+) value to (\S+).
    Client does include (\S+).
    and others..
    Message builded here will be send in step: Server must response with...
    Message will be send via interface set in init_all.py marked as IFACE.
    """
    dhcpmsg.client_send_msg(msgname, None, None)


@step(r'Send (\S+) with raw appending (.+)')
def send_raw_message(msg_type="", raw_append=None):
    dhcpmsg.build_raw(msg=msg_type, append=raw_append)


@step(r'Client adds to the message (\S+) with value (\S+).')
def client_does_include_with_value(opt_type, value):
    """
    You can choose to include options to message with proposed value. Mostly used only with
    DHCPv4. Also reason why that step is called "Client adds to message" not
    "Client does (NOT )?include" as other step is that lettuce step parser is really... weak.
    What ever I'll do with that always takes wrong step.
    """
    opt_type, value = test_define_value(opt_type, value)
    dhcpmsg.client_does_include(None, opt_type, value)


@step(r'(\S+) does (NOT )?include (\S+).')
def client_does_include(sender_type, opt_type, value=None):
    # add " option." to the end of the step - change all tests!
    """
    You can choose to include options to message (support for every option listed
    in RFC 3315 and more) or to not include options like IA_NA or client_id.
    """
    dhcpmsg.client_does_include(str(sender_type), opt_type, None)


def add_scapy_option(option, where='client'):
    """
    Add option to next message. Forge does cleaver things to world.cliopts so double check if
    that function is actually doing in your test what you expect it does.
    :param option: scapy option, can be just tuple for v4 or scapy.layers.dhcp6 option class
    :param where: decide where option should be added
    """
    if where == 'client':
        world.cliopts.append(option)
    elif where == 'relay':
        world.relayopts.append(option)
    elif where == 'rsso':
        world.rsoo.append(option)
    elif where == 'vendor':
        world.vendor.append(option)
    elif where == 'iaad':
        world.iaad.append(option)
    elif where == 'iapd':
        world.iapd.append(option)
    elif where == 'subopts':
        world.subopts.append(option)
    else:
        assert False, f"where value {where} is not allowed"


@step(r'Relay-agent does include (\S+).')
def relay_agent_does_include(opt_type):
    # add " option." to the end of the step - change all tests!
    """
    """
    # dhcpmsg.relay_agent_does_include(opt_type)


@step(r'Client chooses (GLOBAL)|(LINK_LOCAL) UNICAST address.')
def unicast_address(addr_type, addr_type2):
    """
    Message can be send on 3 different addresses:
    - multicast for DHCPv6
    - unicast global address of the server
    - unicast local address of the server
    Proper configuration in init_all.py required.
    """
    # send true when GLOBAL and False when LINK_LOCAL
    dhcpmsg.unicast_address(True if addr_type else False)


@step(r'Generate new (\S+).')
def generate_new(opt):
    """
    For some test scenarios there is a need for multiple different users, in this step you can
    choose which value needs to be changed:
    for client_id and IA: client
    for client_id only: Client_ID
    for IA: IA
    for IA_PD: IA_PD
    """
    dhcpmsg.generate_new(opt)


@step(r'RelayAgent forwards message encapsulated in (\d+) level(s)?.')
def create_relay_forward(level=1):
    """
    This step is strictly related to step: Client sends message.
    You can put only after that step. They can be seperated with other steps
    which causes to change values/include options

    This step causes to encapsulate builded message in RELAY FORWARD.
    It makes possible testing RELAY-REPLY messages.
    """
    dhcpmsg.create_relay_forward(level)


@step(r'(Client|RelayAgent) adds suboption for vendor specific information with code: (\d+) and data: (\S+).')
def add_vendor_suboption(sender_type, code, data):
    """
    After adding Vendor Specific Option we can decide to add suboptions to it. Please make sure which are
    supported and if it's necessary add suboption by yourself.
    """
    dhcpmsg.add_vendor_suboption(int(code), data)


@step(r'Before sending a message set filed named (\S+) to (\S+) as type (\S+).')
def change_message_filed(message_filed, value, value_type):
    message_filed, value, value_type = test_define_value(message_filed, value, value_type)
    dhcpmsg.change_message_field(message_filed, value, value_type)


# checking DHCP respond
@step(r'Server MUST NOT respond.')
def send_dont_wait_for_message():
    """
    This step causes to send message in cases when we don't expect any response.
    Step used only for v4 testing
    """
    dhcpmsg.send_wait_for_message("MUST", False, None)


@step(r'Server (\S+) (NOT )?respond with (\w+) message.')
def send_wait_for_message(requirement_level: str, message: str, expect_response: bool = True,
                          protocol: str = 'UDP', address: str = None, port: int = None):
    """
    Send messages to server either TCP or UDP, check if response is received.
    :param requirement_level: not used. RFC-grade requirement level e.g. 'MAY', 'MUST'
    :param message: name of message that should be received from a server (if we expect multiple messages,
                     than this is name of the first message)
    :param expect_response: condition if message is expected or not
    :param protocol: choose protocol, for now it's UDP for DHCP messages and TCP for bulk lease query
    :param address: destination address for TCP connection
    :param port: destination port for TCP connection
    :return: list of replies from server
    """
    return dhcpmsg.send_wait_for_message(requirement_level, expect_response, message, protocol, address=address, port=port)


@step(r'(Response|Relayed Message) MUST (NOT )?include option (\d+).')
def response_check_include_option(opt_code, expect_include=True):
    """
    Use this step for parsing respond. For more details please read manual section "Parsing respond"
    """
    return dhcpmsg.response_check_include_option(expect_include, opt_code)


@step(r'(Response|Relayed Message) MUST (NOT )?contain (\S+) (\S+).')
def response_check_content(data_type, value, expected=True):
    """
    """
    # expect, data_type, expected = test_define_value(expect, data_type, expected)
    dhcpmsg.response_check_content(expected, data_type, value)


@step(r'(Response|Relayed Message) option (\d+) MUST (NOT )?contain (\S+) (\S+).')
def response_check_option_content(opt_code, data_type, expected_value, expect_include=True):
    """
    Detailed parsing of received option. For more details please read manual section "Parsing respond"
    """
    data_type, expected_value = test_define_value(data_type, expected_value)
    if data_type == "sub-option":
        return dhcpmsg.response_check_include_suboption(opt_code, expect_include, expected_value)
    return dhcpmsg.response_check_option_content(opt_code, expect_include, data_type, expected_value)


def response_check_option_content_more(opt_code, data_type, expected_value):
    """
    Check subsequent options. Only to be called after the first option was checked with response_check_option_content.
    """
    data_type, expected_value = test_define_value(data_type, expected_value)
    return dhcpmsg.response_check_option_content_more(opt_code, data_type, expected_value)


@step(r'(Response|Relayed Message) sub-option (\d+) from option (\d+) MUST (NOT )?contain (\S+) (\S+).')
def response_check_suboption_content(subopt_code, opt_code, data_type, value, expect_include=True):
    """
    Some options can include suboptions, we can test them too.
    For more details please read manual section "Parsing respond"
    """
    dhcpmsg.response_check_suboption_content(subopt_code, opt_code, expect_include, data_type, value)


def get_suboption(opt_code, subopt_code):
    return dhcpmsg.get_suboption(opt_code, subopt_code)


# building DNS messages
@step(r'Client for DNS Question Record uses address: (\S+) type (\S+) class (\S+).')
def dns_question_record(addr, qtype, qclass):
    dns.dns_question_record(str(addr), qtype, qclass)


@step(r'Client sends DNS query.')
def client_send_dns_query(dns_addr=None, dns_port=None):
    dns.prepare_query(dns_addr=dns_addr, dns_port=dns_port)


# checking DNS respond
@step(r'DNS server (\S+) (NOT )?respond with DNS query.')
def send_wait_for_query(type, expect_include=True, iface=None):
    """
    This step causes to send message to server and capture respond.
    """
    dns.send_wait_for_query(type, expect_include, iface=iface)


@step(r'Received DNS query MUST (NOT )?contain (\S+) with value (\S+).')
def dns_check(expect, data_type, expected_data_value):
    dns.check_dns_respond(expect, str(data_type), expected_data_value)
    # later probably we'll have to change MUST on (\S+) for sth like MAY


@step(r'Received DNS query MUST include (NOT )?empty (QUESTION|ANSWER|AUTHORITATIVE_NAMESERVERS|ADDITIONAL_RECORDS) part.')
def dns_option(part_name, expect_include=True):
    dns.check_dns_option(expect_include, str(part_name))
    # later probably we'll have to change MUST on (\S+) for sth like MAY


@step(r'Received DNS part (QUESTION|ANSWER|AUTHORITATIVE_NAMESERVERS|ADDITIONAL_RECORDS) MUST (NOT )?contain (\S+) with value (\S+).')
def dns_option_content(part_name, value_name, value, expect_include=True):
    dns.dns_option_content(part_name, expect_include, str(value_name), str(value))
    # later probably we'll have to change MUST on (\S+) for sth like MAY


# save option from received message
@step(r'Client copies (\S+) option from received message.')
def client_copy_option(option_name, copy_all=False):
    """
    When we need to send the same option back to server (e.g. Server ID) we can use this step.
    Copied option is automatically added to next generated message, and erased.
    """
    assert len(world.srvmsg), "No messages received, nothing to copy."
    dhcpmsg.client_copy_option(option_name, copy_all)


def clean_saved_options():
    """
    Clean all previously saved options
    """
    world.savedmsg = {}


@step(r'Client saves (\S+) option from received message.')
def client_save_option(option_name):
    """
    In time we need to include one option more then one time in different messages, we can
    choose to save it in memory. Memory will be erased at the end of the test, or when we
    decide to clear it in step "Client adds saved options. And erase.
    """
    assert len(world.srvmsg), "No messages received, nothing to save."
    dhcpmsg.client_save_option(option_name)


@step(r'Client saves into set no. (\d+) (\S+) option from received message.')
def client_save_option_count(count, option_name):
    """
    """
    assert len(world.srvmsg), "No messages received, nothing to save."
    dhcpmsg.client_save_option(option_name, count)


@step(r'Client adds saved options. And (DONT )?Erase.')
def client_add_saved_option(erase=False):
    """
    This step causes to include saved options to message. Also we can decide to keep or clear
    memory.
    """
    assert len(world.savedmsg), "No options to add."
    dhcpmsg.client_add_saved_option(erase)


@step(r'Client adds saved options in set no. (\d+). And (DONT )?Erase.')
def client_add_saved_option_count(count, erase=False):
    """
    """
    assert len(world.savedmsg), "No options to add."
    dhcpmsg.client_add_saved_option(erase, count)


@step(r'Save (\S+) value from (\d+) option.')
def save_value_from_option(value_name, option_name):
    """
    This step can be used to save value of some option field for
    further usage. It's like client_save_option but only for
    one specific field of given option.
    """
    dhcpmsg.save_value_from_option(value_name, option_name)


@step(r'Received (\S+) value in option (\d+) is the same as saved value.')
def compare_values(value_name, option_name):
    """
    If you have used step save_value_from_option, then this step will
    compare the earlier saved value with the recent received value.
    Note that names of fields that values are being compared should
    be the same.
    """
    dhcpmsg.compare_values(value_name, option_name)


# other
@step(r'Set network variable (\S+) with value (\S+).')
def network_variable(value_name, value):
    value_name, value = test_define_value(value_name, value)
    multi_protocol_functions.change_network_variables(value_name, value)


@step(r'Table (\S+) in (\S+) database MUST (NOT )?contain line or phrase: (.+)')
def table_contains_line(table_name, db_type, line, expect=True):
    """
    Check if in table X in database type Y include line.
    Be aware that tested line is every thing after "line: " until end of the line.
    """
    table_name, db_type, line = test_define_value(table_name, db_type, line)
    multi_protocol_functions.db_table_contains_line(table_name, db_type, line=line, expect=expect)


def table_contains_line_n_times(table_name, db_type, n, line, destination=world.f_cfg.mgmt_address):
    """
    Check if in table X in database type Y include line.
    Be aware that tested line is every thing after "line: " until end of the line.
    """
    table_name, db_type, line = test_define_value(table_name, db_type, line)
    multi_protocol_functions.db_table_contains_line_n_times(table_name, db_type, n=n, line=line, destination=destination)


@step(r'Remove all records from table (\S+) in (\S+) database.')
def remove_from_db_table(table_name, db_type, destination=world.f_cfg.mgmt_address):
    table_name, db_type = test_define_value(table_name, db_type)
    multi_protocol_functions.remove_from_db_table(table_name, db_type, destination=destination)


@step(r'Sleep for (\S+) (seconds|second|milliseconds|millisecond).')
def forge_sleep(time_val, time_units='seconds'):
    """
    Pause the test for selected amount of time counted in seconds or milliseconds.
    """
    time_val, time_units = test_define_value(time_val, time_units)
    print("Sleep for %s %s" % (time_val, time_units))
    multi_protocol_functions.forge_sleep(int(time_val), str(time_units))


@step(r'Pause the Test.')
def test_pause():
    """
    Pause the test for any reason. Very good to debug problems. Checking server configuration
    and so on.... Do NOT put it in automatic tests, it blocks test until user will:
        Press any key to continue.
    """
    multi_protocol_functions.test_pause()


@step(r'End test.')
def test_stop():
    assert False, "Test ended."


@step(r'Fail test.')
def test_fail():
    assert False, "Test failed on purpose."


@step(r'Client download file from server stored in: (\S+).')
def copy_remote(remote_path, local_filename='downloaded_file', dest=world.f_cfg.mgmt_address):
    """
    Download file from remote server. It is stored in test directory.
    And named "downloaded_file"
    """
    remote_path = test_define_value(remote_path)[0]
    multi_protocol_functions.copy_file_from_server(remote_path, local_filename, dest=dest)


@step(r'Client compares downloaded file from server with local file stored in: (\S+).')
def compare_file(remote_path):
    """
    Compare two files, our local and "downloaded_file".
    """
    remote_path = test_define_value(remote_path)[0]
    multi_protocol_functions.compare_file(remote_path)


@step(r'Client sends local file stored in: (\S+) to server, to location: (\S+).')
def send_file_to_server(local_path, remote_path):
    """
    If you need send some file to server, use that step.
    """
    local_path, remote_path = test_define_value(local_path, remote_path)
    multi_protocol_functions.send_file_to_server(local_path, remote_path)


@step(r'Client removes file from server located in: (\S+).')
def remove_file_from_server(remote_path, dest=world.f_cfg.mgmt_address):
    """
    If you need to remove file from a server, please do so.
    """
    remote_path = test_define_value(remote_path)[0]
    multi_protocol_functions.remove_file_from_server(remote_path, dest=dest)


@step(r'Add environment variable named (\S+) to value (.+)')
def set_env(env_name, env_value):
    multi_protocol_functions.set_value(env_name, env_value)


@step(r'User define temporary variable: (\S+) with value (.+)')
def add_variable_temporary(variable_name, variable_val):
    """
    User can define his own variable, that can be called from any place in test scenario,
    by $(variable_name). Allowed signs in variable name are: capitalized letters and '_'.

    Temporary variable will be stored in world.define and cleared at the end of scenario.
    """
    multi_protocol_functions.add_variable(variable_name, variable_val, 0)


@step(r'User define permanent variable: (\S+) with value (\S+).')
def add_variable_permanent(variable_name, variable_val):
    """
    User can define his own variable, that can be called from any place in test scenario,
    by $(variable_name). Allowed signs in variable name are: capitalized letters and '_'.

    Permanent variable will be placed at the end of the init_all.py file. It won't be removed.
    User can do so by removing it from file.
    """
    multi_protocol_functions.add_variable(variable_name, variable_val, 1)


@step(r'Let us celebrate this SUCCESS!')
def test_victory():
    """
    Use your imagination.
    """
    multi_protocol_functions.user_victory()


@step(r'Execute command (\S+) with arguments: (.+)')
def execute_shell_cmd(path, dest=world.f_cfg.mgmt_address, save_results=True):
    path = test_define_value(path)[0]
    result = multi_protocol_functions.execute_shell_cmd(path, dest=dest, save_results=save_results)
    assert result.succeeded
    return result


@step(r'Execute command (\S+) with arguments: (.+)')
def execute_kea_shell(args, exp_result=0, exp_failed=False):
    args = test_define_value(args)[0]
    path = world.f_cfg.sbin_join('kea-shell')
    result = multi_protocol_functions.execute_shell_cmd(path + ' ' + args, exp_failed=exp_failed)
    result = json.loads(result)
    assert result[0]['result'] == exp_result
    return result


@step(r'Check socket connectivity on address (\S+) and port (\S+).')
def check_socket(socket_address, socket_port):
    pass


@step(r'Check socket connectivity on server in path (\S+).')
def check_socket_server_site(socket_path):
    pass


@step(r'Send ctrl cmd (.+) using UNIX socket (\S+) to server (.+).')
def send_ctrl_cmd_via_socket(command, socket_name=None, destination_address=world.f_cfg.mgmt_address,
                             exp_result=0, exp_failed=False):
    if isinstance(command, dict):
        substitute_vars(command)
        destination_address = test_define_value(destination_address)[0]
    else:
        destination_address, command = test_define_value(destination_address, command)
    return multi_protocol_functions.send_ctrl_cmd_via_socket(command, socket_name, destination_address,
                                                             exp_result, exp_failed)


@step(r'Send ctrl cmd (.+) using HTTP (\S+):(\S+) connection.')
def send_ctrl_cmd_via_http(command, address='$(MGMT_ADDRESS)', port=8000, exp_result=0, exp_failed=False, https=False, verify=None, cert=None,
                           headers=None):
    if isinstance(command, dict):
        substitute_vars(command)
        address, port = test_define_value(address, port)
    else:
        address, port, command = test_define_value(address, port, command)
    return multi_protocol_functions.send_ctrl_cmd_via_http(command, address, int(port), exp_result, exp_failed, https, verify, cert, headers)


def send_ctrl_cmd(cmd, channel='http', service=None, exp_result=0, exp_failed=False, address=world.f_cfg.mgmt_address, verify=None, cert=None,
                  headers=None, port=8000):
    """Send request to DHCP Kea server over Unix socket or over HTTP via CA."""

    if channel in ['http', 'https']:
        if service != 'agent':
            if world.proto == 'v4':
                cmd["service"] = ['dhcp4']
            else:
                cmd["service"] = ['dhcp6']

    if channel == 'http':
        response = send_ctrl_cmd_via_http(cmd, address, port, exp_result=exp_result, exp_failed=exp_failed, headers=headers)
        if isinstance(response, dict):
            response = response
        else:
            response = response[0] if response else response
    elif channel == 'https':
        response = send_ctrl_cmd_via_http(cmd, address, port, exp_result=exp_result, exp_failed=exp_failed, https=True,
                                          verify=verify, cert=cert, headers=headers)
        # in https connection to control agent results is returned via dict not list as everywhere else,
        # so there is small trick for temp testing
        if isinstance(response, dict):
            response = response
        else:
            response = response[0] if response else response
    elif channel == 'socket':
        response = send_ctrl_cmd_via_socket(cmd, destination_address=address, exp_result=exp_result, exp_failed=exp_failed)
    else:
        raise ValueError('unsupported channel type: %s' % str(channel))
    return response


@step(r'Loops config: Save leases details.')
def loops_config_sld():
    dhcpmsg.loops_config_sld()


@step(r'Loops config: choose (\S+) from (file )?(.+)')
def values_for_loops(value_name, file_flag, values):
    dhcpmsg.values_for_loops(value_name, file_flag, values)


@step(r'Exchange messages (\S+) - (\S+) (\d+) times.')
def loops(message_type_1, message_type_2, repeat):
    tmp = world.f_cfg.show_packets_from
    world.f_cfg.show_packets_from = ""
    dhcpmsg.loops(message_type_1, message_type_2, repeat)
    world.f_cfg.show_packets_from = tmp


def get_all_leases():
    return dhcpmsg.get_all_leases()


def check_leases(leases_list, backend='memfile', dest=world.f_cfg.mgmt_address, should_succeed=True):
    dest = test_define_value(dest)[0]
    multi_protocol_functions.check_leases(leases_list, backend=backend, destination=dest, should_succeed=should_succeed)


def lease_dump(backend, db_name=world.f_cfg.db_name, db_user=world.f_cfg.db_user,
               db_passwd=world.f_cfg.db_passwd, destination_address=world.f_cfg.mgmt_address,
               out="/tmp/lease_dump.csv"):
    return multi_protocol_functions.lease_dump(backend, db_name, db_user, db_passwd,
                                               destination_address, out)


def lease_upload(backend, leases_file, db_name=world.f_cfg.db_name, db_user=world.f_cfg.db_user,
                 db_passwd=world.f_cfg.db_passwd, destination_address=world.f_cfg.mgmt_address):
    return multi_protocol_functions.lease_upload(backend, leases_file, db_name, db_user, db_passwd,
                                                 destination_address)


def get_option(msg, opt_code):
    return dhcpmsg.get_option(msg, opt_code)


def get_subopt_from_option(exp_opt_code, exp_subopt_code):
    return dhcpmsg.get_subopt_from_option(exp_opt_code, exp_subopt_code)


def DO(address=None, options=None, chaddr='ff:01:02:03:ff:04'):
    return dhcpmsg.DO(address, options, chaddr)


def RA(address, options=None, response_type='ACK', chaddr='ff:01:02:03:ff:04',
       init_reboot=False, subnet_mask='255.255.255.0', fqdn=None):
    return dhcpmsg.RA(address, options, response_type, chaddr, init_reboot, subnet_mask, fqdn)


def DORA(address=None, options=None, exchange='full', response_type='ACK', chaddr='ff:01:02:03:ff:04',
         init_reboot=False, subnet_mask='255.255.255.0', fqdn=None):
    return dhcpmsg.DORA(address, options, exchange, response_type, chaddr, init_reboot, subnet_mask, fqdn)


def check_IA_NA(address, status_code=DHCPv6_STATUS_CODES['Success'], expect=True):
    return dhcpmsg.check_IA_NA(address, status_code, expect)


def check_IA_PD(prefix, prefix_length=None, status_code=DHCPv6_STATUS_CODES['Success'], expect=True):
    return dhcpmsg.check_IA_PD(prefix, prefix_length, status_code, expect)


def SA(address=None, delegated_prefix=None, relay_information=False,
       status_code=DHCPv6_STATUS_CODES['Success'], duid='00:03:00:01:f6:f5:f4:f3:f2:01', iaid=None,
       linkaddr='2001:db8:1::1000', ifaceid='port1234'):
    return dhcpmsg.SA(address, delegated_prefix, relay_information, status_code, duid, iaid,
                      linkaddr, ifaceid)


def SARR(address=None, delegated_prefix=None, relay_information=False,
         status_code=DHCPv6_STATUS_CODES['Success'], exchange='full',
         duid='00:03:00:01:f6:f5:f4:f3:f2:01', iaid=None,
         linkaddr='2001:db8:1::1000', ifaceid='port1234'):
    return dhcpmsg.SARR(address, delegated_prefix, relay_information,
                        status_code, exchange, duid, iaid, linkaddr, ifaceid)


def BOOTP_REQUEST_and_BOOTP_REPLY(address: str,
                                  chaddr: str = 'ff:01:02:03:ff:04',
                                  client_id: str = None):
    return dhcpmsg.BOOTP_REQUEST_and_BOOTP_REPLY(address=address,
                                                 chaddr=chaddr,
                                                 client_id=client_id)


def get_address_facing_remote_address(addr: str = world.f_cfg.mgmt_address):
    """
    Get address of an interface that is facing other address in forge setup
    :param addr: ip address of remote system
    :return: string, local ip address
    """
    addr = test_define_value(addr)[0]
    return multi_protocol_functions.get_address_of_local_vm(addr)


def start_fuzzing():
    """
    Initialize any variables that may be used in fuzz tests.
    """
    world.fuzzing = True
    seed = random.randint(0, 100)
    print(f'Using seed {seed}.')
    random.seed(seed)
    world.coin_toss = random.randint(1, 100) % 2 == 0


def enable_tcpdump(file_name: str = "my_capture.pcap", iface: str = None,
                   port_filter: str = None, location: str = 'local'):
    """
    Start tcpdump process, can be enabled on local system or remote, with custom port filtering
    :param file_name: name of capture file, default is capture.pcap so please don't use it
    :param iface: network interface on which tcpdump will be enabled
    :param port_filter: port filter (e.g. 'port 53' or 'port 8080 or port 8000' by default it will filter
    out everything except dhcp ports and dns
    :param location: local for system on which forge is running, or ip address of any system that is used during test

    Example how to use entire set of tcpdump commands:
    srv_msg.enable_tcpdump(file_name='abc.pcap', location=world.f_cfg.mgmt_address, port_filter='port 53')
    <send traffic>
    srv_msg.kill_tcpdump(location=world.f_cfg.mgmt_address)
    srv_msg.download_tcpdump_capture(location=world.f_cfg.mgmt_address, file_name='abc.pcap')
    """
    start_tcpdump(file_name=file_name, iface=iface, port_filter=port_filter, location=location)


def kill_tcpdump(location: str = 'local'):
    """
    Stop tcpdump instances running on system
    :param location: local for system on which forge is running, or ip address of any system that is used during test
    """
    stop_tcpdump(location=location)


def get_tcpdump_capture(location, file_name):
    """
    Download capture files to tests results
    :param location: ip address of remote system on which tcpdump was enabled
    :param file_name: name of capture file
    """
    download_tcpdump_capture(location=location, file_name=file_name)


def tcp_messages_include(**kwargs):
    dhcpmsg.tcp_messages_include(**kwargs)


def tcp_get_message(**kwargs):
    return dhcpmsg.tcp_get_message(**kwargs)


def send_over_tcp(msg, address=None, port=None, parse=False, number_of_connections=1, print_all=True):
    return dhcpmsg.send_over_tcp(msg, address=address, port=port, parse=parse,
                                 number_of_connections=number_of_connections, print_all=print_all)


def check_if_address_belongs_to_subnet(subnet: str = None, address: str = None):
    """
    Check if address belongs to subnet. Accepts v4 and v6
    :param subnet: subnet definition e.g. '2001:db8:1::/64'
    :param address: ip address e.g. '2001:db8:2::1'
    """
    if subnet is None:
        assert False, "You need to specify subnet"
    if address is None:
        lease = get_all_leases()
        if isinstance(lease, list):
            lease = lease[0]

        address = lease['address']

    assert ipaddress.ip_address(address) in ipaddress.ip_network(subnet), f"Address {address} " \
                                                                          f"does NOT belong to subnet {subnet}"
    log.debug("%s fit into %s", address, subnet)
