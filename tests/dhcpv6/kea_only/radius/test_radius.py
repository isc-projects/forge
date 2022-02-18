import pytest

from cb_model import setup_server_with_radius
from forge_cfg import world
from softwaresupport import radius


@pytest.mark.v6
@pytest.mark.radius
@pytest.mark.parametrize('mode', ['lease-in-pool', 'lease-out-of-pool'])
@pytest.mark.parametrize('scope', ['subnet', 'network', 'subnet-level-class', 'two-networks'])
def test_radius(dhcp_version: str, mode: str, scope: str):
    '''
    Check various RADIUS scenarios.
    dhcp_version: 'v4' or 'v6'
    mode: position of lease relative to pool
    scope: different configurations
    '''

    # Provide RADIUS configuration and start RADIUS server.
    radius.init_and_start_radius()

    # Configure Kea.
    if dhcp_version == 'v4':
        addresses = {
          '50-5': '192.168.50.5',
          '50-6': '192.168.50.6',
          '50-7': '192.168.50.7',
          '52-52': '192.168.52.52',
          '60-5': '192.168.60.5',
          '60-6': '192.168.60.6',
          '70-5': '192.168.70.5',
        }
        subnets = {
          '50': '192.168.50.0/24',
          '60': '192.168.60.0/24',
          '70': '192.168.70.0/24',
        }
    elif dhcp_version == 'v6':
        addresses = {
          '50-5': '2001:db8:50::5',
          '50-6': '2001:db8:50::6',
          '50-7': '2001:db8:50::7',
          '52-52': '2001:db8:52::52',
          '60-5': '2001:db8:60::5',
          '60-6': '2001:db8:60::6',
          '70-5': '2001:db8:70::5',
        }
        subnets = {
          '50': '2001:db8:50::/64',
          '60': '2001:db8:60::/64',
          '70': '2001:db8:70::/64',
        }
    v = world.proto[1]
    if scope == 'subnet':
        config = {
          f'subnet{v}': [
            {
              'interface': '$(SERVER_IFACE)',
              'pools': [
                {
                  'client-class': 'gold',
                  'pool': f"{addresses['50-5']} - {addresses['50-5']}"
                }
              ],
              'subnet': subnets['50']
            }
          ]
        }
    elif scope == 'network':
        config = {
          'reservation-mode': 'global',
          'shared-networks': [
            {
              'name': 'net-1',
              f'subnet{v}': [
                {
                  'interface': '$(SERVER_IFACE)',
                  'pools': [
                    {
                      'client-class': 'gold',
                      'pool': f"{addresses['50-5']} - {addresses['50-5']}"
                    }
                  ],
                  'subnet': subnets['50']
                }
              ]
            }
          ]
        }
    elif scope == 'subnet-level-class':
        config = {
          'reservation_mode': 'global',
          'shared_networks': [
            {
              'name': 'net-1',
              f'subnet{v}': [
                {
                  'subnet': subnets['50'],
                  'interface': '$(SERVER_IFACE)',
                  'pools': [
                    {
                      'pool': f"{addresses['50-5']} - {addresses['50-5']}",
                      'client-class': 'gold'
                    }, {
                      'pool': f"{addresses['50-6']} - {addresses['50-6']}",
                      'client-class': 'silver'
                    }, {
                      'pool': f"{addresses['50-7']} - {addresses['50-7']}",
                      'client-class': 'bronze'
                    }
                  ]
                },
                {
                  'subnet': subnets['70'],
                  'client-class': 'platinum',
                  'interface': '$(SERVER_IFACE)',
                  'pools': [
                    {
                      'pool': f"{addresses['70-5']} - {addresses['70-5']}"
                    }
                  ]
                }
              ]
            }
          ]
        }
    elif scope == 'two-networks':
        config = {
          'reservation_mode': 'global',
          'shared_networks': [
            {
              'name': 'net-1',
              f'subnet{v}': [
                {
                  'subnet': subnets['50'],
                  'interface': '$(SERVER_IFACE)',
                  'pools': [
                    {
                      'pool': f"{addresses['50-5']} - {addresses['50-5']}",
                      'client-class': 'gold'
                    }, {
                      'pool': f"{addresses['50-6']} - {addresses['50-6']}",
                      'client-class': 'silver'
                    }, {
                      'pool': f"{addresses['50-7']} - {addresses['50-7']}",
                      'client-class': 'bronze'
                    }
                  ]
                },
                {
                  'subnet': subnets['60'],
                  'interface': '$(SERVER_IFACE)',
                  'pools': [
                    {
                      'pool': f"{addresses['60-5']} - {addresses['60-5']}",
                      'client-class': 'gold'
                    }, {
                      'pool': f"{addresses['60-6']} - {addresses['60-6']}",
                      'client-class': 'silver'
                    }
                  ]
                }
              ]
            }
          ]
        }
    setup_server_with_radius(**config)

    # Check the leases.
    if scope == 'subnet-level-class':
        # Platinum client gets platinum lease.
        radius.get_address(mac='08:00:27:b0:c8:01',
                           expected_lease=addresses['70-5'])

    elif scope == 'two-networks':
        gold_ips = set([addresses['50-5'], addresses['60-5']])
        silver_ips = set([addresses['50-6'], addresses['60-6']])

        # Get the lease that is configured explicitly in RADIUS with
        # Framed-IP-Address.
        radius.get_address(mac='08:00:27:b0:c1:42',
                           expected_lease=addresses['52-52'])

        # ### Take all addresses from gold pools. ###
        # Get the first gold lease.
        yiaddr = radius.get_address(mac='08:00:27:b0:c5:01')
        assert yiaddr in gold_ips
        gold_ips.remove(yiaddr)

        # Get the second and last gold lease.
        yiaddr = radius.get_address(mac='08:00:27:b0:c5:02')
        assert yiaddr in gold_ips
        gold_ips.remove(yiaddr)

        # No more leases.
        radius.send_message_and_expect_no_more_leases(mac='08:00:27:b0:c5:03')

        # ### Take all addresses from silver pools. ###
        # Get the first silver lease.
        yiaddr = radius.get_address(mac='08:00:27:b0:c6:01')
        assert yiaddr in silver_ips
        silver_ips.remove(yiaddr)

        # Get the second and last silver lease.
        yiaddr = radius.get_address(mac='08:00:27:b0:c6:02')
        assert yiaddr in silver_ips
        silver_ips.remove(yiaddr)

        # No more leases.
        radius.send_message_and_expect_no_more_leases(mac='08:00:27:b0:c6:03')

        # ### Take all addresses from bronze pools. ###
        # Get the first and only bronze lease.
        radius.get_address(mac='08:00:27:b0:c7:01',
                           expected_lease=addresses['50-7'])

        # No more leases.
        radius.send_message_and_expect_no_more_leases(mac='08:00:27:b0:c7:02')

    elif mode == 'lease-in-pool':
        # Get a lease that is explicitly configured in RADIUS as
        # Framed-IP-Address that is part of a configured pool in Kea.
        radius.get_address(mac='08:00:27:b0:c5:10',
                           expected_lease=addresses['50-5'])

        # A client with a gold Framed-Pool should get no lease because the
        # pool is full.
        radius.send_message_and_expect_no_more_leases(mac='08:00:27:b0:c5:01')

    elif mode == 'lease-out-of-pool':
        # Get a lease that is explicitly configured in RADIUS as
        # Framed-IP-Address that is outside of any configured pool in Kea.
        radius.get_address(mac='08:00:27:b0:c1:42',
                           expected_lease=addresses['52-52'])

        # A client with a gold Framed-Pool should get the lease because the
        # pool has a free lease.
        radius.get_address(mac='08:00:27:b0:c5:01',
                           expected_lease=addresses['50-5'])
