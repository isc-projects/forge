# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from src import srv_msg
from src.forge_cfg import world


def send_cmd(cmd, db_type='', server_tags=None, **kwargs):
    if server_tags is None:
        server_tags = ["all"]
    cmd = {"command": cmd,
           "arguments": {"remote": {"type": db_type}}}
    if server_tags != "forbidden":
        cmd['arguments']['server-tags'] = server_tags
    cmd['arguments'].update(kwargs)
    response = srv_msg.send_ctrl_cmd(cmd)
    return response


def global_option_set(options, db_type='', server_tags=None):
    cmd = f'remote-option{world.proto[1]}-global-set'
    response = send_cmd(cmd, db_type, server_tags, options=options)
    return response


def client_class_set(classes, db_type='', server_tags=None):
    if not isinstance(classes, list):
        classes = [classes]
    kwargs = {"client-classes": classes}
    cmd = f'remote-class{world.proto[1]}-set'
    response = send_cmd(cmd, db_type, server_tags, **kwargs)
    return response


def client_class_del(class_name, db_type=''):
    server_tags = "forbidden"
    kwargs = {"client-classes": [{"name": class_name}]}
    cmd = f'remote-class{world.proto[1]}-del'
    response = send_cmd(cmd, db_type, server_tags, **kwargs)
    return response


def global_option_del(options, db_type='', server_tags=None):
    cmd = f'remote-option{world.proto[1]}-global-del'
    response = send_cmd(cmd, db_type, server_tags, options=options)
    return response


def global_parameter_set(parameters, db_type='', server_tags=None):
    cmd = f'remote-global-parameter{world.proto[1]}-set'
    response = send_cmd(cmd, db_type, server_tags, parameters=parameters)
    return response


def subnet_set(subnets, db_type='', server_tags=None):
    if not isinstance(subnets, list):
        subnets = [subnets]
    cmd = f'remote-subnet{world.proto[1]}-set'
    response = send_cmd(cmd, db_type, server_tags, subnets=subnets)
    return response


def network_set(networks, db_type='', server_tags=None):
    if not isinstance(networks, list):
        networks = [networks]
    kwargs = {"shared-networks": networks}
    cmd = f'remote-network{world.proto[1]}-set'
    response = send_cmd(cmd, db_type, server_tags, **kwargs)
    return response


def subnet_del_by_id(subnet_id, db_type='', server_tags=None):
    server_tags = "forbidden"
    kwargs = {"subnets": [{"id": subnet_id}]}
    cmd = f'remote-subnet{world.proto[1]}-del-by-id'
    response = send_cmd(cmd, db_type, server_tags, **kwargs)
    return response


def subnet_del_by_prefix(subnet_prefix, db_type='', server_tags=None):
    server_tags = "forbidden"
    kwargs = {"subnets": [{"subnet": subnet_prefix}]}
    cmd = f'remote-subnet{world.proto[1]}-del-by-prefix'
    response = send_cmd(cmd, db_type, server_tags, **kwargs)
    return response
