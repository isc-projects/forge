# Copyright (C) 2022-2024 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# pylint: disable=consider-using-f-string
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=no-else-continue
# pylint: disable=no-else-return
# pylint: disable=useless-object-inheritance

import copy
import logging

from src import srv_control, srv_msg, misc
from src.forge_cfg import world
from src.protosupport.multi_protocol_functions import substitute_vars

from .cb_api import global_parameter_set, subnet_set, network_set, client_class_set
from .cb_api import subnet_del_by_prefix, global_option_set, global_option_del, client_class_del


log = logging.getLogger('forge')
world.check_on_reload = True


def get_config():
    cmd = {"command": "config-get", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response['result'] == 0
    return response['arguments']


def _reload():
    # request config reloading
    cmd = {"command": "config-backend-pull", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd)
    assert response == {'result': 0, 'text': 'On demand configuration update successful.'}


class ConfigElem(object):
    def __init__(self, parent_cfg):
        self.parent_cfg = parent_cfg

    def get_root(self):
        if self.parent_cfg:
            return self.parent_cfg.get_root()
        else:
            return self

    def get_parent(self):
        return self.parent_cfg


class ConfigNetworkModel(ConfigElem):
    def __init__(self, parent_cfg, network_cfg):
        ConfigElem.__init__(self, parent_cfg)
        self.cfg = network_cfg

    def get_dict(self):
        cfg = copy.deepcopy(self.cfg)

        subnets = self.parent_cfg.get_subnets(network=self.cfg['name'])
        if subnets:
            proto = world.proto[1]
            subnets_key = 'subnet' + proto
            cfg[subnets_key] = []
            for sn in subnets:
                cfg[subnets_key].append(sn.get_dict())

        return cfg

    def update(self, backend=None, **kwargs):
        for param, val in kwargs.items():
            param = param.replace('_', '-')
            if val is None:
                if param in self.cfg:
                    del self.cfg[param]
            else:
                self.cfg[param] = val

        # send command
        response = network_set(self.cfg, db_type=backend)
        assert response["result"] == 0

        # request config reloading and check result
        config = self.get_root().reload_and_check()

        return config


class ConfigSubnetModel(ConfigElem):
    def __init__(self, parent_cfg, subnet_cfg):
        ConfigElem.__init__(self, parent_cfg)
        self.cfg = subnet_cfg
        if 'shared-network-name' not in self.cfg:
            self.cfg['shared-network-name'] = ''

    def get_dict(self):
        cfg = copy.deepcopy(self.cfg)
        del cfg['shared-network-name']
        return cfg

    def update(self, backend, **kwargs):
        # prepare arguments
        if 'pool' in kwargs:
            pool = kwargs.pop('pool')
            self.cfg['pools'] = [{"pool": pool}]

        for param, val in kwargs.items():
            param = param.replace('_', '-')
            if val is None:
                if param in self.cfg:
                    del self.cfg[param]
            else:
                self.cfg[param] = val

        # send command
        response = subnet_set(self.cfg, db_type=backend)
        assert response["result"] == 0

        # request config reloading and check result
        config = self.get_root().reload_and_check()

        return config

    def delete(self, backend):
        response = subnet_del_by_prefix(self.cfg['subnet'], db_type=backend)
        assert response["result"] == 0

        config = self.get_root().reload_and_check()
        return config


CONFIG_DEFAULTS = {}
CONFIG_DEFAULTS['v4'] = {
    'decline-probation-period': 86400,
    'echo-client-id': True,
    'match-client-id': True,
    'next-server': '0.0.0.0',
    'reservations-global': False,
    'reservations-in-subnet': True,
    'reservations-out-of-pool': False,
    't1-percent': 0.5,
    't2-percent': 0.875,
    'valid-lifetime': 7200,
    }
CONFIG_DEFAULTS['v6'] = {
    'calculate-tee-times': True,
    'decline-probation-period': 86400,
    "mac-sources": ["any"],
    'preferred-lifetime': int(0.625 * 7200),  # last changed as of kea#2835 merged in Kea 2.3.8
    'relay-supplied-options': ["65"],
    'reservations-global': False,
    'reservations-in-subnet': True,
    'reservations-out-of-pool': False,
    "server-id": {
        "enterprise-id": 0,
        "htype": 0,
        "identifier": "",
        "persist": True,
        "time": 0,
        "type": "LLT"
    },
    't1-percent': 0.5,
    't2-percent': 0.8,
    'valid-lifetime': 7200,
}


def get_cfg_default(name):
    return CONFIG_DEFAULTS[world.proto][name]


def _to_list(val):
    if not isinstance(val, list):
        return [val]
    return val


class ConfigModel(ConfigElem):
    def __init__(self, init_cfg, force_reload=True):
        ConfigElem.__init__(self, None)
        self.cfg = init_cfg
        self.subnets = {}
        self.subnet_id = 0
        self.shared_networks = {}
        self.options = {}
        self.client_classes = []

        if 'subnets' in init_cfg:
            for sn in init_cfg['subnets']:
                subnet_cfg = ConfigSubnetModel(self, sn)
                self.subnets[sn['subnet']] = subnet_cfg

        self.force_reload = force_reload

    def get_dict(self):
        proto = world.proto[1]

        cfg = copy.deepcopy(self.cfg)
        if self.subnets:
            subnets_key = 'subnet' + proto
            cfg[subnets_key] = []
            for sn in self.subnets.values():
                if sn.cfg['shared-network-name'] == '':
                    cfg[subnets_key].append(sn.get_dict())

        if self.shared_networks:
            cfg['shared-networks'] = []
            for net in self.shared_networks.values():
                cfg['shared-networks'].append(net.get_dict())

        if world.f_cfg.install_method == 'make':
            loggers = {"output": world.f_cfg.log_join('kea.log'),
                       "flush": True,
                       "maxsize": 10240000,
                       "maxver": 1,
                       "pattern": ""}
        else:
            loggers = {"output": "stdout",
                       "flush": True,
                       "pattern": ""}

        # loggers config
        cfg["loggers"] = [{"name": "kea-dhcp" + proto,
                           "output-options": [loggers],
                           "debuglevel": 99,
                           "severity": "DEBUG"}]

        # some default settings
        cfg['ddns-replace-client-name'] = 'never'
        cfg['ddns-generated-prefix'] = 'myhost'
        cfg['ddns-send-updates'] = True
        cfg['ddns-conflict-resolution-mode'] = 'check-with-dhcid'

        # combining whole config
        dhcp_key = 'Dhcp' + proto
        cfg = {dhcp_key: cfg,
               "Control-agent": {"http-host": '$(MGMT_ADDRESS)',
                                 "http-port": 8000,
                                 "control-sockets": {"dhcp" + proto: {"socket-type": 'unix',
                                                                      "socket-name": world.f_cfg.run_join('control_socket')}}}}

        substitute_vars(cfg)

        return cfg

    def reload_and_check(self):
        if not self.force_reload:
            return {}

        _reload()
        if world.check_on_reload:
            config = self.compare_local_with_server()
            return config
        else:
            return {}

    def compare_local_with_server(self):
        proto = world.proto[1]
        dhcp_key = 'Dhcp' + proto
        # get config seen by server and compare it with our configuration
        srv_config = get_config()
        my_cfg = self.get_dict()

        # log.info('MY CFG\n%s', pprint.pformat(my_cfg))
        # log.info('KEA CFG\n%s', pprint.pformat(srv_config['Dhcp4']))
        _compare(srv_config[dhcp_key], my_cfg[dhcp_key])
        return srv_config

    def set_global_parameter(self, **kwargs):
        # prepare command
        server_tags = None
        backend = None
        parameters = {}
        for param, val in kwargs.items():
            if val is None:
                if param in self.cfg:
                    del self.cfg[param]
            if param == "server_tags":
                server_tags = _to_list(val)
                continue
            if param == "backend":
                backend = val
                continue
            else:
                param = param.replace('_', '-')
                parameters[param] = val
                self.cfg[param] = val

        if "server_tags" in kwargs:
            del kwargs["server_tags"]
        if "backend" in kwargs:
            del kwargs["backend"]

        response = global_parameter_set(parameters, db_type=backend, server_tags=server_tags)
        assert response["result"] == 0

        # request config reloading and check result
        config = self.reload_and_check()

        return config

    def add_network(self, **kwargs):
        # prepare command
        server_tags = None
        backend = None
        network = {
            "name": "floor13",
            "interface": "$(SERVER_IFACE)"}

        for param, val in kwargs.items():
            if val is None:
                continue
            if param == 'option_data':
                val = _to_list(val)
            if param == "server_tags":
                server_tags = _to_list(val)
                continue
            if param == "backend":
                backend = val
                continue
            param = param.replace('_', '-')
            network[param] = val

            if param == 'interface-id':
                del network['interface']

        if "server_tags" in kwargs:
            del kwargs["server_tags"]
        if "backend" in kwargs:
            del kwargs["backend"]

        # send command
        response = network_set(network, db_type=backend, server_tags=server_tags)
        assert response["result"] == 0

        network_cfg = ConfigNetworkModel(self, network)
        self.shared_networks[network['name']] = network_cfg

        # request config reloading and check result
        config = self.reload_and_check()

        return network_cfg, config

    def update_network(self, backend=None, **kwargs):
        # find network
        if 'network' not in kwargs:
            assert len(self.shared_networks) == 1
            network = list(self.shared_networks.values())[0]
        else:
            network = None
            for n in self.shared_networks.values():
                if n['name'] == kwargs['network']:
                    network = n
            if network is None:
                raise Exception('Cannot find network %s for update' % kwargs['network'])

        config = network.update(db_type=backend, **kwargs)
        return config

    def gen_subnet_id(self):
        self.subnet_id += 1
        return self.subnet_id

    def add_option(self, **kwargs):
        backend = None
        server_tags = None
        option = {"code": 0,
                  "data": None,
                  "csv-format": None,
                  "name": None,
                  "space": None}
        for param, val in kwargs.items():
            if val is None:
                continue
            if param == "server_tags":
                server_tags = _to_list(val)
                continue
            if param == "backend":
                backend = val
                continue
            param = param.replace('_', '-')
            option[param] = val
        self.cfg["option-data"] = [option]

        if "server_tags" in kwargs:
            del kwargs["server_tags"]
        if "backend" in kwargs:
            del kwargs["backend"]

        # send command
        response = global_option_set([option], db_type=backend, server_tags=server_tags)
        assert response["result"] == 0

        # request config reloading and check result
        config = self.reload_and_check()

        return config

    def del_option(self, **kwargs):
        server_tags = None
        backend = None
        option = {"code": 0}
        for param, val in kwargs.items():
            if val is None:
                continue
            if param == "server_tags":
                server_tags = _to_list(val)
                continue
            if param == "backend":
                backend = val
                continue
            param = param.replace('_', '-')
            option[param] = val
        if "server_tags" in kwargs:
            del kwargs["server_tags"]
        if "backend" in kwargs:
            del kwargs["backend"]

        self.cfg["option-data"] = []

        # send command
        response = global_option_del([option], db_type=backend, server_tags=server_tags)
        assert response["result"] == 0

        # request config reloading and check result
        config = self.reload_and_check()

        return config

    def add_subnet(self, **kwargs):
        # prepare command
        server_tags = None
        backend = None
        default_pool_range = "192.168.50.1-192.168.50.100" if world.proto == 'v4' else '2001:db8:1::1-2001:db8:1::100'
        subnet = {
            "id": self.gen_subnet_id(),
            "subnet": "192.168.50.0/24" if world.proto == 'v4' else '2001:db8:1::/64',
            "interface": "$(SERVER_IFACE)",
            "shared-network-name": "",
            "pools": [{"pool": kwargs.pop('pool') if 'pool' in kwargs else default_pool_range,
                       "option-data": _to_list(kwargs.pop('pool_option_data'))
                       if 'pool_option_data' in kwargs else []}]}

        for param, val in kwargs.items():
            if val is None:
                continue
            if param == 'network':
                param = 'shared-network-name'
                val = val.cfg['name']
            if param == 'option_data':
                val = _to_list(val)
            if param == "server_tags":
                server_tags = _to_list(val)
                continue
            if param == "backend":
                backend = val
                continue
            param = param.replace('_', '-')
            subnet[param] = val

            if param == 'interface-id':
                del subnet['interface']

        if "server_tags" in kwargs:
            del kwargs["server_tags"]
        if "backend" in kwargs:
            del kwargs["backend"]

        # send command
        response = subnet_set(subnet, db_type=backend, server_tags=server_tags)
        assert response["result"] == 0

        subnet_cfg = ConfigSubnetModel(self, subnet)
        self.subnets[subnet['subnet']] = subnet_cfg

        # request config reloading and check result
        config = self.get_root().reload_and_check()

        return subnet_cfg, config

    def update_subnet(self, backend=None, **kwargs):
        # find subnet
        if 'subnet' not in kwargs:
            assert len(self.subnets) == 1
            subnet = list(self.subnets.values())[0]
        else:
            subnet = None
            for sn in self.subnets.values():
                if sn['subnet'] == kwargs['subnet']:
                    subnet = sn
            if subnet is None:
                raise Exception('Cannot find subnet %s for update' % kwargs['subnet'])

        config = subnet.update(backend, **kwargs)
        return config

    def del_subnet(self, backend=None, **kwargs):
        # find subnet
        if 'subnet' not in kwargs:
            assert len(self.subnets) == 1
            subnet = list(self.subnets.values())[0]
        else:
            subnet = None
            for sn in self.subnets.values():
                if sn['subnet'] == kwargs['subnet']:
                    subnet = sn
            if subnet is None:
                raise Exception('Cannot find subnet %s for update' % kwargs['subnet'])

        del self.subnets[subnet.cfg['subnet']]

        config = subnet.delete(backend)
        return config

    def get_subnets(self, network=None):
        subnets = []
        for sn in self.subnets.values():
            if (network is not None and sn.cfg['shared-network-name'] == network) or network is None:
                subnets.append(sn)
        return subnets

    def add_class(self, **kwargs):
        if "client-classes" not in self.cfg:
            self.cfg["client-classes"] = []
        server_tags = None
        backend = None
        client_class = {'boot-file-name': '',
                        'next-server': '0.0.0.0',
                        'option-data': [],
                        'option-def': [],
                        'server-hostname': '',
                        'valid-lifetime': 7200}
        if world.proto == 'v6':
            client_class = {'option-data': [],
                            'valid-lifetime': 7200,
                            'preferred-lifetime': 3600}
        for param, val in kwargs.items():
            if val is None:
                continue
            if param == "server_tags":
                server_tags = _to_list(val)
                continue
            if param == "backend":
                backend = val
                continue
            param = param.replace('_', '-')
            client_class[param] = val
        self.cfg["client-classes"].append(client_class)
        self.client_classes.append(client_class)

        if "server_tags" in kwargs:
            del kwargs["server_tags"]
        if "backend" in kwargs:
            del kwargs["backend"]

        # send command
        response = client_class_set([client_class], db_type=backend, server_tags=server_tags)
        assert response["result"] == 0

        # request config reloading and check result
        config = self.reload_and_check()

        return client_class, config

    def del_class(self, class_name=None, backend=None):
        # find subnet
        my_class = None
        idx = None
        print(self.client_classes)
        for singe_class in self.client_classes:
            if singe_class['name'] == class_name:
                my_class = singe_class
                idx = self.client_classes.index(my_class)

        if my_class is None:
            raise Exception('Cannot find class %s to delete' % class_name)
        if my_class is not None:
            del self.client_classes[idx]
            del self.cfg["client-classes"][idx]

        response = client_class_del(class_name, backend)
        assert response["result"] == 0

        config = self.get_root().reload_and_check()
        return config


def _merge_configs(a, b, path=None):
    if path is None:
        path = []
    for k in b:
        if k in a:
            if isinstance(a[k], dict) and isinstance(b[k], dict):
                _merge_configs(a[k], b[k], path + [str(k)])
            elif isinstance(a[k], list) and isinstance(b[k], list):
                for al, bl in zip(a[k], b[k]):
                    _merge_configs(al, bl)
            elif a[k] == b[k]:
                pass
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(k)]))
        else:
            a[k] = b[k]
    return a


def _compare(recv_any, exp_any):
    if isinstance(exp_any, dict):
        _compare_dicts(recv_any, exp_any)
    elif isinstance(recv_any, list):
        _compare_lists(recv_any, exp_any)
    else:
        assert recv_any == exp_any


def _compare_dicts(rcvd_dict, exp_dict):
    all_keys = set(rcvd_dict.keys()).union(set(exp_dict.keys()))
    for k in all_keys:
        if k in ['id', 'config-control', 'lease-database', 'server-tag', 'server-tags',
                 'interfaces-config', 'dhcp-queue-control', 'dhcp-ddns',
                 'hooks-libraries', 'sanity-checks', 'expired-leases-processing',
                 'control-socket', 'host-reservation-identifiers', 'relay',
                 'hostname-char-set', 'statistic-default-sample-count',
                 'multi-threading', 'ip-reservations-unique',
                 'ddns-use-conflict-resolution',
                 # those values depends on configured valid-lifetime and preferred-lifetime
                 # let's ignore it for now since we don't have procedure to check it
                 # qa-dhcp #287
                 'max-valid-lifetime', 'min-valid-lifetime', 'max-preferred-lifetime', 'min-preferred-lifetime',
                 'allocator', 'pd-allocator',
                 ]:
            # TODO: for now ignore these fields
            continue
        if k in exp_dict:
            if exp_dict[k]:
                assert k in rcvd_dict, f'expected: {k} in {rcvd_dict}'
                _compare(rcvd_dict[k], exp_dict[k])
            else:
                assert k not in rcvd_dict or rcvd_dict[k] == exp_dict[k], f'expected: {k} not in {rcvd_dict} or {rcvd_dict[k]} == {exp_dict[k]}'
        if k in rcvd_dict and rcvd_dict[k]:
            if k not in exp_dict:
                if k in CONFIG_DEFAULTS[world.proto]:
                    assert rcvd_dict[k] == CONFIG_DEFAULTS[world.proto][k], f'expected: {rcvd_dict[k]} == {CONFIG_DEFAULTS[world.proto][k]}'
                else:
                    assert k in exp_dict, f'expected: {k} in {exp_dict}'
            else:
                _compare(rcvd_dict[k], exp_dict[k])


def _compare_lists(rcvd_list, exp_list):
    assert len(rcvd_list) == len(exp_list)
    for r_v, e_v in zip(rcvd_list, exp_list):
        _compare(r_v, e_v)


def _normalize_keys(kwargs):
    kwargs2 = {}
    for k, v in kwargs.items():
        nk = k.replace('_', '-')
        kwargs2[nk] = v
    return kwargs2


def setup_server(destination: str = world.f_cfg.mgmt_address,
                 interface: str = world.f_cfg.server_iface,
                 **kwargs):
    """
    Create a basic configuration and send it to the Kea server.

    :param destination: address of server that is being set up
    :param interface: the client-facing interface on the server
    :param kwargs: dynamic set of arguments
    :return: the configuration that was sent to Kea and sometimes as a second
        variable: the configuration retrieved through "config-get"
    """

    misc.test_setup()

    srv_control.config_srv_subnet('$(EMPTY)', '$(EMPTY)')

    config_model_args = {}
    init_cfg = {"interfaces-config": {"interfaces": [interface]},
                "lease-database": {"type": "memfile"},
                "control-socket": {"socket-type": 'unix',
                                   "socket-name": world.f_cfg.run_join('control_socket')}}

    for param, val in kwargs.items():
        if val is None or param == 'check-config':
            continue
        if param in ['force-reload']:
            # these fields are passed to ConfigModel
            config_model_args['force_reload'] = val
            continue

        param = param.replace('_', '-')
        init_cfg[param] = val

    cfg = ConfigModel(init_cfg, **config_model_args)

    srv_control.agent_control_channel()  # to force enabling ctrl-agent
    srv_control.build_and_send_config_files(cfg=cfg.get_dict(), dest=destination)
    srv_control.start_srv('DHCP', 'started')

    # check actual configuration if requested
    if 'check-config' in kwargs and kwargs['check-config']:
        srv_config = cfg.compare_local_with_server()
        return cfg, srv_config

    return cfg


def setup_server_for_config_backend_cmds(**kwargs):
    default_cfg = {"hooks-libraries": [{"library": world.f_cfg.hooks_join("libdhcp_cb_cmds.so")}],
                   "server-tag": "abc",
                   "parked-packet-limit": 256}
    db = {"config-control": {"config-databases": [{"user": "$(DB_USER)",
                                                   "password": "$(DB_PASSWD)",
                                                   "name": "$(DB_NAME)",
                                                   "type": ""}]}}
    kwargs = _normalize_keys(kwargs)
    if "server-tag" in kwargs:
        default_cfg["server-tag"] = kwargs["server-tag"]
        del kwargs["server-tag"]
    if "backend-type" in kwargs:
        if kwargs["backend-type"] not in ["mysql", "postgresql"]:
            assert False, f"Kea does not support {kwargs['backend-type']} as config backend."

        db["config-control"]["config-databases"][0]["type"] = kwargs["backend-type"]

        if kwargs["backend-type"] == "postgresql":
            default_cfg["hooks-libraries"].append({"library": world.f_cfg.hooks_join("libdhcp_pgsql_cb.so")})
        else:
            default_cfg["hooks-libraries"].append({"library": world.f_cfg.hooks_join("libdhcp_mysql_cb.so")})

        del kwargs["backend-type"]
    else:  # let' for now keep default value, but it may result in missing some tests with pgsql backend
        db["config-control"]["config-databases"][0]["type"] = "mysql"
        default_cfg["hooks-libraries"].append({"library": world.f_cfg.hooks_join("libdhcp_mysql_cb.so")})

    if "hooks-libraries" in kwargs:
        default_cfg["hooks-libraries"] += kwargs["hooks-libraries"]
        del kwargs["hooks-libraries"]

    default_cfg.update(db)
    init_cfg = _merge_configs(default_cfg, kwargs)
    result = setup_server(**init_cfg)

    return result


def setup_server_with_radius(destination: str = world.f_cfg.mgmt_address,
                             interface: str = world.f_cfg.server_iface,
                             **kwargs):
    """
    Create a RADIUS configuration and send it to the Kea server.

    :param destination: address of server that is being set up
    :param interface: the client-facing interface on the server
    :param kwargs: dynamic set of arguments
    :return: the configuration that was sent to Kea
    """

    if world.proto == 'v4':
        expression = "hexstring(pkt4.mac, ':')"
    else:
        expression = "substring(hexstring(option[1].hex, ':'), 12, 17)"

    default_cfg = {"hooks-libraries": [{
        # Load the host cache hook library. It is needed by the RADIUS
        # library to keep the attributes from authorization to later user
        # for accounting.
        "library": world.f_cfg.hooks_join("libdhcp_host_cache.so")
    }, {
        # Load the RADIUS hook library.
        "library": world.f_cfg.hooks_join("libdhcp_radius.so"),
        "parameters": {
            "client-id-printable": True,
            "reselect-subnet-address": True,
            "reselect-subnet-pool": True,
            # Configure an access (aka authentication/authorization) server.
            "access": {
                # This starts the list of access servers
                "servers": [
                    {
                        # These are parameters for the first (and only) access server
                        "name": destination,
                        "port": 1812,
                        "secret": "testing123"
                    }
                ],
                "attributes": [
                    {
                        "name": "User-Password",
                        "expr": expression
                    }
                ]
            },
            "accounting": {
                "servers": [
                    {
                        # These are parameters for the first (and only) access server
                        "name": destination,
                        "port": 1813,
                        "secret": "testing123"
                    }
                ]
            }
        }
    }]}

    kwargs = _normalize_keys(kwargs)
    init_cfg = _merge_configs(default_cfg, kwargs)
    result = setup_server(destination=destination, interface=interface, **init_cfg)

    # Update dhcp_cfg and subnet_cnt in case further changes are done to the config.
    world.dhcp_cfg = result.get_dict()[f'Dhcp{world.proto[1]}']
    srv_control.update_subnet_counter()

    return result
