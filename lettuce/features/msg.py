from lettuce import world, step
from terrain import PROTO
import importlib

# Tomek: For some reason importing terrain does not help, as the
# @before.each_scenario is not called, so the world do not have proto set up.
# Therefore I imported PROTO constant and use it directly. It's a hack, but it
# works. If you know how to fix is properly, plese do so.

dhcpmsg = importlib.import_module("protosupport.%s.msg"  % (PROTO))

@step('Client requests option (\d+).')
def client_requests_option(step, opt_type):
    dhcpmsg.client_requests_option(step, opt_type)

@step('Client sends (\w+) message( with (\w+) option)?')
def client_send_msg(step, msgname, opt_type, unknown):
    dhcpmsg.client_send_msg(step, msgname, opt_type, unknown)

@step('Server MUST (NOT )?respond with (\w+) message')
def send_wait_for_message(step, yes_or_no, message):
    print "client_send_msg:{message}.\n".format(**locals())
    presence = True if yes_or_no == None else False 
    dhcpmsg.send_wait_for_message(step, presence ,message)

@step('Response MUST (NOT )?include option (\d+).')
def response_check_include_option(step, yes_or_no, opt_code):
    include = not (yes_or_no == "NOT ")
    dhcpmsg.response_check_include_option(step, include, opt_code)

@step('Response option (\d+) MUST (NOT )?contain (\S+) (\S+).')
def response_check_option_content(step, opt_code, expect, data_type, expected):
    dhcpmsg.response_check_option_content(step, opt_code, expect, data_type, expected)

@step('Client copies (\S+) option from received message.')
def client_copy_option(step, option_name):
    assert len(world.srvmsg), "No messages received, nothing to copy."

    dhcpmsg.client_copy_option(step, option_name)

@step('Client does NOT include (\S+).')
def client_doesnt_include(step, opt_type):
    dhcpmsg.client_doesnt_include(step, opt_type)