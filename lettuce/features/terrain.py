from lettuce import world, before


# Defines server type. Supported values are: isc-dhcp4, isc-dhcp6, kea4, kea6, dibbler
SERVER_TYPE="kea4"
PROTO = "v4"

world.cfg = {}
world.cfg["server_type"] = SERVER_TYPE    
world.cfg["proto"] = PROTO  

@before.all
def initialize():
    world.proto = PROTO
