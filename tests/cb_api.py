import srv_msg

def send_cmd(cmd, db_type='mysql', server_tags=None, **kwargs):
    if server_tags is None:
        server_tags = ["default"]
    cmd = {"command": 'remote-' + cmd,
           "arguments": {"remote": {"type": db_type},
                         "server-tags": server_tags}}
    cmd['arguments'].update(kwargs)
    response = srv_msg.send_request('v4', cmd)
    return response


def global_parameter4_set(parameters, db_type='mysql', server_tags=None):
    response = send_cmd('global-parameter4-set', db_type, server_tags, parameters=parameters)
    return response


def subnet4_set(subnets, db_type='mysql', server_tags=None):
    if not isinstance(subnets, list):
        subnets = [subnets]
    response = send_cmd('subnet4-set', db_type, server_tags, subnets=subnets)
    return response


def network4_set(networks, db_type='mysql', server_tags=None):
    if not isinstance(networks, list):
        networks = [networks]
    kwargs = {"shared-networks": networks}
    response = send_cmd('network4-set', db_type, server_tags, **kwargs)
    return response


def subnet4_del_by_id(subnet_id, db_type='mysql', server_tags=None):
    kwargs = {"subnets": [{"id": subnet_id}]}
    response = send_cmd('subnet4-del-by-id', db_type, server_tags, **kwargs)
    return response


def subnet4_del_by_prefix(subnet_prefix, db_type='mysql', server_tags=None):
    kwargs = {"subnets": [{"subnet": subnet_prefix}]}
    response = send_cmd('subnet4-del-by-prefix', db_type, server_tags, **kwargs)
    return response
