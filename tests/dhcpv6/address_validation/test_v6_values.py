"""DHCPv6 values"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import references
import srv_control


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.values
@pytest.mark.disabled
def test_v6_values_address1():
    # that test will probably fail in step 'server is configured in case servers like ISC-DHCPv6, OS wont assign multicast address

    misc.test_setup()
    srv_control.config_srv_subnet('ff02::/64', 'ff02::1-ff02::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv_during_process('DHCP', 'configuration')

    references.references_check('RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.values
@pytest.mark.disabled
def test_v6_values_address2():

    misc.test_setup()
    srv_control.config_srv_subnet('::/64', '::1-::1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv_during_process('DHCP', 'configuration')

    references.references_check('RFC3315')
