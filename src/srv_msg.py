# Copyright (C) 2013-2025 Internet Systems Consortium, Inc. ("ISC")
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
# pylint: disable=too-many-arguments

"""Functions used in building or transmitting messages/packets."""

import random
import json
import importlib
import ipaddress
import logging

from scapy.layers.dhcp6 import DUID_LLT, DUID_LL, DUID_EN
from .forge_cfg import world, step
from .protosupport import dns, multi_protocol_functions
from .protosupport.multi_protocol_functions import test_define_value, substitute_vars
from .softwaresupport.multi_server_functions import start_tcpdump, stop_tcpdump, download_tcpdump_capture

log = logging.getLogger('forge')


class Dispatcher(object):
    """Dispatcher."""

    def __getattr__(self, attr_name):
        """__getattr__.

        :param attr_name:
        """
        mod = importlib.import_module("src.protosupport.%s.srv_msg" % world.f_cfg.proto)
        return getattr(mod, attr_name)


dhcpmsg = Dispatcher()


# config values return
def get_interface():
    """Get interface.

    :return:
    :rtype:
    """
    return world.f_cfg.iface


def get_proto_version():
    """Get protocol version.

    :return:
    :rtype:
    """
    return world.f_cfg.proto


def get_server_interface():
    """Get server interface.

    :return:
    :rtype:
    """
    return world.f_cfg.server_iface


def get_server_path():
    """Get server path.

    :return:
    :rtype:
    """
    return world.f_cfg.software_install_path


# building DHCP messages
@step(r'Client requests option (\d+).')
def client_requests_option(opt_type):
    """Add Option: Request Option with requested option code.

    :param opt_type:
    :type opt_type:
    """
    dhcpmsg.client_requests_option(opt_type)


@step(r'(Client|RelayAgent) sets (\w+) value to (\S+).')
def client_sets_value(sender_type, value_name, new_value):
    """User can set values like: address, T1 or DUID to make test scenario more accurate.

    :param sender_type:
    :type sender_type:
    :param value_name:
    :type value_name:
    :param new_value:
    :type new_value:
    """
    # that is also used for DNS messages and RelayForward message but sender_type was
    # introduced just to keep tests cleaner - it's unused in the code.
    # if we pass DUID class do not check defined values
    if not isinstance(new_value, (DUID_LLT, DUID_LL, DUID_EN)):
        value_name, new_value = test_define_value(value_name, new_value)
    dhcpmsg.client_sets_value(value_name, new_value)


@step(r'Through (\S+) interface to address (\S+) client sends (\w+) message.')
def client_send_msg_via_interface(iface, addr, msgname):
    r"""Build message (e.g. SOLICIT) with all details specified in steps.

    Like:
    Client sets (\w+) value to (\S+).
    Client does include (\S+).
    and others..
    Message builded here will be send in step: Server must response with...

    :param iface:
    :type iface:
    :param addr:
    :type addr:
    :param msgname:
    :type msgname:
    """
    msgname, iface, addr = test_define_value(msgname, iface, addr)
    dhcpmsg.client_send_msg(msgname, iface, addr)


@step(r'Client sends (\w+) message.')
def client_send_msg(msgname, iface=None):
    r"""Build message (e.g. SOLICIT) with all details specified in steps.

    Like:
    Client sets (\w+) value to (\S+).
    Client does include (\S+).
    and others..
    Message builded here will be send in step: Server must response with...
    Message will be send via interface set in init_all.py marked as IFACE.

    :param msgname:
    :type msgname:
    :param iface: (Default value = None)
    :type iface:
    """
    dhcpmsg.client_send_msg(msgname, iface, None)


@step(r'Send (\S+) with raw appending (.+)')
def send_raw_message(msg_type="", raw_append=None):
    """Send raw message.

    :param msg_type: (Default value = "")
    :type msg_type:
    :param raw_append: (Default value = None)
    :type raw_append:
    """
    dhcpmsg.build_raw(msg=msg_type, append=raw_append)


@step(r'Client adds to the message (\S+) with value (\S+).')
def client_does_include_with_value(opt_type, value):
    """Include options to message with proposed value.

    Mostly used only with
    DHCPv4. Also reason why that step is called "Client adds to message" not
    "Client does (NOT )?include" as other step is that lettuce step parser is really... weak.
    What ever I'll do with that always takes wrong step.

    :param opt_type:
    :type opt_type:
    :param value:
    :type value:
    """
    assert world.f_cfg.proto == 'v4', 'funciton only used for DHCPv4'
    opt_type, value = test_define_value(opt_type, value)
    dhcpmsg.client_does_include(None, opt_type, value)


def client_v6_does_include_with_value(sender_type, opt_type, value):
    """Insert an option into the DHCPv6 client message.

    :param sender_type: who inserted the option
    :type sender_type:
    :param opt_type: option name
    :type opt_type:
    :param value: option value
    :type value:
    """
    assert world.f_cfg.proto == 'v6', 'function only used for DHCPv6'
    opt_type, value = test_define_value(opt_type, value)
    dhcpmsg.client_does_include(sender_type, opt_type, value)


@step(r'(\S+) does (NOT )?include (\S+).')
def client_does_include(sender_type, opt_type, value=None):
    """Include options to message.

    Supports every option listed in RFC 3315 and more or to not include options like IA_NA or client_id.

    :param sender_type:
    :type sender_type:
    :param opt_type:
    :type opt_type:
    :param value: (Default value = None)
    :type value:
    """
    # add " option." to the end of the step - change all tests!
    dhcpmsg.client_does_include(str(sender_type), opt_type, None)


def add_scapy_option(option, where='client'):
    """Add option to next message.

    Forge does cleaver things to world.cliopts so double check if
    that function is actually doing in your test what you expect it does.

    :param option: scapy option, can be just tuple for v4 or scapy.layers.dhcp6 option class
    :type option:
    :param where: decide where option should be added (Default value = 'client')
    :type where:
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
    """relay_agent_does_include.

    :param opt_type:
    :type opt_type:
    """
    # add " option." to the end of the step - change all tests!
    # dhcpmsg.relay_agent_does_include(opt_type)


@step(r'Client chooses (GLOBAL)|(LINK_LOCAL) UNICAST address.')
def unicast_address(addr_type, addr_type2):
    """Message can be sent on 3 different addresses.

    - multicast for DHCPv6
    - unicast global address of the server
    - unicast local address of the server

    Proper configuration in init_all.py required.

    :param addr_type:
    :type addr_type:
    :param addr_type2:
    :type addr_type2:
    """
    # send true when GLOBAL and False when LINK_LOCAL
    dhcpmsg.unicast_address(True if addr_type else False)


@step(r'Generate new (\S+).')
def generate_new(opt):
    """Change option values in scenarios with multiple different users.

    for client_id and IA: client
    for client_id only: Client_ID
    for IA: IA
    for IA_PD: IA_PD

    :param opt:
    :type opt:
    """
    dhcpmsg.generate_new(opt)


@step(r'RelayAgent forwards message encapsulated in (\d+) level(s)?.')
def create_relay_forward(level=1):
    """create_relay_forward.

    This step is strictly related to step: Client sends message.

    You can put only after that step. They can be seperated with other steps
    which causes to change values/include options

    This step causes to encapsulate builded message in RELAY FORWARD.
    It makes possible testing RELAY-REPLY messages.

    :param level: (Default value = 1)
    :type level:
    """
    dhcpmsg.create_relay_forward(level)


@step(r'(Client|RelayAgent) adds suboption for vendor specific information with code: (\d+) and data: (\S+).')
def add_vendor_suboption(sender_type, code, data):
    """add_vendor_suboption.

    After adding Vendor Specific Option we can decide to add suboptions to it. Please make sure which are
    supported and if it's necessary add suboption by yourself.

    :param sender_type:
    :type sender_type:
    :param code:
    :type code:
    :param data:
    :type data:
    """
    dhcpmsg.add_vendor_suboption(int(code), data)


@step(r'Before sending a message set filed named (\S+) to (\S+) as type (\S+).')
def change_message_filed(message_filed, value, value_type):
    """change_message_filed.

    :param message_filed:
    :type message_filed:
    :param value:
    :type value:
    :param value_type:
    :type value_type:
    """
    message_filed, value, value_type = test_define_value(message_filed, value, value_type)
    dhcpmsg.change_message_field(message_filed, value, value_type)


# checking DHCP respond
@step(r'Server MUST NOT respond.')
def send_dont_wait_for_message(iface=None, ignore_response=False):
    """Send message in cases when we don't expect any response.

    Step used only for v4 testing

    :param iface: (Default value = None)
    :type iface:
    :param ignore_response: (Default value = False)
    :type ignore_response:
    """
    dhcpmsg.send_wait_for_message("MUST", False, None, iface=iface, ignore_response=ignore_response)


@step(r'Server (\S+) (NOT )?respond with (\w+) message.')
def send_wait_for_message(requirement_level: str, message: str, expect_response: bool = True,
                          protocol: str = 'UDP', address: str = None, port: int = None,
                          iface: str = None):
    """Send messages to server either TCP or UDP, check if response is received.

    :param requirement_level: not used. RFC-grade requirement level e.g. 'MAY', 'MUST'
    :type requirement_level:
    :param message: name of message that should be received from a server (if we expect multiple messages,
    :type message: str
    :param expect_response: condition if message is expected or not
    :type expect_response: bool
    :param protocol: choose protocol, for now it's UDP for DHCP messages and TCP for bulk lease query
    :type protocol: str:
    :param address: destination address for TCP connection
    :type address: str
    :param port: destination port for TCP connection
    :type port: int
    :param iface: (Default value = None)
    :type iface: str:
    :return: list of replies from server
    :rtype:
    """
    return dhcpmsg.send_wait_for_message(requirement_level, expect_response, message, protocol,
                                         address=address, port=port, iface=iface)


@step(r'(Response|Relayed Message) MUST (NOT )?include option (\d+).')
def response_check_include_option(opt_code, expect_include=True):
    """Use this step for parsing respond. For more details please read manual section "Parsing respond".

    :param opt_code:
    :type opt_code:
    :param expect_include: (Default value = True)
    :type expect_include:
    :return:
    :rtype:
    """
    return dhcpmsg.response_check_include_option(expect_include, opt_code)


@step(r'(Response|Relayed Message) MUST (NOT )?contain (\S+) (\S+).')
def response_check_content(data_type, value, expected=True):
    """response_check_content.

    :param data_type:
    :type data_type:
    :param value:
    :type value:
    :param expected: (Default value = True)
    :type expected:
    """
    # expect, data_type, expected = test_define_value(expect, data_type, expected)
    dhcpmsg.response_check_content(expected, data_type, value)


@step(r'(Response|Relayed Message) option (\d+) MUST (NOT )?contain (\S+) (\S+).')
def response_check_option_content(opt_code, data_type, expected_value, expect_include=True):
    """Detailed parsing of received option. For more details please read manual section "Parsing respond".

    :param opt_code:
    :type opt_code:
    :param data_type:
    :type data_type:
    :param expected_value:
    :type expected_value:
    :param expect_include: (Default value = True)
    :type expect_include:
    :return:
    :rtype:
    """
    data_type, expected_value = test_define_value(data_type, expected_value)
    if data_type == "sub-option":
        return dhcpmsg.response_check_include_suboption(opt_code, expect_include, expected_value)
    return dhcpmsg.response_check_option_content(opt_code, expect_include, data_type, expected_value)


def response_check_option_content_more(opt_code, data_type, expected_value):
    """Check subsequent options. Only to be called after the first option was checked with response_check_option_content.

    :param opt_code:
    :type opt_code:
    :param data_type:
    :type data_type:
    :param expected_value:
    :type expected_value:
    :return:
    :rtype:
    """
    data_type, expected_value = test_define_value(data_type, expected_value)
    return dhcpmsg.response_check_option_content_more(opt_code, data_type, expected_value)


@step(r'(Response|Relayed Message) sub-option (\d+) from option (\d+) MUST (NOT )?contain (\S+) (\S+).')
def response_check_suboption_content(subopt_code, opt_code, data_type, value, expect_include=True):
    """Include suboptions, we can test them too.

    For more details please read manual section "Parsing respond"

    :param subopt_code:
    :type subopt_code:
    :param opt_code:
    :type opt_code:
    :param data_type:
    :type data_type:
    :param value:
    :type value:
    :param expect_include: (Default value = True)
    :type expect_include:
    """
    dhcpmsg.response_check_suboption_content(subopt_code, opt_code, expect_include, data_type, value)


def get_suboption(opt_code, subopt_code):
    """Get suboption.

    :param opt_code:
    :type opt_code:
    :param subopt_code:
    :type subopt_code:
    :return:
    :rtype:
    """
    return dhcpmsg.get_suboption(opt_code, subopt_code)


# building DNS messages
@step(r'Client for DNS Question Record uses address: (\S+) type (\S+) class (\S+).')
def dns_question_record(addr, qtype, qclass):
    """dns_question_record.

    :param addr:
    :type addr:
    :param qtype:
    :type qtype:
    :param qclass:
    :type qclass:
    """
    dns.dns_question_record(str(addr), qtype, qclass)


@step(r'Client sends DNS query.')
def client_send_dns_query(dns_addr=None, dns_port=None):
    """client_send_dns_query.

    :param dns_addr: (Default value = None)
    :type dns_addr:
    :param dns_port: (Default value = None)
    :type dns_port:
    """
    dns.prepare_query(dns_addr=dns_addr, dns_port=dns_port)


# checking DNS respond
@step(r'DNS server (\S+) (NOT )?respond with DNS query.')
def send_wait_for_query(type, expect_include=True, iface=None):
    """Send message to server and capture respond.

    :param type:
    :type type:
    :param expect_include: (Default value = True)
    :type expect_include:
    :param iface: (Default value = None)
    :type iface:
    """
    dns.send_wait_for_query(type, expect_include, iface=iface)


@step(r'Received DNS query MUST (NOT )?contain (\S+) with value (\S+).')
def dns_check(expect, data_type, expected_data_value):
    """DNS check.

    :param expect:
    :type expect:
    :param data_type:
    :type data_type:
    :param expected_data_value:
    :type expected_data_value:
    """
    dns.check_dns_respond(expect, str(data_type), expected_data_value)
    # later probably we'll have to change MUST on (\S+) for sth like MAY


@step(r'Received DNS query MUST include (NOT )?empty (QUESTION|ANSWER|AUTHORITATIVE_NAMESERVERS|ADDITIONAL_RECORDS) part.')
def dns_option(part_name, expect_include=True):
    """DNS option.

    :param part_name:
    :type part_name:
    :param expect_include: (Default value = True)
    :type expect_include:
    """
    dns.check_dns_option(expect_include, str(part_name))
    # later probably we'll have to change MUST on (\S+) for sth like MAY


@step(r'Received DNS part (QUESTION|ANSWER|AUTHORITATIVE_NAMESERVERS|ADDITIONAL_RECORDS) MUST (NOT )?contain (\S+) with value (\S+).')
def dns_option_content(part_name, value_name, value, expect_include=True):
    """DNS option content.

    :param part_name:
    :type part_name:
    :param value_name:
    :type value_name:
    :param value:
    :type value:
    :param expect_include: (Default value = True)
    :type expect_include:
    """
    dns.dns_option_content(part_name, expect_include, str(value_name), str(value))
    # later probably we'll have to change MUST on (\S+) for sth like MAY


# save option from received message
@step(r'Client copies (\S+) option from received message.')
def client_copy_option(option_name, copy_all=False):
    """client_copy_option.

    When we need to send the same option back to server (e.g. Server ID) we can use this step.
    Copied option is automatically added to next generated message, and erased.

    :param option_name:
    :type option_name:
    :param copy_all: (Default value = False)
    :type copy_all:
    """
    assert len(world.srvmsg), "No messages received, nothing to copy."
    dhcpmsg.client_copy_option(option_name, copy_all)


def clean_saved_options():
    """Clean all previously saved options."""
    world.savedmsg = {}


@step(r'Client saves (\S+) option from received message.')
def client_save_option(option_name):
    """client_save_option.

    In time we need to include one option more then one time in different messages, we can
    choose to save it in memory. Memory will be erased at the end of the test, or when we
    decide to clear it in step "Client adds saved options. And erase.

    :param option_name:
    :type option_name:
    """
    assert len(world.srvmsg), "No messages received, nothing to save."
    dhcpmsg.client_save_option(option_name)


@step(r'Client saves into set no. (\d+) (\S+) option from received message.')
def client_save_option_count(count, option_name):
    """client_save_option_count.

    :param count:
    :type count:
    :param option_name:
    :type option_name:
    """
    assert len(world.srvmsg), "No messages received, nothing to save."
    dhcpmsg.client_save_option(option_name, count)


@step(r'Client adds saved options. And (DONT )?Erase.')
def client_add_saved_option(erase=False):
    """Include saved options to message. Also we can decide to keep or clear memory.

    :param erase: (Default value = False)
    :type erase:
    """
    assert len(world.savedmsg), "No options to add."
    dhcpmsg.client_add_saved_option(erase)


@step(r'Client adds saved options in set no. (\d+). And (DONT )?Erase.')
def client_add_saved_option_count(count, erase=False):
    """client_add_saved_option_count.

    :param count:
    :type count:
    :param erase: (Default value = False)
    :type erase:
    """
    assert len(world.savedmsg), "No options to add."
    dhcpmsg.client_add_saved_option(erase, count)


@step(r'Save (\S+) value from (\d+) option.')
def save_value_from_option(value_name, option_name):
    """Save value of some option field for further usage.

    It's like client_save_option but only for one specific field of given option.

    :param value_name:
    :type value_name:
    :param option_name:
    :type option_name:
    """
    dhcpmsg.save_value_from_option(value_name, option_name)


@step(r'Received (\S+) value in option (\d+) is the same as saved value.')
def compare_values(value_name, option_name):
    """Compare values.

    If you have used step save_value_from_option, then this step will
    compare the earlier saved value with the recent received value.
    Note that names of fields that values are being compared should
    be the same.

    :param value_name:
    :type value_name:
    :param option_name:
    :type option_name:
    """
    dhcpmsg.compare_values(value_name, option_name)


# other
@step(r'Set network variable (\S+) with value (\S+).')
def network_variable(value_name, value):
    """Set network variable.

    :param value_name:
    :type value_name:
    :param value:
    :type value:
    """
    value_name, value = test_define_value(value_name, value)
    multi_protocol_functions.change_network_variables(value_name, value)


@step(r'Table (\S+) in (\S+) database MUST (NOT )?contain line or phrase: (.+)')
def table_contains_line(table_name, db_type, line, expect=True):
    """Check if in table X in database type Y include line.

    Be aware that tested line is every thing after "line: " until end of the line.

    :param table_name:
    :type table_name:
    :param db_type:
    :type db_type:
    :param line:
    :type line:
    :param expect: (Default value = True)
    :type expect:
    """
    table_name, db_type, line = test_define_value(table_name, db_type, line)
    multi_protocol_functions.db_table_contains_line(table_name, db_type, line=line, expect=expect)


def table_contains_line_n_times(table_name, db_type, n, line, destination=world.f_cfg.mgmt_address):
    """Check if in table X in database type Y include line.

    Be aware that tested line is every thing after "line: " until end of the line.

    :param table_name:
    :type table_name:
    :param db_type:
    :type db_type:
    :param n:
    :type n:
    :param line:
    :type line:
    :param destination: (Default value = world.f_cfg.mgmt_address)
    :type destination:
    """
    table_name, db_type, line = test_define_value(table_name, db_type, line)
    multi_protocol_functions.db_table_contains_line_n_times(table_name, db_type, n=n, line=line, destination=destination)


@step(r'Remove all records from table (\S+) in (\S+) database.')
def remove_from_db_table(table_name, db_type, destination=world.f_cfg.mgmt_address):
    """Remove all entries from database table.

    :param table_name:
    :type table_name:
    :param db_type:
    :type db_type:
    :param destination: (Default value = world.f_cfg.mgmt_address)
    :type destination:
    """
    table_name, db_type = test_define_value(table_name, db_type)
    multi_protocol_functions.remove_from_db_table(table_name, db_type, destination=destination)


@step(r'Sleep for (\S+) (seconds|second|milliseconds|millisecond).')
def forge_sleep(time_val, time_units='seconds'):
    """Pause the test for selected amount of time counted in seconds or milliseconds.

    :param time_val:
    :type time_val:
    :param time_units: (Default value = 'seconds')
    :type time_units:
    """
    time_val, time_units = test_define_value(time_val, time_units)
    print("Sleep for %s %s" % (time_val, time_units))
    multi_protocol_functions.forge_sleep(int(time_val), str(time_units))


@step(r'Pause the Test.')
def test_pause():
    """Pause the test for any reason.

    Very good to debug problems. Checking server configuration
    and so on.... Do NOT put it in automatic tests, it blocks test until user will:
    Press any key to continue.
    """
    multi_protocol_functions.test_pause()


@step(r'End test.')
def test_stop():
    """End test."""
    assert False, "Test ended."


@step(r'Fail test.')
def test_fail():
    """Fail test."""
    assert False, "Test failed on purpose."


@step(r'Client download file from server stored in: (\S+).')
def copy_remote(remote_path, local_filename='downloaded_file', dest=world.f_cfg.mgmt_address):
    """Download file from remote server.

    It is stored in test directory.
    And named "downloaded_file"

    :param remote_path:
    :type remote_path:
    :param local_filename: (Default value = 'downloaded_file')
    :type local_filename:
    :param dest: (Default value = world.f_cfg.mgmt_address)
    :type dest:
    """
    remote_path = test_define_value(remote_path)[0]
    multi_protocol_functions.copy_file_from_server(remote_path, local_filename, dest=dest)


@step(r'Client compares downloaded file from server with local file stored in: (\S+).')
def compare_file(remote_path):
    """Compare two files, our local and "downloaded_file".

    :param remote_path:
    :type remote_path:
    """
    remote_path = test_define_value(remote_path)[0]
    multi_protocol_functions.compare_file(remote_path)


@step(r'Client sends local file stored in: (\S+) to server, to location: (\S+).')
def send_file_to_server(local_path, remote_path):
    """If you need send some file to server, use that step.

    :param local_path:
    :type local_path:
    :param remote_path:
    :type remote_path:
    """
    local_path, remote_path = test_define_value(local_path, remote_path)
    multi_protocol_functions.send_file_to_server(local_path, remote_path)


@step(r'Client removes file from server located in: (\S+).')
def remove_file_from_server(remote_path, dest=world.f_cfg.mgmt_address):
    """If you need to remove file from a server, please do so.

    :param remote_path:
    :type remote_path:
    :param dest: (Default value = world.f_cfg.mgmt_address)
    :type dest:
    """
    remote_path = test_define_value(remote_path)[0]
    multi_protocol_functions.remove_file_from_server(remote_path, dest=dest)


@step(r'Add environment variable named (\S+) to value (.+)')
def set_env(env_name, env_value):
    """Set environment variable.

    :param env_name:
    :type env_name:
    :param env_value:
    :type env_value:
    """
    multi_protocol_functions.set_value(env_name, env_value)


@step(r'User define temporary variable: (\S+) with value (.+)')
def add_variable_temporary(variable_name, variable_val):
    """Define variable that can be called from any place in test scenario by $(variable_name).

    Allowed signs in variable name are: capitalized letters and '_'.

    Temporary variable will be stored in world.define and cleared at the end of scenario.

    :param variable_name:
    :type variable_name:
    :param variable_val:
    :type variable_val:
    """
    multi_protocol_functions.add_variable(variable_name, variable_val, 0)


@step(r'User define permanent variable: (\S+) with value (\S+).')
def add_variable_permanent(variable_name, variable_val):
    """Define variable that can be called from any place in test scenario by $(variable_name).

    Allowed signs in variable name are: capitalized letters and '_'.

    Permanent variable will be placed at the end of the init_all.py file. It won't be removed.
    User can do so by removing it from file.

    :param variable_name:
    :type variable_name:
    :param variable_val:
    :type variable_val:
    """
    multi_protocol_functions.add_variable(variable_name, variable_val, 1)


@step(r'Let us celebrate this SUCCESS!')
def test_victory():
    """Use your imagination."""
    multi_protocol_functions.user_victory()


@step(r'Execute command (\S+) with arguments: (.+)')
def execute_shell_cmd(path, dest=world.f_cfg.mgmt_address, save_results=True):
    """Execute shell command.

    :param path:
    :type path:
    :param dest: (Default value = world.f_cfg.mgmt_address)
    :type dest:
    :param save_results: (Default value = True)
    :type save_results:
    :return:
    :rtype:
    """
    path = test_define_value(path)[0]
    result = multi_protocol_functions.execute_shell_cmd(path, dest=dest, save_results=save_results)
    assert result.succeeded
    return result


@step(r'Execute command (\S+) with arguments: (.+)')
def execute_kea_shell(args, exp_result=0, exp_failed=False):
    """Execute kea-shell command.

    :param args:
    :type args:
    :param exp_result: (Default value = 0)
    :type exp_result:
    :param exp_failed: (Default value = False)
    :type exp_failed:
    :return:
    :rtype:
    """
    args = test_define_value(args)[0]
    path = world.f_cfg.sbin_join('kea-shell')
    if "--auth-user" not in args and "--auth-password" not in args:
        args = f" --auth-user {world.f_cfg.auth_user} --auth-password {world.f_cfg.auth_passwd} {args}"
    result = multi_protocol_functions.execute_shell_cmd(path + ' ' + args, exp_failed=exp_failed)
    result = json.loads(result)
    assert result[0]['result'] == exp_result, result
    return result


@step(r'Check socket connectivity on address (\S+) and port (\S+).')
def check_socket(socket_address, socket_port):
    """Check socket.

    :param socket_address:
    :type socket_address:
    :param socket_port:
    :type socket_port:
    """


@step(r'Check socket connectivity on server in path (\S+).')
def check_socket_server_site(socket_path):
    """check_socket_server_site.

    :param socket_path:
    :type socket_path:
    """


@step(r'Send ctrl cmd (.+) using UNIX socket (\S+) to server (.+).')
def send_ctrl_cmd_via_socket(command, socket_name=None, destination_address=world.f_cfg.mgmt_address,
                             exp_result=0, exp_failed=False):
    """Send control command via socket.

    :param command:
    :type command:
    :param socket_name: (Default value = None)
    :type socket_name:
    :param destination_address: (Default value = world.f_cfg.mgmt_address)
    :type destination_address:
    :param exp_result: (Default value = 0)
    :type exp_result:
    :param exp_failed: (Default value = False)
    :type exp_failed:
    :return:
    :rtype:
    """
    if isinstance(command, dict):
        substitute_vars(command)
        destination_address = test_define_value(destination_address)[0]
    else:
        destination_address, command = test_define_value(destination_address, command)
    return multi_protocol_functions.send_ctrl_cmd_via_socket(command, socket_name, destination_address,
                                                             exp_result, exp_failed)


@step(r'Send ctrl cmd (.+) using HTTP (\S+):(\S+) connection.')
def send_ctrl_cmd_via_http(command, address='$(MGMT_ADDRESS)', port=8000, exp_result=0, exp_failed=False, https=False, verify=None, cert=None,
                           headers=None, auth=None):
    """Send control command via HTTP.

    :param command:
    :type command:
    :param address: (Default value = '$(MGMT_ADDRESS)')
    :type address:
    :param port: (Default value = 8000)
    :type port:
    :param exp_result: (Default value = 0)
    :type exp_result:
    :param exp_failed: (Default value = False)
    :type exp_failed:
    :param https: (Default value = False)
    :type https:
    :param verify: (Default value = None)
    :type verify:
    :param cert: (Default value = None)
    :type cert:
    :param headers: (Default value = None)
    :type headers:
    :param auth: (Default value = None) user and password for basic authentication, format: "user:password"
    :type auth: str
    :return:
    :rtype:
    """
    if isinstance(command, dict):
        substitute_vars(command)
        address, port = test_define_value(address, port)
    else:
        address, port, command = test_define_value(address, port, command)
    return multi_protocol_functions.send_ctrl_cmd_via_http(command, address, int(port), exp_result, exp_failed, https, verify, cert, headers, auth)


def send_ctrl_cmd(cmd, channel='http', service=None, exp_result=0, exp_failed=False, address=world.f_cfg.mgmt_address, verify=None, cert=None,
                  headers=None, port=8000, auth=None):
    """Send request to DHCP Kea server over Unix socket or over HTTP via CA.

    :param cmd:
    :type cmd:
    :param channel: (Default value = 'http')
    :type channel:
    :param service: (Default value = None)
    :type service:
    :param exp_result: (Default value = 0)
    :type exp_result:
    :param exp_failed: (Default value = False)
    :type exp_failed:
    :param address: (Default value = world.f_cfg.mgmt_address)
    :type address:
    :param verify: (Default value = None)
    :type verify:
    :param cert: (Default value = None)
    :type cert:
    :param headers: (Default value = None)
    :type headers:
    :param port: (Default value = 8000)
    :type port:
    :param auth: (Default value = None) user and password for basic authentication, format: "user:password"
    :type auth: str
    :return:
    :rtype:
    """
    if channel in ['http', 'https']:
        if service != 'agent':
            if world.proto == 'v4':
                cmd["service"] = ['dhcp4']
            else:
                cmd["service"] = ['dhcp6']

    # if auth is None or auth != "missing":
    if channel == 'http':
        response = send_ctrl_cmd_via_http(cmd, address, port, exp_result=exp_result, exp_failed=exp_failed, headers=headers, auth=auth)
        if isinstance(response, dict):
            response = response
        else:
            response = response[0] if response else response
    elif channel == 'https':
        response = send_ctrl_cmd_via_http(cmd, address, port, exp_result=exp_result, exp_failed=exp_failed, https=True,
                                          verify=verify, cert=cert, headers=headers, auth=auth)
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
    """loops_config_sld."""
    dhcpmsg.loops_config_sld()


@step(r'Loops config: choose (\S+) from (file )?(.+)')
def values_for_loops(value_name, file_flag, values):
    """values_for_loops.

    :param value_name:
    :type value_name:
    :param file_flag:
    :type file_flag:
    :param values:
    :type values:
    """
    dhcpmsg.values_for_loops(value_name, file_flag, values)


@step(r'Exchange messages (\S+) - (\S+) (\d+) times.')
def loops(message_type_1, message_type_2, repeat):
    """loops.

    :param message_type_1:
    :type message_type_1:
    :param message_type_2:
    :type message_type_2:
    :param repeat:
    :type repeat:
    """
    tmp = world.f_cfg.show_packets_from
    world.f_cfg.show_packets_from = ""
    dhcpmsg.loops(message_type_1, message_type_2, repeat)
    world.f_cfg.show_packets_from = tmp


def get_all_leases():
    """Get all leases.

    :return:
    :rtype:
    """
    return dhcpmsg.get_all_leases()


def check_leases(leases_list, backend='memfile', dest=world.f_cfg.mgmt_address, should_succeed=True):
    """Check leases.

    :param leases_list:
    :type leases_list:
    :param backend: database backend (Default value = 'memfile')
    :type backend: str
    :param dest: (Default value = world.f_cfg.mgmt_address)
    :type dest:
    :param should_succeed: (Default value = True)
    :type should_succeed:
    """
    dest = test_define_value(dest)[0]
    multi_protocol_functions.check_leases(leases_list, backend=backend, destination=dest, should_succeed=should_succeed)


def lease_dump(backend, db_name=world.f_cfg.db_name, db_user=world.f_cfg.db_user,
               db_passwd=world.f_cfg.db_passwd, destination_address=world.f_cfg.mgmt_address,
               out="/tmp/lease_dump.csv"):
    """Dump leases.

    :param backend: database backend
    :type backend: str
    :param db_name: (Default value = world.f_cfg.db_name)
    :type db_name:
    :param db_user: (Default value = world.f_cfg.db_user)
    :type db_user:
    :param db_passwd: (Default value = world.f_cfg.db_passwd)
    :type db_passwd:
    :param destination_address: (Default value = world.f_cfg.mgmt_address)
    :type destination_address:
    :param out: (Default value = "/tmp/lease_dump.csv")
    :type out:
    :return:
    :rtype:
    """
    return multi_protocol_functions.lease_dump(backend, db_name, db_user, db_passwd,
                                               destination_address, out)


def lease_upload(backend, leases_file, db_name=world.f_cfg.db_name, db_user=world.f_cfg.db_user,
                 db_passwd=world.f_cfg.db_passwd, destination_address=world.f_cfg.mgmt_address):
    """Upload leases.

    :param backend: database backend
    :type backend: str
    :param leases_file:
    :type leases_file:
    :param db_name: (Default value = world.f_cfg.db_name)
    :type db_name:
    :param db_user: (Default value = world.f_cfg.db_user)
    :type db_user:
    :param db_passwd: (Default value = world.f_cfg.db_passwd)
    :type db_passwd:
    :param destination_address: (Default value = world.f_cfg.mgmt_address)
    :type destination_address:
    :return:
    :rtype:
    """
    return multi_protocol_functions.lease_upload(backend, leases_file, db_name, db_user, db_passwd,
                                                 destination_address)


def print_leases(backend='memfile', db_name=world.f_cfg.db_name, db_user=world.f_cfg.db_user,
                 db_passwd=world.f_cfg.db_passwd, destination_address=world.f_cfg.mgmt_address):
    """Print leases.

    :param backend: database backend (Default value = 'memfile')
    :type backend: str
    :param db_name: (Default value = world.f_cfg.db_name)
    :type db_name:
    :param db_user: (Default value = world.f_cfg.db_user)
    :type db_user:
    :param db_passwd: (Default value = world.f_cfg.db_passwd)
    :type db_passwd:
    :param destination_address: (Default value = world.f_cfg.mgmt_address)
    :type destination_address:
    :return:
    :rtype:
    """
    return multi_protocol_functions.print_leases(backend, db_name, db_user, db_passwd, destination_address)


def get_option(msg, opt_code):
    """Get option.

    :param msg:
    :type msg:
    :param opt_code:
    :type opt_code:
    :return:
    :rtype:
    """
    return dhcpmsg.get_option(msg, opt_code)


def get_subopt_from_option(exp_opt_code, exp_subopt_code):
    """Get suboption from option.

    :param exp_opt_code:
    :type exp_opt_code:
    :param exp_subopt_code:
    :type exp_subopt_code:
    :return:
    :rtype:
    """
    return dhcpmsg.get_subopt_from_option(exp_opt_code, exp_subopt_code)


def DO(address=None, options=None, chaddr='ff:01:02:03:ff:04', iface=None):
    """Do discover-offer.

    :param address: (Default value = None)
    :type address:
    :param options: (Default value = None)
    :type options:
    :param chaddr: (Default value = 'ff:01:02:03:ff:04')
    :type chaddr:
    :param iface: (Default value = None)
    :type iface:
    :return:
    :rtype:
    """
    return dhcpmsg.DO(address, options, chaddr, iface=iface)


def RA(address, options=None, response_type='ACK', chaddr='ff:01:02:03:ff:04',
       init_reboot=False, subnet_mask='255.255.255.0', fqdn=None, iface=None):
    """Do request-acknowledgement.

    :param address:
    :type address:
    :param options: (Default value = None)
    :type options:
    :param response_type: (Default value = 'ACK')
    :type response_type:
    :param chaddr: (Default value = 'ff:01:02:03:ff:04')
    :type chaddr:
    :param init_reboot: (Default value = False)
    :type init_reboot:
    :param subnet_mask: (Default value = '255.255.255.0')
    :type subnet_mask:
    :param fqdn: (Default value = None)
    :type fqdn:
    :param iface: (Default value = None)
    :type iface:
    :return:
    :rtype:
    """
    return dhcpmsg.RA(address, options, response_type, chaddr, init_reboot, subnet_mask, fqdn, iface=iface)


def DORA(address=None, options=None, exchange='full', response_type='ACK', chaddr='ff:01:02:03:ff:04',
         init_reboot=False, subnet_mask='255.255.255.0', fqdn=None, iface=None):
    """Do DORA.

    :param address: (Default value = None)
    :type address:
    :param options: (Default value = None)
    :type options:
    :param exchange: (Default value = 'full')
    :type exchange:
    :param response_type: (Default value = 'ACK')
    :type response_type:
    :param chaddr: (Default value = 'ff:01:02:03:ff:04')
    :type chaddr:
    :param init_reboot: (Default value = False)
    :type init_reboot:
    :param subnet_mask: (Default value = '255.255.255.0')
    :type subnet_mask:
    :param fqdn: (Default value = None)
    :type fqdn:
    :param iface: (Default value = None)
    :type iface:
    :return:
    :rtype:
    """
    return dhcpmsg.DORA(address, options, exchange, response_type, chaddr, init_reboot, subnet_mask, fqdn, iface=iface)


def check_IA_NA(address, status_code=None, expect=True):
    """check_IA_NA.

    :param address:
    :type address:
    :param status_code: (Default value = None)
    :type status_code:
    :param expect: (Default value = True)
    :type expect:
    :return:
    :rtype:
    """
    return dhcpmsg.check_IA_NA(address, status_code, expect)


def check_IA_PD(prefix, status_code=None, expect=True):
    """check_IA_PD.

    :param prefix:
    :type prefix:
    :param status_code: (Default value = None)
    :type status_code:
    :param expect: (Default value = True)
    :type expect:
    :return:
    :rtype:
    """
    return dhcpmsg.check_IA_PD(prefix, status_code, expect)


def SA(address=None, delegated_prefix=None, relay_information=False,
       status_code_IA_NA=None, status_code_IA_PD=None,
       duid='00:03:00:01:f6:f5:f4:f3:f2:01', iaid=None,
       linkaddr='2001:db8:1::1000', ifaceid='port1234',
       vendor=None):
    """Do solicit-advertisement.

    :param address: (Default value = None)
    :type address:
    :param delegated_prefix: (Default value = None)
    :type delegated_prefix:
    :param relay_information: (Default value = False)
    :type relay_information:
    :param status_code_IA_NA: (Default value = None)
    :type status_code_IA_NA:
    :param status_code_IA_PD: (Default value = None)
    :type status_code_IA_PD:
    :param duid: (Default value = '00:03:00:01:f6:f5:f4:f3:f2:01')
    :type duid:
    :param iaid: (Default value = None)
    :type iaid:
    :param linkaddr: (Default value = '2001:db8:1::1000')
    :type linkaddr:
    :param ifaceid: (Default value = 'port1234')
    :type ifaceid:
    :param vendor: (Default value = None)
    :type vendor:
    :return:
    :rtype:
    """
    return dhcpmsg.SA(address, delegated_prefix, relay_information,
                      status_code_IA_NA, status_code_IA_PD,
                      duid, iaid,
                      linkaddr, ifaceid, vendor)


def SARR(address=None, delegated_prefix=None, relay_information=False,
         status_code_IA_NA=None, status_code_IA_PD=None, exchange='full',
         duid='00:03:00:01:f6:f5:f4:f3:f2:01', iaid=None,
         linkaddr='2001:db8:1::1000', ifaceid='port1234', iface=None,
         vendor=None):
    """Do SARR.

    :param address: (Default value = None)
    :type address:
    :param delegated_prefix: (Default value = None)
    :type delegated_prefix:
    :param relay_information: (Default value = False)
    :type relay_information:
    :param status_code_IA_NA: (Default value = None)
    :type status_code_IA_NA:
    :param status_code_IA_PD: (Default value = None)
    :type status_code_IA_PD:
    :param exchange: (Default value = 'full')
    :type exchange:
    :param duid: (Default value = '00:03:00:01:f6:f5:f4:f3:f2:01')
    :type duid:
    :param iaid: (Default value = None)
    :type iaid:
    :param linkaddr: (Default value = '2001:db8:1::1000')
    :type linkaddr:
    :param ifaceid: (Default value = 'port1234')
    :type ifaceid:
    :param iface: (Default value = None)
    :type iface:
    :param vendor: (Default value = None)
    :type vendor:
    :return:
    :rtype:
    """
    return dhcpmsg.SARR(address, delegated_prefix, relay_information,
                        status_code_IA_NA, status_code_IA_PD, exchange,
                        duid, iaid, linkaddr, ifaceid, iface, vendor)


def BOOTP_REQUEST_and_BOOTP_REPLY(address: str,
                                  chaddr: str = 'ff:01:02:03:ff:04',
                                  client_id: str = None):
    """BOOTP_REQUEST_and_BOOTP_REPLY.

    :param address: str:
    :type address: str:
    :param chaddr: str: (Default value = 'ff:01:02:03:ff:04')
    :type chaddr: str:
    :param client_id: str: (Default value = None)
    :type client_id: str:
    :return:
    :rtype:
    """
    return dhcpmsg.BOOTP_REQUEST_and_BOOTP_REPLY(address=address,
                                                 chaddr=chaddr,
                                                 client_id=client_id)


def get_address_facing_remote_address(addr: str = world.f_cfg.mgmt_address):
    """Get address of an interface that is facing other address in forge setup.

    :param addr: ip address of remote system
    :type addr: str:
    :return: string, local ip address
    :rtype:
    """
    addr = test_define_value(addr)[0]
    return multi_protocol_functions.get_address_of_local_vm(addr)


def start_fuzzing():
    """Initialize any variables that may be used in fuzz tests."""
    world.fuzzing = True
    # [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
    seed = random.randint(0, 100)  # nosec B311
    print(f'Using seed {seed}.')
    random.seed(seed)
    world.coin_toss = random.randint(1, 100) % 2 == 0  # nosec B311


def enable_tcpdump(file_name: str = "my_capture.pcap", iface: str = None,
                   port_filter: str = None, location: str = 'local'):
    """Start tcpdump process, can be enabled on local system or remote, with custom port filtering.

    Example how to use entire set of tcpdump commands:
    srv_msg.enable_tcpdump(file_name='abc.pcap', location=world.f_cfg.mgmt_address, port_filter='port 53')
    <send traffic>
    srv_msg.kill_tcpdump(location=world.f_cfg.mgmt_address)
    srv_msg.download_tcpdump_capture(location=world.f_cfg.mgmt_address, file_name='abc.pcap')

    :param file_name: name of capture file, default is capture.pcap so please don't use it
    :type file_name: str
    :param iface: network interface on which tcpdump will be enabled
    :type iface: str
    :param port_filter: port filter (e.g. 'port 53' or 'port 8080 or port 8000' by default it will filter
        out everything except dhcp ports and dns
    :type port_filter: str
    :param location: local for system on which forge is running, or ip address of any system that is used during test
    :type location: str
    """
    start_tcpdump(file_name=file_name, iface=iface, port_filter=port_filter, location=location)


def kill_tcpdump(location: str = 'local'):
    """Stop tcpdump instances running on system.

    :param location: local for system on which forge is running, or ip address of any system that is used during test
    :type location: str:
    """
    stop_tcpdump(location=location)


def get_tcpdump_capture(location, file_name):
    """Download capture files to tests results.

    :param location: ip address of remote system on which tcpdump was enabled
    :type location:
    :param file_name: name of capture file
    :type file_name:
    """
    download_tcpdump_capture(location=location, file_name=file_name)


def tcp_messages_include(**kwargs):
    """tcp_messages_include.

    :param kwargs:
    :type kwargs:
    """
    dhcpmsg.tcp_messages_include(**kwargs)


def tcp_get_message(**kwargs):
    """tcp_get_message.

    :param kwargs:
    :type kwargs:
    :return:
    :rtype:
    """
    return dhcpmsg.tcp_get_message(**kwargs)


def send_over_tcp(msg, address=None, port=None, parse=False, number_of_connections=1, print_all=True):
    """Send over TCP.

    :param msg:
    :type msg:
    :param address: (Default value = None)
    :type address:
    :param port: (Default value = None)
    :type port:
    :param parse: (Default value = False)
    :type parse:
    :param number_of_connections: (Default value = 1)
    :type number_of_connections:
    :param print_all: (Default value = True)
    :type print_all:
    :return:
    :rtype:
    """
    return dhcpmsg.send_over_tcp(msg, address=address, port=port, parse=parse,
                                 number_of_connections=number_of_connections, print_all=print_all)


def check_if_address_belongs_to_subnet(subnet: str = None, address: str = None):
    """Check if address belongs to subnet. Accepts v4 and v6.

    :param subnet: subnet definition e.g. '2001:db8:1::/64'
    :type subnet: str:
    :param address: ip address e.g. '2001:db8:2::1'
    :type address: str:
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


def create_db_dump(database: str, db_name: str = world.f_cfg.db_name,
                   db_user: str = world.f_cfg.db_user, db_password: str = world.f_cfg.db_passwd,
                   destination_address=world.f_cfg.mgmt_address, file_name=None):
    """Create database dump.

    :param database: str:
    :type database: str:
    :param db_name: str: (Default value = world.f_cfg.db_name)
    :type db_name: str:
    :param db_user: str: (Default value = world.f_cfg.db_user)
    :type db_user: str:
    :param db_password: str: (Default value = world.f_cfg.db_passwd)
    :type db_password: str:
    :param destination_address: (Default value = world.f_cfg.mgmt_address)
    :type destination_address:
    :param file_name: (Default value = None)
    :type file_name:
    """
    multi_protocol_functions.create_db_dump(database, db_name, db_user, db_password, destination_address, file_name)


def restore_db_from_dump(database: str, db_name: str = None,
                         db_user: str = None, db_password: str = world.f_cfg.db_passwd,
                         destination_address=world.f_cfg.mgmt_address, file_name=None):
    """Restore database from dump.

    :param database: str:
    :type database: str:
    :param db_name: str: (Default value = None)
    :type db_name: str:
    :param db_user: str: (Default value = None)
    :type db_user: str:
    :param db_password: str: (Default value = world.f_cfg.db_passwd)
    :type db_password: str:
    :param destination_address: (Default value = world.f_cfg.mgmt_address)
    :type destination_address:
    :param file_name: (Default value = None)
    :type file_name:
    """
    multi_protocol_functions.restore_db_from_dump(database, db_name, db_user, db_password, destination_address, file_name)
