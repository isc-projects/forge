from lettuce import world, step
from init_all import SERVER_TYPE
import importlib
dhcpfun = importlib.import_module("serversupport.%s.functions"  % (SERVER_TYPE))

def test_define_value(*args):
    """
    Designed to use in test scenarios values from ini_all.py file. To makes them even more portable
    You can use steps like:
		Client download file from server stored in: $SERVER_SETUP_DIRother_dir/my_file
	or 
		Client removes file from server located in: $SERVER_INSTALL_DIRmy_file

    $ sign is very important without it Forge wont find variable in init_all.

    There is no slash ("/") between $SERVER_INSTALL_DIR and my_file because variable $SERVER_INSTALL_DIR
    should end with slash.

    You can use any variable form init_all in that way. Also you can add them using step:
	"Client defines new variable: (\S+) with value (\S+)."

    """
    tested_args = []
    for i in range(len(args)):
        tmp = str(args[i])
        if tmp[0] == "$":#r'[\W_]+'
            counter = 1
            variable = ""
            flag = True
            for i in range(len(tmp)):
                if tmp[i] == "$":
                    continue
                if tmp[i].isupper() or tmp[i] == "_" or tmp[i].isdigit() and flag:
                    variable += tmp[i]
                    counter += 1
                else:
                    flag = False
            try:
                imported = getattr(__import__('init_all', fromlist = [variable]), variable)
            except:
                assert False, "No variable in init_all.py named: " + variable
            print imported+tmp[counter:]
            tested_args.append(imported+tmp[counter:])
        else:
            tested_args.append(args[i]) 
    return tested_args
        
##server configurations
@step('Server is configured with (\S+) subnet with (\S+) pool.')
def config_srv_subnet(step, subnet, pool):
    """
    Adds server configuration with specified subnet and pool.
    subnet may define specific subnet or use the word "default"
    pool may define specific pool range or use the word "default"

    Setting subnet in that way, will cause to set in on interface you set in 
    init_all.py as variable "SERVER_IFACE" leave it to None if you don want to set 
    interface.
    """
    #subnet, pool = test_define_value( subnet, pool)
    dhcpfun.prepare_cfg_subnet(step, subnet, pool)

@step('Server is configured with another subnet: (\S+) with (\S+) pool on interface (\S+).')
def config_srv_another_subnet(step, subnet, pool, interface):
    """
    Add another subnet with specified subnet/pool/interface.
    """
    if SERVER_TYPE in ['dibbler', 'isc_dhcp4', 'isc_dhcp6']:
        assert False, "Test temporary available only for Kea servers."
    #subnet, pool, interface = test_define_value( subnet, pool, interface)
    dhcpfun.config_srv_another_subnet(step, subnet, pool, interface)

@step('Server is configured with another subnet: (\S+) with (\S+) pool.')
def config_srv_another_subnet_no_interface(step, subnet, pool):
    """
    Add another subnet to config file without interface specified.
    """
    if SERVER_TYPE in ['dibbler', 'isc_dhcp4', 'isc_dhcp6']:
        assert False, "Test temporary available only for Kea servers."
    #subnet, pool = test_define_value( subnet, pool)
    dhcpfun.config_srv_another_subnet(step, subnet, pool, None)

@step('Server is configured with (\S+) prefix in subnet (\d+) with (\d+) prefix length and (\d+) delegated prefix length.')#  
def config_srv_prefix(step, prefix, subnet, length, delegated_length ):
    """
    Adds server configuration with specified prefix.
    """
    #prefix, length, delegated_length, subnet = test_define_value(prefix, length, delegated_length, subnet)
    dhcpfun.prepare_cfg_prefix(step, prefix, length, delegated_length, subnet)
    
@step('Server is configured with (\S+) option with value (\S+).')
def config_srv_opt(step, option_name, option_value):
    """
    Add to configuration options like: preference, dns servers..
    This step causes to set in to main space!
    """
    #option_name, option_value = test_define_value( option_name, option_value)
    dhcpfun.prepare_cfg_add_option(step, option_name, option_value, 'dhcp6')

@step('On space (\S+) server is configured with (\S+) option with value (\S+).')
def config_srv_opt_space(step, space, option_name, option_value):
    """
    Add to configuration options like: preference, dns servers.. but you can specify
    to which space should that be included. 
    """
    #option_name, option_value, space = test_define_value(option_name, option_value, space)
    dhcpfun.prepare_cfg_add_option(step, option_name, option_value, space)

@step('Server is configured with custom option (\S+)/(\d+) with type (\S+) and value (\S+).')
def config_srv_custom_opt(step, opt_name, opt_code, opt_type, opt_value):
    """
    Prepare server configuration with the specified custom option.
    opt_name name of the option, e.g. foo
    opt_code code of the option, e.g. 100
    opt_type type of the option, e.g. uint8 (see bind10 guide for complete list)
    opt_value value of the option, e.g. 1
    """
    #opt_name, opt_code, opt_type, opt_value = test_define_value(opt_name, opt_code, opt_type, opt_value)
    dhcpfun.prepare_cfg_add_custom_option(step, opt_name, opt_code, opt_type, opt_value, 'dhcp6')

@step('On space (\S+) server is configured with a custom option (\S+)/(\d+) with type (\S+) and value (\S+).')
def config_srv_custom_opt_space(step, space, opt_name, opt_code, opt_type, opt_value):
    """
    Same step like ............. but specify that option on different space then main.
    """
    #opt_name, opt_code, opt_type, opt_value, space = test_define_value(opt_name, opt_code, opt_type, opt_value, space)
    dhcpfun.prepare_cfg_add_custom_option(step, opt_name, opt_code, opt_type, opt_value, space)

@step('Time (\S+) is configured with value (\d+).')
def set_time(step, which_time, value):
    """
    Change values of T1, T2, preffered lifetime and valid lifetime.
    """
    #which_time, value = test_define_value(which_time, value)
    dhcpfun.set_time(step, which_time, value)

@step('Run configuration command: (.+)')
def run_command(step, command):
    """
    Add single line to configuration, there is no validation within this step.
    Be aware what you are putting this and in what moment. If you use that
    I recommend set variable "SAVE_CONFIG_FILES" to True.
    
    Includes everything after "command: " to the end of the line.
    """
    dhcpfun.run_command(step, command)
    
##subnet options
@step('Server is configured with (\S+) option in subnet (\d+) with value (\S+).')
def config_srv(step, option_name, subnet, option_value):
    """
    Prepare server configuration with the specified option.
    option_name name of the option, e.g. dns-servers (number may be used here)
    option_value value of the configuration
    """
    #option_name, subnet, option_value = test_define_value(option_name, subnet, option_value)
    dhcpfun.prepare_cfg_add_option_subnet(step, option_name, subnet, option_value)

##server management
@step('(Server is started.)|(Server failed to start. During (\S+) process.)')
def start_srv(step, started , failed, process):
    """
    Decide which you want, start server of failed start (testing incorrect configuration)
    Also decide in which part should it failed.
    """
    # pass True for 'Server is started' and False for 'Server failed to start.'
    start = True if started is not None else False
    dhcpfun.start_srv(start, process)

@step('Restart server.')
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
    
