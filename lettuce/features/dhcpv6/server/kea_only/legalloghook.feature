Feature: Kea6 Legal logging hook
Testing hook that is creating additional file with detailed logs about clients

@v6 @dhcp6 @kea_only @legal_logging
Scenario: v6.loggers.legal-log-hook-address-assigned-duid

Test Procedure:
Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.

Test Setup:
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
Time preferred-lifetime is configured with value 400.
Time valid-lifetime is configured with value 600.
Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so.
Send server configuration using SSH and config-file.
DHCP server is started.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
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
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client does include client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

@v6 @dhcp6 @kea_only @legal_logging
Scenario: v6.loggers.legal-log-hook-address-assigned-duid-mysql

Remove all records from table logs in MySQL database.

Test Setup:
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
Time preferred-lifetime is configured with value 400.
Time valid-lifetime is configured with value 600.
Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so.
To hook no. 1 add parameter named name with value: $(DB_NAME)
To hook no. 1 add parameter named password with value: $(DB_PASSWD)
To hook no. 1 add parameter named type with value: mysql
To hook no. 1 add parameter named user with value: $(DB_USER)
Send server configuration using SSH and config-file.
DHCP server is started.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
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
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client does include client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Table logs in MySQL database MUST contain line or phrase: Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)

@v6 @dhcp6 @kea_only @legal_logging
Scenario: v6.loggers.legal-log-hook-address-assigned-duid-pgsql

Remove all records from table logs in PostgreSQL database.

Test Setup:
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
Time preferred-lifetime is configured with value 400.
Time valid-lifetime is configured with value 600.
Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so.
To hook no. 1 add parameter named name with value: $(DB_NAME)
To hook no. 1 add parameter named password with value: $(DB_PASSWD)
To hook no. 1 add parameter named type with value: postgresql
To hook no. 1 add parameter named user with value: $(DB_USER)
Send server configuration using SSH and config-file.
DHCP server is started.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
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
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client does include client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Table logs in PostgreSQL database MUST contain line or phrase: Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)

@v6 @dhcp6 @kea_only @legal_logging
Scenario: v6.loggers.legal-log-hook-address-renewed-duid

Test Procedure:
Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.

Test Setup:
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
Time preferred-lifetime is configured with value 400.
Time valid-lifetime is configured with value 600.
Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so.
Send server configuration using SSH and config-file.
DHCP server is started.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
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
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client does include client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client does include client-id.
Client sends RENEW message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.
File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)
File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: Address:3000::5 has been renewed for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)


@v6 @dhcp6 @kea_only @legal_logging
Scenario: v6.loggers.legal-log-hook-address-renewed-duid-mysql

Test Procedure:
Remove all records from table logs in MySQL database.

Test Setup:
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
Time preferred-lifetime is configured with value 400.
Time valid-lifetime is configured with value 600.
Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so.
To hook no. 1 add parameter named name with value: $(DB_NAME)
To hook no. 1 add parameter named password with value: $(DB_PASSWD)
To hook no. 1 add parameter named type with value: mysql
To hook no. 1 add parameter named user with value: $(DB_USER)
Send server configuration using SSH and config-file.
DHCP server is started.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
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
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client does include client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client does include client-id.
Client sends RENEW message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Table logs in MySQL database MUST contain line or phrase: Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)
Table logs in MySQL database MUST contain line or phrase: Address:3000::5 has been renewed for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)

@v6 @dhcp6 @kea_only @legal_logging
Scenario: v6.loggers.legal-log-hook-address-renewed-duid-pgsql

Test Procedure:
Remove all records from table logs in PostgreSQL database.

Test Setup:
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
Time preferred-lifetime is configured with value 400.
Time valid-lifetime is configured with value 600.
Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so.
To hook no. 1 add parameter named name with value: $(DB_NAME)
To hook no. 1 add parameter named password with value: $(DB_PASSWD)
To hook no. 1 add parameter named type with value: postgresql
To hook no. 1 add parameter named user with value: $(DB_USER)
Send server configuration using SSH and config-file.
DHCP server is started.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
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
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client does include client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client does include client-id.
Client sends RENEW message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Table logs in PostgreSQL database MUST contain line or phrase: Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)
Table logs in PostgreSQL database MUST contain line or phrase: Address:3000::5 has been renewed for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)


@v6 @dhcp6 @kea_only @legal_logging
Scenario: v6.loggers.legal-log-hook-address-rebind-duid

Test Procedure:
Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.

Test Setup:
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
Time preferred-lifetime is configured with value 400.
Time valid-lifetime is configured with value 600.
Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so.
Send server configuration using SSH and config-file.
DHCP server is started.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
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
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client does include client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
Client copies IA_NA option from received message.
Client does include client-id.
Client sends REBIND message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.
File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)
# Spec says that when we are rebinding address it will be logged 'renewed', misleading :/
File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: Address:3000::5 has been renewed for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)

@v6 @dhcp6 @kea_only @legal_logging
Scenario: v6.loggers.legal-log-hook-address-rebind-duid-pgsql

Test Procedure:
Remove all records from table logs in PostgreSQL database.

Test Setup:
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
Time preferred-lifetime is configured with value 400.
Time valid-lifetime is configured with value 600.
Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so.
To hook no. 1 add parameter named name with value: $(DB_NAME)
To hook no. 1 add parameter named password with value: $(DB_PASSWD)
To hook no. 1 add parameter named type with value: postgresql
To hook no. 1 add parameter named user with value: $(DB_USER)
Send server configuration using SSH and config-file.
DHCP server is started.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
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
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client does include client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
Client copies IA_NA option from received message.
Client does include client-id.
Client sends REBIND message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Table logs in PostgreSQL database MUST contain line or phrase: Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)
# Spec says that when we are rebinding address it will be logged 'renewed', misleading :/
Table logs in PostgreSQL database MUST contain line or phrase: Address:3000::5 has been renewed for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)

@v6 @dhcp6 @kea_only @legal_logging
Scenario: v6.loggers.legal-log-hook-address-rebind-duid-mysql

Test Procedure:
Remove all records from table logs in MySQL database.

Test Setup:
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
Time preferred-lifetime is configured with value 400.
Time valid-lifetime is configured with value 600.
Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so.
To hook no. 1 add parameter named name with value: $(DB_NAME)
To hook no. 1 add parameter named password with value: $(DB_PASSWD)
To hook no. 1 add parameter named type with value: mysql
To hook no. 1 add parameter named user with value: $(DB_USER)
Send server configuration using SSH and config-file.
DHCP server is started.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
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
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client does include client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
Client copies IA_NA option from received message.
Client does include client-id.
Client sends REBIND message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Table logs in MySQL database MUST contain line or phrase: Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)
# Spec says that when we are rebinding address it will be logged 'renewed', misleading :/
Table logs in MySQL database MUST contain line or phrase: Address:3000::5 has been renewed for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)

@v6 @dhcp6 @kea_only @legal_logging
Scenario: v6.loggers.legal-log-hook-address-assigned-docsis-modem

Test Procedure:
Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.

Test Setup:
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
Time preferred-lifetime is configured with value 400.
Time valid-lifetime is configured with value 600.
Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so.
Run configuration command: "mac-sources": [ "docsis-modem" ]
Send server configuration using SSH and config-file.
DHCP server is started.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
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
Client sets enterprisenum value to 4491.
Client does include vendor-class.
Client adds suboption for vendor specific information with code: 36 and data: f6:f5:f4:f3:f2:01.
Client does include vendor-specific-info.
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client does include client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.
File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:01 (from DOCSIS MODEM)

@v6 @dhcp6 @kea_only @legal_logging
Scenario: v6.loggers.legal-log-hook-address-assigned-docsis-modem-pgsql

Test Procedure:
Remove all records from table logs in PostgreSQL database.

Test Setup:
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
Time preferred-lifetime is configured with value 400.
Time valid-lifetime is configured with value 600.
Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so.
To hook no. 1 add parameter named name with value: $(DB_NAME)
To hook no. 1 add parameter named password with value: $(DB_PASSWD)
To hook no. 1 add parameter named type with value: postgresql
To hook no. 1 add parameter named user with value: $(DB_USER)
Run configuration command: "mac-sources": [ "docsis-modem" ]
Send server configuration using SSH and config-file.
DHCP server is started.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
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
Client sets enterprisenum value to 4491.
Client does include vendor-class.
Client adds suboption for vendor specific information with code: 36 and data: f6:f5:f4:f3:f2:01.
Client does include vendor-specific-info.
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client does include client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Table logs in PostgreSQL database MUST contain line or phrase: Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:01 (from DOCSIS MODEM)

@v6 @dhcp6 @kea_only @legal_logging
Scenario: v6.loggers.legal-log-hook-address-assigned-docsis-modem-mysql

Test Procedure:
Remove all records from table logs in MySQL database.

Test Setup:
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
Time preferred-lifetime is configured with value 400.
Time valid-lifetime is configured with value 600.
Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so.
To hook no. 1 add parameter named name with value: $(DB_NAME)
To hook no. 1 add parameter named password with value: $(DB_PASSWD)
To hook no. 1 add parameter named type with value: mysql
To hook no. 1 add parameter named user with value: $(DB_USER)
Run configuration command: "mac-sources": [ "docsis-modem" ]
Send server configuration using SSH and config-file.
DHCP server is started.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
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
Client sets enterprisenum value to 4491.
Client does include vendor-class.
Client adds suboption for vendor specific information with code: 36 and data: f6:f5:f4:f3:f2:01.
Client does include vendor-specific-info.
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client does include client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Table logs in MySQL database MUST contain line or phrase: Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:01 (from DOCSIS MODEM)

@v6 @dhcp6 @kea_only @legal_logging
Scenario: v6.loggers.legal-log-hook-address-assigned-docsis-cmts

Test Procedure:
Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.

Test Setup:
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
Time preferred-lifetime is configured with value 400.
Time valid-lifetime is configured with value 600.
Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so.
Run configuration command: "mac-sources": [ "docsis-cmts" ]
Send server configuration using SSH and config-file.
DHCP server is started.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

Test Procedure:
Client copies IA_NA option from received message.
Client copies server-id option from received message.
Client does include client-id.
Client sends REQUEST message.

RelayAgent sets enterprisenum value to 4491.
RelayAgent does include vendor-class.
RelayAgent adds suboption for vendor specific information with code: 1026 and data: 00:f5:f4:00:f2:01.
RelayAgent does include vendor-specific-info.
RelayAgent does include interface-id.
RelayAgent forwards message encapsulated in 1 level.

Pass Criteria:
Server MUST respond with RELAYREPLY message.
Response MUST include option 18.
Response MUST include option 9.
Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.
File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:01 and hardware address: hwtype=1 00:f5:f4:00:f2:01 (from DOCSIS CMTS)

@v6 @dhcp6 @kea_only @legal_logging
Scenario: v6.loggers.legal-log-hook-address-assigned-docsis-cmts-pgsql

Test Procedure:
Remove all records from table logs in PostgreSQL database.

Test Setup:
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
Time preferred-lifetime is configured with value 400.
Time valid-lifetime is configured with value 600.
Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so.
To hook no. 1 add parameter named name with value: $(DB_NAME)
To hook no. 1 add parameter named password with value: $(DB_PASSWD)
To hook no. 1 add parameter named type with value: postgresql
To hook no. 1 add parameter named user with value: $(DB_USER)
Run configuration command: "mac-sources": [ "docsis-cmts" ]
Send server configuration using SSH and config-file.
DHCP server is started.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

Test Procedure:
Client copies IA_NA option from received message.
Client copies server-id option from received message.
Client does include client-id.
Client sends REQUEST message.

RelayAgent sets enterprisenum value to 4491.
RelayAgent does include vendor-class.
RelayAgent adds suboption for vendor specific information with code: 1026 and data: 00:f5:f4:00:f2:01.
RelayAgent does include vendor-specific-info.
RelayAgent does include interface-id.
RelayAgent forwards message encapsulated in 1 level.

Pass Criteria:
Server MUST respond with RELAYREPLY message.
Response MUST include option 18.
Response MUST include option 9.

Table logs in PostgreSQL database MUST contain line or phrase: Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:01 and hardware address: hwtype=1 00:f5:f4:00:f2:01 (from DOCSIS CMTS)

@v6 @dhcp6 @kea_only @legal_logging
Scenario: v6.loggers.legal-log-hook-address-assigned-docsis-cmts-mysql

Test Procedure:
Remove all records from table logs in MySQL database.

Test Setup:
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
Time preferred-lifetime is configured with value 400.
Time valid-lifetime is configured with value 600.
Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so.
To hook no. 1 add parameter named name with value: $(DB_NAME)
To hook no. 1 add parameter named password with value: $(DB_PASSWD)
To hook no. 1 add parameter named type with value: mysql
To hook no. 1 add parameter named user with value: $(DB_USER)
Run configuration command: "mac-sources": [ "docsis-cmts" ]
Send server configuration using SSH and config-file.
DHCP server is started.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

Test Procedure:
Client copies IA_NA option from received message.
Client copies server-id option from received message.
Client does include client-id.
Client sends REQUEST message.

RelayAgent sets enterprisenum value to 4491.
RelayAgent does include vendor-class.
RelayAgent adds suboption for vendor specific information with code: 1026 and data: 00:f5:f4:00:f2:01.
RelayAgent does include vendor-specific-info.
RelayAgent does include interface-id.
RelayAgent forwards message encapsulated in 1 level.

Pass Criteria:
Server MUST respond with RELAYREPLY message.
Response MUST include option 18.
Response MUST include option 9.

Table logs in MySQL database MUST contain line or phrase: Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:01 and hardware address: hwtype=1 00:f5:f4:00:f2:01 (from DOCSIS CMTS)

@v6 @dhcp6 @kea_only @legal_logging
Scenario: v6.loggers.legal-log-hook-address-assigned-relay

Test Procedure:
Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.

Test Setup:
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
Time preferred-lifetime is configured with value 400.
Time valid-lifetime is configured with value 600.
Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so.
Send server configuration using SSH and config-file.
DHCP server is started.

Test Procedure:
Client sets DUID value to 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01.
Client requests option 7.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

Test Procedure:
Client copies IA_NA option from received message.
Client sets DUID value to 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01.
Client copies server-id option from received message.
Client requests option 7.
Client does include client-id.
Client sends REQUEST message.

Client sets enterprisenum value to 666.
Client sets subscriber_id value to 50.
Client does include remote-id.
Client does include subscriber-id.
RelayAgent sets linkaddr value to 3000::1005.
RelayAgent sets ifaceid value to abc.
RelayAgent does include interface-id.
RelayAgent forwards message encapsulated in 5 level.

Pass Criteria:
Server MUST respond with RELAYREPLY message.
Response MUST include option 18.
Response MUST include option 9.
Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.
File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01 and hardware address: hwtype=1 f6:f5:f4:f3:f2:01 (from DUID) connected via relay
File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: connected via relay at address:
File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: for client on link address: 3000::1005, hop count: 5

@v6 @dhcp6 @kea_only @legal_logging
Scenario: v6.loggers.legal-log-hook-address-assigned-relay-pgsql

Test Procedure:
Remove all records from table logs in PostgreSQL database.

Test Setup:
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
Time preferred-lifetime is configured with value 400.
Time valid-lifetime is configured with value 600.
Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so.
To hook no. 1 add parameter named name with value: $(DB_NAME)
To hook no. 1 add parameter named password with value: $(DB_PASSWD)
To hook no. 1 add parameter named type with value: postgresql
To hook no. 1 add parameter named user with value: $(DB_USER)
Send server configuration using SSH and config-file.
DHCP server is started.

Test Procedure:
Client sets DUID value to 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01.
Client requests option 7.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

Test Procedure:
Client copies IA_NA option from received message.
Client sets DUID value to 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01.
Client copies server-id option from received message.
Client requests option 7.
Client does include client-id.
Client sends REQUEST message.

Client sets enterprisenum value to 666.
Client sets subscriber_id value to 50.
Client does include remote-id.
Client does include subscriber-id.
RelayAgent sets linkaddr value to 3000::1005.
RelayAgent sets ifaceid value to abc.
RelayAgent does include interface-id.
RelayAgent forwards message encapsulated in 5 level.

Pass Criteria:
Server MUST respond with RELAYREPLY message.
Response MUST include option 18.
Response MUST include option 9.

Table logs in PostgreSQL database MUST contain line or phrase: Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01 and hardware address: hwtype=1 f6:f5:f4:f3:f2:01 (from DUID) connected via relay
Table logs in PostgreSQL database MUST contain line or phrase: connected via relay at address:
Table logs in PostgreSQL database MUST contain line or phrase: for client on link address: 3000::1005, hop count: 5

@v6 @dhcp6 @kea_only @legal_logging
Scenario: v6.loggers.legal-log-hook-address-assigned-relay-mysql

Test Procedure:
Remove all records from table logs in MySQL database.

Test Setup:
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
Time preferred-lifetime is configured with value 400.
Time valid-lifetime is configured with value 600.
Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so.
To hook no. 1 add parameter named name with value: $(DB_NAME)
To hook no. 1 add parameter named password with value: $(DB_PASSWD)
To hook no. 1 add parameter named type with value: mysql
To hook no. 1 add parameter named user with value: $(DB_USER)
Send server configuration using SSH and config-file.
DHCP server is started.

Test Procedure:
Client sets DUID value to 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01.
Client requests option 7.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

Test Procedure:
Client copies IA_NA option from received message.
Client sets DUID value to 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01.
Client copies server-id option from received message.
Client requests option 7.
Client does include client-id.
Client sends REQUEST message.

Client sets enterprisenum value to 666.
Client sets subscriber_id value to 50.
Client does include remote-id.
Client does include subscriber-id.
RelayAgent sets linkaddr value to 3000::1005.
RelayAgent sets ifaceid value to abc.
RelayAgent does include interface-id.
RelayAgent forwards message encapsulated in 5 level.

Pass Criteria:
Server MUST respond with RELAYREPLY message.
Response MUST include option 18.
Response MUST include option 9.

Table logs in MySQL database MUST contain line or phrase: Address:3000::5 has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:01:00:01:52:7b:a8:f0:f6:f5:f4:f3:f2:01 and hardware address: hwtype=1 f6:f5:f4:f3:f2:01 (from DUID) connected via relay
Table logs in MySQL database MUST contain line or phrase: connected via relay at address:
Table logs in MySQL database MUST contain line or phrase: for client on link address: 3000::1005, hop count: 5


@v6 @dhcp6 @kea_only @legal_logging
Scenario: v6.loggers.legal-log-hook-with-flex-id-address-assigned-mysql

Remove all records from table logs in MySQL database.

Test Setup:
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
Time preferred-lifetime is configured with value 400.
Time valid-lifetime is configured with value 600.
Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by flex-id 01:02:03:04:05:06.
For host reservation entry no. 0 in subnet 0 add address with value 3000::f.
Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so.
To hook no. 1 add parameter named name with value: $(DB_NAME)
To hook no. 1 add parameter named password with value: $(DB_PASSWD)
To hook no. 1 add parameter named type with value: mysql
To hook no. 1 add parameter named user with value: $(DB_USER)
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so.
To hook no. 2 add parameter named identifier-expression with value: vendor[4491].option[1026].hex
Add to config file line: "host-reservation-identifiers": [  "duid",  "flex-id" ]
Send server configuration using SSH and config-file.
DHCP server is started.

Test Procedure:
Client sets enterprisenum value to 4491.
Client does include vendor-class.
Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:04:05:06.
Client does include vendor-specific-info.

Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.
Response sub-option 5 from option 3 MUST contain address 3000::f.

Test Procedure:
Client sets enterprisenum value to 4491.
Client does include vendor-class.
Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:04:05:06.
Client does include vendor-specific-info.
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client does include client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Table logs in MySQL database MUST contain line or phrase: Address:3000::f has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)

@v6 @dhcp6 @kea_only @legal_logging
Scenario: v6.loggers.legal-log-hook-with-flex-id-address-assigned-pgsql

Remove all records from table logs in PostgreSQL database.

Test Setup:
Time renew-timer is configured with value 100.
Time rebind-timer is configured with value 200.
Time preferred-lifetime is configured with value 400.
Time valid-lifetime is configured with value 600.
Server is configured with 3000::/64 subnet with 3000::5-3000::50 pool.
Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by flex-id 01:02:03:04:05:06.
For host reservation entry no. 0 in subnet 0 add address with value 3000::f.
Server is configured with 3001:: prefix in subnet 0 with 90 prefix length and 94 delegated prefix length.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so.
To hook no. 1 add parameter named name with value: $(DB_NAME)
To hook no. 1 add parameter named password with value: $(DB_PASSWD)
To hook no. 1 add parameter named type with value: postgresql
To hook no. 1 add parameter named user with value: $(DB_USER)
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so.
To hook no. 2 add parameter named identifier-expression with value: vendor[4491].option[1026].hex
Add to config file line: "host-reservation-identifiers": [  "duid",  "flex-id" ]
Send server configuration using SSH and config-file.
DHCP server is started.

Test Procedure:
Client sets enterprisenum value to 4491.
Client does include vendor-class.
Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:04:05:06.
Client does include vendor-specific-info.

Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.
Response sub-option 5 from option 3 MUST contain address 3000::f.

Test Procedure:
Client sets enterprisenum value to 4491.
Client does include vendor-class.
Client adds suboption for vendor specific information with code: 1026 and data: 01:02:03:04:05:06.
Client does include vendor-specific-info.
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:04.
Client copies server-id option from received message.
Client copies IA_NA option from received message.
Client does include client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Table logs in PostgreSQL database MUST contain line or phrase: Address:3000::f has been assigned for 0 hrs 10 mins 0 secs to a device with DUID: 00:03:00:01:f6:f5:f4:f3:f2:04 and hardware address: hwtype=1 f6:f5:f4:f3:f2:04 (from DUID)
