from lettuce import world, step
from init_all import SOFTWARE_UNDER_TEST
import importlib

dhcpfun = importlib.import_module("softwaresupport.%s.functions"  % SOFTWARE_UNDER_TEST)


@step('Client is started.')
def config_srv_subnet(step):
   dhcpfun.start_clnt()