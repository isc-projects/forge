from lettuce import world, before


# Defines server type. Supported values are: isc-dhcp4, isc-dhcp6, kea4, kea6, dibbler
SERVER_TYPE="kea4"
PROTO = "v4"

# Defines name of the interface
IFACE="eth1"

SRV4_ADDR = "192.168.1.1"
REL4_ADDR = "192.168.1.2"
DEFAULT_SUBNET_V4 = "192.0.2.0/24"
DEFAULT_POOL_V4 = "192.0.2.1 - 192.0.2.10"

@before.each_scenario
def initialize(scenario):    
    world.climsg = []  # Message(s) to be sent
    world.cfg = {}
    world.cfg["iface"] = IFACE
    world.cfg["server_type"] = SERVER_TYPE    
    world.cfg["srv4_addr"] = SRV4_ADDR
    world.cfg["rel4_addr"] = REL4_ADDR
    world.cfg["default_subnet_v4"] = DEFAULT_SUBNET_V4
    world.cfg["default_pool_v4"] = DEFAULT_POOL_V4
    world.proto = PROTO

initialize(None)