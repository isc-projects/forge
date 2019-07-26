import srv_msg
from forge_cfg import world


def send_cmd(cmd, db_type='mysql', server_tags=None, **kwargs):
    if server_tags is None:
        server_tags = ["all"]
    cmd = {"command": cmd,
           "arguments": {"remote": {"type": db_type}}}
    if server_tags != "forbidden":
        cmd['arguments']['server-tags'] = server_tags
    cmd['arguments'].update(kwargs)
    response = srv_msg.send_ctrl_cmd(cmd)
    return response


def global_option_set(options, db_type='mysql', server_tags=None):
    cmd = 'remote-option%s-global-set' % world.proto[1]
    response = send_cmd(cmd, db_type, server_tags, options=options)
    return response


def global_option_del(options, db_type='mysql', server_tags=None):
    cmd = 'remote-option%s-global-del' % world.proto[1]
    response = send_cmd(cmd, db_type, server_tags, options=options)
    return response


def global_parameter_set(parameters, db_type='mysql', server_tags=None):
    cmd = 'remote-global-parameter%s-set' % world.proto[1]
    response = send_cmd(cmd, db_type, server_tags, parameters=parameters)
    return response


def subnet_set(subnets, db_type='mysql', server_tags=None):
    if not isinstance(subnets, list):
        subnets = [subnets]
    cmd = 'remote-subnet%s-set' % world.proto[1]
    response = send_cmd(cmd, db_type, server_tags, subnets=subnets)
    return response


def network_set(networks, db_type='mysql', server_tags=None):
    if not isinstance(networks, list):
        networks = [networks]
    kwargs = {"shared-networks": networks}
    cmd = 'remote-network%s-set' % world.proto[1]
    response = send_cmd(cmd, db_type, server_tags, **kwargs)
    return response


def subnet_del_by_id(subnet_id, db_type='mysql', server_tags=None):
    server_tags = "forbidden"
    kwargs = {"subnets": [{"id": subnet_id}]}
    cmd = 'remote-subnet%s-del-by-id' % world.proto[1]
    response = send_cmd(cmd, db_type, server_tags, **kwargs)
    return response


def subnet_del_by_prefix(subnet_prefix, db_type='mysql', server_tags=None):
    server_tags = "forbidden"
    kwargs = {"subnets": [{"subnet": subnet_prefix}]}
    cmd = 'remote-subnet%s-del-by-prefix' % world.proto[1]
    response = send_cmd(cmd, db_type, server_tags, **kwargs)
    return response
