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

@step("Client is configured to include (another )?(\S+) option.")
def client_option_req(step, another, opt):
    another1 = not (another == "another ")
    clntFunc.client_option_req(step, another1, opt)

@step("Restart client.")
def client_restart(step):
    clntFunc.restart_clnt(step)

@step("Client MUST (NOT )?use prefix with values given by server.")
def client_parse_config(step, yes_no):
    contain = not (yes_no == "NOT ")
    clntFunc.client_parse_config(step, contain)
