# Copyright (C) 2022 Internet Systems Consortium.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea Control channel TLS connection tests"""

# pylint: disable=invalid-name,line-too-long,unused-argument

import pytest
import os
from base64 import b64encode
from src import misc
from src import srv_msg
from src import srv_control
from src.forge_cfg import world

# note: a lot of reconfigures in all those tests could be done by config-set, this would make tests cleaner
# but due to discovered bug https://gitlab.isc.org/isc-projects/kea/-/issues/2475 I choose to go with reconfigure


@pytest.mark.v4
@pytest.mark.ca
def test_rbac_cert_subject():
    """
    Test assign-role-method set to cert subject
    """
    # Create certificates.
    certificate = srv_control.generate_certificate()
    # Download required certificates.
    ca_cert = certificate.download('ca_cert')
    client_cert = certificate.download('client_cert')
    client_key = certificate.download('client_key')

    # generate more sets of client certificates
    certificate.generate_client(cn='not_kea_client',
                                client_key_name='new_client_key.pem',
                                client_csr_name='new_client.csr',
                                client_cert_name='new_client_cert.pem')
    client_cert_2 = certificate.download('new_client_cert.pem')
    client_key_2 = certificate.download('new_client_key.pem')

    certificate.generate_client(cn='kea_client_2',
                                client_key_name='kea_client_2_key.pem',
                                client_csr_name='kea_client_2.csr',
                                client_cert_name='kea_client_2_cert.pem')
    client_cert_3 = certificate.download('kea_client_2_cert.pem')
    client_key_3 = certificate.download('kea_client_2_key.pem')

    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    # Configure Control Agent to use TLS.
    world.ca_cfg["Control-agent"]["trust-anchor"] = certificate.ca_cert
    world.ca_cfg["Control-agent"]["cert-file"] = certificate.server_cert
    world.ca_cfg["Control-agent"]["key-file"] = certificate.server_key
    world.ca_cfg["Control-agent"]["cert-required"] = True
    hook = [{
        "library": world.f_cfg.hooks_join("libca_rbac.so"),
        "parameters": {
            "assign-role-method": "cert-subject",
            "api-files": os.path.join(world.f_cfg.software_install_path, "share/kea/api"),
            "require-tls": True,
            "roles": [
                {
                    "name": "client",
                    "accept-commands":
                        {
                            "commands": ["config-get"]
                         },
                    "reject-commands": "ALL",

                    "list-match-first": "accept"
                },
                {
                    "name": "kea_client_2",
                    "accept-commands": "ALL",
                    "reject-commands":
                        {
                            "commands": ["config-get"]
                        },
                    "list-match-first": "reject"
                }
            ]
        }
    }]

    world.ca_cfg["Control-agent"]["hooks-libraries"] = hook
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = {"command": "config-get", "arguments": {}}
    resp = srv_msg.send_ctrl_cmd(cmd, 'https', verify=ca_cert, cert=(client_cert, client_key))
    cmd = {"command": "config-get", "arguments": {}}
    resp = srv_msg.send_ctrl_cmd(cmd, 'https', service='agent', verify=ca_cert, cert=(client_cert, client_key))
    assert resp["arguments"]["Control-agent"]["hooks-libraries"] == hook

    for i in ["status-get", "list-commands", "config-get"]:
        cmd = {"command": i, "arguments": {}}
        resp = srv_msg.send_ctrl_cmd(cmd, 'https', verify=ca_cert, cert=(client_cert_2, client_key_2), exp_result=403)
        assert resp['text'] == 'Forbidden', f"text message from response should be 'Forbidden' it is {resp} instead."

    for i in ["list-commands", "status-get"]:
        cmd = {"command": i, "arguments": {}}
        resp = srv_msg.send_ctrl_cmd(cmd, 'https', verify=ca_cert, cert=(client_cert, client_key), exp_result=403)
        assert resp['text'] == 'Forbidden', f"text message from response should be 'Forbidden' it is {resp} instead."

    for i in ["list-commands", "status-get"]:
        cmd = {"command": i, "arguments": {}}
        resp = srv_msg.send_ctrl_cmd(cmd, 'https', service='agent', verify=ca_cert, cert=(client_cert, client_key),
                                     exp_result=403)
        assert resp['text'] == 'Forbidden', f"text message from response should be 'Forbidden' it is {resp} instead."

    for i in ["list-commands", "status-get"]:
        cmd = {"command": i, "arguments": {}}
        resp = srv_msg.send_ctrl_cmd(cmd, 'https', service='agent', verify=ca_cert, cert=(client_cert_3, client_key_3))
        resp = srv_msg.send_ctrl_cmd(cmd, 'https', verify=ca_cert, cert=(client_cert_3, client_key_3))

    cmd = {"command": "config-get", "arguments": {}}
    resp = srv_msg.send_ctrl_cmd(cmd, 'https', service='agent', verify=ca_cert, cert=(client_cert_3, client_key_3),
                                 exp_result=403)
    assert resp['text'] == 'Forbidden', f"text message from response should be 'Forbidden' it is {resp} instead."


@pytest.mark.v4
@pytest.mark.ca
def test_rbac_cert_issuer():
    """
    Test assign-role-method set to cert issuer
    """
    # Create certificates.
    certificate = srv_control.generate_certificate()
    # Download required certificates.
    ca_cert = certificate.download('ca_cert')
    client_cert = certificate.download('client_cert')
    client_key = certificate.download('client_key')

    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    # Configure Control Agent to use TLS.
    world.ca_cfg["Control-agent"]["trust-anchor"] = certificate.ca_cert
    world.ca_cfg["Control-agent"]["cert-file"] = certificate.server_cert
    world.ca_cfg["Control-agent"]["key-file"] = certificate.server_key
    world.ca_cfg["Control-agent"]["cert-required"] = True
    hook = [{
        "library": world.f_cfg.hooks_join("libca_rbac.so"),
        "parameters": {
            "assign-role-method": "cert-issuer",
            "api-files": os.path.join(world.f_cfg.software_install_path, "share/kea/api"),
            "require-tls": True,
            "roles": [
                {
                    "name": "Kea",
                    "accept-commands":
                        {
                            "commands": ["config-get", "config-set"]
                         },
                    "reject-commands": "ALL",
                    "list-match-first": "accept"
                }
            ]
        }
    }]

    world.ca_cfg["Control-agent"]["hooks-libraries"] = hook
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # allowed commands
    cmd = {"command": "config-get", "arguments": {}}
    resp = srv_msg.send_ctrl_cmd(cmd, 'https', verify=ca_cert, cert=(client_cert, client_key))
    cmd = {"command": "config-get", "arguments": {}}
    resp = srv_msg.send_ctrl_cmd(cmd, 'https', service='agent', verify=ca_cert, cert=(client_cert, client_key))
    assert resp["arguments"]["Control-agent"]["hooks-libraries"] == hook

    # some of not allowed
    for i in ["status-get", "list-commands"]:
        cmd = {"command": i, "arguments": {}}
        resp = srv_msg.send_ctrl_cmd(cmd, 'https', verify=ca_cert, cert=(client_cert, client_key), exp_result=403)
        assert resp['text'] == 'Forbidden', f"text message from response should be 'Forbidden' it is {resp} instead."

    # let's change config for different ca issuer
    hook[0]["parameters"]["roles"][0]["name"] = "NOT_KEA"
    world.ca_cfg["Control-agent"]["hooks-libraries"] = hook

    # configure it via config-set
    cmd = {"command": "config-set", "arguments": world.ca_cfg}
    resp = srv_msg.send_ctrl_cmd(cmd, 'https', service='agent', verify=ca_cert, cert=(client_cert, client_key))

    # and now all commands will fail:
    for i in ["status-get", "list-commands", "config-set", "config-get"]:
        cmd = {"command": i, "arguments": {}}
        resp = srv_msg.send_ctrl_cmd(cmd, 'https', verify=ca_cert, cert=(client_cert, client_key), exp_result=403)
        assert resp['text'] == 'Forbidden', f"text message from response should be 'Forbidden' it is {resp} instead."


@pytest.mark.v4
@pytest.mark.ca
@pytest.mark.parametrize('tls', [True, False])
def test_rbac_remote_address(tls):
    """
    Test assign-role-method set to remote-address, with tls or without
    """
    if tls:
        # Create certificates.
        certificate = srv_control.generate_certificate()
        # Download required certificates.
        ca_cert = certificate.download('ca_cert')
        client_cert = certificate.download('client_cert')
        client_key = certificate.download('client_key')

    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    # Configure Control Agent to use TLS.
    if tls:
        world.ca_cfg["Control-agent"]["trust-anchor"] = certificate.ca_cert
        world.ca_cfg["Control-agent"]["cert-file"] = certificate.server_cert
        world.ca_cfg["Control-agent"]["key-file"] = certificate.server_key
        world.ca_cfg["Control-agent"]["cert-required"] = True
    hook = [{
        "library": world.f_cfg.hooks_join("libca_rbac.so"),
        "parameters": {
            "assign-role-method": "remote-address",
            "api-files": os.path.join(world.f_cfg.software_install_path, "share/kea/api"),
            "require-tls": tls,
            "roles": [
                {
                    "name": srv_msg.get_address_facing_remote_address(),
                    "accept-commands":
                        {
                            "commands": ["config-get", "config-set"]
                         },
                    "reject-commands": "ALL",

                    "list-match-first": "accept"
                }
            ]
        }
    }]

    world.ca_cfg["Control-agent"]["hooks-libraries"] = hook
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = {"command": "config-get", "arguments": {}}
    resp = srv_msg.send_ctrl_cmd(cmd,
                                 'https' if tls else 'http',  # depends on tls parameter
                                 verify=ca_cert if tls else None,  # depends on tls parameter
                                 cert=(client_cert, client_key) if tls else None)  # depends on tls parameter
    cmd = {"command": "config-get", "arguments": {}}
    resp = srv_msg.send_ctrl_cmd(cmd,
                                 'https' if tls else 'http',  # depends on tls parameter
                                 service='agent',
                                 verify=ca_cert if tls else None,  # depends on tls parameter
                                 cert=(client_cert, client_key) if tls else None)  # depends on tls parameter
    assert resp["arguments"]["Control-agent"]["hooks-libraries"] == hook

    cmds = ["list-commands", "status-get"]
    service = [None, 'agent']

    for i, x in tuple(zip(cmds, service)):
        cmd = {"command": i, "arguments": {}}
        resp = srv_msg.send_ctrl_cmd(cmd,
                                     'https' if tls else 'http',
                                     service=x,
                                     verify=ca_cert if tls else None,
                                     cert=(client_cert, client_key) if tls else None,
                                     exp_result=403)
        assert resp['text'] == 'Forbidden', f"text message from response should be 'Forbidden' it is {resp} instead."

    # let's change config for different ca issuer
    hook[0]["parameters"]["roles"][0]["name"] = "192.168.51.33"
    world.ca_cfg["Control-agent"]["hooks-libraries"] = hook

    # configure it via config-set
    cmd = {"command": "config-set", "arguments": world.ca_cfg}
    resp = srv_msg.send_ctrl_cmd(cmd,
                                 'https' if tls else 'http',
                                 service='agent',
                                 verify=ca_cert if tls else None,
                                 cert=(client_cert, client_key) if tls else None)

    cmds = ["list-commands", "status-get", "config-get", "config-set"]
    service = [None, 'agent']
    for i, x in tuple(zip(cmds, service)):
        cmd = {"command": i, "arguments": {}}
        resp = srv_msg.send_ctrl_cmd(cmd,
                                     'https' if tls else 'http',
                                     service=x,
                                     verify=ca_cert if tls else None,
                                     cert=(client_cert, client_key) if tls else None,
                                     exp_result=403)
        assert resp['text'] == 'Forbidden', f"text message from response should be 'Forbidden' it is {resp} instead."


@pytest.mark.v4
@pytest.mark.ca
@pytest.mark.parametrize('tls', [False, True])
def test_rbac_basic_authentication(tls):
    """
    Test assign-role-method set to basic authentication, with or without tls enabled
    :param tls: bool, tls value
    """
    # Create certificates.
    if tls:
        certificate = srv_control.generate_certificate()
        # Download required certificates.
        ca_cert = certificate.download('ca_cert')
        client_cert = certificate.download('client_cert')
        client_key = certificate.download('client_key')

    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    # Configure Control Agent to use TLS.
    if tls:
        world.ca_cfg["Control-agent"]["trust-anchor"] = certificate.ca_cert
        world.ca_cfg["Control-agent"]["cert-file"] = certificate.server_cert
        world.ca_cfg["Control-agent"]["key-file"] = certificate.server_key
        world.ca_cfg["Control-agent"]["cert-required"] = tls

    world.ca_cfg["Control-agent"].update({"authentication": {
            "type": "basic",
            "clients":
            [
                {
                    "user": "admin",
                    "password": "1234"
                },
                {
                    "user": "admin2",
                    "password": "1234"
                }
            ]
        }})

    hook = [{
        "library": world.f_cfg.hooks_join("libca_rbac.so"),
        "parameters": {
            "assign-role-method": "basic-authentication",
            "api-files": os.path.join(world.f_cfg.software_install_path, "share/kea/api"),
            "require-tls": tls,
            "roles": [
                {
                    "name": "admin",
                    "accept-commands":
                        {
                            "commands": ["config-get", "list-commands"]
                         },
                    "reject-commands": "ALL",

                    "list-match-first": "accept"
                },
                {
                    "name": "admin2",
                    "accept-commands": "ALL",
                    "reject-commands":
                        {
                            "commands": ["status-get"]
                        },
                    "list-match-first": "reject"
                }
            ]
        }
    }]

    world.ca_cfg["Control-agent"]["hooks-libraries"] = hook
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmds = ["list-commands", "config-get"]
    service = [None, 'agent']

    # first admin, check commands that should be accepted
    for i, x in tuple(zip(cmds, service)):
        cmd = {"command": i, "arguments": {}}
        headers = {'Authorization': f'Basic {b64encode(b"admin:1234").decode("ascii")}'}
        # send different command if there is tls enabled or not
        resp = srv_msg.send_ctrl_cmd(cmd,  # command
                                     'https' if tls else 'http',   # depends on tls parameter
                                     service=x, headers=headers,
                                     verify=ca_cert if tls else None,   # depends on tls parameter
                                     cert=(client_cert, client_key) if tls else None)    # depends on tls parameter

    # first admin, check commands that should be rejected
    cmds = ["status-get", "config-set"]
    service = [None, 'agent']

    # first admin, check commands that should be accepted
    for i, x in tuple(zip(cmds, service)):
        cmd = {"command": i, "arguments": {}}
        headers = {'Authorization': f'Basic {b64encode(b"admin:1234").decode("ascii")}'}
        resp = srv_msg.send_ctrl_cmd(cmd, 'https' if tls else 'http',
                                     service=x, headers=headers, exp_result=403,
                                     verify=ca_cert if tls else None,
                                     cert=(client_cert, client_key) if tls else None)
        assert resp['text'] == 'Forbidden', f"text message from response should be 'Forbidden' it is {resp} instead."

    # first admin, check login failure (401 is unauthorised via basic authentication, 403 is forbidden via rbac)
    cmd = {"command": "config-get", "arguments": {}}
    headers = {'Authorization': f'Basic {b64encode(b"admin:admin").decode("ascii")}'}
    resp = srv_msg.send_ctrl_cmd(cmd, 'https' if tls else 'http',
                                 headers=headers, exp_result=401,
                                 verify=ca_cert if tls else None,
                                 cert=(client_cert, client_key) if tls else None)

    # second admin, check commands that should be rejected, but authorised (should have 403 instead of 401)
    cmd = {"command": "status-get", "arguments": {}}

    headers = {'Authorization': f'Basic {b64encode(b"admin2:1234").decode("ascii")}'}
    resp = srv_msg.send_ctrl_cmd(cmd, 'https' if tls else 'http',
                                 headers=headers, exp_result=403,
                                 verify=ca_cert if tls else None,
                                 cert=(client_cert, client_key) if tls else None)
    assert resp['text'] == 'Forbidden', f"text message from response should be 'Forbidden' it is {resp} instead."

    # second admin, check commands that should be accepted
    cmds = ["config-get", "list-commands"]
    service = [None, 'agent']

    for i, x in tuple(zip(cmds, service)):
        cmd = {"command": i, "arguments": {}}
        headers = {'Authorization': f'Basic {b64encode(b"admin2:1234").decode("ascii")}'}
        resp = srv_msg.send_ctrl_cmd(cmd, 'https' if tls else 'http',
                                     service=x, headers=headers,
                                     verify=ca_cert if tls else None,
                                     cert=(client_cert, client_key) if tls else None)


def _preconfigure_test():
    """
    A lot of tests below use the same basic configuration
    :return: list, part of a Control Agent configuration
    """
    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    world.ca_cfg["Control-agent"].update({"authentication": {
        "type": "basic",
        "clients":
            [
                {
                    "user": "admin",
                    "password": "1234"
                },
                {
                    "user": "admin2",
                    "password": "1234"
                },
                {
                    "user": "admin3",
                    "password": "1234"
                }
            ]
    }})

    hook = [{
        "library": world.f_cfg.hooks_join("libca_rbac.so"),
        "parameters": {
            "assign-role-method": "basic-authentication",
            "api-files": os.path.join(world.f_cfg.software_install_path, "share/kea/api"),
            "require-tls": False,
            "roles": []
        }
    }]
    return hook


def _send_cmd(cmd, user='admin', service=None, result=0):
    """
    Send command to control agent
    :param cmd: dict command
    :param user: string, user name
    :param service: string, service name
    :param result: check value of result parameter in response
    :return: dict, json response
    """
    passwd = b64encode(b"%b:1234" % user.encode('utf8')).decode("ascii")
    headers = {'Authorization': f'Basic {passwd}'}
    return srv_msg.send_ctrl_cmd(cmd, 'http', service=service, headers=headers, exp_result=result)


@pytest.fixture()
def make_sure_file_is_correct():
    """
    Backup dhcp-disable.json file before test, and restore it after
    """
    f = os.path.join(world.f_cfg.get_share_path(), 'api/dhcp-disable.json')
    srv_msg.execute_shell_cmd(f"sed -i'' 's/read/write/' {f}")  # make sure it has correct access
    srv_msg.execute_shell_cmd(f"cp {f} ~/dhcp-disable.json.bk")  # backup file
    yield
    srv_msg.execute_shell_cmd(f"cp ~/dhcp-disable.json.bk {f}")  # restore backup after the test


@pytest.mark.v4
@pytest.mark.ca
def test_rbac_access_by_read_write(make_sure_file_is_correct):
    """
    Check ACLs based on READ and WRITE key words, also check how changing command definition files
    in share/api will reflect on Control Agent work
    :param make_sure_file_is_correct:  fixture that will backup and restore dhcp-disable.json file
    """
    roles = [
        {
            "name": "admin",
            "accept-commands": "READ",
            "reject-commands": "WRITE",
            "list-match-first": "reject"
        },
        {
            "name": "admin2",
            "accept-commands": "WRITE",
            "reject-commands": "READ",
            "list-match-first": "reject"
        }
    ]

    hook = _preconfigure_test()
    hook[0]["parameters"]["roles"] = roles
    world.ca_cfg["Control-agent"]["hooks-libraries"] = hook
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # admin should have read access but not writel
    _send_cmd({"command": "dhcp-disable", "arguments": {}}, result=403)
    _send_cmd({"command": "dhcp-enable", "arguments": {}}, result=403)
    _send_cmd({"command": "build-report", "arguments": {}})
    _send_cmd({"command": "list-commands", "arguments": {}})

    # admin2 should have the opposite
    _send_cmd({"command": "dhcp-disable", "arguments": {}}, user='admin2')
    _send_cmd({"command": "dhcp-enable", "arguments": {}}, user='admin2')
    _send_cmd({"command": "build-report", "arguments": {}}, user='admin2', result=403)
    _send_cmd({"command": "list-commands", "arguments": {}}, user='admin2', result=403)

    # let's change installed json file of dhcp-disable command from write access to read access
    f = os.path.join(world.f_cfg.get_share_path(), 'api/dhcp-disable.json')
    srv_msg.execute_shell_cmd(f"sed -i'' 's/write/read/' {f}")

    # restart everything
    srv_control.start_srv('DHCP', 'restarted')
    # now admin2 should be rejected and admin accepted
    _send_cmd({"command": "dhcp-disable", "arguments": {}}, user='admin2', result=403)
    _send_cmd({"command": "dhcp-disable", "arguments": {}})

    # remove file completely
    srv_msg.execute_shell_cmd(f"rm -f {f}")
    # restart everything
    srv_control.start_srv('DHCP', 'restarted')
    # kea should assume rejection
    _send_cmd({"command": "dhcp-disable", "arguments": {}}, user='admin2', result=403)
    _send_cmd({"command": "dhcp-disable", "arguments": {}}, result=403)


@pytest.mark.v4
@pytest.mark.ca
def test_rbac_access_by_name_removed_file(make_sure_file_is_correct):
    """
    Check how Control Agent reacts on removed command definition file from share/api
    :param make_sure_file_is_correct: fixture that will backup and restore dhcp-disable.json file
    """
    roles = [
        {
            "name": "admin",
            "accept-commands": {"commands": ["dhcp-disable"]},
            "reject-commands": "READ",
            "list-match-first": "accept"
        },
        {
            "name": "admin2",
            "accept-commands": "READ",
            "reject-commands": "WRITE",
            "list-match-first": "reject"
        }
    ]

    hook = _preconfigure_test()
    hook[0]["parameters"]["roles"] = roles
    world.ca_cfg["Control-agent"]["hooks-libraries"] = hook
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    # remove file that define access level
    f = os.path.join(world.f_cfg.get_share_path(), 'api/dhcp-disable.json')
    srv_msg.execute_shell_cmd(f"rm -f {f}")

    # before restart admin2 should be rejected but admin right is based on command name, should work
    _send_cmd({"command": "dhcp-disable", "arguments": {}}, user='admin2', result=403)
    _send_cmd({"command": "dhcp-disable", "arguments": {}})

    srv_control.start_srv('DHCP', 'stopped')

    # start without dhcp-disable file, agent should log an error and exit
    srv_control.start_srv('DHCP', 'started', should_succeed=False)


@pytest.mark.v4
@pytest.mark.ca
def test_rbac_access_by_name_removed_file_2(make_sure_file_is_correct):
    """
    Check how Control Agent reacts on removed command definition file from share/api
    :param make_sure_file_is_correct: fixture that will backup and restore dhcp-disable.json file
    """
    # remove file that define access level
    f = os.path.join(world.f_cfg.get_share_path(), 'api/dhcp-disable.json')
    srv_msg.execute_shell_cmd(f"rm -f {f}")

    roles = [
        {
            "name": "admin",
            "accept-commands": {"commands": ["dhcp-disable"]},
            "reject-commands": "READ",
            "list-match-first": "accept"
        },
        {
            "name": "admin2",
            "accept-commands": "READ",
            "reject-commands": "WRITE",
            "list-match-first": "reject"
        }
    ]

    hook = _preconfigure_test()
    hook[0]["parameters"]["roles"] = roles
    world.ca_cfg["Control-agent"]["hooks-libraries"] = hook
    srv_control.build_and_send_config_files()

    # start without dhcp-disable file, agent should log an error and exit
    srv_control.start_srv('DHCP', 'started', should_succeed=False)

    # now let's add dhcp-disable as our custom command in custom hook, and add 3rd admin based on
    # our new my-custom-hook
    roles.append(
        {
            "name": "admin3",
            "accept-commands": {"hook": "my-custom-hook"},
            "reject-commands": "ALL",
            "list-match-first": "accept"
        })
    hook = _preconfigure_test()
    hook[0]["parameters"]["roles"] = roles

    # add dhcp-disable as custom command, from custom hook
    hook[0]["parameters"].update(
        {
            "commands": [
                {
                    "name": "dhcp-disable",
                    "access": "write",
                    "hook": "my-custom-hook"
                }
            ]
        }
    )

    world.ca_cfg["Control-agent"]["hooks-libraries"] = hook
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # before restart admin2 should be rejected but admin right is based on command name, should work
    _send_cmd({"command": "dhcp-disable", "arguments": {}}, user='admin2', result=403)
    _send_cmd({"command": "dhcp-disable", "arguments": {}})

    # admin3 should be able to use just dhcp-disable
    _send_cmd({"command": "dhcp-enable", "arguments": {}}, user='admin3', result=403)
    _send_cmd({"command": "dhcp-disable", "arguments": {}}, user='admin3')


@pytest.mark.v4
@pytest.mark.ca
def test_rbac_access_by_all_none():
    """
    Check key words ALL and NONE in ACL definition and "list-match-first" parameter
    """
    roles = [
        {
            "name": "admin",
            "accept-commands": "ALL",
            "reject-commands": "NONE",
            "list-match-first": "reject"
        },
        {
            "name": "admin2",
            "accept-commands": "NONE",
            "reject-commands": "ALL",
            "list-match-first": "reject"
        }
    ]

    hook = _preconfigure_test()
    hook[0]["parameters"]["roles"] = roles
    world.ca_cfg["Control-agent"]["hooks-libraries"] = hook
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    for i in ["dhcp-disable", "status-get"]:  # one command is read other is write
        # admin should be accepted in all commands
        _send_cmd({"command": i, "arguments": {}})
        # admin2 should be rejected
        _send_cmd({"command": i, "arguments": {}}, user='admin2', result=403)

    # let's change match first list, and result should be the same
    roles = [
        {
            "name": "admin",
            "accept-commands": "ALL",
            "reject-commands": "NONE",
            "list-match-first": "accept"
        },
        {
            "name": "admin2",
            "accept-commands": "NONE",
            "reject-commands": "ALL",
            "list-match-first": "accept"
        }
    ]
    hook = _preconfigure_test()
    hook[0]["parameters"]["roles"] = roles
    world.ca_cfg["Control-agent"]["hooks-libraries"] = hook
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'restarted')

    for i in ["dhcp-disable", "status-get"]:
        # admin should be rejected in all commands
        _send_cmd({"command": i, "arguments": {}})
        # admin2 should be accepted
        _send_cmd({"command": i, "arguments": {}}, user='admin2', result=403)

    # one role, both list ALL, result should depend on list-mach-first
    roles = [
        {
            "name": "admin",
            "accept-commands": "ALL",
            "reject-commands": "ALL",
            "list-match-first": "accept"
        }
    ]
    hook = _preconfigure_test()
    hook[0]["parameters"]["roles"] = roles
    world.ca_cfg["Control-agent"]["hooks-libraries"] = hook
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'restarted')

    for i in ["dhcp-disable", "status-get"]:
        # admin should be rejected in all commands
        _send_cmd({"command": i, "arguments": {}})

    # one role, both list ALL, result should depend on list-mach-first
    roles = [
        {
            "name": "admin",
            "accept-commands": "ALL",
            "reject-commands": "ALL",
            "list-match-first": "reject"
        }
    ]
    hook = _preconfigure_test()
    hook[0]["parameters"]["roles"] = roles
    world.ca_cfg["Control-agent"]["hooks-libraries"] = hook
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'restarted')

    for i in ["dhcp-disable", "status-get"]:
        # admin should be rejected in all commands
        _send_cmd({"command": i, "arguments": {}}, result=403)


@pytest.mark.v4
@pytest.mark.ca
def test_rbac_access_by_hook_name():
    """
    Check ACL based on hook names
    """
    roles = [
        {
            "name": "admin",
            "accept-commands": {"hook": "lease_cmds"},
            "reject-commands": "ALL",
            "list-match-first": "accept",
        },
        {
            "name": "admin2",
            "accept-commands": "ALL",
            "reject-commands": {"hook": "cb_cmds"},
            "list-match-first": "reject"
        }
    ]

    hook = _preconfigure_test()
    hook[0]["parameters"]["roles"] = roles
    world.ca_cfg["Control-agent"]["hooks-libraries"] = hook
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    for i in ["dhcp-disable", "status-get", "remote-option4-pool-set"]:  # read, write and cb_cmds
        _send_cmd({"command": i, "arguments": {}}, result=403)

    # leases_cmds hook command should be accepted by CA and passed to Kea, but then it will fail, hook is not loaded
    rsp = _send_cmd({"command": "lease4-get-by-client-id", "arguments": {}}, result=2)
    assert "command not supported" in rsp["text"], '"command not supported" missing from return text msg.'

    # admin2 will be accepted in all cmds except cb_cmds hook
    for i in ["dhcp-disable", "status-get"]:
        _send_cmd({"command": i, "arguments": {}}, user='admin2')

    # accepted but failed
    _send_cmd({"command": "lease4-get-by-client-id", "arguments": {}}, user='admin2', result=2)
    assert "command not supported" in rsp["text"], '"command not supported" missing from return text msg.'

    # remote-option4-pool-set is from cb_cmds should be rejected
    _send_cmd({"command": "remote-option4-pool-set", "arguments": {}}, user='admin2', result=403)


@pytest.mark.v4
@pytest.mark.ca
def test_rbac_access_by_commands_with_other_list():
    """
    Check "other-commands" ACL definition
    """
    roles = [
        {
            "name": "admin",
            "accept-commands": {"commands": ["list-commands"]},
            "reject-commands": {"commands": ["config-get", "status-get", "lease4-get-by-client-id"]},
            "other-commands": "reject",  # by default this is reject
            "list-match-first": "reject"
        }
    ]

    hook = _preconfigure_test()
    hook[0]["parameters"]["roles"] = roles
    world.ca_cfg["Control-agent"]["hooks-libraries"] = hook
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # all in reject and other should be rejected
    for i in ["config-get", "status-get", "lease4-get-by-client-id", "build-report", "config-reload"]:
        _send_cmd({"command": i, "arguments": {}}, result=403)
    # just list-commands should work
    _send_cmd({"command": "list-commands", "arguments": {}})

    # now other list is accept
    roles = [
        {
            "name": "admin",
            "accept-commands": {"commands": ["list-commands"]},
            "reject-commands": {"commands": ["config-get", "status-get", "lease4-get-by-client-id"]},
            "other-commands": "accept",  # by default this is reject
            "list-match-first": "reject"
        }
    ]

    hook = _preconfigure_test()
    hook[0]["parameters"]["roles"] = roles
    world.ca_cfg["Control-agent"]["hooks-libraries"] = hook
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'restarted')

    # all in reject should be rejected
    for i in ["config-get", "status-get", "lease4-get-by-client-id"]:
        _send_cmd({"command": i, "arguments": {}}, result=403)

    # list-commands and other should be accepted
    for i in ["list-commands", "build-report", "config-reload"]:
        _send_cmd({"command": i, "arguments": {}})

    # should be accepted but fail due to not loaded hook
    _send_cmd({"command": "lease4-get", "arguments": {}}, result=2)


@pytest.mark.v4
@pytest.mark.ca
def test_rbac_filter_responses():
    """
    Check response filtering defined in "response-filters": ["list-commands"]
    """
    roles = [
        {
            "name": "admin",
            "accept-commands": "ALL",
            "reject-commands": {"hook": "subnet_cmds"},
            "list-match-first": "reject",
        }
    ]

    hook = _preconfigure_test()
    hook[0]["parameters"]["roles"] = roles
    world.ca_cfg["Control-agent"]["hooks-libraries"] = hook
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    resp = _send_cmd({"command": "list-commands", "arguments": {}})

    assert "subnet4-del" in resp["arguments"], "returned list do not contain commands from subnet_cmds hook"
    assert "subnet6-del" in resp["arguments"], "returned list do not contain commands from subnet_cmds hook"
    assert "network6-get" in resp["arguments"], "returned list do not contain commands from subnet_cmds hook"
    assert "network4-add" in resp["arguments"], "returned list do not contain commands from subnet_cmds hook"

    roles = [
        {
            "name": "admin",
            "accept-commands": "ALL",
            "reject-commands":  {"hook": "subnet_cmds"},
            "list-match-first": "reject",
            "response-filters": ["list-commands"],
        }
    ]

    hook = _preconfigure_test()
    hook[0]["parameters"]["roles"] = roles
    world.ca_cfg["Control-agent"]["hooks-libraries"] = hook
    srv_control.add_hooks('libdhcp_subnet_cmds.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # with "response-filters": ["list-commands"] non allowed comments should be filtered out
    resp2 = _send_cmd({"command": "list-commands", "arguments": {}})

    assert "subnet4-del" not in resp2["arguments"], "returned list do contain commands from subnet_cmds hook"
    assert "subnet6-del" not in resp2["arguments"], "returned list do contain commands from subnet_cmds hook"
    assert "network6-get" not in resp2["arguments"], "returned list do contain commands from subnet_cmds hook"
    assert "network4-add" not in resp2["arguments"], "returned list do contain commands from subnet_cmds hook"

    assert len(resp2["arguments"]) < len(resp["arguments"]),\
        "We should get smaller number of commands back in second response"


@pytest.mark.v4
@pytest.mark.ca
@pytest.mark.disabled
def test_default_role():
    # not sure how to test it
    hook = _preconfigure_test()
    hook[0]["parameters"].update({"default-role": {
        "accept-commands": "READ",
        "reject-commands": "WRITE",
    }})

    world.ca_cfg["Control-agent"]["hooks-libraries"] = hook
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # default roles will accept read and reject write commands
    for i in ["config-get", "status-get"]:
        _send_cmd({"command": i, "arguments": {}})
    for i in ["config-set", "dhcp-disable"]:
        _send_cmd({"command": i, "arguments": {}}, result=403)


@pytest.mark.v4
@pytest.mark.ca
def test_unknown_role():
    """
    Check if redefinition of unknown-rule works
    """
    hook = _preconfigure_test()
    hook[0]["parameters"].update({"unknown-role": {
        "accept-commands": "READ",
        "reject-commands": "WRITE",
    }})

    world.ca_cfg["Control-agent"]["hooks-libraries"] = hook
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # unknown roles will accept read and reject write commands
    for i in ["config-get", "status-get"]:
        _send_cmd({"command": i, "arguments": {}})
    for i in ["config-set", "dhcp-disable"]:
        _send_cmd({"command": i, "arguments": {}}, result=403)

    hook = _preconfigure_test()
    hook[0]["parameters"].update({"unknown-role": {
        "accept-commands": {"commands": ["list-commands"]},
        "reject-commands": "ALL",
        "list-match-first": "accept"
    }})

    world.ca_cfg["Control-agent"]["hooks-libraries"] = hook
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'restarted')

    for i in ["list-commands"]:
        _send_cmd({"command": i, "arguments": {}})
    for i in ["config-set", "dhcp-disable", "config-get", "status-get"]:
        _send_cmd({"command": i, "arguments": {}}, result=403)


@pytest.mark.v4
@pytest.mark.ca
def test_creating_access_list_for_multiple_use_cases():
    """
    Define multiple ACLs in "access-control-lists" and then use those in different roles
    """
    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    world.ca_cfg["Control-agent"].update({"authentication": {
        "type": "basic",
        "clients":
            [
                {
                    "user": "admin",
                    "password": "1234"
                },
                {
                    "user": "admin2",
                    "password": "1234"
                },
                {
                    "user": "admin3",
                    "password": "1234"
                }
            ]
    }})

    hook = [{
        "library": world.f_cfg.hooks_join("libca_rbac.so"),
        "parameters": {
            "assign-role-method": "basic-authentication",
            "api-files": os.path.join(world.f_cfg.software_install_path, "share/kea/api"),
            "require-tls": False,
            "access-control-lists": [
                {"my-list-one": {"or": [{"hook": "subnet_cmds"}, {"commands": ["list-commands"]}]}},
                {"my-list-two": {"and": ["READ", {"not": {"commands": ["config-get"]}}]}},
                {"my-list-three": {"or": [{"hook": "subnet_cmds"}, {"hook": "class_cmds"}, {"hook": "lease_cmds"}]}}
            ],
            "roles": [
                {
                    "name": "admin",
                    "accept-commands": "my-list-one",
                    "reject-commands": "ALL",
                    "list-match-first": "accept"
                },
                {
                    "name": "admin2",
                    "accept-commands": "my-list-two",
                    "reject-commands": "ALL",
                    "list-match-first": "accept"
                }
            ],
            "unknown-role": {
                "accept-commands": "my-list-three",
                "reject-commands": "ALL",
            }
        }
    }]

    world.ca_cfg["Control-agent"]["hooks-libraries"] = hook
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # let's check admin, should be able to get list-commands and some from subnet_cmds
    for i in ["list-commands"]:
        _send_cmd({"command": i, "arguments": {}})

    for i in ["network6-add", "subnet4-get", "subnet6-get", "subnet6-update"]:
        # hook is not loaded, rbac should accept but command will fail
        _send_cmd({"command": i, "arguments": {}}, result=2)

    for i in ["config-set", "dhcp-disable", "config-get", "status-get"]:
        _send_cmd({"command": i, "arguments": {}}, result=403)

    # admin2 should be able to use READ command but not config-get, all the rest should be dropped
    for i in ["status-get", "build-report", "version-get"]:
        _send_cmd({"command": i, "arguments": {}}, user='admin2')

    for i in ["subnet4-get", "subnet6-get"]:
        # hook is not loaded, rbac should accept but command will fail
        _send_cmd({"command": i, "arguments": {}}, user='admin2', result=2)

    for i in ["config-set", "dhcp-disable", "config-get", "statistic-reset-all"]:
        _send_cmd({"command": i, "arguments": {}}, result=403)

    # admin3 has no role configured, so will get unknown which allow 3 hooks
    for i in ["subnet4-get", "subnet6-get", "network6-add", "class-update", "lease6-get", "lease6-add"]:
        # hook is not loaded, rbac should accept but command will fail
        _send_cmd({"command": i, "arguments": {}}, user='admin3', result=2)

    for i in ["config-set", "dhcp-disable", "config-get", "statistic-reset-all", "cache-remove"]:
        # host_cache hook added
        _send_cmd({"command": i, "arguments": {}}, user='admin3', result=403)


@pytest.mark.v4
@pytest.mark.ca
def test_mixed_roles():
    """
    Test all access lists types and logic in one single ACL
    """
    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    world.ca_cfg["Control-agent"].update({"authentication": {
        "type": "basic",
        "clients":
            [
                {
                    "user": "admin",
                    "password": "1234"
                }
            ]
    }})

    hook = [{
        "library": world.f_cfg.hooks_join("libca_rbac.so"),
        "parameters": {
            "assign-role-method": "basic-authentication",
            "api-files": os.path.join(world.f_cfg.software_install_path, "share/kea/api"),
            "require-tls": False,
            "roles": [
                {
                    "name": "admin",
                    "accept-commands": {"or": [{"and": [{"hook": "subnet_cmds"}, {"not": "WRITE"}]},
                                               {"and": [{"hook": "lease_cmds"}, {"not": "WRITE"}]},
                                               {"commands": ["config-get", "list-commands"]},
                                               ]},
                    "reject-commands": "ALL",
                    "list-match-first": "accept"
                }
            ]
        }
    }]

    world.ca_cfg["Control-agent"]["hooks-libraries"] = hook
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # basically admin can use READ commands from subnet_cmds and lease_cmds hooks, and config-get, list-commands
    # various commands
    for i in ["class-get", "status-get", "config-set", "build-report"]:
        _send_cmd({"command": i, "arguments": {}}, result=403)

    # not allowed commands from subnet_cmds and lease_cmds
    for i in ["network4-subnet-del", "subnet6-delta-add", "subnet4-add", "lease6-del", "lease4-del", "lease4-wipe"]:
        _send_cmd({"command": i, "arguments": {}}, result=403)

    # allowed commands config-get, list-commands
    for i in ["config-get", "list-commands"]:
        _send_cmd({"command": i, "arguments": {}})

    # allowed READ commands from hooks (allowed but fail because hooks are not loaded)
    for i in ["subnet6-list", "subnet4-get", "lease6-get", "lease4-get", "lease4-get-all"]:
        _send_cmd({"command": i, "arguments": {}}, result=2)
