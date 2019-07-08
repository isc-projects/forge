# Copyright (C) 2018 Internet Systems Consortium.
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND INTERNET SYSTEMS CONSORTIUM
# DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# INTERNET SYSTEMS CONSORTIUM BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
# FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
# WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
# Author: Wlodzimierz Wencel

import os
import sys

from forge_cfg import world
from softwaresupport.multi_server_functions import (fabric_run_command, fabric_send_file,
    remove_local_file, copy_configuration_file, fabric_sudo_command, json_file_layout,
    fabric_download_file, fabric_remove_file_command, locate_entry)


# IMPORTANT NOTE:
# FOR NOW IT"S SOLUTION FOR DATABASE/NETCONF CONFIGURATION
# SHOULD BE APPLIED TO JSON :)
# CONFIGURATION WILL BBE GENERATED EVERY TIME, BUT UPLOADED ONLY ON DEMAND

class KeaConfiguration:
    def __init__(self):
        self.config_type_default = "yang"  # define which config will used as default for all tests
        self.config_type_temporary = "yang"  # used in tests where multiple config backends will be used
        self.final_config_script = ""
        self.destination_address = world.f_cfg.mgmt_address
        # create empty lists, there can be multiple pools etc.
        self.optionList = []
        self.poolList = []
        self.subnetList = []
        self.sharednetworkList = []
        self.optiondefList = []
        self.reservationList = []
        self.loggerList = [ConfigurationLogging()]
        self.classList = []
        self.globalparameterList = [ConfigurationGlobalParameters('def', 'def')]

    def addpool(self, pool):
        self.poolList.append(pool)

    def addreservation(self, host):
        self.reservationList.append(host)

    def addsubnet(self, subnet):
        self.subnetList.append(subnet)

    def addsharednetwork(self, network):
        self.sharednetworkList.append(network)

    def addoption(self, option):
        self.optionList.append(option)

    def addoptiondef(self, optiondef):
        self.optiondefList.append(optiondef)

    def addglobalparameter(self, param):
        self.globalparameterList.append(param)

    def addclass(self, cls):
        self.classList.append(cls)

    def getsubnetlength(self):
        return len(self.subnetList)

    def getreservationlength(self):
        return len(self.reservationList)

    def getoptionlength(self):
        return len(self.optionList)

    def getoptiondeflength(self):
        return len(self.optiondefList)

    def getpoollength(self):
        return len(self.poolList)

    def getsharednetworklength(self):
        return len(self.sharednetworkList)

    def getglobalparamlength(self):
        return len(self.globalparameterList)

    def getloggerlength(self):
        return len(self.loggerList)

    def getclasslenght(self):
        return len(self.classList)

    def inner_getattr(self, list_name, list_id, item):
        return getattr(getattr(self, list_name)[list_id], item)

    def updatevaluesubnet(self, value_name, value, list_id):
        # TODO what if parameter is a list
        # if type(self.inner_getattr('subnetList', list_id, value_name)) is list:
        #     getattr(self.subnetList[list_id], value_name).append(value)
        setattr(self.subnetList[list_id], value_name.replace("-", "_"), value)

    def updatevalueoption(self, value_name, value, list_id):
        setattr(self.optionList[list_id], value_name.replace("-", "_"), value)

    def updatevaluereservation(self, value_name, value, list_id):
        setattr(self.reservationList[list_id], value_name.replace("-", "_"), value)

    def updatevaluenetwork(self, value_name, value, list_id):
        setattr(self.sharednetworkList[list_id], value_name.replace("-", "_"), value)

    def updatevaluepool(self, value_name, value, list_id):
        setattr(self.poolList[list_id], value_name.replace("-", "_"), value)

    def updatevalueglobalparam(self, value_name, value, list_id=0):
        setattr(self.globalparameterList[list_id], value_name.replace("-", "_"), value)

    def updatevalueclass(self, value_name, value, list_id):
        setattr(self.classList[list_id], value_name.replace("-", "_"), value)

    # def ifemptyglobalparameterlist(self):
    #     return 1 if self.getglobalparamlength() == 0 else 0

    def build_mysql_script(self):
        pass
        # TODO implement this

    def build_pgsql_script(self):
        pass
        # TODO implement this

    def build_json_script(self):
        pass
        # TODO implement this

    def add_to_xml_script(self, leaf_name, part=None):
        # todo could be local function in build_xml_script()
        if len(str(part)) > 0:
            if part is None:
                self.final_config_script += '<' + leaf_name + '>'
            else:
                self.final_config_script += '<' + leaf_name + '>' + str(part) + '</' + leaf_name + '>'

    def build_xml_script(self):
        # functions to save coding lines while creating xml file:
        def add_option_def(option):
            self.add_to_xml_script('code', option.code)
            self.add_to_xml_script('space', option.space)
            self.add_to_xml_script('data', option.value)
            self.add_to_xml_script('name', option.name)
            self.add_to_xml_script('csv-format', option.csv_format)
            self.add_to_xml_script('always-send', option.persistent)
            self.add_to_xml_script('user-context', option.user_context)

        # all the rest of the config
        self.add_to_xml_script('config xmlns="urn:ietf:params:xml:ns:yang:kea-dhcp4-server"')
        # interface
        tmp = self.globalparameterList[0]
        self.add_to_xml_script('decline-probation-period', tmp.decline_probation_period)
        self.add_to_xml_script('interfaces-config')
        self.add_to_xml_script('interfaces', tmp.interface)
        self.add_to_xml_script('re-detect', tmp.re_detect)
        self.add_to_xml_script('/interfaces-config')

        # classes
        self.add_to_xml_script('client-classes')
        for each_class in self.classList:
            self.add_to_xml_script('client-class')
            self.add_to_xml_script('boot-file-name', each_class.boot_file_name)
            self.add_to_xml_script('name', each_class.name)
            self.add_to_xml_script('next-server', each_class.next_server)
        #                           "option-data": [],
        #                           "option-def": [],
            self.add_to_xml_script('server-hostname', each_class.server_hostname)
            self.add_to_xml_script('test', each_class.test)
            self.add_to_xml_script('/client-class')
        self.add_to_xml_script('/client-classes')
        self.add_to_xml_script('expired-leases-processing')
        # self.add_to_xml_script('expired-leases-processing')
        self.add_to_xml_script('reclaim-timer-wait-time', tmp.reclaim_timer_wait_time)
        self.add_to_xml_script('flush-reclaimed-timer-wait-time', tmp.flush_reclaimed_timer_wait_time)
        self.add_to_xml_script('hold-reclaimed-time', tmp.hold_reclaimed_time)
        self.add_to_xml_script('max-reclaim-leases', tmp.max_reclaim_leases)
        self.add_to_xml_script('max-reclaim-time', tmp.max_reclaim_time)
        self.add_to_xml_script('unwarned-reclaim-cycles', tmp.unwarned_reclaim_cycles)
        # self.add_to_xml_script('/expired-leases-processing')
        self.add_to_xml_script('/expired-leases-processing')

        # option definitions
        if self.getoptiondeflength() > 0:
            self.add_to_xml_script('option-def-list')
            for each_optiondef in self.optiondefList:
                    self.add_to_xml_script('option-def')
                    self.add_to_xml_script('code', each_optiondef.code)
                    self.add_to_xml_script('space', each_optiondef.space)
                    self.add_to_xml_script('name', each_optiondef.name)
                    self.add_to_xml_script('encapsulate', each_optiondef.encapsulate)
                    self.add_to_xml_script('record-types', each_optiondef.record_types)
                    self.add_to_xml_script('type', each_optiondef.op_type)
                    self.add_to_xml_script('/option-def')
            self.add_to_xml_script('/option-def-list')

        # global options
        if self.getoptionlength() > 0:
            self.add_to_xml_script('option-data-list')
            for each_option in self.optionList:
                if each_option.dhcp_client_class is None and each_option.dhcp_subnet_id is None and each_option.shared_network_name is None and each_option.pool_id is None:
                        self.add_to_xml_script('option-data')
                        add_option_def(each_option)
                        self.add_to_xml_script('/option-data')
            self.add_to_xml_script('/option-data-list')

        # control socket
        self.add_to_xml_script('control-socket')
        self.add_to_xml_script('socket-name', tmp.socket_name)
        self.add_to_xml_script('socket-type', tmp.socket_type)
        self.add_to_xml_script('/control-socket')

        # lease database
        self.add_to_xml_script('lease-database')
        self.add_to_xml_script('database-type', tmp.db_leases_type)
        if tmp.db_leases_type == "memfile":
            self.add_to_xml_script('name', tmp.file_name)
            self.add_to_xml_script('persist', tmp.persist)
            self.add_to_xml_script('lfc-interval', tmp.lfc_interval)
        elif tmp.db_leases_type.lower() == "mysql" or tmp.db_leases_type.lower() == "postgresql":
            self.add_to_xml_script('name', tmp.db_name)
            self.add_to_xml_script('host', tmp.db_host)
            self.add_to_xml_script('user', tmp.db_user)
            self.add_to_xml_script('passwd', tmp.db_passwd)
            self.add_to_xml_script('port', tmp.db_port)
            self.add_to_xml_script('readonly', tmp.db_readonly)
        elif tmp.db_leases_type.lower() == "cassandra":
            self.add_to_xml_script('name', tmp.db_name)
        else:
            assert False, "Forge should not get here... bug!"
        self.add_to_xml_script('/lease-database')
        # host reservation db add here!

        # subnets

        if self.getsubnetlength() > 0:
            self.add_to_xml_script('subnet4')
            for each_subnet in self.subnetList:
                self.add_to_xml_script('subnet4')
                self.add_to_xml_script('id', each_subnet.subnet_id+1)
                self.add_to_xml_script('subnet', each_subnet.subnet_prefix)
                self.add_to_xml_script('valid-lifetime', each_subnet.valid_lifetime)
                self.add_to_xml_script('renew-timer', each_subnet.renew_timer)
                self.add_to_xml_script('rebind-timer', each_subnet.rebind_timer)
                self.add_to_xml_script('interface', each_subnet.interface)
                self.add_to_xml_script('match-client-id', each_subnet.match_clientid)
                self.add_to_xml_script('next-server', each_subnet.next_server)
                self.add_to_xml_script('server-hostname', each_subnet.server_hostname)
                self.add_to_xml_script('boot-file-name', each_subnet.boot_file_name)
                self.add_to_xml_script('subnet-4o6-interface', each_subnet.interface_4o6)
                self.add_to_xml_script('subnet-4o6-interface-id', each_subnet.interface_id_4o6)
                self.add_to_xml_script('subnet-4o6-subnet', each_subnet.subnet_4o6)

                # subnet options
                if self.getoptionlength() > 0:
                    self.add_to_xml_script('option-data-list')
                    for each_option in self.optionList:
                        if each_option.dhcp_subnet_id == each_subnet.subnet_id and each_option.shared_network_name is None and each_option.pool_id is None:
                            self.add_to_xml_script('option-data')
                            add_option_def(each_option)
                            self.add_to_xml_script('/option-data')
                    self.add_to_xml_script('/option-data-list')

                # uses dhcp:subnet-client-class;
                # uses dhcp:subnet-require-client-classes;
                if self.getreservationlength() > 0:
                    self.add_to_xml_script('reservations')
                    for each_reservation in self.reservationList:
                        if each_reservation.subnet_id == each_subnet.subnet_id:
                            self.add_to_xml_script('host')
                            self.add_to_xml_script('identifier-type', each_reservation.host_identifier_type)
                            self.add_to_xml_script('identifier', each_reservation.hw_address)  # can be more
                            self.add_to_xml_script('ip-address', each_reservation.address)
                            self.add_to_xml_script('host-hostname', each_reservation.hostname)
                            self.add_to_xml_script('host-client-classes', each_reservation.host_client_class)
                            if self.getoptionlength() > 0:
                                self.add_to_xml_script('option-data-list')
                                for each_option in self.optionList:
                                    if each_option.reservation_id == each_reservation.reservation_id:
                                        self.add_to_xml_script('option-data')
                                        add_option_def(each_option)
                                        self.add_to_xml_script('/option-data')
                                self.add_to_xml_script('/option-data-list')
                            self.add_to_xml_script('next-server', each_reservation.next_server)
                            self.add_to_xml_script('server-hostname', each_reservation.server_hostname)
                            self.add_to_xml_script('boot-file-name', each_reservation.boot_file_name)
                            self.add_to_xml_script('/host')
                    self.add_to_xml_script('/reservations')

                # add relay, for now just single
                self.add_to_xml_script('relay')
                # TODO change it from single to list
                # for each_relay in each_subnet.relay:
                #     self.add_to_xml_script('ip-address', each_relay)
                self.add_to_xml_script('ip-addresses', each_subnet.relay)
                self.add_to_xml_script('/relay')

                if self.getpoollength() > 0:
                    self.add_to_xml_script('pools')
                    for each_pool in self.poolList:
                        if each_pool.subnet_id == each_subnet.subnet_id:
                            self.add_to_xml_script('pool')
                            self.add_to_xml_script('start-address', each_pool.start_address)
                            self.add_to_xml_script('end-address', each_pool.end_address)
                            self.add_to_xml_script('pool-client-class', each_pool.pool_client_class)
                            self.add_to_xml_script('pool-require-client-classes', each_pool.pool_require_client_classes)
                            self.add_to_xml_script('pool-user-context', each_pool.pool_user_context)
                            # options in pools
                            if self.getoptionlength() > 0:
                                self.add_to_xml_script('option-data-list')
                                for each_option in self.optionList:
                                    if each_option.dhcp_subnet_id == each_subnet.subnet_id and each_option.pool_id == each_pool.pool_id:
                                        self.add_to_xml_script('option-data')
                                        add_option_def(each_option)
                                        self.add_to_xml_script('/option-data')
                                self.add_to_xml_script('/option-data-list')
                            self.add_to_xml_script('/pool')
                    self.add_to_xml_script('/pools')
                self.add_to_xml_script('/subnet4')
            self.add_to_xml_script('/subnet4')

        # check shared networks
        if self.getsharednetworklength() > 0:
            self.add_to_xml_script('shared-networks')
            # loop to add everything from shared network
            self.add_to_xml_script('/shared-networks')
        # logging
        # self.add_to_xml_script('logging')
        # self.add_to_xml_script('loggers')
        # for each in self.loggerList:
        #     self.add_to_xml_script('logger')
        #     self.add_to_xml_script('name', each.name)
        #     self.add_to_xml_script('severity', each.severity)
        #     self.add_to_xml_script('debuglevel', each.debuglevel)
        #     self.add_to_xml_script('output-options')
        #     self.add_to_xml_script('option')
        #     self.add_to_xml_script('output', each.output)
        #     self.add_to_xml_script('flush', each.flush)
        #     self.add_to_xml_script('maxsize', each.maxsize)
        #     self.add_to_xml_script('maxver', each.maxver)
        #     self.add_to_xml_script('/option')
        #     self.add_to_xml_script('/output-options')
        #     self.add_to_xml_script('/logger')
        # self.add_to_xml_script('/loggers')
        # self.add_to_xml_script('/logging')
        self.add_to_xml_script('/config')

        #change self.globalparameterList[0]

        # assert False, self.final_config_script
        import xml.dom.minidom
        xml = xml.dom.minidom.parseString(self.final_config_script)  # or xml.dom.minidom.parseString(xml_string)

        # xml_config = open(world.cfg["cfg_file"]+'XML', 'w')
        # xml_config.write(xml.toprettyxml())
        # xml_config.close()

        # assert False, self.optionList[0].__dict__

    def build_yang_script(self):
        pass

    def sendconfiguration(self):
        # pass
        from kea6_server.functions import set_kea_ctrl_config, start_srv

        # set_kea_ctrl_config()
        # cfg4 = '{"Dhcp4":{"control-socket":{"socket-type":"unix","socket-name":"'+world.f_cfg.software_install_path+'etc/kea/control_socket"}},"Logging":{"loggers":[{"name":"kea-dhcp4","output_options":[{"output":"'+world.f_cfg.software_install_path+'var/log/kea.log"}],"debuglevel":99,"severity":"DEBUG"}]}}'
        # netconfdaemoncfg = '{"Dhcp4":{"control-socket":{"socket-type":"unix","socket-name":"'+world.f_cfg.software_install_path+'etc/kea/control_socket"}}}'
        # config = open(world.cfg["cfg_file"], 'w')
        # config.write(cfg4)
        # config.close()

        # config = open(world.cfg["cfg_file"], 'w')
        # config.write(cfg4)
        # config.close()

        destination_address = world.f_cfg.mgmt_address

        copy_configuration_file(world.cfg["cfg_file"]+'XML', "/yang.xml", destination_host=destination_address)

        copy_configuration_file(world.cfg["cfg_file"], destination_host=destination_address)
        # copy_configuration_file(world.cfg["cfg_file_2"], "/kea_ctrl_config", destination_host=destination_address)
        fabric_send_file(world.cfg["cfg_file"],
                         world.f_cfg.software_install_path + "etc/kea/kea.conf",
                         destination_host=destination_address)
        # fabric_send_file(world.cfg["cfg_file_2"],
        #                  world.f_cfg.software_install_path + "etc/kea/keactrl.conf",
        #                  destination_host=destination_address)
        fabric_send_file(world.cfg["cfg_file"]+'XML',
                         world.f_cfg.software_install_path + "etc/kea/yang.xml",
                         destination_host=destination_address)

        # fabric_sudo_command(world.f_cfg.software_install_path)
        # start_srv(True, "DHCP")

    def updateconfiguration(self):
        pass

    def clearconfiguration(self):
        pass

    def add_to_script(self, part):
        self.final_config_script += part


class ConfigurationClass:
    def __init__(self):
        self.boot_file_name = ""
        self.name = ""
        self.next_server = ""
        self.server_hostname = ""
        self.test = ""
        self.class_id = world.configClass.getclasslength()

    def __getitem__(self, item):
        return getattr(self, item)


class ConfigurationPool:
    def __init__(self, address, subnet_id=None):
        self.start_address = address.split("-")[0]
        self.end_address = address.split("-")[1]
        self.pool_client_class = ""
        self.pool_require_client_classes = ""
        self.pool_user_context = ""
        # relations
        self.subnet_id = int(subnet_id) if subnet_id is not None else world.configClass.getsubnetlength()
        self.pool_id = world.configClass.getpoollength()

    def __getitem__(self, item):
        return getattr(self, item)


class ConfigurationOption:
    def __init__(self, option_name, value, space, custom_code=None, client_class=None,
                 subnet_id=None, shared_id=None, pool_id=None, reservation_id=None):
        self.option_id = 1
        self.name = option_name
        self.code = self.translate_name_to_code(option_name, custom_code)
        self.value = value
        self.formatted_value = ""  # db only
        self.csv_format = ""
        self.space = space
        self.persistent = ""
        self.host_id = ""
        self.scope_id = ""
        self.user_context = ""
        # relations:
        self.dhcp_client_class = int(client_class) if client_class is not None else client_class
        self.dhcp_subnet_id = int(subnet_id) if subnet_id is not None else subnet_id
        self.shared_network_name = int(shared_id) if shared_id is not None else shared_id
        self.pool_id = int(pool_id) if pool_id is not None else pool_id
        self.reservation_id = int(reservation_id) if reservation_id is not None else reservation_id

    def __getitem__(self, item):
        return getattr(self, item)

    def translate_name_to_code(self, option_name, custom_code):
        if custom_code is None:
            if world.proto == "v6":
                return world.kea_options6.get(option_name)
            elif world.proto == "v4":
                return world.kea_options4.get(option_name)
        else:
            return custom_code


class ConfigurationOptionDef:
    def __init__(self, option_name, opt_code, opt_type, value, space):
        self.code = opt_code
        self.name = option_name
        self.space = space
        self.array = "false"
        self.op_type = "record"
        self.encapsulate = ""
        self.record_types = opt_type
        self.user_context = ""
        # old approach was to configure this option right away, maybe we should skip that
        self.add_option(option_name, value, space, opt_code)

    def __getitem__(self, item):
        return getattr(self, item)

    def add_option(self, option_name, value, space, opt_code):
        world.configClass.addoption(ConfigurationOption(option_name, value, space, custom_code=opt_code))


class ConfigurationSubnet:
    def __init__(self, subnet, interface=world.f_cfg.server_iface):
        self.subnet_prefix = subnet
        self.interface_4o6 = ""
        self.interface_id_4o6 = ""
        self.subnet_4o6 = ""
        self.boot_file_name = ""
        self.client_class = ""
        self.interface = interface
        self.match_clientid = ""
        self.next_server = ""
        self.rebind_timer = world.cfg["server_times"]["rebind-timer"]
        self.relay = ""
        self.renew_timer = world.cfg["server_times"]["renew-timer"]
        self.require_client_class = ""
        self.reservation_mode = ""
        self.server_hostname = ""
        self.user_context = ""
        self.valid_lifetime = world.cfg["server_times"]["valid-lifetime"]
        # relations
        self.shared_network_name = ""
        self.subnet_id = world.configClass.getsubnetlength()

    def __getitem__(self, item):
        return getattr(self, item)

        # validation
    def interface_validation(self, value):
        # if value passed is [eth89, 123:123::0] have to bbe changed to eth89/123:123::0
        if value is list:
            return "/".join(value)
        else:
            return value


class ConfigurationSharedNetworks:
    def __init__(self):
        self.interface = ""
        self.match_clientid = 1  # only v4
        self.rebind_timer = ""
        self.relay = ""
        self.renew_timer = ""
        self.require_client_class = ""
        self.reservation_mode = ""
        self.server_hostname = ""
        self.user_context = ""
        self.valid_lifetime = ""
        # relations
        self.client_class = ""

    def __getitem__(self, item):
        return getattr(self, item)


class ConfigurationGlobalParameters:
    # this is completely bullshit, I make copy of that class for each new parameter
    # created by "value_name + value" and take default values form first instance of this class
    def __init__(self, value_name, value, interface=world.f_cfg.server_iface):
        self.value_name = value_name
        self.value = value
        # maybe this won't be needed:
        self.socket_name = os.path.join(world.f_cfg.software_install_path, 'etc/kea/control_socket')
        self.socket_type = "unix"
        self.decline_probation_period = ""
        self.re_detect = ""
        self.interface = interface
        # inside "host-reservation-identifiers": []
        # "hw-address",
        # "duid",
        # "circuit-id",
        # "client-id"

        # inside: expired-leases-processing": {}
        self.flush_reclaimed_timer_wait_time = ""
        self.hold_reclaimed_time = ""
        self.max_reclaim_leases = ""
        self.max_reclaim_time = ""
        self.reclaim_timer_wait_time = ""
        self.unwarned_reclaim_cycles = ""

        # leases:
        self.db_leases_type = "memfile"
        self.lfc_interval = 0
        self.file_name = os.path.join(world.f_cfg.software_install_path, 'var/lib/kea/kea-leases4.csv')
        self.persist = ""
        self.db_name = ""
        self.db_host = ""
        self.db_user = ""
        self.db_passwd = ""
        self.db_port = ""  # not used
        self.db_readonly = ""  # not used
        self.db_connect_timeout = ""  # not yet used
        self.db_contact_points = ""  # not yet used
        self.db_keyspace = ""  # not yet used
        self.db_max_reconnect_tries = ""  # not yet used
        self.db_reconnect_wait_time = ""  # not yet used
        self.db_request_timeout = ""  # not yet used
        self.db_tcp_keepalive = ""  # not yet used
        self.db_tcp_nodelay = ""  # not yet used

    def __getitem__(self, item):
        return getattr(self, item)


class ConfigurationDDNS:
    def __init__(self):
        self.always_include_fqdn = False,
        self.enable_updates = False,
        self.generated_prefix = "myhost",
        self.hostname_char_replacement = "",
        self.hostname_char_set = "",
        self.max_queue_size = 1024,
        self.ncr_format = "JSON",
        self.ncr_protocol = "UDP",
        self.override_client_update = False,
        self.override_no_update = False,
        self.qualifying_suffix = "",
        self.replace_client_name = "never",
        self.sender_ip = "0.0.0.0",
        self.sender_port = 0,
        self.server_ip = "127.0.0.1",
        self.server_port = 53001

    def __getitem__(self, item):
        return getattr(self, item)


class ConfigurationLogging:
    def __init__(self):
        self.debuglevel = 99
        self.name = "kea-dhcp4"
        self.severity = "DEBUG"
        self.flush = "true"
        self.maxsize = ""
        self.maxver = ""
        self.output = os.path.join(world.f_cfg.software_install_path, "var/log/kea.log")

    def __getitem__(self, item):
        return getattr(self, item)


class ConfigurationReservation:
    def __init__(self, host_identifier_type="", host_identifier="", reservation_type="", reservation_value="", subnetid=""):
        self.reservation_id = world.configClass.getreservationlength()
        self.host_identifier_type = host_identifier_type
        self.hw_address = host_identifier if host_identifier_type == "hw-address" else ""  # TODO in v6 can be multiple options
        self.address = reservation_value if reservation_type == "address" else ""
        self.prefix = reservation_value if reservation_type == "prefix" else ""
        self.hostname = reservation_value if reservation_type == "hostname" else ""
        self.boot_file_name = reservation_value if reservation_type == "bootfilename" else ""
        self.next_server = reservation_value if reservation_type == "next-server" else ""
        self.server_hostname = reservation_value if reservation_type == "server-hostname" else ""
        self.subnet_id = subnetid if subnetid != "" else world.configClass.getsubnetlength()
        self.host_client_class = ""

    def __getitem__(self, item):
        return getattr(self, item)


class ConfigurationHooks:
    def __init__(self):
        pass

    def __getitem__(self, item):
        return getattr(self, item)


if __name__ == '__main__':
    pass
    # TODO write tests
