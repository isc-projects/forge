Feature: RFC7550
    Feature designed for IETF 93 Hackathon!

@v6
Scenario: 7550_1

	Test Setup:
    Time preferred-lifetime is configured with value 300.
    Time valid-lifetime is configured with value 400.
    Time renew-timer is configured with value 100.
    Time rebind-timer is configured with value 200.

	#subnet declarations:
	Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::100-2001:db8:1::200 pool.
	Server is configured with 3001:: prefix in subnet 0 with 64 prefix length and 96 delegated prefix length.
    Server is configured with another subnet on interface <interface> with 2001:db8:2::/64 subnet and 2001:db8:2::100-2001:db8:2::200 pool.
	Server is configured with 3002:: prefix in subnet 1 with 64 prefix length and 96 delegated prefix length.

    #logger declarations (one is commented as and example)
	Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
	#Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.

    #enable 7550 support
	Add to config file line: "new-leases-on-renew": False

    #start server:
	DHCP server is started.

	Test Procedure:
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	#Pause the Test.


