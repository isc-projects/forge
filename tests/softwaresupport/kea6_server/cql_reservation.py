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
import logging

from forge_cfg import world

from softwaresupport.multi_server_functions import fabric_run_command, fabric_send_file,\
    remove_local_file, copy_configuration_file, fabric_sudo_command, json_file_layout,\
    fabric_download_file, fabric_remove_file_command, locate_entry

log = logging.getLogger('forge')


list_of_all_reservations = []


class CassandraReservation:

    def __init__(self):
        self.reservation_id = len(list_of_all_reservations) + 1
        list_of_all_reservations.append(self)
        self.identifier_type_number = ""
        self.hostname = ""
        self.identifier_type = ""
        self.identifier_value = ""
        self.dhcp4_subnet_id = "-1"
        self.dhcp6_subnet_id = "-1"
        self.ipv4_address = "-1"
        self.dhcp4_client_classes = ""
        self.dhcp6_client_classes = ""
        self.server_hostname = ""
        self.boot_file_name = ""
        self.next_server = "-1"
        # to ipv6_reservations list please add just dicts:
        #     {"ipv6_address_reservation": "2001::1"}
        #  or {"ipv6_prefix_reservation": "2220::", "ipv6_prefix_len_reservation": 3}
        # TODO: add iaid
        self.ipv6_reservations = []

        # to options list please add just dicts {"code": 1, "option_value": "192.168.1.2",
        #  "space": "dhcp4", "persistent": 1, "scope": }
        self.options = []

        self.configuration_script = ""

    def define_identifier_type_number(self):
        if self.identifier_type == 'hw-address':
            return 0
        elif self.identifier_type == 'duid':
            return 1
        elif self.identifier_type == 'circuit-id':
            return 2
        elif self.identifier_type == 'client-id':
            return 3
        elif self.identifier_type == 'flex-id':
            return 4
        else:
            assert False, "option '%s' not supported" % self.identifier_type

    def add_reserved_option(self, single_option):
        self.options += single_option

    # # Build config file
    # def set_ipv4_address(self):
    #     # self.configuration_script += "\nSET @ipv4_address = '" + self.ipv4_address + "';"
    #
    # def set_dhcp4_client_classes(self):
    #     # self.configuration_script += "\nSET @dhcp4_client_classes = '" + self.dhcp4_client_classes + "';"
    #
    # def set_dhcp6_client_classes(self):
    #     # self.configuration_script += "\nSET @dhcp6_client_classes = '" + self.dhcp6_client_classes + "';"
    #
    # def set_hostname(self):
    #     # self.configuration_script += "\nSET @hostname = '" + self.hostname + "';"
    #
    # def set_identifier_type(self):
    #     # self.configuration_script += "\nSET @identifier_type = '" + self.identifier_type + "';"
    #
    # def set_identifier_value(self):
    #     # self.configuration_script += "\nSET @identifier_value = '" + self.identifier_value + "';"
    #
    # def set_dhcp4_subnet_id(self):
    #     # if self.dhcp4_subnet_id != "":
    #     #     self.dhcp4_subnet_id = str(self.dhcp4_subnet_id)
    #     # self.configuration_script += "\nSET @dhcp4_subnet_id = '" + self.dhcp4_subnet_id + "';"
    #
    # def set_dhcp6_subnet_id(self):
    #     # if self.dhcp6_subnet_id != "":
    #     #     self.dhcp6_subnet_id = str(self.dhcp6_subnet_id)
    #     # self.configuration_script += "\nSET @dhcp6_subnet_id = '" + self.dhcp6_subnet_id + "';"
    #
    # def set_next_server(self):
    #     # self.configuration_script += "\nSET @next_server = '" + self.next_server + "';"
    #
    # def set_server_hostname(self):
    #     # self.configuration_script += "\nSET @server_hostname = '" + self.server_hostname + "';"
    #
    # def set_boot_file_name(self):
    #     # self.configuration_script += "\nSET @boot_file_name = '" + self.boot_file_name + "';"
    #
    # def set_ipv6_reservations(self):
    #     # for each in self.ipv6_reservations:
    #     #     if len(each) == 1:
    #     #         self.configuration_script += "\nINSERT INTO ipv6_reservations(address, type, host_id)"
    #     #         self.configuration_script += "\nVALUES ('{ipv6_address_reservation}'," \
    #     #                                      " 0, @inserted_host_id);".format(**each)
    #     #     if len(each) == 2:
    #     #         self.configuration_script += "\nSET @ipv6_prefix_reservation = " \
    #     #                                      "'{ipv6_prefix_reservation}';".format(**each)
    #     #         if each["ipv6_prefix_len_reservation"] != "":
    #     #             self.configuration_script += "\nSET @ipv6_prefix_len_reservation = '" \
    #     #                                          + str(each["ipv6_prefix_len_reservation"]) + "';"
    #     #             self.configuration_script += "\nINSERT INTO ipv6_reservations(address, prefix_len, type, host_id)\
    #     #                     \nVALUES (@ipv6_prefix_reservation, @ipv6_prefix_len_reservation, 2, @inserted_host_id);"
    #     #     else:
    #     #         pass
    #
    # def set_ipv6_options(self):
    #     # for each in self.options:
    #     #     if len(each) > 0:
    #     #         self.configuration_script += "\nINSERT INTO dhcp6_options (code, formatted_value," \
    #     #                                      " space, persistent, host_id, scope_id)"
    #     #         self.configuration_script += "\nVALUES ({code}, '{option_value}', '{space}', {persistent}," \
    #     #                                      " @inserted_host_id, (SELECT scope_id FROM dhcp_option_scope " \
    #     #                                      "WHERE scope_name = '{scope}'));".format(**each)
    #
    # def set_ipv4_options(self):
    #     # for each in self.options:
    #     #     if len(each) > 0:
    #     #         self.configuration_script += "\nINSERT INTO dhcp4_options (code, formatted_value," \
    #     #                                      " space, persistent, host_id, scope_id)"
    #     #         self.configuration_script += "\nVALUES ({code}, '{option_value}', '{space}', {persistent}," \
    #     #                                      " @inserted_host_id, (SELECT scope_id FROM dhcp_option_scope " \
    #     #                                      "WHERE scope_name = '{scope}'));".format(**each)
    # debug("Received traffic (answered/unanswered): %d/%d packet(s)."
    #       % (len(ans), len(unans)))

    # id bigint,
    # host_identifier blob,
    # host_identifier_type int,
    # host_ipv4_subnet_id int,
    # host_ipv6_subnet_id int,
    # host_ipv4_address int,
    # host_ipv4_next_server int,
    # host_ipv4_server_hostname text,
    # host_ipv4_boot_file_name text,
    # hostname text,
    # user_context text,
    # host_ipv4_client_classes text,
    # host_ipv6_client_classes text,
    # -- reservation
    # reserved_ipv6_prefix_address text,
    # reserved_ipv6_prefix_length int,
    # reserved_ipv6_prefix_address_type int,
    # iaid int,
    # -- option
    # option_universe int,
    # option_code int,
    # option_value blob,
    # option_formatted_value text,
    # option_space text,
    # option_is_persistent boolean,
    # option_client_class text,
    # option_subnet_id int,
    # option_user_context text,
    # option_scope_id int,
    # PRIMARY KEY ((id))

    def build_v6_script(self):
        # if self.identifier_type == "flex-id":
        #     CassandraReservation.hosts_v6 = CassandraReservation.hosts_v6_flex
        # else:
        #     CassandraReservation.hosts_v6 = CassandraReservation.hosts_v6_hex

        local_v6_addr_reservation = ""  # in cassandra this is used for address and prefix
        local_v6_pref_length_res = ""
        local_v6_res_type = ""
        local_identifier_type = self.define_identifier_type_number()
        for res in self.ipv6_reservations:
            if len(res) == 1:
                local_v6_addr_reservation = res["ipv6_address_reservation"]
                local_v6_pref_length_res = '-1'
                local_v6_res_type = "0"
            if len(res) == 2:
                local_v6_addr_reservation = res["ipv6_prefix_reservation"]
                local_v6_pref_length_res = res["ipv6_prefix_len_reservation"]
                local_v6_res_type = "2"
#
#         self.identifier_value = self.identifier_value.replace(":", "")
#         self.configuration_script += '''INSERT INTO host_reservations ("id", "host_identifier", "host_identifier_type", "host_ipv4_subnet_id", "host_ipv6_subnet_id", "host_ipv4_address", "host_ipv4_next_server", "host_ipv4_server_hostname", "host_ipv4_boot_file_name", "hostname", "user_context", "host_ipv4_client_classes", "host_ipv6_client_classes", "reserved_ipv6_prefix_address", "reserved_ipv6_prefix_length", "reserved_ipv6_prefix_address_type", "iaid", "option_universe", "option_code", "option_value", "option_formatted_value", "option_space", "option_is_persistent", "option_client_class", "option_subnet_id", "option_user_context", "option_scope_id") VALUES
# (%d, textAsBlob('%s'), %s, %s, %s, %s, %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, %s, %s, %s, %s, textAsBlob('%s'), '%s', '%s', %s, '%s', %s, '%s', %s);
# ''' % (self.reservation_id, self.identifier_value, local_identifier_type, self.dhcp4_subnet_id,
#                     self.dhcp6_subnet_id, self.ipv4_address, self.next_server, self.server_hostname,
#                     self.boot_file_name, self.hostname, "00", self.dhcp4_client_classes, self.dhcp6_subnet_id,
#                     local_v6_addr_reservation, local_v6_pref_length_res, local_v6_res_type, "-1",
#                     "-1", "-1", "", "", "", "false", "", "-1", "", "-1")


    def build_v4_script(self):
        pass
        # if self.identifier_type == "flex-id":
        #     CassandraReservation.hosts_v4 = CassandraReservation.hosts_v4_flex
        # else:
        #     CassandraReservation.hosts_v4 = CassandraReservation.hosts_v4_hex

    def build_script(self):
        if world.proto == "v4":
            self.build_v4_script()
        elif world.proto == "v6":
            self.build_v6_script()

    def print_config(self):
        log.info(self.configuration_script)


def enable_db_backend_reservation():
    world.reservation_backend = "cql"


def new_db_backend_reservation(reservation_identifier, reservation_identifier_value):
    enable_db_backend_reservation()
    reservation_record = CassandraReservation()
    reservation_record.identifier_type = reservation_identifier
    reservation_record.identifier_value = reservation_identifier_value


def update_db_backend_reservation(field_name, field_value, reservation_record_id):
    for each_record in list_of_all_reservations:
        if each_record.reservation_id == reservation_record_id:
            each_record.__dict__[field_name] = field_value


def ipv6_prefix_db_backend_reservation(reserved_prefix, reserved_prefix_len, reserved_iaid, reservation_record_id):
    for each_record in list_of_all_reservations:
        if each_record.reservation_id == reservation_record_id:
            each_record.ipv6_reservations.append({"ipv6_prefix_reservation": reserved_prefix,
                                                  "ipv6_prefix_len_reservation": reserved_prefix_len})  # TODO iaid


def ipv6_address_db_backend_reservation(reserved_address, reserved_iaid, reservation_record_id):
    for each_record in list_of_all_reservations:
        if each_record.reservation_id == reservation_record_id:
            each_record.ipv6_reservations.append({"ipv6_address_reservation": reserved_address})  # TODO iaid


def option_db_record_reservation(reserved_option_code, reserved_option_value, reserved_option_space,
                                 reserved_option_persistent, reserved_option_client_class, reserved_subnet_id, reserved_option_scope,
                                 reservation_record_id):
    for each_record in list_of_all_reservations:
        if each_record.reservation_id == reservation_record_id:
            each_record.options.append({"code": reserved_option_code, "option_value": reserved_option_value,
                                        "space": reserved_option_space, "persistent": reserved_option_persistent,
                                        "scope": reserved_option_scope})  # TODO client class


def upload_db_reservation(exp_failed=False):
    db_name = world.f_cfg.db_name
    db_user = world.f_cfg.db_user
    db_passwd = world.f_cfg.db_passwd
    fail_spotted = False
    while list_of_all_reservations:
        each_record = list_of_all_reservations.pop()
        log.info(each_record.__dict__)
        each_record.build_script()
        db_reservation = open("db_reservation", 'w')
        db_reservation.write(each_record.configuration_script)
        db_reservation.close()
        remote_db_path = world.f_cfg.tmp_join("db_reservation")
        fabric_send_file("db_reservation", remote_db_path)
        copy_configuration_file("db_reservation")
        remove_local_file("db_reservation")
        result = fabric_sudo_command('cqlsh --keyspace=keatest --user=keatest --password=keatest -f ' + remote_db_path))
        if exp_failed:
            if result.failed:
                fail_spotted = True
        else:
            assert result.succeeded

    if exp_failed:
        assert fail_spotted


def clear_all_reservations():
    db_name = world.f_cfg.db_name
    db_user = world.f_cfg.db_user
    db_passwd = world.f_cfg.db_passwd
    command = 'for table_name in host_reservations; do cqlsh --keyspace=keatest' \
              ' --user=keatest --password=keatest -e "TRUNCATE $table_name;"' \
              ' ; done'.format(**locals())
    fabric_run_command(command)
    fabric_run_command(command)


def remove_db_reservation():
    # TODO
    pass


if __name__ == '__main__':
    world.proto = "v6"
    test_v6_CassandraReservation_class = CassandraReservation()
    test_v6_CassandraReservation_class.hostname = "some.host.name.com"
    test_v6_CassandraReservation_class.identifier_type = "duid"
    test_v6_CassandraReservation_class.identifier_value = "00:02:00:00:09:BF:10:20:03:04:05:06:07:08"
    test_v6_CassandraReservation_class.ipv6_reservations.append({"ipv6_address_reservation": "2001:db8:1::1111"})
    test_v6_CassandraReservation_class.ipv6_reservations.append({"ipv6_address_reservation": "2001:db8:1::2222"})
    test_v6_CassandraReservation_class.ipv6_reservations.append({"ipv6_prefix_reservation": "2001:db8:1::",
                                                                 "ipv6_prefix_len_reservation": 43})
    test_v6_CassandraReservation_class.ipv6_reservations.append({"ipv6_prefix_reservation": "2001:db8:2::",
                                                                 "ipv6_prefix_len_reservation": 53})
    test_v6_CassandraReservation_class.dhcp4_subnet_id = 4
    test_v6_CassandraReservation_class.dhcp6_subnet_id = 2
    test_v6_CassandraReservation_class.options.append({"code": 1, "option_value": "2001:db8:1::1",
                                                       "space": "dhcp6", "persistent": 1, "scope": "subnet"})
    test_v6_CassandraReservation_class.options.append({"code": 2, "option_value": "2001:db8:1::1",
                                                       "space": "dhcp6", "persistent": 1, "scope": "subnet"})
    # build config:
    test_v6_CassandraReservation_class.build_v6_script()
    # print config:
    test_v6_CassandraReservation_class.print_config()

    # v4 reservation test:
    world.proto = "v4"
    test_v4_CassandraReservation_class = CassandraReservation()
    test_v4_CassandraReservation_class.hostname = "22222222some.host.name.com"
    test_v4_CassandraReservation_class.identifier_type = "hw-address"
    test_v4_CassandraReservation_class.identifier_value = "10:20:30:40:50:63"
    test_v4_CassandraReservation_class.ipv4_address = "192.168.1.12"
    test_v4_CassandraReservation_class.dhcp4_subnet_id = 4
    test_v4_CassandraReservation_class.dhcp6_subnet_id = 2
    test_v4_CassandraReservation_class.next_server = "10.0.0.1"
    test_v4_CassandraReservation_class.server_hostname = "example.org"
    test_v4_CassandraReservation_class.boot_file_name = "bootfile.efi"
    test_v4_CassandraReservation_class.options.append({"code": 1, "option_value": "2001:db8:1::1",
                                                       "space": "dhcp4", "persistent": 1, "scope": "subnet"})
    test_v4_CassandraReservation_class.options.append({"code": 2, "option_value": "2001:db8:1::1",
                                                       "space": "dhcp4", "persistent": 1, "scope": "subnet"})
    # build config:
    test_v4_CassandraReservation_class.build_v4_script()
    # print config:
    test_v4_CassandraReservation_class.print_config()

    world.proto = "v6"
    new_db_backend_reservation("duid", "00:02:00:00:09:BF:10:20:03:04:05:06:07:08")
    update_db_backend_reservation("dhcp4_subnet_id", 4, len(list_of_all_reservations))
    update_db_backend_reservation("dhcp6_subnet_id", 9, len(list_of_all_reservations))
    update_db_backend_reservation("hostname", "added.via.functions", len(list_of_all_reservations))
    ipv6_prefix_db_backend_reservation("2001:db8:1::", 43, "", len(list_of_all_reservations))
    ipv6_address_db_backend_reservation("2001:db8:1::1111", "", len(list_of_all_reservations))
    ipv6_address_db_backend_reservation("2001:db8:1::2222", "", len(list_of_all_reservations))
    option_db_record_reservation(1, "2001:db8:1::1", "dhcp6", 1, "", "subnet", len(list_of_all_reservations))
    option_db_record_reservation(2, "2001:db8:1::21", "dhcp6", 0, "", "subnet", len(list_of_all_reservations))
    list_of_all_reservations[len(list_of_all_reservations)-1].build_script()
    list_of_all_reservations[len(list_of_all_reservations)-1].print_config()

    world.proto = "v4"
    new_db_backend_reservation("hw-address", "10:20:30:40:50:33")
    update_db_backend_reservation("ipv4_address", "192.168.1.12", len(list_of_all_reservations))
    update_db_backend_reservation("dhcp4_subnet_id", 66, len(list_of_all_reservations))
    update_db_backend_reservation("dhcp6_subnet_id", 66, len(list_of_all_reservations))
    update_db_backend_reservation("server_hostname", "example.org.added.via.functions", len(list_of_all_reservations))
    update_db_backend_reservation("next_server", "10.0.0.1", len(list_of_all_reservations))
    update_db_backend_reservation("boot_file_name", "bootfile.efi", len(list_of_all_reservations))
    option_db_record_reservation(1, "10.10.10.10", "dhcp4", 1, "", "subnet", len(list_of_all_reservations))
    option_db_record_reservation(5, "10.10.10.10", "dhcp4", 1, "", "subnet", len(list_of_all_reservations))
    option_db_record_reservation(7, "text-value", "dhcp4", 1, "", "subnet", len(list_of_all_reservations))
    list_of_all_reservations[len(list_of_all_reservations)-1].build_script()
    list_of_all_reservations[len(list_of_all_reservations)-1].print_config()

    for each in list_of_all_reservations:
        del each
