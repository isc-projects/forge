from fabric.context_managers import settings, hide
from fabric.operations import sudo
from lettuce import world, before, after
from scapy.config import conf
from scapy.layers.dhcp6 import DUID_LLT
import os
import shutil
import sys
import time

# Defines server type. Supported values are: isc-dhcp4, isc-dhcp6, kea4, kea6, dibbler
SERVER_TYPE="kea6"
PROTO = "v6"

# Defines name of the interface
IFACE="eth7"

# Parameters specific to DHCPv4 tests
SRV4_ADDR = "192.168.56.2"
REL4_ADDR = "192.168.56.3"

# defines client MAC (used for DUID generation)
CLI_MAC="08:00:27:58:f1:e8"

# defines path to configuration file
CFG_FILE="kea.conf"

# In order to make sure we start all tests with a 'clean' environment,
# We perform a number of initialization steps, like restoring configuration
# files, and removing generated data files.

# This approach may not scale; if so we should probably provide specific
# initialization steps for scenarios. But until that is shown to be a problem,
# It will keep the scenarios cleaner.

# This is a list of files that are freshly copied before each scenario
# The first element is the original, the second is the target that will be
# used by the tests that need them
copylist = [ ]

# This is a list of files that, if present, will be removed before each scenario
removelist = [ ]

# When waiting for output data of a running process, use OUTPUT_WAIT_INTERVAL
# as the interval in which to check again if it has not been found yet.
# If we have waited OUTPUT_WAIT_MAX_INTERVALS times, we will abort with an
# error (so as not to hang indefinitely)
OUTPUT_WAIT_INTERVAL = 0.5
OUTPUT_WAIT_MAX_INTERVALS = 20

# This are required management information about device under test (the one that
# tested server will be running on) root privileges are required!
#ip address and port. ssh port default 22
MGMT_ADDRESS='192.168.50.50:22'
MGMT_USERNAME='root'
MGMT_PASSWORD='m'

# @todo: There were RunningProcess and RunningProcesses classes here, but they
# were removed. They were used to start and stop processes on a local machine.
# We should either use fabric directly or copy those classes over and modify
# their methods to use fabric for remote process management.

# @todo: This must be moved to serversupport/ dir.
def bind10 (host, cmd): 
    """
    Start/kill bind10
    """
    with settings(host_string=host, user=MGMT_USERNAME, password=MGMT_PASSWORD):
        with hide('running', 'stdout', 'stderr'):
            sudo(cmd, pty=True)

@before.all
def server_start():
    """
    Server starting before testing
    """
    if (SERVER_TYPE in ['kea', 'kea4', 'kea6']):
        print "--- Starting Bind:"
        try:
            #comment line below to turn off starting bind
            bind10(MGMT_ADDRESS, cmd='(rm nohup.out; nohup bind10 &); sleep 2' )
            print "----- Bind10 successfully started"
        except :
            print "----- Bind10 start failed\n\nSomething go wrong with connection\nPlease make sure it's configured properly\nIP address: %s\nMac address: %s\nNetwork interface: %s" %(MGMT_ADDRESS, CLI_MAC, IFACE)
            sys.exit()
    else:
        print "Server other than kea not implemented yet"
@before.each_scenario
def initialize(scenario):    

    world.climsg = []  # Message(s) to be sent
    world.cliopts = [] # Option(s) to be included in the next message sent
    world.srvmsg = []  # Server's response(s)

    world.cfg = {}
    world.cfg["iface"] = IFACE
    world.cfg["server_type"] = SERVER_TYPE    
    world.cfg["srv4_addr"] = SRV4_ADDR
    world.cfg["rel4_addr"] = REL4_ADDR
    world.cfg["cfg_file"] = "server.cfg"
    world.cfg["mgmt_addr"] = MGMT_ADDRESS
    world.cfg["mgmt_user"] = MGMT_USERNAME
    world.cfg["mgmt_pass"] = MGMT_PASSWORD

    world.cfg["conf"] = "" # Just empty config for now

    world.proto = PROTO

    # Setup scapy for v4
    conf.iface = IFACE
    conf.checkIPaddr = False # DHCPv4 is sent from 0.0.0.0, so response matching may confuse scapy

    # Setup scapy for v6
    conf.iface6 = IFACE
    conf.use_pcap = True

    # Setup DUID for DHCPv6 (and also for DHCPv4, see RFC4361)
    if (not hasattr(world.cfg, "cli_duid")):
        world.cfg["cli_duid"] = DUID_LLT(timeval = int(time.time()), lladdr = CLI_MAC)

    # Some tests can modify the settings. If the tests fail half-way, or
    # don't clean up, this can leave configurations or data in a bad state,
    # so we copy them from originals before each scenario
    # @todo: This should be done remotely, using fabric or something similar
    for item in copylist:
        shutil.copy(item[0], item[1])

    for item in removelist:
        if os.path.exists(item):
            os.remove(item)

initialize(None)

@after.each_scenario
def cleanup(scenario):
    """
    Global cleanup for each scenario.
    """
    
@after.all
def say_goodbye(total):
    """
    Server stopping after whole work
    """
    print "%d of %d scenarios passed." % (
        total.scenarios_passed,
        total.scenarios_ran
    )

    bind10(MGMT_ADDRESS, cmd='pkill -f b10-*' )

    print "Goodbye."
