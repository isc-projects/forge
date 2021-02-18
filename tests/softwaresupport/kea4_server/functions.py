# Copyright (C) 2013-2020 Internet Systems Consortium.
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

from softwaresupport.kea import build_config_files, build_and_send_config_files
from softwaresupport.kea import clear_all, clear_logs, clear_leases, start_srv
from softwaresupport.kea import start_srv, stop_srv, restart_srv, reconfigure_srv
from softwaresupport.kea import agent_control_channel, save_logs, save_leases
from softwaresupport.kea import ha_add_parameter_to_hook, add_hooks, add_parameter_to_hook, add_logger
from softwaresupport.kea import open_control_channel_socket, create_new_class, add_test_to_class
from softwaresupport.kea import set_time, add_line_in_global, config_srv_another_subnet
from softwaresupport.kea import prepare_cfg_add_custom_option, add_interface, add_pool_to_subnet
from softwaresupport.kea import set_conf_parameter_global, set_conf_parameter_subnet, add_line_in_subnet
from softwaresupport.kea import add_line_to_shared_subnet, add_to_shared_subnet, set_conf_parameter_shared_subnet
from softwaresupport.kea import prepare_cfg_subnet_specific_interface, prepare_cfg_subnet
from softwaresupport.kea import prepare_cfg_add_option, prepare_cfg_add_option_subnet
from softwaresupport.kea import prepare_cfg_add_option_shared_subnet, config_client_classification
from softwaresupport.kea import kea_otheroptions, add_option_to_defined_class, config_require_client_classification
from softwaresupport.kea import host_reservation, host_reservation_extension, add_siaddr, disable_client_echo
from softwaresupport.kea import update_ha_hook_parameter, db_setup
# TODO remove this file :) but this is another set of reworks so for another time
