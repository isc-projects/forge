# Copyright (C) 2013-2023 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# pylint: disable=unused-import

# Author: Wlodzimierz Wencel

"""Functions for Kea 4 server. Useless file, up for deletion."""

from src.softwaresupport.kea import build_config_files, build_and_send_config_files
from src.softwaresupport.kea import clear_all, clear_logs, clear_leases
from src.softwaresupport.kea import start_srv, stop_srv, restart_srv, reconfigure_srv
from src.softwaresupport.kea import add_http_control_channel, save_logs, save_leases
from src.softwaresupport.kea import ha_add_parameter_to_hook, add_hooks, delete_hooks, add_parameter_to_hook, add_logger
from src.softwaresupport.kea import open_control_channel_socket, create_new_class, add_test_to_class
from src.softwaresupport.kea import set_time, add_line_in_global, config_srv_another_subnet
from src.softwaresupport.kea import prepare_cfg_add_custom_option, add_interface, add_pool_to_subnet
from src.softwaresupport.kea import set_conf_parameter_global, set_conf_parameter_subnet, add_line_in_subnet
from src.softwaresupport.kea import add_line_to_shared_subnet, add_to_shared_subnet, set_conf_parameter_shared_subnet
from src.softwaresupport.kea import prepare_cfg_subnet_specific_interface, prepare_cfg_subnet
from src.softwaresupport.kea import prepare_cfg_add_option, prepare_cfg_add_option_subnet, prepare_cfg_add_option_pool
from src.softwaresupport.kea import prepare_cfg_add_option_shared_network, config_client_classification
from src.softwaresupport.kea import kea_otheroptions, add_option_to_defined_class, config_require_client_classification
from src.softwaresupport.kea import host_reservation, host_reservation_extension, add_siaddr, disable_client_echo
from src.softwaresupport.kea import update_ha_hook_parameter, db_setup, generate_certificate
from src.softwaresupport.kea import disable_lease_affinity, update_expired_leases_processing, configure_multi_threading
from src.softwaresupport.kea import config_pool_client_classification, add_database_hook, enable_https
from src.softwaresupport.kea import define_host_db_backend, define_lease_db_backend, run_test_config, get_kea_version
# TODO remove this file :) but this is another set of reworks so for another time
