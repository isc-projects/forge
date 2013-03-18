from lettuce import world, step
import importlib
dhcpmsg = importlib.import_module("protosupport.%s.msg"  % (world.proto)) 

@step('Client requests option (\d+).')
def client_requests_option(step, opt_type):
    dhcpmsg.client_requests_option(step, opt_type)

@step('Client sends (\w+) message( with (\w+) option)?')
def client_send_msg(step, msgname, opt_type, unknown):
    dhcpmsg.client_send_msg(step, msgname, opt_type, unknown)
