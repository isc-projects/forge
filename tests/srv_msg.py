# Copyright (C) 2013-2017 Internet Systems Consortium.
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND INTERNET SYSTEMS CONSORTIUM
# DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# INTERNET SYSTEMS CONSORTIUM BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
# FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
# WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# Author: Wlodzimierz Wencel

import sys
import json
import importlib

from forge_cfg import world, step
from protosupport import dns, multi_protocol_functions
from protosupport.multi_protocol_functions import test_define_value, substitute_vars


class Dispatcher(object):
    def __getattr__(self, attr_name):
        mod = importlib.import_module("protosupport.%s.srv_msg" % world.f_cfg.proto)
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


##building DHCP messages
@step('Client requests option (\d+).')
def client_requests_option(opt_type):
    """
    Add Option: Request Option with requested option code
    """
    dhcpmsg.client_requests_option(opt_type)


@step('(Client|RelayAgent) sets (\w+) value to (\S+).')
def client_sets_value(sender_type, value_name, new_value):
    """
    User can set values like: address, T1 or DUID to make test scenario
    more accurate.
    """
    # that is also used for DNS messages and RelayForward message but sender_type was
    # introduced just to keep tests cleaner - it's unused in the code.
    value_name, new_value = test_define_value(value_name, new_value)
    dhcpmsg.client_sets_value(value_name, new_value)


@step('Through (\S+) interface to address (\S+) client sends (\w+) message.')
def client_send_msg_via_interface(iface, addr, msgname):
    """
    This step actually build message (e.g. SOLICIT) with all details
    specified in steps like:
    Client sets (\w+) value to (\S+).
    Client does include (\S+).
    and others..
    Message builded here will be send in step: Server must response with...
    """
    msgname, iface, addr = test_define_value(msgname, iface, addr)
    dhcpmsg.client_send_msg(msgname, iface, addr)


@step('Client sends (\w+) message.')
def client_send_msg(msgname):
    """
    This step actually build message (e.g. SOLICIT) with all details
    specified in steps like:
    Client sets (\w+) value to (\S+).
    Client does include (\S+).
    and others..
    Message builded here will be send in step: Server must response with...
    Message will be send via interface set in init_all.py marked as IFACE.
    """
    dhcpmsg.client_send_msg(msgname, None, None)


@step('Client adds to the message (\S+) with value (\S+).')
def client_does_include_with_value(opt_type, value):
    """
    You can choose to include options to message with proposed value. Mostly used only with
    DHCPv4. Also reason why that step is called "Client adds to message" not
    "Client does (NOT )?include" as other step is that lettuce step parser is really... weak.
    What ever I'll do with that always takes wrong step.
    """
    opt_type, value = test_define_value(opt_type, value)
    dhcpmsg.client_does_include(None, opt_type, value)


@step('(\S+) does (NOT )?include (\S+).')
def client_does_include(sender_type, yes_or_not, opt_type):
    # add " option." to the end of the step - change all tests!
    """
    You can choose to include options to message (support for every option listed
    in RFC 3315 and more) or to not include options like IA_NA or client_id.
    """
    dhcpmsg.client_does_include(str(sender_type), opt_type, None)


@step('Relay-agent does include (\S+).')
def relay_agent_does_include(opt_type):
    # add " option." to the end of the step - change all tests!
    """
    """
    #dhcpmsg.relay_agent_does_include(opt_type)


@step('Client chooses (GLOBAL)|(LINK_LOCAL) UNICAST address.')
def unicast_addres(addr_type, addr_type2):
    """
    Message can be send on 3 different addresses:
    - multicast for DHCPv6
    - unicast global address of the server
    - unicast local address of the server
    Proper configuration in ini_all.py required.
    """
    # send true when GLOBAL and False when LINK_LOCAL
    dhcpmsg.unicast_addres(True if addr_type else False)


@step('Generate new (\S+).')
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


@step('RelayAgent forwards message encapsulated in (\d+) level(s)?.')
def create_relay_forward(level=1):
    """
    This step is strictly related to step: Client sends message.
    You can put only after that step. They can be seperated with other steps
    which causes to change values/include options

    This step causes to encapsulate builded message in RELAY FORWARD.
    It makes possible testing RELAY-REPLY messages.
    """
    dhcpmsg.create_relay_forward(level)


@step('(Client|RelayAgent) adds suboption for vendor specific information with code: (\d+) and data: (\S+).')
def add_vendor_suboption(sender_type, code, data):
    """
    After adding Vendor Specific Option we can decide to add suboptions to it. Please make sure which are
    supported and if it's necessary add suboption by yourself.
    """
    dhcpmsg.add_vendor_suboption(int(code), data)


@step('Before sending a message set filed named (\S+) to (\S+) as type (\S+).')
def change_message_filed(message_filed, value, value_type):
    message_filed, value, value_type = test_define_value(message_filed, value, value_type)
    dhcpmsg.change_message_field(message_filed, value, value_type)


##checking DHCP respond
@step('Server MUST NOT respond.')
def send_dont_wait_for_message():
    """
    This step causes to send message in cases when we don't expect any response.
    Step used only for v4 testing
    """
    dhcpmsg.send_wait_for_message("MUST", False, "None")


@step('Server (\S+) (NOT )?respond with (\w+) message.')
def send_wait_for_message(server_type, yes_or_no, message):
    """
    This step causes to send message to server and capture respond.
    """
    presence = True if yes_or_no is None else False
    return dhcpmsg.send_wait_for_message(server_type, presence, message)


@step('(Response|Relayed Message) MUST (NOT )?include option (\d+).')
def response_check_include_option(resp_rel, yes_or_no, opt_code):
    """
    Use this step for parsing respond. For more details please read manual section "Parsing respond"
    """
    include = not (yes_or_no == "NOT ")
    dhcpmsg.response_check_include_option(include, opt_code)


@step('(Response|Relayed Message) MUST (NOT )?contain (\S+) (\S+).')
def response_check_content(resp_rel, expect, data_type, expected):
    """
    """
    #expect, data_type, expected = test_define_value(expect, data_type, expected)
    dhcpmsg.response_check_content(expect, data_type, expected)


@step('(Response|Relayed Message) option (\d+) MUST (NOT )?contain (\S+) (\S+).')
def response_check_option_content(resp_rel, opt_code, expect, data_type, expected_value):
    """
    Detailed parsing of received option. For more details please read manual section "Parsing respond"
    """
    data_type, expected_value = test_define_value(data_type, expected_value)
    if data_type == "sub-option":
        dhcpmsg.response_check_include_suboption(opt_code, expect, expected_value)
    else:
        dhcpmsg.response_check_option_content(opt_code, expect, data_type, expected_value)


@step('(Response|Relayed Message) sub-option (\d+) from option (\d+) MUST (NOT )?contain (\S+) (\S+).')
def response_check_suboption_content(resp_rel, subopt_code, opt_code, expect, data_type, expected):
    """
    Some options can include suboptions, we can test them too.
    For more details please read manual section "Parsing respond"
    """
    dhcpmsg.response_check_suboption_content(subopt_code, opt_code, expect, data_type, expected)


def get_suboption(opt_code, subopt_code):
    return dhcpmsg.get_suboption(opt_code, subopt_code)


##building DNS messages
@step('Client for DNS Question Record uses address: (\S+) type (\S+) class (\S+).')
def dns_question_record(addr, qtype, qclass):
    dns.dns_question_record(str(addr), qtype, qclass)


@step('For DNS query client sets (\w+) value to (\S+).')
def dns_query_set_value(variable_name, value):
    dns.set_val()


@step('Client sends DNS query.')
def client_send_dns_query():
    dns.prepare_query()


##checking DNS respond
@step('DNS server (\S+) (NOT )?respond with DNS query.')
def send_wait_for_query(type, yes_or_no):
    """
    This step causes to send message to server and capture respond.
    """
    presence = True if yes_or_no is None else False
    dns.send_wait_for_query(type, presence)


@step('Received DNS query MUST (NOT )?contain (\S+) with value (\S+).')
def dns_check(expect, data_type, expected_data_value):
    dns.check_dns_respond(expect, str(data_type), expected_data_value)
    # later probably we'll have to change MUST on (\S+) for sth like MAY


@step('Received DNS query MUST include (NOT )?empty (QUESTION|ANSWER|AUTHORITATIVE_NAMESERVERS|ADDITIONAL_RECORDS) part.')
def dns_option(expect_empty, part_name):
    dns.check_dns_option(expect_empty, str(part_name))
    # later probably we'll have to change MUST on (\S+) for sth like MAY


@step('Received DNS part (QUESTION|ANSWER|AUTHORITATIVE_NAMESERVERS|ADDITIONAL_RECORDS) MUST (NOT )?contain (\S+) with value (\S+).')
def dns_option_content(part_name, expect, value_name, value):
    dns.dns_option_content(part_name, expect, str(value_name), str(value))
    # later probably we'll have to change MUST on (\S+) for sth like MAY


##save option from received message
@step('Client copies (\S+) option from received message.')
def client_copy_option(option_name):
    """
    When we need to send the same option back to server (e.g. Server ID) we can use this step.
    Copied option is automatically added to next generated message, and erased.
    """
    assert len(world.srvmsg), "No messages received, nothing to copy."
    dhcpmsg.client_copy_option(option_name)


@step('Client saves (\S+) option from received message.')
def client_save_option(option_name):
    """
    In time we need to include one option more then one time in different messages, we can
    choose to save it in memory. Memory will be erased at the end of the test, or when we
    decide to clear it in step "Client adds saved options. And erase.
    """
    assert len(world.srvmsg), "No messages received, nothing to save."
    dhcpmsg.client_save_option(option_name)


@step('Client saves into set no. (\d+) (\S+) option from received message.')
def client_save_option_count(count, option_name):
    """
    """
    assert len(world.srvmsg), "No messages received, nothing to save."
    dhcpmsg.client_save_option(option_name, count)


@step('Client adds saved options. And (DONT )?Erase.')
def client_add_saved_option(yes_or_no):
    """
    This step causes to include saved options to message. Also we can decide to keep or clear
    memory.
    """
    assert len(world.savedmsg), "No options to add."
    erase = True if yes_or_no is None else False
    dhcpmsg.client_add_saved_option(erase)


@step('Client adds saved options in set no. (\d+). And (DONT )?Erase.')
def client_add_saved_option_count(count, yes_or_no):
    """
    """
    assert len(world.savedmsg), "No options to add."
    erase = True if yes_or_no is None else False
    dhcpmsg.client_add_saved_option(erase, count)


@step('Save (\S+) value from (\d+) option.')
def save_value_from_option(value_name, option_name):
    """
    This step can be used to save value of some option field for
    further usage. It's like client_save_option but only for
    one specific field of given option.
    """
    dhcpmsg.save_value_from_option(value_name, option_name)


@step('Received (\S+) value in option (\d+) is the same as saved value.')
def compare_values(value_name, option_name):
    """
    If you have used step save_value_from_option, then this step will
    compare the earlier saved value with the recent received value.
    Note that names of fields that values are being compared should
    be the same.
    """
    dhcpmsg.compare_values(value_name, option_name)


##other
@step('Set network variable (\S+) with value (\S+).')
def network_variable(value_name, value):
    value_name, value = test_define_value(value_name, value)
    multi_protocol_functions.change_network_variables(value_name, value)


@step('File stored in (\S+) MUST (NOT )?contain line or phrase: (.+)')
def file_contains_line(file_path, condition, line):
    """
    Check if Log includes line.
    Be aware that tested line is every thing after "line: " until end of the line.
    """
    file_path, line = test_define_value(file_path, line)
    multi_protocol_functions.regular_file_contain(file_path, condition, line)


@step('DNS log MUST (NOT )?contain line: (.+)')
def dns_log_contains(condition, line):
    """
    Check if DNS log includes line.
    Be aware that tested line is every thing after "line: " until end of the line.
    """
    line = test_define_value(line)[0]
    multi_protocol_functions.regular_file_contain(world.cfg["dns_log_file"], condition, line)


def log_contains(line, log_file=None):
    line = test_define_value(line)[0]
    multi_protocol_functions.log_contains(line, None, log_file)


def log_doesnt_contain(line, log_file=None):
    line = test_define_value(line)[0]
    multi_protocol_functions.log_contains(line, 'NOT', log_file)


def lease_file_contains(line):
    line = test_define_value(line)[0]
    multi_protocol_functions.regular_file_contain(world.f_cfg.get_leases_path(), None, line)


def lease_file_doesnt_contain(line):
    line = test_define_value(line)[0]
    multi_protocol_functions.regular_file_contain(world.f_cfg.get_leases_path(), True, line)


@step('Remote (\S+) file stored in (\S+) MUST (NOT )?contain line or phrase: (.+)')
def remote_log_includes_line(destination, file_path, condition, line):
    """
    Check if Log includes line.
    Be aware that tested line is every thing after "line: " until end of the line.
    """
    destination, file_path, line = test_define_value(destination, file_path, line)
    multi_protocol_functions.regular_file_contain(file_path, condition, line, destination=destination)


@step('Table (\S+) in (\S+) database MUST (NOT )?contain line or phrase: (.+)')
def table_contains_line(table_name, db_type, condition, line):
    """
    Check if in table X in database type Y include line.
    Be aware that tested line is every thing after "line: " until end of the line.
    """
    table_name, db_type, line = test_define_value(table_name, db_type, line)
    multi_protocol_functions.db_table_contain(table_name, db_type, condition, line)


@step('Remove all records from table (\S+) in (\S+) database.')
def remove_from_db_table(table_name, db_type):
    table_name, db_type = test_define_value(table_name, db_type)
    multi_protocol_functions.remove_from_db_table(table_name, db_type)


@step('(\S+) log contains (\d+) of line: (.+)')
def log_includes_count(server_type, count, line):
    """
    Check if Log includes line.
    Be aware that tested line is every thing after "line: " until end of the line.
    """
    count, line = test_define_value(count, line)
    multi_protocol_functions.log_contains_count(server_type, count, line)


@step('Sleep for (\S+) (seconds|second|milliseconds|millisecond).')
def forge_sleep(time_val, time_units):
    """
    Pause the test for selected amount of time counted in seconds or milliseconds.
    """
    time_val, time_units = test_define_value(time_val, time_units)
    multi_protocol_functions.forge_sleep(int(time_val), str(time_units))


@step('Pause the Test.')
def test_pause():
    """
    Pause the test for any reason. Very good to debug problems. Checking server configuration
    and so on.... Do NOT put it in automatic tests, it blocks test until user will:
        Press any key to continue.
    """
    multi_protocol_functions.test_pause()


@step('End test.')
def test_stop():
    assert False, "Test ended."


@step('Fail test.')
def test_fail():
    assert False, "Test failed on purpose."


@step('Client download file from server stored in: (\S+).')
def copy_remote(remote_path):
    """
    Download file from remote server. It is stored in test directory.
    And named "downloaded_file"
    """
    remote_path = test_define_value(remote_path)[0]
    multi_protocol_functions.copy_file_from_server(remote_path)


@step('Client compares downloaded file from server with local file stored in: (\S+).')
def compare_file(remote_path):
    """
    Compare two files, our local and "downloaded_file".
    """
    remote_path = test_define_value(remote_path)[0]
    multi_protocol_functions.compare_file(remote_path)


@step('Downloaded file MUST (NOT )?contain line: (.+)')
def file_includes_line(condition, line):
    """
    Check if downloaded file includes line.
    Be aware that tested line is every thing after "line: " until end of the line.
    """
    line = test_define_value(line)[0]
    multi_protocol_functions.file_includes_line(condition, line)


@step('Client sends local file stored in: (\S+) to server, to location: (\S+).')
def send_file_to_server(local_path, remote_path):
    """
    If you need send some file to server, use that step.
    """
    local_path, remote_path = test_define_value(local_path, remote_path)
    multi_protocol_functions.send_file_to_server(local_path, remote_path)


@step('Client removes file from server located in: (\S+).')
def remove_file_from_server(remote_path):
    """
    If you need to remove file from a server, please do so.
    """
    remote_path = test_define_value(remote_path)[0]
    multi_protocol_functions.remove_file_from_server(remote_path)


@step('Add environment variable named (\S+) to value (.+)')
def set_env(env_name, env_value):
    multi_protocol_functions.set_value(env_name, env_value)


@step('User define temporary variable: (\S+) with value (.+)')
def add_variable_temporary(variable_name, variable_val):
    """
    User can define his own variable, that can be called from any place in test scenario,
    by $(variable_name). Allowed signs in variable name are: capitalized letters and '_'.

    Temporary variable will be stored in world.define and cleared at the end of scenario.
    """
    multi_protocol_functions.add_variable(variable_name, variable_val, 0)


@step('User define permanent variable: (\S+) with value (\S+).')
def add_variable_permanent(variable_name, variable_val):
    """
    User can define his own variable, that can be called from any place in test scenario,
    by $(variable_name). Allowed signs in variable name are: capitalized letters and '_'.

    Permanent variable will be placed at the end of the init_all.py file. It won't be removed.
    User can do so by removing it from file.
    """
    multi_protocol_functions.add_variable(variable_name, variable_val, 1)


@step('Let us celebrate this SUCCESS!')
def test_victory():
    """
    Use your imagination.
    """
    multi_protocol_functions.user_victory()


@step('Execute command (\S+) with arguments: (.+)')
def execute_shell_cmd(path, arg):
    path, arg = test_define_value(path, arg)
    result = multi_protocol_functions.execute_shell_cmd(path, arg)
    assert result.succeeded
    return result


@step('Execute command (\S+) with arguments: (.+)')
def execute_kea_shell(args):
    args = test_define_value(args)[0]
    path = world.f_cfg.sbin_join('kea-shell')
    result = multi_protocol_functions.execute_shell_cmd(path, args)
    result = json.loads(result)
    assert result[0]['result'] == 0
    return result


@step('Check socket connectivity on address (\S+) and port (\S+).')
def check_socket(socket_address, socket_port):
    pass


@step('Check socket connectivity on server in path (\S+).')
def check_socket_server_site(socket_path):
    pass


@step('Send ctrl cmd (.+) using UNIX socket (\S+) to server (.+).')
def send_ctrl_cmd_via_socket(command, socket_name=None, destination_address=world.f_cfg.mgmt_address,
                             exp_result=0, exp_failed=False):
    if isinstance(command, dict):
        substitute_vars(command)
        destination_address = test_define_value(destination_address)[0]
    else:
        destination_address, command = test_define_value(destination_address, command)
    return multi_protocol_functions.send_ctrl_cmd_via_socket(command, socket_name, destination_address,
                                                             exp_result, exp_failed)


@step('Send ctrl cmd (.+) using HTTP (\S+):(\S+) connection.')
def send_ctrl_cmd_via_http(command, address='$(MGMT_ADDRESS)', port='8000', exp_result=0):
    if isinstance(command, dict):
        substitute_vars(command)
        address, port = test_define_value(address, port)
    else:
        address, port, command = test_define_value(address, port, command)
    return multi_protocol_functions.send_ctrl_cmd_via_http(command, address, int(port), exp_result)


def send_ctrl_cmd(cmd, channel='http', service=None, exp_result=0):
    """Send request to DHCP Kea server over Unix socket or over HTTP via CA."""

    if channel == 'http':
        if service != 'agent':
            if world.proto == 'v4':
                cmd["service"] = ['dhcp4']
            else:
                cmd["service"] = ['dhcp6']

    if channel == 'http':
        response = send_ctrl_cmd_via_http(cmd, '$(MGMT_ADDRESS)', 8000, exp_result=exp_result)
        response = response[0]
    elif channel == 'socket':
        response = send_ctrl_cmd_via_socket(cmd, exp_result=exp_result)
    else:
        raise ValueError('unsupported channel type: %s' % str(channel))
    return response


@step('JSON response in (\S+) MUST (NOT )?include value: (.+)')
def json_response_parsing(parameter_name, condition, parameter_value):
    parameter_name, parameter_value = test_define_value(parameter_name, parameter_value)
    multi_protocol_functions.parse_json_file(condition, str(parameter_name), str(parameter_value))


## loops
## testing in loops is new feature that gives possibility to send lot of messages without
## writing usual steps for each message. This feature is not fully tested.

# @step('Start fuzzing. Time: (\d+) (hours|minutes).')
# def start_fuzzing(time_period, time_units):
#     dhcpmsg.start_fuzzing(time_period, time_units)
#
# @step('Start fuzzing.')
# def start_fuzzing():
#     dhcpmsg.start_fuzzing()


@step('Loops config: Save leases details.')
def loops_config_sld():
    dhcpmsg.loops_config_sld()


@step('Loops config: choose (\S+) from (file )?(.+)')
def values_for_loops(value_name, file_flag, values):
    dhcpmsg.values_for_loops(value_name, file_flag, values)


@step('Exchange messages (\S+) - (\S+) (\d+) times.')
def loops(message_type_1, message_type_2, repeat):
    tmp = world.f_cfg.show_packets_from
    world.f_cfg.show_packets_from = ""
    dhcpmsg.loops(message_type_1, message_type_2, repeat)
    world.f_cfg.show_packets_from = tmp
