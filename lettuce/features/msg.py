from lettuce import world, step
import importlib
dhcpmsg = importlib.import_module("protosupport.%s.msg"  % (world.cfg["proto"])) 

@step('Client requests option (\d+).')
def client_requests_option(step, opt_type):
    dhcpmsg.client_requests_option(step, opt_type)
