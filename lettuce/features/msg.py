from lettuce import world, step
from init_all import PROTO
import importlib

# Tomek: For some reason importing terrain does not help, as the
# @before.each_scenario is not called, so the world do not have proto set up.
# Therefore I imported PROTO constant and use it directly. It's a hack, but it
# works. If you know how to fix is properly, plese do so.

dhcpmsg = importlib.import_module("protosupport.%s.msg"  % (PROTO))

##building messages 
@step('Client requests option (\d+).')
def client_requests_option(step, opt_type):
    dhcpmsg.client_requests_option(step, opt_type)

@step('Client sends (\w+) message( with (\w+) option)?')
def client_send_msg(step, msgname, opt_type, unknown):
    dhcpmsg.client_send_msg(step, msgname, opt_type, unknown)

@step('Client does (NOT )?include (\S+).')
def client_does_include(step, yes_or_not, opt_type):
    dhcpmsg.client_does_include(step, opt_type)

@step('Client chooses UNICAST address.')
def unicast_addres(step):
    dhcpmsg.unicast_addres(step)

@step('Generate new client-id.')
def new_client_id(step):
    dhcpmsg.new_client_id(step)

@step('...using relay-agent encapsulated in (\d+) level(s)?.')
def create_relay_forward(step, level, s ):
    dhcpmsg.create_relay_forward(step, level)

##checking respond
@step('Server MUST (NOT )?respond with (\w+) message')
def send_wait_for_message(step, yes_or_no, message):
    get_common_logger().debug("client_send_msg:{message}.\n".format(**locals()))
    presence = True if yes_or_no == None else False 
    dhcpmsg.send_wait_for_message(step, presence ,message)

@step('Response MUST (NOT )?include option (\d+).')
def response_check_include_option(step, yes_or_no, opt_code):
    include = not (yes_or_no == "NOT ")
    dhcpmsg.response_check_include_option(step, include, opt_code)

@step('Response option (\d+) MUST (NOT )?contain (\S+) (\S+).')
def response_check_option_content(step, opt_code, expect, data_type, expected):
    if str(data_type) == "message":
        dhcpmsg.response_check_include_message(step, opt_code, expect, data_type, expected)
    else:
        dhcpmsg.response_check_option_content(step, opt_code, expect, data_type, expected)

##save option from received message
@step('Client copies (\S+) option from received message.')
def client_copy_option(step, option_name):
    """
    Copied option is automatically added to next generated message, and erased.
    """
    assert len(world.srvmsg), "No messages received, nothing to copy."
    dhcpmsg.client_copy_option(step, option_name)

@step('Client save (\S+) option from received message.')
def client_save_option(step, option_name):
    """
    Saved option is kept in memory till end of the test, or step 'Client adds saved option'
    """
    assert len(world.srvmsg), "No messages received, nothing to copy."
    dhcpmsg.client_save_option(step, option_name)

@step('Client adds saved options.')
def client_add_saved_option(step):
    assert len(world.srvmsg), "No messages received, nothing to copy."
    dhcpmsg.client_add_saved_option(step)
    
##modification of the test run
@step('Pause the Test.')
def test_pause(step):
    """
    Pause the test for any reason. Press any key to continue.
    """
    dhcpmsg.test_pause(step)
