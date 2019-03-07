"""Kea config backend testing: fixed fields set based on next-server, server-hostname and boot-file-name settings."""

import pytest

from .cb_cmds import setup_server_for_config_backend_cmds
from .cb_cmds import get_address, set_subnet, set_network


pytestmark = [pytest.mark.kea_only,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.config_backend]


@pytest.mark.v4
@pytest.mark.parametrize("initial_next_server,initial_server_hostname,initial_boot_file_name",
                         [(None, None, None),                              # pick defaults
                          ('1.1.1.1', 'aaa.example.com', '/boot/aaa')])    # some specific initial values
def test_subnet(initial_next_server, initial_server_hostname, initial_boot_file_name):
    setup_server_for_config_backend_cmds(next_server=initial_next_server,
                                         server_hostname=initial_server_hostname,
                                         boot_file_name=initial_boot_file_name)

    # TODO: it does not work yet
    # set_subnet()
    # get_address(exp_next_server=initial_next_server if initial_next_server else '0.0.0.0',
    #             exp_server_hostname=initial_server_hostname if initial_server_hostname else '',
    #             exp_boot_file_name=initial_boot_file_name if initial_boot_file_name else '')

    # set_global_parameter(next_server='2.2.2.2',
    #                      server_hostname='bbb.example.com',
    #                      boot_file_name='/boot/bbb')
    # get_address(exp_next_server='2.2.2.2',
    #             exp_server_hostname='bbb.example.com',
    #             exp_boot_file_name='/boot/bbb')

    # del_subnet()
    set_subnet(next_server='3.3.3.3',
               server_hostname='ccc.example.com',
               boot_file_name='/boot/ccc')
    get_address(exp_next_server='3.3.3.3',
                exp_server_hostname='ccc.example.com',
                exp_boot_file_name='/boot/ccc')

    set_subnet(next_server='4.4.4.4',
               server_hostname='ddd.example.com',
               boot_file_name='/boot/ddd')
    get_address(exp_next_server='4.4.4.4',
                exp_server_hostname='ddd.example.com',
                exp_boot_file_name='/boot/ddd')


@pytest.mark.v4
@pytest.mark.parametrize("initial_next_server,initial_server_hostname,initial_boot_file_name",
                         [(None, None, None),                              # pick defaults
                          ('1.1.1.1', 'aaa.example.com', '/boot/aaa')])    # some specific initial values
def test_network(initial_next_server, initial_server_hostname, initial_boot_file_name):
    setup_server_for_config_backend_cmds(next_server=initial_next_server,
                                         server_hostname=initial_server_hostname,
                                         boot_file_name=initial_boot_file_name)

    # TODO: it does not work yet
    # set_subnet()
    # get_address(exp_next_server=initial_next_server if initial_next_server else '0.0.0.0',
    #             exp_server_hostname=initial_server_hostname if initial_server_hostname else '',
    #             exp_boot_file_name=initial_boot_file_name if initial_boot_file_name else '')

    # set_global_parameter(next_server='2.2.2.2',
    #                      server_hostname='bbb.example.com',
    #                      boot_file_name='/boot/bbb')
    # get_address(exp_next_server='2.2.2.2',
    #             exp_server_hostname='bbb.example.com',
    #             exp_boot_file_name='/boot/bbb')

    set_network(network_next_server='3.3.3.3',
                network_server_hostname='ccc.example.com',
                network_boot_file_name='/boot/ccc')
    get_address(exp_next_server='3.3.3.3',
                exp_server_hostname='ccc.example.com',
                exp_boot_file_name='/boot/ccc')

    # TODO: add more cases but it does not work yet
