Feature: CVE-2015-8373
  Check if Kea does not crash after receiving blank client id option.
  https://kb.isc.org/article/AA-01318/214/CVE-2015-8373-ISC-Kea%3A-unexpected-termination-while-handling-a-malformed-packet.html
  Kea trac ticket 4206

@v6 @dhcp6 @confirm @CVE2015
Scenario: v6.CVE.2015.8373.confirm-with-empty-client-id-INFO

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

Test Procedure:
Client copies IA_NA option from received message.
Client copies server-id option from received message.
Client requests option 7.
Client does include client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client saves IA_NA option from received message.
Client adds saved options. And DONT Erase.
Client does include empty-client-id.
Client sends CONFIRM message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client requests option 7.
Client does include client-id.
Client sends CONFIRM message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 13.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @confirm @CVE2015
Scenario: v6.CVE.2015.8373.confirm-with-empty-client-id-FATAL

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity FATAL, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

Test Procedure:
Client copies IA_NA option from received message.
Client copies server-id option from received message.
Client requests option 7.
Client does include client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client saves IA_NA option from received message.
Client adds saved options. And DONT Erase.
Client does include empty-client-id.
Client sends CONFIRM message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client requests option 7.
Client does include client-id.
Client sends CONFIRM message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 13.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @confirm @CVE2015
Scenario: v6.CVE.2015.8373.confirm-with-empty-client-id-ERROR

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity ERROR, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

Test Procedure:
Client copies IA_NA option from received message.
Client copies server-id option from received message.
Client requests option 7.
Client does include client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client saves IA_NA option from received message.
Client adds saved options. And DONT Erase.
Client does include empty-client-id.
Client sends CONFIRM message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client requests option 7.
Client does include client-id.
Client sends CONFIRM message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 13.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @confirm @CVE2015
Scenario: v6.CVE.2015.8373.confirm-with-empty-client-id-WARN

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity WARN, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

Test Procedure:
Client copies IA_NA option from received message.
Client copies server-id option from received message.
Client requests option 7.
Client does include client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client saves IA_NA option from received message.
Client adds saved options. And DONT Erase.
Client does include empty-client-id.
Client sends CONFIRM message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client requests option 7.
Client does include client-id.
Client sends CONFIRM message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 13.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @confirm @CVE2015
Scenario: v6.CVE.2015.8373.confirm-with-empty-client-id-DEBUG

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

Test Procedure:
Client copies IA_NA option from received message.
Client copies server-id option from received message.
Client requests option 7.
Client does include client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client saves IA_NA option from received message.
Client adds saved options. And DONT Erase.
Client does include empty-client-id.
Client sends CONFIRM message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client requests option 7.
Client does include client-id.
Client sends CONFIRM message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 13.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @decline @CVE2015
Scenario: v6.CVE.2015.8373.decline-with-empty-client-id-DEBUG

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
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

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client does include empty-client-id.
Client saves IA_NA option from received message.
Client saves server-id option from received message.
Client adds saved options. And DONT Erase.
Client sends DECLINE message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client does include client-id.
Client sends DECLINE message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @decline @CVE2015
Scenario: v6.CVE.2015.8373.decline-with-empty-client-id-INFO

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
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

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client does include empty-client-id.
Client saves IA_NA option from received message.
Client saves server-id option from received message.
Client adds saved options. And DONT Erase.
Client sends DECLINE message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client does include client-id.
Client sends DECLINE message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @decline @CVE2015
Scenario: v6.CVE.2015.8373.decline-with-empty-client-id-FATAL

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity FATAL, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
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

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client does include empty-client-id.
Client saves IA_NA option from received message.
Client saves server-id option from received message.
Client adds saved options. And DONT Erase.
Client sends DECLINE message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client does include client-id.
Client sends DECLINE message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @decline @CVE2015
Scenario: v6.CVE.2015.8373.decline-with-empty-client-id-ERROR

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity ERROR, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
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

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client does include empty-client-id.
Client saves IA_NA option from received message.
Client saves server-id option from received message.
Client adds saved options. And DONT Erase.
Client sends DECLINE message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client does include client-id.
Client sends DECLINE message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @decline @CVE2015
Scenario: v6.CVE.2015.8373.decline-with-empty-client-id-WARN

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity WARN, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
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

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client does include empty-client-id.
Client saves IA_NA option from received message.
Client saves server-id option from received message.
Client adds saved options. And DONT Erase.
Client sends DECLINE message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client does include client-id.
Client sends DECLINE message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @rebind @CVE2015
Scenario: v6.CVE.2015.8373.rebind-with-empty-client-id-

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
DHCP server is started.

Test Procedure:
Client requests option 7.
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

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client does include empty-client-id.
Client saves IA_NA option from received message.
Client adds saved options. And DONT Erase.
Client sends REBIND message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client does include client-id.
Client sends REBIND message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @rebind @CVE2015
Scenario: v6.CVE.2015.8373.rebind-with-empty-client-id-FATAL

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity FATAL, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
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

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client does include empty-client-id.
Client saves IA_NA option from received message.
Client adds saved options. And DONT Erase.
Client sends REBIND message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client does include client-id.
Client sends REBIND message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @rebind @CVE2015
Scenario: v6.CVE.2015.8373.rebind-with-empty-client-id-ERROR

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity ERROR, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
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

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client does include empty-client-id.
Client saves IA_NA option from received message.
Client adds saved options. And DONT Erase.
Client sends REBIND message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client does include client-id.
Client sends REBIND message.


Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @rebind @CVE2015
Scenario: v6.CVE.2015.8373.rebind-with-empty-client-id-WARN

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity WARN, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
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

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client does include empty-client-id.
Client saves IA_NA option from received message.
Client adds saved options. And DONT Erase.
Client sends REBIND message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client does include client-id.
Client sends REBIND message.


Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @rebind @CVE2015
Scenario: v6.CVE.2015.8373.rebind-with-empty-client-id-INFO

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
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

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client does include empty-client-id.
Client saves IA_NA option from received message.
Client adds saved options. And DONT Erase.
Client sends REBIND message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client does include client-id.
Client sends REBIND message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @rebind @CVE2015
Scenario: v6.CVE.2015.8373.rebind-with-empty-client-id-DEBUG

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
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

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client does include empty-client-id.
Client saves IA_NA option from received message.
Client adds saved options. And DONT Erase.
Client sends REBIND message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client does include client-id.
Client sends REBIND message.


Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @release @CVE2015
Scenario: v6.CVE.2015.8373.release-with-empty-client-id-FATAL

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity FATAL, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
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

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client does include empty-client-id.
Client saves IA_NA option from received message.
Client saves server-id option from received message.
Client adds saved options. And DONT Erase.
Client sends RELEASE message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client does include client-id.
Client sends RELEASE message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 13.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @release @CVE2015
Scenario: v6.CVE.2015.8373.release-with-empty-client-id-ERROR

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity ERROR, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
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

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client does include empty-client-id.
Client saves IA_NA option from received message.
Client saves server-id option from received message.
Client adds saved options. And DONT Erase.
Client sends RELEASE message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client does include client-id.
Client sends RELEASE message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 13.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @release @CVE2015
Scenario: v6.CVE.2015.8373.release-with-empty-client-id-WARN

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity WARN, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
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

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client does include empty-client-id.
Client saves IA_NA option from received message.
Client saves server-id option from received message.
Client adds saved options. And DONT Erase.
Client sends RELEASE message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client does include client-id.
Client sends RELEASE message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 13.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @release @CVE2015
Scenario: v6.CVE.2015.8373.release-with-empty-client-id-INFO

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
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

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client does include empty-client-id.
Client saves IA_NA option from received message.
Client saves server-id option from received message.
Client adds saved options. And DONT Erase.
Client sends RELEASE message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client does include client-id.
Client sends RELEASE message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 13.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @release @CVE2015
Scenario: v6.CVE.2015.8373.release-with-empty-client-id-DEBUG

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
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

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client does include empty-client-id.
Client saves IA_NA option from received message.
Client saves server-id option from received message.
Client adds saved options. And DONT Erase.
Client sends RELEASE message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client does include client-id.
Client sends RELEASE message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 13.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @renew @CVE2015
Scenario: v6.CVE.2015.8373.renew-with-empty-client-id-FATAL

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity FATAL, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
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

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client does include empty-client-id.
Client saves IA_NA option from received message.
Client saves server-id option from received message.
Client adds saved options. And DONT Erase.
Client sends RENEW message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client does include client-id.
Client sends RENEW message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.
Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @renew @CVE2015
Scenario: v6.CVE.2015.8373.renew-with-empty-client-id-ERROR

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity ERROR, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
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

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client does include empty-client-id.
Client saves IA_NA option from received message.
Client saves server-id option from received message.
Client adds saved options. And DONT Erase.
Client sends RENEW message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client does include client-id.
Client sends RENEW message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @renew @CVE2015
Scenario: v6.CVE.2015.8373.renew-with-empty-client-id-WARN

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity WARN, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
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

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client does include empty-client-id.
Client saves IA_NA option from received message.
Client saves server-id option from received message.
Client adds saved options. And DONT Erase.
Client sends RENEW message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client does include client-id.
Client sends RENEW message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @renew @CVE2015
Scenario: v6.CVE.2015.8373.renew-with-empty-client-id-INFO

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
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

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client does include empty-client-id.
Client saves IA_NA option from received message.
Client saves server-id option from received message.
Client adds saved options. And DONT Erase.
Client sends RENEW message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client does include client-id.
Client sends RENEW message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @renew @CVE2015
Scenario: v6.CVE.2015.8373.renew-with-empty-client-id-DEBUG

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
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

Pass Criteria:
Server MUST respond with REPLY message.

Test Procedure:
Client does include empty-client-id.
Client saves IA_NA option from received message.
Client saves server-id option from received message.
Client adds saved options. And DONT Erase.
Client sends RENEW message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client does include client-id.
Client sends RENEW message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @request @CVE2015
Scenario: v6.CVE.2015.8373.request-with-empty-client-id-FATAL

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity FATAL, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

Test Procedure:
Client saves server-id option from received message.
Client saves IA_NA option from received message.
Client adds saved options. And DONT Erase.
Client does include empty-client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client does include client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @request @CVE2015
Scenario: v6.CVE.2015.8373.request-with-empty-client-id-ERROR

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity ERROR, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

Test Procedure:
Client saves server-id option from received message.
Client saves IA_NA option from received message.
Client adds saved options. And DONT Erase.
Client does include empty-client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client does include client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @request @CVE2015
Scenario: v6.CVE.2015.8373.request-with-empty-client-id-WARN

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity WARN, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

Test Procedure:
Client saves server-id option from received message.
Client saves IA_NA option from received message.
Client adds saved options. And DONT Erase.
Client does include empty-client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client does include client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @request @CVE2015
Scenario: v6.CVE.2015.8373.request-with-empty-client-id-INFO

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

Test Procedure:
Client saves server-id option from received message.
Client saves IA_NA option from received message.
Client adds saved options. And DONT Erase.
Client does include empty-client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client does include client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @request @CVE2015
Scenario: v6.CVE.2015.8373.request-with-empty-client-id-DEBUG

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

Test Procedure:
Client saves server-id option from received message.
Client saves IA_NA option from received message.
Client adds saved options. And DONT Erase.
Client does include empty-client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST NOT respond with REPLY message.

Test Procedure:
Client adds saved options. And Erase.
Client does include client-id.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with REPLY message.
Response MUST include option 1.
Response MUST include option 2.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @solicit @CVE2015
Scenario: v6.CVE.2015.8373.solicit-with-empty-client-id-FATAL

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity FATAL, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
Client does include empty-client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond with ADVERTISE message.

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

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @solicit @CVE2015
Scenario: v6.CVE.2015.8373.solicit-with-empty-client-id-ERROR

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity ERROR, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
Client does include empty-client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond with ADVERTISE message.

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

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @solicit @CVE2015
Scenario: v6.CVE.2015.8373.solicit-with-empty-client-id-WARN

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity WARN, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
Client does include empty-client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond with ADVERTISE message.

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

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @solicit @CVE2015
Scenario: v6.CVE.2015.8373.solicit-with-empty-client-id-INFO

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity INFO, severity level None and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
Client does include empty-client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond with ADVERTISE message.

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

Test Procedure:
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.

@v6 @dhcp6 @solicit @CVE2015
Scenario: v6.CVE.2015.8373.solicit-with-empty-client-id-DEBUG

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 99 and log file kea.log.
DHCP server is started.
Test Procedure:
Client requests option 7.
Client does include empty-client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond with ADVERTISE message.

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

@v6 @dhcp6 @solicit @CVE2015
Scenario: v6.CVE.2015.8373.solicit-with-empty-client-id-DEBUG44

Test Setup:

Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 44 and log file kea.log.
DHCP server is started.
Test Procedure:
Client requests option 7.
Client does include empty-client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond with ADVERTISE message.

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

@v6 @dhcp6 @solicit @CVE2015
Scenario: v6.CVE.2015.8373.solicit-with-empty-client-id-DEBUG45

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6, severity DEBUG, severity level 45 and log file kea.log.
DHCP server is started.
Test Procedure:
Client requests option 7.
Client does include empty-client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond with ADVERTISE message.

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

@v6 @dhcp6 @solicit @CVE2015 @detailed
Scenario: v6.CVE.2015.8373.solicit-with-empty-client-id-DEBUGalloc-engine

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6.alloc-engine, severity DEBUG, severity level 99 and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
Client does include empty-client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond with ADVERTISE message.

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

@v6 @dhcp6 @solicit @CVE2015 @detailed
Scenario: v6.CVE.2015.8373.solicit-with-empty-client-id-DEBUGbad-packets

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6.bad-packets, severity DEBUG, severity level 99 and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
Client does include empty-client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond with ADVERTISE message.

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

@v6 @dhcp6 @solicit @CVE2015 @detailed
Scenario: v6.CVE.2015.8373.solicit-with-empty-client-id-DEBUGcallouts

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6.callouts, severity DEBUG, severity level 99 and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
Client does include empty-client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond with ADVERTISE message.

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

@v6 @dhcp6 @solicit @CVE2015 @detailed
Scenario: v6.CVE.2015.8373.solicit-with-empty-client-id-DEBUGcommands

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6.commands, severity DEBUG, severity level 99 and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
Client does include empty-client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond with ADVERTISE message.

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

@v6 @dhcp6 @solicit @CVE2015 @detailed
Scenario: v6.CVE.2015.8373.solicit-with-empty-client-id-DEBUGddns

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6.ddns, severity DEBUG, severity level 99 and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
Client does include empty-client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond with ADVERTISE message.

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

@v6 @dhcp6 @solicit @CVE2015 @detailed
Scenario: v6.CVE.2015.8373.solicit-with-empty-client-id-DEBUG.dhcp6

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6.dhcp6, severity DEBUG, severity level 99 and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
Client does include empty-client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond with ADVERTISE message.

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

@v6 @dhcp6 @solicit @CVE2015 @detailed
Scenario: v6.CVE.2015.8373.solicit-with-empty-client-id-DEBUGdhcpsrv

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6.dhcpsrv, severity DEBUG, severity level 99 and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
Client does include empty-client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond with ADVERTISE message.

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

@v6 @dhcp6 @solicit @CVE2015 @detailed
Scenario: v6.CVE.2015.8373.solicit-with-empty-client-id-DEBUGeval

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6.eval, severity DEBUG, severity level 99 and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
Client does include empty-client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond with ADVERTISE message.

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

@v6 @dhcp6 @solicit @CVE2015 @detailed
Scenario: v6.CVE.2015.8373.solicit-with-empty-client-id-DEBUGhooks

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6.hooks, severity DEBUG, severity level 99 and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
Client does include empty-client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond with ADVERTISE message.

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

@v6 @dhcp6 @solicit @CVE2015 @detailed
Scenario: v6.CVE.2015.8373.solicit-with-empty-client-id-DEBUGhosts

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6.hosts, severity DEBUG, severity level 99 and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
Client does include empty-client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond with ADVERTISE message.

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

@v6 @dhcp6 @solicit @CVE2015 @detailed
Scenario: v6.CVE.2015.8373.solicit-with-empty-client-id-DEBUGleases

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6.leases, severity DEBUG, severity level 99 and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
Client does include empty-client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond with ADVERTISE message.

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

@v6 @dhcp6 @solicit @CVE2015 @detailed
Scenario: v6.CVE.2015.8373.solicit-with-empty-client-id-DEBUGoptions

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6.options, severity DEBUG, severity level 99 and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
Client does include empty-client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond with ADVERTISE message.

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

@v6 @dhcp6 @solicit @CVE2015 @detailed
Scenario: v6.CVE.2015.8373.solicit-with-empty-client-id-DEBUpackets

Test Setup:
Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
Server logging system is configured with logger type kea-dhcp6.packets, severity DEBUG, severity level 99 and log file kea.log.
DHCP server is started.

Test Procedure:
Client requests option 7.
Client does include empty-client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST NOT respond with ADVERTISE message.

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