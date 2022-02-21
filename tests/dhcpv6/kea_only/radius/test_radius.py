import pytest

from cb_model import setup_server_with_radius
from softwaresupport import radius


@pytest.mark.v6
@pytest.mark.radius
@pytest.mark.parametrize('config_type', ['subnet', 'network', 'subnet-level-class', 'two-networks'])
@pytest.mark.parametrize('lease_position', ['lease-in-pool', 'lease-out-of-pool'])
def test_radius(dhcp_version: str, config_type: str, lease_position: str):
    '''
    Check various RADIUS scenarios.

    :param dhcp_version: the DHCP version used in testing
    :param config_type: different configuration types used in testing
    :param lease_position: position of test lease relative to pool e.g. in pool orout of pool
    '''

    # Provide RADIUS configuration and start RADIUS server.
    radius.init_and_start_radius()

    # Configure Kea.
    addresses, subnets, configs = radius.get_test_case_variables(dhcp_version)
    setup_server_with_radius(**configs[config_type])

    # Check the leases.
    radius.check_leases(config_type, lease_position, addresses, subnets)
