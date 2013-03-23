from lettuce import world, before
from scapy.config import conf

# Defines server type. Supported values are: isc-dhcp4, isc-dhcp6, kea4, kea6, dibbler
SERVER_TYPE="kea4"
PROTO = "v4"

# Defines name of the interface
IFACE="eth2"

SRV4_ADDR = "192.168.56.2"
REL4_ADDR = "192.168.56.3"

@before.each_scenario
def initialize(scenario):    
    world.climsg = []  # Message(s) to be sent
    world.cfg = {}
    world.cfg["iface"] = IFACE
    world.cfg["server_type"] = SERVER_TYPE    
    world.cfg["srv4_addr"] = SRV4_ADDR
    world.cfg["rel4_addr"] = REL4_ADDR
    world.cfg["cfg_file"] = "server.cfg"
    world.proto = PROTO
    conf.iface = IFACE
    conf.checkIPaddr = False # DHCPv4 is sent from 0.0.0.0, so response matching may confuse scapy


initialize(None)