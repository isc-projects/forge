# Copyright (C) 2013-2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# pylint: disable=invalid-name,line-too-long,unused-import, unused-argument

# Author: Wlodzimierz Wencel

# pylint: disable=unused-argument,unused-import

import logging

from src.protosupport.multi_protocol_functions import test_pause
from .functions_ddns import add_forward_ddns, add_reverse_ddns, add_keys, build_ddns_config


log = logging.getLogger('forge')


def config_srv_id(*args):
    pass


def set_time(*args):
    pass


def add_interface(*args):
    pass


def add_defaults():
    pass


def set_conf_parameter_global(*args):
    pass


def set_conf_parameter_subnet(parameter_name, value, subnet_id):
    pass


def prepare_cfg_subnet(*args):
    pass


def prepare_cfg_subnet_specific_interface(interface, address, subnet, pool):
    pass


def add_to_shared_subnet(subnet_id, shared_subnet_id):
    pass


def add_line_to_shared_subnet(subnet_id, cfg_line):
    pass


def prepare_cfg_add_option_shared_subnet(option_name, shared_subnet, option_value):
    pass


def set_conf_parameter_shared_subnet(parameter_name, value, subnet_id):
    pass


def add_pool_to_subnet(pool, subnet):
    pass


def config_srv_another_subnet(subnet, pool, iface):
    pass


def config_client_classification(subnet, option_value):
    pass


def prepare_cfg_prefix(prefix, length, delegated_length, subnet):
    pass


def prepare_cfg_add_option(*args):
    pass


def prepare_cfg_add_custom_option(opt_name, opt_code, opt_type, opt_value, space):
    pass


def prepare_cfg_add_option_subnet(option_name, subnet, option_value):
    pass


def add_line_in_global(command):
    pass


def add_line_in_subnet(subnetid, command):
    pass


def set_logger(*args):
    pass


def host_reservation(*args):
    pass


def host_reservation_extension(*args):
    pass


def create_new_class(*args):
    pass


def add_test_to_class(*args):
    pass


def add_option_to_defined_class(*args):
    pass


def check_kea_status():
    pass


def set_kea_ctrl_config():
    pass


def add_simple_opt(passed_option):
    pass


def add_option_to_main(option, value):
    pass


def config_add_reservation_database():
    pass


def config_db_backend():
    pass


def add_hooks(library_path):
    pass


def delete_hooks(hook_patterns):
    pass


def add_parameter_to_hook(hook_number_or_name, parameter_name, parameter_value):
    pass


def add_logger(log_type, severity, severity_level, logging_file):
    pass


def open_control_channel_socket(socket_type, socket_name):
    pass


def agent_control_channel(host_address, host_port, socket_type, socket_name):
    pass


def cfg_write():
    pass


def check_kea_process_result(succeed, result, process):
    pass


def build_and_send_config_files():
    pass


def start_srv(*args):
    log.info("Prepare server as stated in the test, press Enter to continue.")
    test_pause()


def reconfigure_srv(*args):
    log.info("Prepare server as stated in the test, press Enter to continue.")
    test_pause()


def stop_srv(*args):
    pass


def restart_srv():
    log.info("I changes needed, prepare server as stated in the test, press Enter to continue.")
    test_pause()


def clear_leases():
    pass


def save_leases():
    pass


def save_logs():
    pass


def clear_all():
    pass
