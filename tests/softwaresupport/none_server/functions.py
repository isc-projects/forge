# Copyright (C) 2013-2017 Internet Systems Consortium.
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

import logging

from functions_ddns import add_forward_ddns, add_reverse_ddns, add_keys, build_ddns_config
from protosupport.multi_protocol_functions import test_pause


log = logging.getLogger('forge')


def config_srv_id(id_type, id_value):
    pass


def set_time(*args):
    pass


def add_interface(eth):
    pass


def add_defaults():
    pass


def set_conf_parameter_global(parameter_name, value):
    pass


def set_conf_parameter_subnet(parameter_name, value, subnet_id):
    pass


def prepare_cfg_subnet(subnet, pool, eth = None):
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


def config_srv_another_subnet(subnet, pool, eth):
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


def add_parameter_to_hook(hook_no, parameter_name, parameter_value):
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


def build_and_send_config_files(connection_type, configuration_type="config-file"):
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
