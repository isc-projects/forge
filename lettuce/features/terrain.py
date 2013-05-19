from fabric.context_managers import settings, hide
from fabric.operations import sudo
from lettuce import world, before, after
from logging_facility import *
from scapy.config import conf
from scapy.layers.dhcp6 import DUID_LLT
import os
import shutil
import sys
import time
from init_all import *


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

def kill_bind10(host):
    """
    Kill any running bind10 instance
    """
    get_common_logger().debug("--- Killing all running Bind instances")
    cmd = 'pkill b10-*; sleep 5'
    with settings(host_string=host, user=MGMT_USERNAME, password=MGMT_PASSWORD):
        with settings(warn_only=True):
            sudo(cmd, pty=True)

@before.all
def server_start():
    """
    Server starting before testing
    """
    # Initialize the common logger. The instance of this logger can
    # be instantiated by get_common_logger()
    logger_initialize(LOGLEVEL)

    # Make sure there is noo garbage instance of bind10 running.
    kill_bind10(MGMT_ADDRESS)

    if (SERVER_TYPE in ['kea', 'kea4', 'kea6']):
        get_common_logger().debug("--- Starting Bind:")
        try:
            #comment line below to turn off starting bind
            bind10(MGMT_ADDRESS, cmd='(rm nohup.out; nohup ' + SERVER_INSTALL_DIR
                   + 'sbin/bind10 &); sleep 2' )
            get_common_logger().debug("----- Bind10 successfully started")
        except :
            get_common_logger().error("----- Bind10 start failed\n\nSomething go wrong with connection\nPlease make sure it's configured properly\nIP address: %s\nMac address: %s\nNetwork interface: %s" %(MGMT_ADDRESS, CLI_MAC, IFACE))
            sys.exit()
    else:
        get_common_logger().error("Server other than kea not implemented yet")
        
    #If relay is used routing needs to be reconfigured on DUT
    try:
        if REL4_ADDR and (SERVER_TYPE  == 'kea4'):
            with settings(host_string=MGMT_ADDRESS, user=MGMT_USERNAME, password=MGMT_PASSWORD):
                sudo("route add -host %s gw %s" % (GIADDR4, REL4_ADDR))
    except:
        pass # most likely REL4_ADDR caused this exception -> we do not use relay
       

@before.each_scenario
def initialize(scenario):    

    world.climsg = []  # Message(s) to be sent
    world.cliopts = [] # Option(s) to be included in the next message sent
    world.srvmsg = []  # Server's response(s)

    world.cfg = {}
    world.cfg["iface"] = IFACE
    world.cfg["server_type"] = SERVER_TYPE
    try:    
        world.cfg["srv4_addr"] = SRV4_ADDR
        world.cfg["rel4_addr"] = REL4_ADDR
        world.cfg["giaddr4"] = GIADDR4
    except:
        pass
    world.cfg["cfg_file"] = "server.cfg"
    world.cfg["mgmt_addr"] = MGMT_ADDRESS
    world.cfg["mgmt_user"] = MGMT_USERNAME
    world.cfg["mgmt_pass"] = MGMT_PASSWORD
    world.cfg["conf"] = "" # Just empty config for now

    world.proto = PROTO

    # messages validation for v6 DO NOT CHANGE THIS!
    world.cfg["client_id"] = True
    world.cfg["wrong_server_id"] = False
    world.cfg["wrong_client_id"] = False
    world.cfg["unicast"] = False
    
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
    get_common_logger().info("%d of %d scenarios passed." % (
        total.scenarios_passed,
        total.scenarios_ran
    ))

    kill_bind10(MGMT_ADDRESS)

    try:
        if REL4_ADDR and (SERVER_TYPE  == 'kea4'):
            with settings(host_string=MGMT_ADDRESS, user=MGMT_USERNAME, password=MGMT_PASSWORD):
                sudo("route del -host %s" % (GIADDR4))
    except NameError:
        pass # most likely REL4_ADDR caused this exception -> we do not use relay

    
    get_common_logger().info("Goodbye.")
