from lettuce import world, step
import importlib
dhcpfun = importlib.import_module("serversupport.%s.functions"  % (world.cfg["server_type"])) 


@step('Server is configured with (\S+) subnet with (\S+) pool.')
def config_srv_subnet(step, subnet, pool):
    """
    Adds server configuration with specified subnet and pool.
    subnet may define specific subnet or use the word "default"
    pool may define specific pool range or use the word "default"
    """
    if (not "conf" in world.cfg):
        world.cfg["conf"] = ""
    dhcpfun.prepare_cfg_subnet(step, subnet, pool)
    
@step('Server is configured with (\S+) option with value (\S+).')
def config_srv_opt(step, option_name, option_value):
    dhcpfun.prepare_cfg_add_option(step, option_name, option_value)


