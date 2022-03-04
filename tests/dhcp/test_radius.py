import pytest

from cb_model import setup_server_with_radius
from forge_cfg import world
from softwaresupport import radius


# pylint: disable=unused-argument
@pytest.mark.v4
@pytest.mark.v4_bootp
@pytest.mark.v6
@pytest.mark.radius
@pytest.mark.parametrize('config_type', ['subnet', 'network', 'multiple-subnets'])
@pytest.mark.parametrize('has_reservation', ['client-has-reservation-in-radius', 'client-has-no-reservation-in-radius'])
def test_radius(dhcp_version: str, config_type: str, has_reservation: str):
    '''
    Check RADIUS functionality on various Kea configurations.
    See radius.check_leases() for explanations on what the parametrizations mean.

    :param dhcp_version: the DHCP version used in testing
    :param config_type: different configurations used in testing
    :param has_reservation: whether the first client coming in with a request has its lease or pool reserved in RADIUS
    '''

    # Provide RADIUS configuration and start RADIUS server.
    radius.init_and_start_radius()

    # Configure Kea.
    addresses, subnets, configs = radius.get_test_case_variables()
    setup_server_with_radius(**configs[config_type])

    # Check the leases.
    radius.check_leases(config_type, has_reservation, addresses, subnets)
