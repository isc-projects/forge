Feature: Logging in Kea
    Tests for different loggers in Kea server.

@v6 @kea_only @logging
    Scenario: v6.loggers.options-debug
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server logging system is configured with logger type kea-dhcp6.options, severity DEBUG, severity level 99 and log file kea.log.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.


	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp6.options


@v6 @kea_only @logging
    Scenario: v6.loggers.options-info
	Test Setup:
    #TODO negative testing
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server logging system is configured with logger type kea-dhcp6.options, severity INFO, severity level None and log file kea.log.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp6.options


@v6 @kea_only @logging
    Scenario: v6.loggers.bad-packets-debug
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server logging system is configured with logger type kea-dhcp6.bad-packets, severity DEBUG, severity level 99 and log file kea.log.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	#message wont contain client-id option
    Client does include IA-NA.
    Client sends SOLICIT message.

	Server MUST NOT respond.
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp6.bad-packets

@v6 @kea_only @logging
    Scenario: v6.loggers.bad-packets-info
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server logging system is configured with logger type kea-dhcp6.bad-packets, severity INFO, severity level None and log file kea.log.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	#message wont contain client-id option
    Client does include IA-NA.
    Client sends SOLICIT message.

	Server MUST NOT respond.
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp6.bad-packets

@v6 @kea_only @logging
    Scenario: v6.loggers.dhcp6
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server logging system is configured with logger type kea-dhcp6.dhcp6, severity DEBUG, severity level 99 and log file kea.log.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client requests option 7.
	Client does include client-id.
    Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp6.dhcp6

@v6 @kea_only @logging
    Scenario: v6.loggers.dhcp6-info
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server logging system is configured with logger type kea-dhcp6.dhcp6, severity INFO, severity level None and log file kea.log.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.

	Test Procedure:
	Client requests option 7.
	Client does include client-id.
    Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp6.dhcp6
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: INFO  \[kea-dhcp6.dhcp6


@v6 @kea_only @logging
    Scenario: v6.loggers.alloc-engine
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server logging system is configured with logger type kea-dhcp6.alloc-engine, severity DEBUG, severity level 99 and log file kea.log.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp6.alloc-engine

@v6 @kea_only @logging
    Scenario: v6.loggers.dhcpsrv-debug
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server logging system is configured with logger type kea-dhcp6.dhcpsrv, severity DEBUG, severity level 99 and log file kea.log.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp6.dhcpsrv

@v6 @kea_only @logging
    Scenario: v6.loggers.dhcpsrv-info
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server logging system is configured with logger type kea-dhcp6.dhcpsrv, severity INFO, severity level None and log file kea.log.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp6.dhcpsrv
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: INFO  \[kea-dhcp6.dhcpsrv


@v6 @kea_only @logging
    Scenario: v6.loggers.leases-debug
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server logging system is configured with logger type kea-dhcp6.leases, severity DEBUG, severity level 99 and log file kea.log.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp6.leases

@v6 @kea_only @logging
    Scenario: v6.loggers.leases-info
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server logging system is configured with logger type kea-dhcp6.leases, severity INFO, severity level None and log file kea.log.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp6.leases

@v6 @kea_only @logging
    Scenario: v6.loggers.packets-debug
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server logging system is configured with logger type kea-dhcp6.packets, severity DEBUG, severity level 99 and log file kea.log.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
  	Client does include client-id.
    Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp6.packets

@v6 @kea_only @logging
    Scenario: v6.loggers.packets-info
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server logging system is configured with logger type kea-dhcp6.packets, severity INFO, severity level None and log file kea.log.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp6.packets

@v6 @kea_only @logging
    Scenario: v6.loggers.hosts-debug
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server logging system is configured with logger type kea-dhcp6.hosts, severity DEBUG, severity level 99 and log file kea.log.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp6.hosts

@v6 @kea_only @logging
    Scenario: v6.loggers.hosts-info
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server logging system is configured with logger type kea-dhcp6.hosts, severity INFO, severity level None and log file kea.log.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp6.hosts

@v6 @kea_only @logging
    Scenario: v6.loggers.all
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.


	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp6.packets
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp6.leases
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp6.dhcpsrv
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp6.alloc-engine
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp6.dhcp6
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp6.options


@v6 @kea_only @logging
    Scenario: v6.loggers.all-different-levels-same-file
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server logging system is configured with logger type kea-dhcp6.dhcp6, severity INFO, severity level None and log file kea.log.
    Server logging system is configured with logger type kea-dhcp6.dhcpsrv, severity INFO, severity level None and log file kea.log.
	Server logging system is configured with logger type kea-dhcp6.options, severity DEBUG, severity level 99 and log file kea.log.
    Server logging system is configured with logger type kea-dhcp6.packets, severity DEBUG, severity level 99 and log file kea.log.
    Server logging system is configured with logger type kea-dhcp6.leases, severity WARN, severity level None and log file kea.log.
    Server logging system is configured with logger type kea-dhcp6.alloc-engine, severity DEBUG, severity level 50 and log file kea.log.
	Server logging system is configured with logger type kea-dhcp6.bad-packets, severity DEBUG, severity level 25 and log file kea.log.
	Server logging system is configured with logger type kea-dhcp6.options, severity INFO, severity level None and log file kea.log.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client requests option 7.
	#message wont contain client-id option
    Client does include IA-NA.
    Client sends SOLICIT message.

	Server MUST NOT respond.

	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp6.packets
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp6.leases
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp6.alloc-engine
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp6.dhcp6
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: INFO  \[kea-dhcp6.dhcp6
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp6.dhcpsrv
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: INFO  \[kea-dhcp6.dhcpsrv
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp6.options


@v6 @kea_only @logging
    Scenario: v6.loggers.all-different-levels-different-file
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server logging system is configured with logger type kea-dhcp6.dhcp6, severity INFO, severity level None and log file kea.log1.
    Server logging system is configured with logger type kea-dhcp6.dhcpsrv, severity INFO, severity level None and log file kea.log2.
	Server logging system is configured with logger type kea-dhcp6.options, severity DEBUG, severity level 99 and log file kea.log3.
    Server logging system is configured with logger type kea-dhcp6.packets, severity DEBUG, severity level 99 and log file kea.log4.
    Server logging system is configured with logger type kea-dhcp6.leases, severity WARN, severity level None and log file kea.log5.
    Server logging system is configured with logger type kea-dhcp6.alloc-engine, severity DEBUG, severity level 50 and log file kea.log6.
	Server logging system is configured with logger type kea-dhcp6.bad-packets, severity DEBUG, severity level 25 and log file kea.log7.
	Server logging system is configured with logger type kea-dhcp6.options, severity INFO, severity level None and log file kea.log8.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client does include client-id.
    Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	#message wont contain client-id option
    Client does include IA-NA.
    Client sends SOLICIT message.

	Server MUST NOT respond.

	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log4 MUST contain line or phrase: DEBUG \[kea-dhcp6.packets
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log5 MUST NOT contain line or phrase: DEBUG \[kea-dhcp6.leases
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log6 MUST contain line or phrase: DEBUG \[kea-dhcp6.alloc-engine
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log1 MUST NOT contain line or phrase: DEBUG \[kea-dhcp6.dhcp6
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log1 MUST contain line or phrase: INFO  \[kea-dhcp6.dhcp6
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log2 MUST NOT contain line or phrase: DEBUG \[kea-dhcp6.dhcpsrv
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log2 MUST contain line or phrase: INFO  \[kea-dhcp6.dhcpsrv
	File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log3 MUST NOT contain line or phrase: DEBUG \[kea-dhcp6.options

@v6 @kea_only @logging
    Scenario: ddns6.logging-all-types-debug

    Test Setup:
    Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    DDNS server is configured with qualifying-suffix option set to abc.com.
    Add forward DDNS with name six.example.com. and key EMPTY_KEY on address 2001:db8:1::1000 and port 53.
    Add reverse DDNS with name 1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. and key EMPTY_KEY on address 2001:db8:1::1000 and port 53.
    Server logging system is configured with logger type kea-dhcp-ddns, severity DEBUG, severity level 99 and log file kea.log.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 1.
    Response MUST include option 2.

    Test Procedure:
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client saves into set no. 1 IA_NA option from received message.
    Client saves into set no. 1 server-id option from received message.
    Client adds saved options in set no. 1. And DONT Erase.
    Client sets FQDN_domain_name value to sth6.six.example.com..
    Client sets FQDN_flags value to S.
    Client does include fqdn.
    Client does include client-id.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 1.
    Response MUST include option 2.
    Response MUST include option 39.
    Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    Response option 39 MUST contain fqdn sth6.six.example.com.

    Test Procedure:
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client adds saved options in set no. 1. And DONT Erase.
    Client does include client-id.
    Client sends RELEASE message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 1.
    Response MUST include option 2.

    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: INFO  \[kea-dhcp-ddns.dhcpddns
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp-ddns.dhcpddns
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp-ddns.libdhcp-ddns
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp-ddns.d2-to-dns
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: ERROR \[kea-dhcp-ddns.d2-to-dns
    File stored in $(SOFTWARE_INSTALL_DIR)var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp-ddns.dhcp-to-d2