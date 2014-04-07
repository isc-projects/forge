from lettuce import world, step
from init_all import CLIENT_TYPE
import importlib

dhcpfun = importlib.import_module("clientsupport.%s.functions"  % (CLIENT_TYPE))


@step('Client testing...')
def config_srv_subnet(step):
    pass
   # dhcpfun.start_clnt()