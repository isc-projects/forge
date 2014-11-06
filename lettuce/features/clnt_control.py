from lettuce import world, step
from init_all import SOFTWARE_UNDER_TEST, DHCP
import importlib
from terrain import declare_all

declare_all()
DNS = ""
for each_client_name in SOFTWARE_UNDER_TEST:
    if each_client_name in DHCP and "client" in each_client_name:
        dhcp = importlib.import_module("softwaresupport.%s.functions" % each_client_name)
        world.cfg["dhcp_under_test"] = each_client_name
    elif each_client_name in DNS:
        # for future use, import DNS not declare it.
        pass

@step("Setting up test.")
def client_setup(step):
    dhcp.client_setup(step)


@step('Client is started.')
def config_srv_subnet(step):
    dhcp.start_clnt(step)


@step("Client is configured to request (\S+) option.")
def client_option_req(step, opt):
    dhcp.client_option_req(step, opt)
