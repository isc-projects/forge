Feature: Logging in Kea
    Tests for different loggers in Kea server.

@v4 @kea_only @logging
    Scenario: v4.loggers.options-debug

	Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server logging system is configured with logger type kea-dhcp4.options, severity DEBUG, severity level 99 and log file kea.log.
    Server is configured with time-offset option with value 50.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client requests option 1.
    Client requests option 2.
    Client requests option 7.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
	Client adds to the message requested_addr with value 192.168.50.1.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.

    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:11.
    Client adds to the message client_id with value 00010203040111.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp4.options

@v4 @kea_only @logging
    Scenario: v4.loggers.options-info

	Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server logging system is configured with logger type kea-dhcp4.options, severity INFO, severity level None and log file kea.log.
    Server is configured with time-offset option with value 50.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client requests option 1.
    Client requests option 2.
    Client requests option 7.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
	Client adds to the message requested_addr with value 192.168.50.1.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.

    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:11.
    Client adds to the message client_id with value 00010203040111.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp4.options

@v4 @kea_only @logging
    Scenario: v4.loggers.bad-packets-debug
	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server logging system is configured with logger type kea-dhcp4.bad-packets, severity DEBUG, severity level 99 and log file kea.log.
	Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client requests option 1.
    Client requests option 2.
    Client requests option 7.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
	Client adds to the message requested_addr with value 192.168.50.100.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with NAK message.
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp4.bad-packets

@v4 @kea_only @logging
    Scenario: v4.loggers.bad-packets-info
	Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
	Server logging system is configured with logger type kea-dhcp4.bad-packets, severity INFO, severity level None and log file kea.log.
	Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client requests option 1.
    Client requests option 2.
    Client requests option 7.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
	Client adds to the message requested_addr with value 192.168.50.100.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with NAK message.
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp4.bad-packets

@v4 @kea_only @logging
    Scenario: v4.loggers.dhcp4
    Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server logging system is configured with logger type kea-dhcp4.dhcp4, severity DEBUG, severity level 99 and log file kea.log.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client requests option 1.
    Client requests option 2.
    Client requests option 7.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
	Client adds to the message requested_addr with value 192.168.50.1.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.

    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:11.
    Client adds to the message client_id with value 00010203040111.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp4.dhcp4
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: INFO  \[kea-dhcp4.dhcp4

@v4 @kea_only @logging
    Scenario: v4.loggers.dhcp4-info
    Test Setup:
	Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server logging system is configured with logger type kea-dhcp4.dhcp4, severity INFO, severity level None and log file kea.log.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client requests option 1.
    Client requests option 2.
    Client requests option 7.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
	Client adds to the message requested_addr with value 192.168.50.1.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.

    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:11.
    Client adds to the message client_id with value 00010203040111.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp4.dhcp4
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: INFO  \[kea-dhcp4.dhcp4


@v4 @kea_only @logging
    Scenario: v4.loggers.alloc-engine
    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server logging system is configured with logger type kea-dhcp4.alloc-engine, severity DEBUG, severity level 99 and log file kea.log.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client requests option 1.
    Client requests option 2.
    Client requests option 7.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client requests option 1.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.

    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:11.
    Client adds to the message client_id with value 00010203040111.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp4.alloc-engine


@v4 @kea_only @logging
    Scenario: v4.loggers.dhcpsrv-debug
    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server logging system is configured with logger type kea-dhcp4.dhcpsrv, severity DEBUG, severity level 99 and log file kea.log.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client requests option 1.
    Client requests option 2.
    Client requests option 7.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client requests option 1.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.

    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:11.
    Client adds to the message client_id with value 00010203040111.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.

    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp4.dhcpsrv
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: INFO  \[kea-dhcp4.dhcpsrv

@v4 @kea_only @logging
    Scenario: v4.loggers.dhcpsrv-info
    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server logging system is configured with logger type kea-dhcp4.dhcpsrv, severity INFO, severity level None and log file kea.log.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client requests option 1.
    Client requests option 2.
    Client requests option 7.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client requests option 1.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.

    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:11.
    Client adds to the message client_id with value 00010203040111.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.

    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp4.dhcpsrv
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: INFO  \[kea-dhcp4.dhcpsrv


@v4 @kea_only @logging
    Scenario: v4.loggers.leases-debug
	Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server logging system is configured with logger type kea-dhcp4.leases, severity DEBUG, severity level 99 and log file kea.log.
	Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client requests option 1.
    Client requests option 2.
    Client requests option 7.
    Client sets chaddr value to 00:00:00:00:00:22.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:22.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client requests option 1.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:21.
    Client copies server_id option from received message.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.

    Pass Criteria:
    Server MUST NOT respond.

	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: INFO  \[kea-dhcp4.leases
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp4.leases

@v4 @kea_only @logging
    Scenario: v4.loggers.leases-info
	Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server logging system is configured with logger type kea-dhcp4.leases, severity INFO, severity level None and log file kea.log.
	Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client requests option 1.
    Client requests option 2.
    Client requests option 7.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client requests option 1.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.

    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:11.
    Client adds to the message client_id with value 00010203040111.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp4.leases

@v4 @kea_only @logging
Scenario: v4.loggers.packets-debug
    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server logging system is configured with logger type kea-dhcp4.packets, severity DEBUG, severity level 99 and log file kea.log.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client requests option 1.
    Client requests option 2.
    Client requests option 7.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client requests option 1.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.

    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:11.
    Client adds to the message client_id with value 00010203040111.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp4.packets

@v4 @kea_only @logging
Scenario: v4.loggers.packets-info
    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server logging system is configured with logger type kea-dhcp4.packets, severity INFO, severity level None and log file kea.log.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client requests option 1.
    Client requests option 2.
    Client requests option 7.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client requests option 1.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.

    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:11.
    Client adds to the message client_id with value 00010203040111.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp4.packets

@v4 @kea_only @logging
Scenario: v4.loggers.hosts-debug
    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server logging system is configured with logger type kea-dhcp4.hosts, severity DEBUG, severity level 99 and log file kea.log.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client requests option 1.
    Client requests option 2.
    Client requests option 7.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client requests option 1.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.

    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:11.
    Client adds to the message client_id with value 00010203040111.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp4.hosts

@v4 @kea_only @logging
Scenario: v4.loggers.hosts-info
    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server logging system is configured with logger type kea-dhcp4.hosts, severity INFO, severity level None and log file kea.log.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client requests option 1.
    Client requests option 2.
    Client requests option 7.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client requests option 1.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.

    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:11.
    Client adds to the message client_id with value 00010203040111.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp4.hosts

@v4 @kea_only @logging
Scenario: v4.loggers.all
    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server logging system is configured with logger type kea-dhcp4, severity DEBUG, severity level 99 and log file kea.log.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client requests option 1.
    Client requests option 2.
    Client requests option 7.
    Client sets chaddr value to 00:00:00:00:00:33.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:33.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client requests option 1.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:31.
    Client saves into set no. 1 server_id option from received message.
    Client adds saved options in set no. 1. And DONT Erase.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.

    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:33.
    Client adds saved options in set no. 1. And DONT Erase.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.

    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client requests option 1.
    Client requests option 2.
    Client requests option 7.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client requests option 1.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.

    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:11.
    Client adds to the message client_id with value 00010203040111.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.

    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp4.packets
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp4.dhcpsrv
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp4.alloc-engine
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp4.dhcp4
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp4.options
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp4.leases
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: INFO  \[kea-dhcp4.leases

@v4 @kea_only @logging
    Scenario: v4.loggers.all-different-levels-same-file
    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server logging system is configured with logger type kea-dhcp4.dhcp4, severity INFO, severity level None and log file kea.log.
    Server logging system is configured with logger type kea-dhcp4.dhcpsrv, severity INFO, severity level None and log file kea.log.
    Server logging system is configured with logger type kea-dhcp4.options, severity DEBUG, severity level 99 and log file kea.log.
    Server logging system is configured with logger type kea-dhcp4.packets, severity DEBUG, severity level 99 and log file kea.log.
    Server logging system is configured with logger type kea-dhcp4.leases, severity WARN, severity level None and log file kea.log.
    Server logging system is configured with logger type kea-dhcp4.alloc-engine, severity DEBUG, severity level 50 and log file kea.log.
    Server logging system is configured with logger type kea-dhcp4.bad-packets, severity DEBUG, severity level 25 and log file kea.log.
    Server logging system is configured with logger type kea-dhcp4.options, severity INFO, severity level None and log file kea.log.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client requests option 1.
    Client requests option 2.
    Client requests option 7.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client requests option 1.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.

    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:11.
    Client adds to the message client_id with value 00010203040111.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.

    Test Procedure:
    Client requests option 1.
    Client requests option 2.
    Client requests option 7.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
	Client adds to the message requested_addr with value 192.168.50.100.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with NAK message.

    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp4.packets
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp4.leases
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp4.alloc-engine
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp4.dhcp4
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: INFO  \[kea-dhcp4.dhcp4
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp4.dhcpsrv
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: INFO  \[kea-dhcp4.dhcpsrv
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp4.options


@v4 @kea_only @logging
    Scenario: v4.loggers.all-different-levels-different-file
    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server logging system is configured with logger type kea-dhcp4.dhcp4, severity INFO, severity level None and log file kea.log1.
    Server logging system is configured with logger type kea-dhcp4.dhcpsrv, severity INFO, severity level None and log file kea.log2.
    Server logging system is configured with logger type kea-dhcp4.options, severity DEBUG, severity level 99 and log file kea.log3.
    Server logging system is configured with logger type kea-dhcp4.packets, severity DEBUG, severity level 99 and log file kea.log4.
    Server logging system is configured with logger type kea-dhcp4.leases, severity WARN, severity level None and log file kea.log5.
    Server logging system is configured with logger type kea-dhcp4.alloc-engine, severity DEBUG, severity level 50 and log file kea.log6.
    Server logging system is configured with logger type kea-dhcp4.bad-packets, severity DEBUG, severity level 25 and log file kea.log6.
    Server logging system is configured with logger type kea-dhcp4.options, severity INFO, severity level None and log file kea.log6.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client requests option 1.
    Client requests option 2.
    Client requests option 7.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.1.
    Client requests option 1.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client sets ciaddr value to 192.168.50.1.
    Client sends RELEASE message.

    Pass Criteria:
    Server MUST NOT respond.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:11.
    Client adds to the message client_id with value 00010203040111.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.

    Test Procedure:
    Client requests option 1.
    Client requests option 2.
    Client requests option 7.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
	Client adds to the message requested_addr with value 192.168.50.100.
	Client requests option 1.
	Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with NAK message.

    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log4 MUST contain line or phrase: DEBUG \[kea-dhcp4.packets
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log5 MUST NOT contain line or phrase: DEBUG \[kea-dhcp4.leases
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log6 MUST contain line or phrase: DEBUG \[kea-dhcp4.alloc-engine
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log1 MUST NOT contain line or phrase: DEBUG \[kea-dhcp4.dhcp4
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log1 MUST contain line or phrase: INFO  \[kea-dhcp4.dhcp4
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log2 MUST NOT contain line or phrase: DEBUG \[kea-dhcp4.dhcpsrv
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log2 MUST contain line or phrase: INFO  \[kea-dhcp4.dhcpsrv
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log3 MUST NOT contain line or phrase: DEBUG \[kea-dhcp4.options

@v4 @kea_only @logging
    Scenario: ddns4.logging-all-types-debug

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    DDNS server is configured with qualifying-suffix option set to abc.com.
    Add forward DDNS with name four.example.com. and key forge.sha1.key on address 192.168.50.252 and port 53.
    Add reverse DDNS with name 50.168.192.in-addr.arpa. and key forge.sha1.key on address 192.168.50.252 and port 53.
    Add DDNS key named forge.sha1.key based on HMAC-SHA1 with secret value PN4xKZ/jDobCMlo4rpr70w==.
    Server logging system is configured with logger type kea-dhcp-ddns, severity DEBUG, severity level 99 and log file kea.log.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.10.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client saves into set no. 1 server_id option from received message.
    Client adds saved options in set no. 1. And DONT Erase.
    Client adds to the message requested_addr with value 192.168.50.10.
    Client requests option 1.
    Client sets FQDN_domain_name value to aa.four.example.com..
    Client sets FQDN_flags value to S.
    Client does include fqdn.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.10.
    Response MUST include option 1.
    Response option 1 MUST contain value 255.255.255.0.
    Response MUST include option 81.
    Response option 81 MUST contain flags 1. #later make it 's' 'n' and 'o'
    Response option 81 MUST contain fqdn aa.four.example.com..


    Test Procedure:
    Client adds saved options in set no. 1. And DONT Erase.
    Client sets ciaddr value to 192.168.50.10.
    Client sends RELEASE message.

    Pass Criteria:
    Server MUST NOT respond.
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: INFO  \[kea-dhcp-ddns.dhcpddns
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp-ddns.dhcpddns
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp-ddns.libdhcp-ddns
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp-ddns.d2-to-dns
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: ERROR \[kea-dhcp-ddns.d2-to-dns
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp-ddns.dhcp-to-d2