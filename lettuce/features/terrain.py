from lettuce import world, before


# Defines server type. Supported values are: isc-dhcp4, isc-dhcp6, kea4, kea6, dibbler
SERVER_TYPE="kea4"
PROTO = "v4"

# Defines name of the interface
IFACE="eth1"

SRV4_ADDR = "172.16.0.1"
REL4_ADDR = "172.16.0.2"

@before.each_scenario
def initialize(scenario):    
    world.climsg = []  # Message(s) to be sent
    world.cfg = {}
    world.cfg["iface"] = IFACE
    world.cfg["server_type"] = SERVER_TYPE    
    world.cfg["srv4_addr"] = SRV4_ADDR
    world.cfg["rel4_addr"] = REL4_ADDR
    world.proto = PROTO

initialize(None)