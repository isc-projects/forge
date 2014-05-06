from lettuce import world, step
from init_all import SOFTWARE_UNDER_TEST
import importlib

clntFunc = importlib.import_module("softwaresupport.%s.functions"  % SOFTWARE_UNDER_TEST)


@step("Setting up test.")
def client_setup(step):
    clntFunc.client_setup(step)

@step('Client is started.')
def config_srv_subnet(step):
   clntFunc.start_clnt(step)

@step("Client is configured to request (\S+) option.")
def client_option_req(step, opt):
    clntFunc.client_option_req(step, opt)
