from lettuce import world, step
from init_all import SERVER_TYPE
import importlib
dhcpfun = importlib.import_module("serversupport.%s.functions"  % (SERVER_TYPE))

##server configurations
@step('Server is configured with (\S+) subnet with (\S+) pool.')
def config_srv_subnet(step, subnet, pool):
    """
    Adds server configuration with specified subnet and pool.
    subnet may define specific subnet or use the word "default"
    pool may define specific pool range or use the word "default"
    """

    dhcpfun.prepare_cfg_subnet(step, subnet, pool)
    
@step('Server is configured with (\S+) option with value (\S+).')
def config_srv_opt(step, option_name, option_value):
    dhcpfun.prepare_cfg_add_option(step, option_name, option_value)

@step('Server is configured with custom option (\S+)/(\d+) with type (\S+) and value (\S+).')
def config_srv_custom_opt(step, opt_name, opt_code, opt_type, opt_value):
    """
    Prepare server configuration with the specified custom option.
    opt_name name of the option, e.g. foo
    opt_code code of the option, e.g. 100
    opt_type type of the option, e.g. uint8 (see bind10 guide for complete list)
    opt_value value of the option, e.g. 1
    """

    dhcpfun.prepare_cfg_add_custom_option(step, opt_name, opt_code, opt_type, opt_value)

##subnet options
@step('Server is configured with (\S+) option in subnet (\d+) with value (\S+).')
def config_srv(step, option_name, subnet, option_value):
    """
    Prepare server configuration with the specified option.
    option_name name of the option, e.g. dns-servers (number may be used here)
    option_value value of the configuration
    """
    dhcpfun.prepare_cfg_add_option_subnet(step, option_name, subnet, option_value)

##server management
@step('Server is started.')
def start_srv(step):
    dhcpfun.start_srv()

@step('Server is restarted.')
def restart_srv(step):
    """
    Restart DHCPv6 without changing server configuration
    """
    dhcpfun.restart_srv()


@step('Server is stopped.')
def stop_srv(step):
    """
    For test that demands turning off server in the middle
    """
    dhcpfun.stop_srv()
    
