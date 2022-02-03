"""ISC_DHCP DHCPv6 two server setup test"""
# This is example file to how write test that are using two virtual systems.
# Both of those systems have to have installed isc-dhcp and bind (for ddns tests)
# If forge + vagrant is used isc-dhcp and bind are installed:
# ./forge config kea-dirs /home/ubuntu/
# ./forge config ccache-dir /tmp
# ./forge --lxc --sid all -s ubuntu-20.04 setup --dhcpd
# ./forge --lxc --sid all -s ubuntu-20.04 install-dhcpd <path-to-sources>
# Both systems are accessible by world.f_cfg.mgmt_address and world.f_cfg.mgmt_address_2 inside test
# To access systems directly:
# list all created systems: vagrant global-status
# vagrant ssh <system-id> -c "bash"

# pylint: disable=invalid-name,line-too-long

import pytest
import misc
import srv_control
import srv_msg

# if used those 3 functions has to be imported directly
# from softwaresupport.isc_dhcp6_server.functions_ddns import add_forward_ddns, add_reverse_ddns
# from softwaresupport.isc_dhcp6_server.functions import add_line_in_global

from forge_cfg import world


@pytest.fixture(autouse=True)
def kill_kea_on_second_system():
    # kill kea and clear data at the beginning and at the end
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
    yield
    srv_control.clear_some_data('all', dest=world.f_cfg.mgmt_address_2)
    srv_control.clear_some_data('all', service='dns', dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
    # TODO figure out why we don't download all at the end, in kea HA we do


def _get_address(duid, address):
    """
    Get assigned address from DHCP server using full SARR exchange
    :param duid: string with DUID used by client
    :param address: string with expected address in IA-NA option
    """
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'ia_id', 666)
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'ia_id', 666)
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', address)


@pytest.mark.v6
@pytest.mark.dhcpd
def test_dhcpd_two_servers():
    """
    This is example test, how to use forge + vagrant setup to execute tests using both virtual systems
    """
    # start first server
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # get an address
    _get_address('00:03:00:01:f6:f5:f4:f3:f2:01', "2001:db8:1::50")

    # stop server
    srv_control.start_srv('DHCP', 'stopped')

    # start second server, setp misc.test_setup() is mandatory!
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::150-2001:db8:1::150')
    srv_control.build_and_send_config_files(dest=world.f_cfg.mgmt_address_2)
    srv_control.start_srv('DHCP', 'started', dest=world.f_cfg.mgmt_address_2)

    # get an address
    _get_address('00:03:00:01:f6:f5:f4:f3:f2:01', "2001:db8:1::150")
    srv_control.start_srv('DHCP', 'stopped', dest=world.f_cfg.mgmt_address_2)
