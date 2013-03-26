from lettuce import world
from textwrap import dedent
from lettuce import world

def prepare_cfg_subnet(step, subnet, pool):

    # subnet defintion Kea4
    subnetcfg ='''\
    config add Dhcp4/subnet4
    config set Dhcp4/subnet4[0]/subnet "{subnet}"
    config set Dhcp4/subnet4[0]/pool [ "{pool}" ]
    config commit\n
    '''.format(**locals())
    
    world.cfg["conf"] += dedent(subnetcfg) 


kea_options4= { "subnet-mask": 1,
                 "routers": 3,
                 "name-servers": 5, # ipv4-address (array)
                 "domain-name-servers": 6, # ipv4-address (array)
                 "domain-name": 15, # fqdn (single)
                 "broadcast-address": 28, # ipv4-address (single)
                 "nis-domain": 40, # string (single)
                 "nis-servers": 41, # ipv4-address (array)
                 "ntp-servers": 42 # ipv4-address (array)
                 }

def prepare_cfg_add_option(step, option_name, option_value):
    if (not "conf" in world.cfg):
        world.cfg["conf"] = ""

    assert option_name in kea_options4, "Unsupported option name " + option_name
    option_code = kea_options4.get(option_name)

    if not hasattr(world, 'kea'):
        world.kea = {}
    else:
        world.kea.clear()
    world.kea["option_cnt"] = 0
    
    option_cnt=world.kea["option_cnt"]
    options = '''\
    config add Dhcp4/option-data
    config set Dhcp4/option-data[{option_cnt}]/name "{option_name}"
    config set Dhcp4/option-data[{option_cnt}]/code {option_code}
    config set Dhcp4/option-data[{option_cnt}]/space "dhcp4"
    config set Dhcp4/option-data[{option_cnt}]/csv-format true
    config set Dhcp4/option-data[{option_cnt}]/data "{option_value}"
    config commit
    '''.format(**locals())
    world.cfg["conf"] +=  dedent(options)
    world.kea["option_cnt"] += 1


def start_srv():
    print("Automatic start for Kea is not implemented yet. Please start Kea")
    print("manually and run the following config (also stored in %s):" % world.cfg["cfg_file"])
    print("------")
    print (world.cfg["conf"])

    configfile = open(world.cfg["cfg_file"], 'w')
    configfile.write(world.cfg["conf"])
    configfile.close()
    print("------")
    raw_input("Press ENTER when ready")

def restart_srv():
    # @todo: Implement this
