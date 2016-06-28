# Copyright (C) 2013-2016 Internet Systems Consortium.
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

from functions_ddns import add_forward_ddns, add_reverse_ddns, add_keys, build_ddns_config

from protosupport.multi_protocol_functions import pasue_test
from logging_facility import *


def set_time(step, which_time, value, subnet = None):
    pass


def add_interface(eth):
    pass


def add_defaults():
    pass


def prepare_cfg_subnet(step, subnet, pool, eth = None):
    pass


def add_pool_to_subnet(step, pool, subnet):
    pass


def config_srv_another_subnet(step, subnet, pool, eth):
    pass


def config_client_classification(step, subnet, option_value):
    pass


def prepare_cfg_prefix(step, prefix, length, delegated_length, subnet):
    pass


def prepare_cfg_add_option(step, option_name, option_value, space,
                           option_code = None, option_type = 'default', where = 'options'):
    pass


def prepare_cfg_add_custom_option(step, opt_name, opt_code, opt_type, opt_value, space):
    pass


def prepare_cfg_add_option_subnet(step, option_name, subnet, option_value):
    pass


def run_command(step, command):
    pass


def set_logger():
    pass


def host_reservation(reservation_type, reserved_value, unique_host_value, subnet):
    pass


def host_reservation_extension(reservation_number, subnet, reservation_type, reserved_value):
    pass


def check_kea_status():
    pass


def set_kea_ctrl_config():
    pass


def add_simple_opt(passed_option):
    pass


def add_option_to_main(option, value):
    pass


def config_db_backend():
    pass


def add_hooks(library_path):
    pass


def add_logger(log_type, severity, severity_level, logging_file):
    pass


def open_control_channel(socket_type, socket_name):
    pass


def cfg_write():
    pass


def check_kea_process_result(succeed, result, process):
    pass


def build_and_send_config_files():
    pass


def start_srv(start, process):
    print "Prepare server as stated in the test, press Enter to continue."
    pasue_test()


def reconfigure_srv():
    print "Prepare server as stated in the test, press Enter to continue."
    pasue_test()


def stop_srv(value = False):
    pass


def restart_srv():
    print "I changes needed, prepare server as stated in the test, press Enter to continue."
    pasue_test()


def clear_leases():
    pass


def save_leases():
    pass


def save_logs():
    pass


def clear_all():
    pass
