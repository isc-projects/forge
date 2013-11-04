from init_all import PROTO
from lettuce import world, step
import importlib

# Tomek: For some reason importing terrain does not help, as the
# @before.each_scenario is not called, so the world do not have proto set up.
# Therefore I imported PROTO constant and use it directly. It's a hack, but it
# works. If you know how to fix is properly, plese do so.

dhcpmsg = importlib.import_module("protosupport.%s.msg"  % (PROTO))
other = importlib.import_module("protosupport.multi_protocol_functions")

##building messages 
@step('Client requests option (\d+).')
def client_requests_option(step, opt_type):
    dhcpmsg.client_requests_option(step, opt_type)

@step('Client sets (\w+) value to (\w+).')
def client_sets_value(step, value_name, new_value):
    dhcpmsg.client_sets_value(step, value_name, new_value)

@step('Client sends (\w+) message( with (\w+) option)?')
def client_send_msg(step, msgname, opt_type, unknown):
    dhcpmsg.client_send_msg(step, msgname, opt_type, unknown)

@step('Client does (NOT )?include (\S+).')
def client_does_include(step, yes_or_not, opt_type):
    dhcpmsg.client_does_include(step, opt_type)

@step('Client chooses (GLOBAL)|(LINK_LOCAL) UNICAST address.')
def unicast_addres(step, addr_type, addr_type2):
    # send true when GLOBAL and False when LINK_LOCAL
    dhcpmsg.unicast_addres(step, True if addr_type else False)

@step('Generate new (\S+).')
def generate_new(step, opt):
    dhcpmsg.generate_new(step,opt)

@step('...using relay-agent encapsulated in (\d+) level(s)?.')
def create_relay_forward(step, level, s ):
    dhcpmsg.create_relay_forward(step, level)
    
@step('Client adds suboption for vendor specific information with code: (\d+) and data: (\w+).')
def add_vendor_suboption(step, code, data):
    dhcpmsg.add_vendor_suboption(step, int(code), data)

##checking respond
@step('Server (\S+) (NOT )?respond with (\w+) message')
def send_wait_for_message(step, type, yes_or_no, message):
    get_common_logger().debug("client_send_msg:{message}.\n".format(**locals()))
    presence = True if yes_or_no == None else False 
    dhcpmsg.send_wait_for_message(step, type, presence, message)

@step('Response MUST (NOT )?include option (\d+).')
def response_check_include_option(step, yes_or_no, opt_code):
    include = not (yes_or_no == "NOT ")
    dhcpmsg.response_check_include_option(step, include, opt_code)

@step('Response option (\d+) MUST (NOT )?contain (\S+) (\S+).')
def response_check_option_content(step, opt_code, expect, data_type, expected):
    dhcpmsg.response_check_option_content(step, 0, opt_code, expect, data_type, expected)
        
@step('Response sub-option (\d+) from option (\d+) MUST (NOT )?contain (\S+) (\S+).')
def response_check_suboption_content(step, subopt_code, opt_code, expect, data_type, expected):
    dhcpmsg.response_check_option_content(step, subopt_code, opt_code, expect, data_type, expected)

@step('Test (\S+) content.')
def test_content(step, test_value):
    dhcpmsg.test_content(test_value)

##save option from received message
@step('Client copies (\S+) option from received message.')
def client_copy_option(step, option_name):
    """
    Copied option is automatically added to next generated message, and erased.
    """
    assert len(world.srvmsg), "No messages received, nothing to copy."
    dhcpmsg.client_copy_option(step, option_name)

@step('Client saves (\S+) option from received message.')
def client_save_option(step, option_name):
    """
    Saved option is kept in memory till end of the test, or step 'Client adds saved option'
    """
    assert len(world.srvmsg), "No messages received, nothing to save."
    dhcpmsg.client_save_option(step, option_name)

@step('Client adds saved options. And (DONT )?Erase.')
def client_add_saved_option(step, yes_or_no):
    assert len(world.savedmsg), "No options to add."
    erase = True if yes_or_no == None else False
    dhcpmsg.client_add_saved_option(step, erase)
    
##other
@step('Pause the Test.')
def test_pause(step):
    """
    Pause the test for any reason. Press any key to continue.
    """
    other.test_pause(step)

@step('Client download file from server stored in: (.+)')
def copy_remote(step, remote_path):
    """
    Download file to automatic compare
    """
    other.copy_file_from_server(step, remote_path)

@step('Client compares downloaded file from server with local file stored in: (.+)')
def compare_file(step, remote_path):
    """
    Compare file 
    """
    other.compare_file(step, remote_path)
        