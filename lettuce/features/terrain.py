from Crypto.Random.random import randint
from init_all import LOGLEVEL, MGMT_ADDRESS, SERVER_TYPE, CLI_MAC, IFACE, \
    REL4_ADDR, SRV4_ADDR, PROTO, copylist, removelist, HISTORY, MGMT_USERNAME, \
    MGMT_PASSWORD, GIADDR4, TCPDUMP, TCPDUMP_INSTALL_DIR
from lettuce import world, before, after
from logging_facility import *
from scapy.all import sniff
from scapy.config import conf
from scapy.layers.dhcp6 import DUID_LLT
from serversupport.bind10 import kill_bind10, start_bind10
import importlib
import os
import shutil
import subprocess
import sys
import time

add_option = {'client_id' : True,
              'preference' : False,
              'time' : False,
              'relay_msg' : False,
              'server_uni' : False,
              'status_code' : False,
              'rapid_commit' : False,
              'interface_id' : False,
              'reconfig' : False,
              'option_request' : False,
              'reconfig_accept' : False,
              'server_id' : False,
              'wrong_client_id' : False,
              'wrong_server_id' : False,
              'IA_NA': True,
              'IA_TA': False,
              'IA_PD': False,
              'IA_Prefix': False,
              'IA_Address': False,
              'vendor_class': False,
              'vendor_specific_info': False
              }
# TODO: add detailed description to every value:
values = {"T1": 0, 
          "T2": 0,
          "address": "::",
          "prefix": "::",
          "plen": 0,  # plz remember, to add prefix and prefix length!
          "preflft" : 0,
          "validlft" : 0,
          "enterprisenum": 0 # vendor 
          #TODO: relay msg values!
          }
# we should consider transfer most of funtions to separate v4 and v6 files
# there is no v4 functions yet.
def set_values():
    world.cfg["values"] = values.copy()
 
def set_options():
    world.cfg["add_option"] = add_option.copy()
    
def add_result_to_raport(info):
    world.result.append(info)

def client_id (mac):
    world.cfg["cli_duid"] = DUID_LLT(timeval = int(time.time()), lladdr = mac )

def ia_id ():
    world.cfg["ia_id"] = randint(1,99999)

def ia_pd ():
    world.cfg["ia_pd"] = randint(1,99999)

@before.all
def server_start():
    """
    Server starting before testing
    """
    world.result = []
    
    # Initialize the common logger. The instance of this logger can
    # be instantiated by get_common_logger()
    logger_initialize(LOGLEVEL)

    if (SERVER_TYPE in ['kea', 'kea4', 'kea6']):
        get_common_logger().debug("Starting Bind:")
        
        try:
            # Make sure there is noo garbage instance of bind10 running.
            kill_bind10(MGMT_ADDRESS)
            start_bind10(MGMT_ADDRESS)
            get_common_logger().debug("Bind10 successfully started")
        except :
            get_common_logger().error("Bind10 start failed\n\nSomething go wrong with connection\nPlease make sure it's configured properly\nIP destination address: %s\nLocal Mac address: %s\nNetwork interface: %s" %(MGMT_ADDRESS, CLI_MAC, IFACE))
            sys.exit()
    elif SERVER_TYPE in ["isc_dhcp6", "dibbler"]:
        stop = importlib.import_module("serversupport.%s.functions"  % (SERVER_TYPE))
        stop.stop_srv()

    else:
        get_common_logger().error("Server "+SERVER_TYPE+" not implemented yet")
        
    #If relay is used routing needs to be reconfigured on DUT
    try:
        if REL4_ADDR and (SERVER_TYPE  == 'kea4'):
            with settings(host_string = MGMT_ADDRESS, user = MGMT_USERNAME, password = MGMT_PASSWORD):
                run("route add -host %s gw %s" % (GIADDR4, REL4_ADDR))
    except:
        pass # most likely REL4_ADDR caused this exception -> we do not use relay

@before.each_scenario
def initialize(scenario):    
    
    world.climsg = []  # Message(s) to be sent
    world.cliopts = [] # Option(s) to be included in the next message sent
    world.srvmsg = []  # Server's response(s)
    world.savedmsg = [] # Saved option(s)
    
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
    
    # RFC 3315 define two addresess:
    # All_DHCP_Relay_Agents_and_Servers = ff02::1:2
    # All DHCP_Servers ff05::1:3 that is deprecated. 
    world.cfg["address_v6"] = "ff02::1:2"
    world.proto = PROTO
    world.cfg["subnet"] = ""
    
    set_values() 
    set_options()
    world.cfg["unicast"] = False
    world.cfg["relay"] = False
    world.oro = None
    world.vendor = []
    world.opts = []
    world.subopts = []
   
    world.name = scenario.name    
    # Setup scapy for v4
    conf.iface = IFACE
    conf.checkIPaddr = False # DHCPv4 is sent from 0.0.0.0, so response matching may confuse scapy

    # Setup scapy for v6
    conf.iface6 = IFACE
    conf.use_pcap = True

    # Setup DUID for DHCPv6 (and also for DHCPv4, see RFC4361)
    if (not hasattr(world.cfg, "cli_duid")):
        client_id (CLI_MAC)
        
    if (not hasattr(world.cfg, "ia_id")):
        ia_id ()
        
    if (not hasattr(world.cfg, "ia_pd")):
        ia_pd ()
    # Some tests can modify the settings. If the tests fail half-way, or
    # don't clean up, this can leave configurations or data in a bad state,
    # so we copy them from originals before each scenario
    # @todo: This should be done remotely, using fabric or something similar
    for item in copylist:
        shutil.copy(item[0], item[1])

    for item in removelist:
        if os.path.exists(item):
            os.remove(item)

    if TCPDUMP:
        # to create separate files for each test we need, test name:
        file_name = str(scenario.name)
        file_name = file_name.replace(".","_")
        # also IP version for tcpdump
        type = 'ip'
        
        if PROTO == "v6":
            type = type +'6'
        cmd = TCPDUMP_INSTALL_DIR+'tcpdump'
        args = [cmd, type, "-i", world.cfg["iface"], "-w", "tests_results/"+file_name+".pcap", "-s", str(65535)]
        get_common_logger().debug("Running tcpdump: ")
        get_common_logger().debug(args)
        # TODO: hide stdout, log it in debug mode
        subprocess.Popen(args)
#initialize()

@before.outline
def outline_before(scenario, number, step, failed):
    """
    For Outline Scenarios, 
        scenario - name
        number - number of scenario
        step - which 'example' from test
        failed - reason of failure
    For more info please read UserHelp - Outline Scenarios
    """
    initialize(None)#we need to initialize all

@after.outline
def outline_result(scenario, number, step, failed):
    """
    For Outline Scenarios, 
        scenario - name
        number - number of scenario
        step - which 'example' from test
        failed - reason of failure
    For more info please read UserHelp - Outline Scenarios
    """
    if len(failed) == 0:
        result = 'False'
    else:
        result = 'True'
    info = str(scenario.name)+str(step)+'\n'+ result
    add_result_to_raport(info)


@after.each_step
def cleanup_option(step):
    #set_options ()
    pass
    
@after.each_scenario
def cleanup(scenario):
    """
    Global cleanup for each scenario. Implemented within tests by "Server is started."
    """
    info = str(scenario.name) +'\n'+ str(scenario.failed)
    if 'outline' not in info:
        add_result_to_raport(info)

    if TCPDUMP:
        args = ["killall tcpdump"]
        subprocess.call(args, shell = True)
        # TODO: log output in debug mode
        
@after.all
def say_goodbye(total):
    """
    Server stopping after whole work
    """
    
    get_common_logger().info("%d of %d scenarios passed." % (
        total.scenarios_passed,
        total.scenarios_ran
    ))
    if HISTORY:
        result = open ('result','w')
        for item in world.result:
            result.write(str(item)+'\n')
        result.close()
        
    if SERVER_TYPE in ['kea', 'kea4', 'kea6']:    
        kill_bind10(MGMT_ADDRESS)
        try:
            if REL4_ADDR and (SERVER_TYPE  == 'kea4'):
                with settings(host_string = MGMT_ADDRESS, user = MGMT_USERNAME, password = MGMT_PASSWORD):
                    run("route del -host %s" % (GIADDR4))
        except NameError:
            pass # most likely REL4_ADDR caused this exception -> we do not use relay
    elif SERVER_TYPE in ['isc_dhcp6','dibbler']:
        stop = importlib.import_module("serversupport.%s.functions"  % (SERVER_TYPE))
        stop.stop_srv()

    get_common_logger().info("Goodbye.")
