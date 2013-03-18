from lettuce import world
import textwrap
def prepare_cfg(step, subnet, pool):

    subnetcfg =\
    '''
    # subnet defintion Kea4
    config add Dhcp4/subnet4
    config set Dhcp4/subnet4[0]/subnet "{subnet}"
    config set Dhcp4/subnet4[0]/pool "[{pool}]"
    config commit\n"
    '''.format(**locals())
    
    world.cfg["conf"] = world.cfg["conf"] + textwrap.dedent(subnetcfg) 



    