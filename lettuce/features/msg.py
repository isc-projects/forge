# Copyright (C) 2013 Internet Systems Consortium.
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

from init_all import PROTO
from lettuce import world, step
import importlib

# Tomek: For some reason importing terrain does not help, as the
# @before.each_scenario is not called, so the world do not have proto set up.
# Therefore I imported PROTO constant and use it directly. It's a hack, but it
# works. If you know how to fix is properly, plese do so.

dhcpmsg = importlib.import_module("protosupport.%s.msg"  % (PROTO))
other = importlib.import_module("protosupport.multi_protocol_functions")

from srv_control import test_define_value 

##building messages 
@step('Client requests option (\d+).')
def client_requests_option(step, opt_type):
    """
    Add Option: Request Option with requested option code
    """
    dhcpmsg.client_requests_option(step, opt_type)

@step('Client sets (\w+) value to (\S+).')
def client_sets_value(step, value_name, new_value):
    """
    User can set values like: address, T1 or DUID to make test scenario 
    more accurate.
    """
    dhcpmsg.client_sets_value(step, value_name, new_value)

@step('Through (\S+) interface to address (\S+) client sends (\w+) message.')
def client_send_msg_via_interface(step, iface, addr, msgname):
    """
    This step actually build message (e.g. SOLICIT) with all details
    specified in steps like:
    Client sets (\w+) value to (\S+).
    Client does include (\S+).
    and others..
    Message builded here will be send in step: Server must response with...
    """
    msgname, iface, addr = test_define_value(msgname, iface, addr)
    dhcpmsg.client_send_msg(step, msgname, iface, addr)

@step('Client sends (\w+) message.')
def client_send_msg(step, msgname):
    """
    This step actually build message (e.g. SOLICIT) with all details
    specified in steps like:
	Client sets (\w+) value to (\S+).
	Client does include (\S+).
	and others..
    Message builded here will be send in step: Server must response with...
    Message will be send via interface set in init_all.py marked as IFACE.
    """
    dhcpmsg.client_send_msg(step, msgname, None, None)

@step('Client does (NOT )?include (\S+).')
def client_does_include(step, yes_or_not, opt_type):
    """
    You can choose to include options to message (support for every option listed
    in RFC 3315 and more) or to not include options like IA_NA or client_id.
    """
    dhcpmsg.client_does_include(step, opt_type, None)

@step('Client does (NOT )?include (\S+) with value (\S+).')
def client_does_include_with_value(step, yes_or_not, opt_type, value):
    """
    You can choose to include options to message (support for every option listed
    in RFC 3315 and more) or to not include options like IA_NA or client_id.
    """
    dhcpmsg.client_does_include(step, opt_type, value)


@step('Client chooses (GLOBAL)|(LINK_LOCAL) UNICAST address.')
def unicast_addres(step, addr_type, addr_type2):
    """
    Message can be send on 3 different addresses:
	- multicast for DHCPv6
	- unicast global address of the server
	- unicast local address of the server
    Proper configuration in ini_all.py required.
    """
    # send true when GLOBAL and False when LINK_LOCAL
    dhcpmsg.unicast_addres(step, True if addr_type else False)

@step('Generate new (\S+).')
def generate_new(step, opt):
    """
    For some test scenarios there is a need for multiple different users, in this step you can 
    choose which value needs to be changed:
	for client_id and IA: client
	for client_id only: Client_ID
	for IA: IA
	for IA_PD: IA_PD
    """
    dhcpmsg.generate_new(step,opt)

@step('...using relay-agent encapsulated in (\d+) level(s)?.')
def create_relay_forward(step, level, s ):
    """
    This step is strictly related to step: Client sends message.
    You can put only after that step. They can be seperated with other steps
    which causes to change values/include options

    This step causes to encapsulate builded message in RELAY FORWARD. 
    It makes possible testing RELAY-REPLY messages.
    """
    dhcpmsg.create_relay_forward(step, level)
    
@step('Client adds suboption for vendor specific information with code: (\d+) and data: (\w+).')
def add_vendor_suboption(step, code, data):
    """
    After adding Vendor Specific Option we can deside to add suboptions to it. Please make sure which are
    supported and if it's nececary add suboption by youself.
    """
    dhcpmsg.add_vendor_suboption(step, int(code), data)

##checking respond
@step('Server MUST NOT respond.')
def send_wait_for_message(step):
    """
    This step causes to send message in cases when we don't expect any response.
    Step used only for v4 testing
    """
    dhcpmsg.send_wait_for_message(step, "MUST", False, "None")

@step('Server (\S+) (NOT )?respond with (\w+) message.')
def send_wait_for_message(step, type, yes_or_no, message):
    """
    This step causes to send message to server and capture respond. 
    """
    presence = True if yes_or_no == None else False 
    dhcpmsg.send_wait_for_message(step, type, presence, message)

@step('Response MUST (NOT )?include option (\d+).')
def response_check_include_option(step, yes_or_no, opt_code):
    """
    Use this step for parsing respond. For more details please read manual section "Parsing respond"
    """
    include = not (yes_or_no == "NOT ")
    dhcpmsg.response_check_include_option(step, include, opt_code)

@step('Response MUST (NOT )?contain (\S+) (\S+).')
def response_check_content(step, expect, data_type, expected):
    """
    """
    dhcpmsg.response_check_content(step, expect, data_type, expected)

@step('Response option (\d+) MUST (NOT )?contain (\S+) (\S+).')
def response_check_option_content(step, opt_code, expect, data_type, expected):
    """
    Detailed parsing of received option. For more details please read manual section "Parsing respond"
    """
    data_type, expected = test_define_value (data_type, expected)
    dhcpmsg.response_check_option_content(step, 0, opt_code, expect, data_type, expected)
        
@step('Response sub-option (\d+) from option (\d+) MUST (NOT )?contain (\S+) (\S+).')
def response_check_suboption_content(step, subopt_code, opt_code, yes_or_no, data_type, expected):
    """
    Some options can include suboptions, we can test them too.
    For more details please read manual section "Parsing respond"
    """
    expect = not (yes_or_no == "NOT ")
    dhcpmsg.response_check_option_content(step, subopt_code, opt_code, expect, data_type, expected)


@step('Test (\S+) content.')
def test_content(step, test_value):
    """
    Temporary unavailable
    """
    pass
    #dhcpmsg.test_content(test_value)

##save option from received message
@step('Client copies (\S+) option from received message.')
def client_copy_option(step, option_name):
    """
    When we need to send the same option back to server (e.g. Server ID) we can use this step.
    Copied option is automatically added to next generated message, and erased.
    """
    assert len(world.srvmsg), "No messages received, nothing to copy."
    dhcpmsg.client_copy_option(step, option_name)

@step('Client saves (\S+) option from received message.')
def client_save_option(step, option_name):
    """
    In time we need to include one option more then one time in different messages, we can
    choose to save it in memory. Memory will be erased at the end of the test, or when we 
    decide to clear it in step "Client adds saved options. And erase.
    """
    assert len(world.srvmsg), "No messages received, nothing to save."
    dhcpmsg.client_save_option(step, option_name)

@step('Client adds saved options. And (DONT )?Erase.')
def client_add_saved_option(step, yes_or_no):
    """
    This step causes to include saved options to message. Also we can decide to keep or clear 
    memory.
    """
    assert len(world.savedmsg), "No options to add."
    erase = True if yes_or_no == None else False
    dhcpmsg.client_add_saved_option(step, erase)

@step('Save (\S+) value from (\d+) option.')
def save_value_from_option(step, value_name, option_name):
    """
    This step can be used to save value of some option field for
    further usage. It's like client_save_option step, but only for
    one specific field of given option.
    """
    dhcpmsg.save_value_from_option(step, value_name, option_name)

@step('Received (\S+) value in option (\d+) is the same as saved value.')
def compare_values(step, value_name, option_name):
    """
    If you have used step save_value_from_option, then this step will
    compare the earlier saved value with the recent received value.
    Note that names of fields that values are being compared should
    be the same.
    """
    dhcpmsg.compare_values(step, value_name, option_name)
    
##other
@step('Pause the Test.')
def test_pause(step):
    """
    Pause the test for any reason. Very good to debug problems. Checking server configuration
    and so on.... Do NOT put it in automatic tests, it blocks test until user will:  
    	Press any key to continue.
    """
    other.test_pause(step)

@step('Client download file from server stored in: (\S+).')
def copy_remote(step, remote_path):
    """
    Download file from remote server. It is stored in test directory.
    And named "downloaded_file"
    """
    remote_path = test_define_value(remote_path)[0]
    other.copy_file_from_server(step, remote_path)

@step('Client compares downloaded file from server with local file stored in: (\S+).')
def compare_file(step, remote_path):
    """
    Compare two files, our local and "downloaded_file".
    """
    remote_path = test_define_value(remote_path)[0]
    other.compare_file(step, remote_path)

@step('Downloaded file MUST (NOT )?contain line: (.+)')
def file_includes_line(step, condition, line):
    """
    Check if downloaded file includes line.
    Be aware that tested line is every thing after "line: " until end of the line.
    """
    line = test_define_value(line)[0]
    other.file_includes_line(step, condition, line)

@step('Client sends local file stored in: (\S+) to server, to location: (\S+).')
def send_file_to_server(step, local_path, remote_path):
    """
    If you need send some file to server, use that step.
    """
    local_path, remote_path = test_define_value(local_path, remote_path)
    other.send_file_to_server(step, local_path, remote_path)

@step('Client removes file from server located in: (\S+).')
def remove_file_from_server(step, remote_path):
    """
    If you need to remove file from a server, please do so.
    """
    remote_path = test_define_value(remote_path)[0]
    other.remove_file_from_server(step, remote_path)

@step('User define temporary variable: (\S+) with value (\S+).')
def add_variable_temporary(step, variable_name, variable_val):
    """
    User can define his own variable, that can be called from any place in test scenario,
    by $(variable_name). Allowed signs in variable name are: capitalized letters and '_'.
    
    Temporary variable will be stored in world.define and cleared at the end of scenario.
    """
    other.add_variable(step, variable_name, variable_val, 0)

@step('User define permanent variable: (\S+) with value (\S+).')
def add_variable_permanent(step, variable_name, variable_val):
    """
    User can define his own variable, that can be called from any place in test scenario,
    by $(variable_name). Allowed signs in variable name are: capitalized letters and '_'.
    
    Permanent variable will be placed at the end of the init_all.py file. It won't be removed.
    User can do so by removing it from file.
    """
    other.add_variable(step, variable_name, variable_val, 1)
    
@step('Let us celebrate this SUCCESS!')
def test_victory(step):
    """
    Use your imagination.
    """
    other.user_victory(step)
