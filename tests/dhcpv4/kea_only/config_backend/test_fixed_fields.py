"""Kea config backend testing: fixed fields set based on next-server, server-hostname and boot-file-name settings."""

import pytest

from dhcp4_scen import get_address
from cb_model import setup_server_for_config_backend_cmds

pytestmark = [pytest.mark.kea_only,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.config_backend,
              pytest.mark.v4]


@pytest.mark.parametrize("initial_next_server,initial_server_hostname,initial_boot_file_name",
                         [(None, None, None),                              # pick defaults
                          ('1.1.1.1', 'aaa.example.com', '/boot/aaa')])    # some specific initial values
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_subnet_override_init(initial_next_server, initial_server_hostname, initial_boot_file_name, backend):
    cfg = setup_server_for_config_backend_cmds(backend_type=backend, next_server=initial_next_server,
                                               server_hostname=initial_server_hostname,
                                               boot_file_name=initial_boot_file_name)

    cfg.add_subnet(backend=backend)
    get_address(exp_next_server=initial_next_server if initial_next_server else '0.0.0.0',
                exp_server_hostname=initial_server_hostname if initial_server_hostname else '',
                exp_boot_file_name=initial_boot_file_name if initial_boot_file_name else '')

    cfg.set_global_parameter(backend=backend, next_server='2.2.2.2',
                             server_hostname='bbb.example.com',
                             boot_file_name='/boot/bbb')
    get_address(exp_next_server='2.2.2.2',
                exp_server_hostname='bbb.example.com',
                exp_boot_file_name='/boot/bbb')


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_subnet_change_params(backend):
    cfg = setup_server_for_config_backend_cmds(backend_type=backend)

    # create one subnet with defaults
    cfg.add_subnet(backend=backend)
    get_address(exp_next_server='0.0.0.0',
                exp_server_hostname='',
                exp_boot_file_name='')

    # set global params and check if they are in returned lease
    cfg.set_global_parameter(backend=backend, next_server='2.2.2.2',
                             server_hostname='bbb.example.com',
                             boot_file_name='/boot/bbb')
    get_address(exp_next_server='2.2.2.2',
                exp_server_hostname='bbb.example.com',
                exp_boot_file_name='/boot/bbb')

    # delete subnet and create new one with explicit params
    # and check if they are in returned lease
    cfg.del_subnet(backend=backend)
    cfg.add_subnet(backend=backend, next_server='3.3.3.3',
                   server_hostname='ccc.example.com',
                   boot_file_name='/boot/ccc')
    get_address(exp_next_server='3.3.3.3',
                exp_server_hostname='ccc.example.com',
                exp_boot_file_name='/boot/ccc')

    # update subnet and check if new params are in returned lease
    cfg.update_subnet(backend=backend, next_server='4.4.4.4',
                      server_hostname='ddd.example.com',
                      boot_file_name='/boot/ddd')
    get_address(exp_next_server='4.4.4.4',
                exp_server_hostname='ddd.example.com',
                exp_boot_file_name='/boot/ddd')


@pytest.mark.parametrize("initial_next_server,initial_server_hostname,initial_boot_file_name",
                         [(None, None, None),                              # pick defaults
                          ('1.1.1.1', 'aaa.example.com', '/boot/aaa')])    # some specific initial values
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_network_override_init(initial_next_server, initial_server_hostname, initial_boot_file_name, backend):
    cfg = setup_server_for_config_backend_cmds(backend_type=backend, next_server=initial_next_server,
                                               server_hostname=initial_server_hostname,
                                               boot_file_name=initial_boot_file_name)

    cfg.add_subnet(backend=backend)
    get_address(exp_next_server=initial_next_server if initial_next_server else '0.0.0.0',
                exp_server_hostname=initial_server_hostname if initial_server_hostname else '',
                exp_boot_file_name=initial_boot_file_name if initial_boot_file_name else '')

    cfg.set_global_parameter(backend=backend, next_server='2.2.2.2',
                             server_hostname='bbb.example.com',
                             boot_file_name='/boot/bbb')
    get_address(exp_next_server='2.2.2.2',
                exp_server_hostname='bbb.example.com',
                exp_boot_file_name='/boot/bbb')


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_network_change_params(backend):
    cfg = setup_server_for_config_backend_cmds(backend_type=backend)

    # add 1 subnet, no shared networks yet, and check received lease
    cfg.add_subnet(backend=backend)
    get_address(exp_next_server='0.0.0.0',  # TODO: why 0.0.0.0? why not ''
                exp_server_hostname='',
                exp_boot_file_name='')

    # change global params and check received lease
    cfg.set_global_parameter(backend=backend, next_server='2.2.2.2',
                             server_hostname='bbb.example.com',
                             boot_file_name='/boot/bbb')
    get_address(exp_next_server='2.2.2.2',
                exp_server_hostname='bbb.example.com',
                exp_boot_file_name='/boot/bbb')

    # delete subnet and add 1 network with 1 subnet
    # and check received lease if it takes params from network now
    cfg.del_subnet(backend=backend)
    network_cfg, _ = cfg.add_network(backend=backend, next_server='3.3.3.3',
                                     server_hostname='ccc.example.com',
                                     boot_file_name='/boot/ccc')

    subnet2_cfg, _ = cfg.add_subnet(backend=backend, network=network_cfg)

    get_address(exp_next_server='3.3.3.3',
                exp_server_hostname='ccc.example.com',
                exp_boot_file_name='/boot/ccc')

    # change params in network's subnet
    # and check received lease if it takes params from subnet now
    subnet2_cfg.update(backend=backend, next_server='4.4.4.4',
                       server_hostname='ddd.example.com',
                       boot_file_name='/boot/ddd')
    get_address(exp_next_server='4.4.4.4',
                exp_server_hostname='ddd.example.com',
                exp_boot_file_name='/boot/ddd')

    # reset params in subnet
    # and check received lease if it takes params from network scope
    subnet2_cfg.update(backend=backend, next_server='',
                       server_hostname='',
                       boot_file_name='')
    get_address(exp_next_server='3.3.3.3',
                exp_server_hostname='ccc.example.com',
                exp_boot_file_name='/boot/ccc')

    # reset params in network
    # and check received lease if it takes params from global scope
    network_cfg.update(backend=backend, next_server='',
                       server_hostname='',
                       boot_file_name='')
    get_address(exp_next_server='2.2.2.2',
                exp_server_hostname='bbb.example.com',
                exp_boot_file_name='/boot/bbb')

    # reset params in global scope
    # and check received lease if it takes default params ie. empty
    cfg.set_global_parameter(backend=backend, next_server='0.0.0.0',
                             server_hostname='',
                             boot_file_name='')
    get_address(exp_next_server='0.0.0.0',  # TODO: why 0.0.0.0? why not ''
                exp_server_hostname='',
                exp_boot_file_name='')
