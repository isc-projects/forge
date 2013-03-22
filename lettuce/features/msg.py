from lettuce import world, step
import importlib
dhcpmsg = importlib.import_module("protosupport.%s.msg"  % (world.proto)) 

@step('Client requests option (\d+).')
def client_requests_option(step, opt_type):
    dhcpmsg.client_requests_option(step, opt_type)

@step('Client sends (\w+) message( with (\w+) option)?')
def client_send_msg(step, msgname, opt_type, unknown):
    dhcpmsg.client_send_msg(step, msgname, opt_type, unknown)

@step('Server MUST respond with (\w+) message')
def send_wait_for_message(step, message):
    dhcpmsg.send_wait_for_message(step, message)

@step('Response MUST (NOT )?include option (\d+).')
def response_check_include_option(step, yes_or_no, opt_code):
    include = not (yes_or_no == "NOT ")
    dhcpmsg.response_check_include_option(step, include, opt_code)

@step('Response option (\d+) MUST (NOT )?contain (\S+) (\S+).')
def response_check_option_content(step, opt_code, expect, data_type, expected):
    dhcpmsg.response_check_option_content(step, opt_code, expect, data_type, expected)
