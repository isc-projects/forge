# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""DDNS control channel basic commands"""

# pylint: disable=invalid-name,line-too-long

import os
import json
import pytest

from src import misc
from src import srv_msg
from src import srv_control
from src.forge_cfg import world


def _send_directly_to_ca(cmd, exp_result=0, address='$(SRV4_ADDR)', exp_failed=False):
    # when sending through http we are getting list, so we want just first element of that list
    result = srv_msg.send_ctrl_cmd_via_http(command=cmd, address=address, exp_result=exp_result, exp_failed=exp_failed)
    if result is None:
        return None
    return result[0]


@pytest.mark.v6
@pytest.mark.ca
@pytest.mark.controlchannel
def test_ca_list():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = dict(command="list-commands", service=[], arguments={})

    response = _send_directly_to_ca(cmd)

    for cmd in ["build-report",
                "config-get",
                "config-reload",
                "config-set",
                "config-test",
                "config-write",
                "list-commands",
                "shutdown",
                "version-get"]:
        assert cmd in response['arguments']


@pytest.mark.v6
@pytest.mark.ca
@pytest.mark.controlchannel
def test_ca_config_get_set():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = dict(command='config-get', arguments={})

    response = _send_directly_to_ca(cmd)

    cfg = response["arguments"]
    # let's dump logging configuration
    del cfg["Control-agent"]["loggers"]
    del world.ca_cfg["Control-agent"]["loggers"]
    # empty list is default config part, in our generated config it's not existing
    del cfg["Control-agent"]["hooks-libraries"]

    assert world.ca_cfg["Control-agent"] == cfg["Control-agent"]

    cmd = dict(command='config-set', arguments=cfg)

    _send_directly_to_ca(cmd)


@pytest.mark.v6
@pytest.mark.ca
@pytest.mark.controlchannel
def test_ca_config_set():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # let's send list-commands to dhcp6 that is running alongside, we expect this command to work
    cmd = dict(command="list-commands", service=['dhcp6'], arguments={})
    response = _send_directly_to_ca(cmd, exp_failed=False)

    # let's check if command went to dhcp6 server
    for cmd in ["config-set",
                "config-test",
                "config-write",
                "dhcp-disable",
                "dhcp-enable",
                "leases-reclaim",
                "libreload",
                "list-commands",
                "server-tag-get",
                "shutdown",
                "statistic-get"]:
        assert cmd in response['arguments']

    # let's create config that will not have configured socked for dhcp
    new_cfg = {"Control-agent": {"control-sockets": {}, "hooks-libraries": [],
                                 "http-host": '$(SRV4_ADDR)', "http-port": 8000}}
    cmd = dict(command='config-set', arguments=new_cfg)

    _send_directly_to_ca(cmd)

    # this will fail (no socket connection)
    cmd = dict(command="list-commands", service=['dhcp6'], arguments={})
    response = _send_directly_to_ca(cmd, exp_result=1)
    assert response["text"] == "forwarding socket is not configured for the server type dhcp6"

    # let's change http-host address
    new_cfg = {"Control-agent": {"control-sockets": {}, "hooks-libraries": [],
                                 "http-host": '$(MGMT_ADDRESS)', "http-port": 8000}}
    cmd = dict(command='config-set', arguments=new_cfg)

    _send_directly_to_ca(cmd)

    # send simple command to old address, it should fail
    cmd = dict(command="list-commands", arguments={})
    _send_directly_to_ca(cmd, exp_failed=True)

    # let's send simple command to new address:
    cmd = dict(command="list-commands", service=[], arguments={})

    response = _send_directly_to_ca(cmd, address='$(MGMT_ADDRESS)')

    for cmd in ["build-report",
                "config-get",
                "config-reload",
                "config-set",
                "config-test",
                "config-write",
                "list-commands",
                "shutdown",
                "version-get"]:
        assert cmd in response['arguments']


@pytest.mark.v6
@pytest.mark.ca
@pytest.mark.disabled
@pytest.mark.controlchannel
def test_ca_config_test():
    # this is bug, won't be fixed #910
    # let's check minimal configuration
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = dict(command='config-get', arguments={})
    response = _send_directly_to_ca(cmd)
    # first check if config we running is accepted back
    cfg = response["arguments"]
    cmd = dict(command='config-test', arguments=cfg)
    _send_directly_to_ca(cmd)

    # create config with different address and test it
    new_cfg = {"Control-agent": {"control-sockets": {}, "hooks-libraries": [],
                                 "http-host": '$(SRV4_ADDR)', "http-port": 8000}}
    cmd = dict(command='config-test', arguments=new_cfg)

    response = _send_directly_to_ca(cmd)
    assert response["text"] == "Configuration check successful"

    # now let's create and check incorrect configuration:
    new_cfg = {"Control-agent": {"control-sockets": {'dhcp6': {'socket-name': '/tmp/control_socket',
                                                               'socket-type': 'SOMETHING'}},
                                 "hooks-libraries": [],
                                 "http-host": '$(SRV4_ADDR)',
                                 "http-port": 8000}}

    cmd = dict(command='config-test', arguments=new_cfg)

    _send_directly_to_ca(cmd, exp_result=1)
    new_cfg = {"Control-agent": {"control-sockets": {'dhcp6': {'socket-name': '/tmp/control_socket',
                                                               'socket-type': 'SOMETHING'}},
                                 "hooks-libraries": [],
                                 "reverse-ddns": {},
                                 "http-host": '$(SRV4_ADDR)',
                                 "http-port": 8000}}

    cmd = dict(command='config-test', arguments=new_cfg)
    _send_directly_to_ca(cmd, exp_result=1)

    # let's now check if CA wasn't reconfigured during config-test
    cmd = dict(command="list-commands", service=[], arguments={})

    response = _send_directly_to_ca(cmd)

    for cmd in ["build-report",
                "config-get",
                "config-reload",
                "config-set",
                "config-test",
                "config-write",
                "list-commands",
                "shutdown",
                "version-get"]:
        assert cmd in response['arguments']


@pytest.mark.v6
@pytest.mark.ca
@pytest.mark.controlchannel
def test_ca_config_reload():
    # let's check minimal configuration
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = dict(command='config-get', arguments={})

    response = _send_directly_to_ca(cmd)

    cfg = response["arguments"]
    # let's dump logging configuration
    del cfg["Control-agent"]["loggers"]
    del world.ca_cfg["Control-agent"]["loggers"]
    # empty list is default config part, in our generated config it's not existing
    del cfg["Control-agent"]["hooks-libraries"]

    assert world.ca_cfg["Control-agent"] == cfg["Control-agent"]

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(MGMT_ADDRESS)')
    srv_control.build_and_send_config_files()

    cmd = dict(command='config-reload', arguments={})
    _send_directly_to_ca(cmd)

    cmd = dict(command="list-commands", arguments={})
    _send_directly_to_ca(cmd, exp_failed=True)

    cmd = dict(command='config-get', arguments={})

    response = _send_directly_to_ca(cmd, address='$(MGMT_ADDRESS)')
    new_cfg = response["arguments"]
    # let's dump logging configuration
    del new_cfg["Control-agent"]["loggers"]
    del world.ca_cfg["Control-agent"]["loggers"]
    # empty list is default config part, in our generated config it's not existing
    del new_cfg["Control-agent"]["hooks-libraries"]
    # if test continue on this point we know that server was reconfigured with proper address
    # now let's check if the rest of the config is correct

    assert world.ca_cfg["Control-agent"] == new_cfg["Control-agent"]


@pytest.mark.v6
@pytest.mark.ca
@pytest.mark.controlchannel
def test_ca_build_report():
    # let's check minimal configuration
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = dict(command='build-report', arguments={})

    response = _send_directly_to_ca(cmd)

    # there is no good way to check specific values, so let's just check that there is there
    assert "Valgrind" in response["text"]
    assert "CXX_VERSION" in response["text"]
    assert "MYSQL_VERSION" in response["text"]
    assert "Included Hooks" in response["text"]


@pytest.mark.v6
@pytest.mark.ca
@pytest.mark.controlchannel
def test_ca_config_write():
    # let's check minimal configuration
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = dict(command='config-write', arguments={"filename": world.f_cfg.data_join("new_CA_config_file")})

    _send_directly_to_ca(cmd)

    srv_msg.copy_remote(world.f_cfg.data_join("new_CA_config_file"))

    # let's load json from downloaded file and check if it is the same what we configured kea with
    with open(os.path.join(world.cfg["test_result_dir"], 'downloaded_file'), 'r', encoding='utf-8') as f:
        downloaded_config = json.load(f)
    del downloaded_config["Control-agent"]["loggers"]
    del world.ca_cfg["Control-agent"]["loggers"]
    del downloaded_config["Control-agent"]["hooks-libraries"]

    assert downloaded_config["Control-agent"] == world.ca_cfg["Control-agent"]


@pytest.mark.v6
@pytest.mark.ca
@pytest.mark.controlchannel
def test_ca_shutdown():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = dict(command='shutdown')
    _send_directly_to_ca(cmd)
    cmd = dict(command='config-write', arguments={})
    _send_directly_to_ca(cmd, exp_failed=True)


@pytest.mark.v6
@pytest.mark.ca
@pytest.mark.controlchannel
def test_ca_version_get():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = dict(command='version-get', arguments={})

    response = _send_directly_to_ca(cmd)
    assert response["arguments"]["extended"]
    # TODO maybe version of kea could be held in forge?
