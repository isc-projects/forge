# Copyright (C) 2017-2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# pylint: disable=unused-argument
# pylint: disable=unused-import

# Author: Wlodzimierz Wencel

from src.forge_cfg import world
from src.softwaresupport.isc_dhcp6_server.functions_ddns import add_ddns_server, add_ddns_server_options
from src.softwaresupport.isc_dhcp6_server.functions_ddns import add_forward_ddns
from src.softwaresupport.isc_dhcp6_server.functions_ddns import add_reverse_ddns, add_keys, build_ddns_config
