Feature: DHCPv6 Moving Client
Simulate situation when client after getting his address get mobile and it is changing subnets.

@v6 @dhcp6 @movingclient
Scenario: v6.movingclient.0

Test Setup:
Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::ff pool.
Server is configured with another subnet: 2001:db8:2::/64 with 2001:db8:2::1-2001:db8:2::10 pool.
Server is configured with another subnet: 2001:db8:3::/64 with 2001:db8:3::1-2001:db8:3::10 pool.
Send server configuration using SSH and config-file.
DHCP server is started.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client sets ia_id value to 1000.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client saves IA_NA option from received message.
Client adds saved options. And DONT Erase.
Client copies server-id option from received message.
Client does include client-id.
Client sends REQUEST message.

RelayAgent sets ifaceid value to xyz.
RelayAgent does include interface-id.
RelayAgent sets linkaddr value to 2001:db8:1::1000.
RelayAgent forwards message encapsulated in 1 level.

Pass Criteria:
Server MUST respond with RELAYREPLY message.
Response MUST include option 9.
Response option 9 MUST contain Relayed Message.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client sets ia_id value to 1000.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client saves IA_NA option from received message.
Client adds saved options. And DONT Erase.
Client copies server-id option from received message.
Client does include client-id.
Client sends REQUEST message.

RelayAgent sets ifaceid value to abc.
RelayAgent does include interface-id.
RelayAgent sets linkaddr value to 2001:db8:2::1000.
RelayAgent forwards message encapsulated in 1 level.

Pass Criteria:
Server MUST respond with RELAYREPLY message.
Response MUST include option 9.
Response option 9 MUST contain Relayed Message.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client sets ia_id value to 1000.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client saves IA_NA option from received message.
Client adds saved options. And DONT Erase.
Client copies server-id option from received message.
Client does include client-id.
Client sends REQUEST message.

RelayAgent sets ifaceid value to abcd.
RelayAgent does include interface-id.
RelayAgent sets linkaddr value to 2001:db8:3::1000.
RelayAgent forwards message encapsulated in 1 level.

Pass Criteria:
Server MUST respond with RELAYREPLY message.
Response MUST include option 9.
Response option 9 MUST contain Relayed Message.

@v6 @dhcp6 @movingclient
Scenario: v6.movingclient.1

Test Setup:
Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::ff pool.
Server is configured with another subnet: 2001:db8:2::/64 with 2001:db8:2::1-2001:db8:2::10 pool.
Send server configuration using SSH and config-file.
DHCP server is started.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client sets ia_id value to 1000.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client saves IA_NA option from received message.
Client adds saved options. And DONT Erase.
Client copies server-id option from received message.
Client does include client-id.
Client sends REQUEST message.

RelayAgent sets ifaceid value to xyz.
RelayAgent does include interface-id.
RelayAgent sets linkaddr value to 2001:db8:1::1000.
RelayAgent forwards message encapsulated in 1 level.

Pass Criteria:
Server MUST respond with RELAYREPLY message.
Response MUST include option 9.
Response option 9 MUST contain Relayed Message.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client sets ia_id value to 1000.
Client adds saved options. And DONT Erase.
Client does include client-id.
Client sends CONFIRM message.

RelayAgent sets ifaceid value to abc.
RelayAgent does include interface-id.
RelayAgent sets linkaddr value to 2001:db8:2::2000.
RelayAgent forwards message encapsulated in 1 level.

Pass Criteria:
Server MUST respond with RELAYREPLY message.
Response MUST include option 9.
Response option 9 MUST contain Relayed Message.
Relayed Message MUST include option 1.
Relayed Message MUST include option 2.
#Relayed Message MUST include option 3.
#Relayed Message option 3 MUST NOT contain sub-option 5.
#Relayed Message option 3 MUST contain sub-option 13.
#Relayed Message sub-option 13 from option 3 MUST contain statuscode 2.

@v6 @dhcp6 @movingclient
Scenario: v6.movingclient.2

Test Setup:
Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::ff pool.
Server is configured with another subnet: 2001:db8:2::/64 with 2001:db8:2::1-2001:db8:2::10 pool.
Send server configuration using SSH and config-file.
DHCP server is started.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client sets ia_id value to 1000.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client saves IA_NA option from received message.
Client adds saved options. And DONT Erase.
Client copies server-id option from received message.
Client does include client-id.
Client sends REQUEST message.

RelayAgent sets ifaceid value to xyz.
RelayAgent does include interface-id.
RelayAgent sets linkaddr value to 2001:db8:1::1000.
RelayAgent forwards message encapsulated in 1 level.

Pass Criteria:
Server MUST respond with RELAYREPLY message.
Response MUST include option 9.
Response option 9 MUST contain Relayed Message.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client sets ia_id value to 1000.
Client adds saved options. And DONT Erase.
Client does include client-id.
Client sends REBIND message.

RelayAgent sets ifaceid value to abc.
RelayAgent does include interface-id.
RelayAgent sets linkaddr value to 2001:db8:2::2000.
RelayAgent forwards message encapsulated in 1 level.

Pass Criteria:
Server MUST respond with RELAYREPLY message.
Response MUST include option 9.
Response option 9 MUST contain Relayed Message.
Relayed Message MUST include option 1.
Relayed Message MUST include option 2.
#Response option 3 MUST contain sub-option 5.
#Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.
#Response sub-option 5 from option 3 MUST contain validlft 4000.
#Response sub-option 5 from option 3 MUST contain address 3000::1.
#Response sub-option 5 from option 3 MUST contain validlft 0.

@v6 @dhcp6 @movingclient
Scenario: v6.movingclient.3

Test Setup:
Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::ff pool.
Server is configured with another subnet: 2001:db8:2::/64 with 2001:db8:2::1-2001:db8:2::10 pool.
Send server configuration using SSH and config-file.
DHCP server is started.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client sets ia_id value to 1000.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client saves IA_NA option from received message.
Client saves server-id option from received message.
Client adds saved options. And DONT Erase.
Client does include client-id.
Client sends REQUEST message.

RelayAgent sets ifaceid value to xyz.
RelayAgent does include interface-id.
RelayAgent sets linkaddr value to 2001:db8:1::1000.
RelayAgent forwards message encapsulated in 1 level.

Pass Criteria:
Server MUST respond with RELAYREPLY message.
Response MUST include option 9.
Response option 9 MUST contain Relayed Message.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client sets ia_id value to 1000.
Client adds saved options. And DONT Erase.
Client does include client-id.
Client sends RELEASE message.

RelayAgent sets ifaceid value to abc.
RelayAgent does include interface-id.
RelayAgent sets linkaddr value to 2001:db8:2::2000.
RelayAgent forwards message encapsulated in 1 level.

Pass Criteria:
Server MUST respond with RELAYREPLY message.
Response MUST include option 9.
Response option 9 MUST contain Relayed Message.
Relayed Message MUST include option 1.
Relayed Message MUST include option 2.

#Response MUST include option 3.
#Response option 3 MUST contain T1 0.
#Response option 3 MUST contain T2 0.
#Response option 3 MUST contain sub-option 13.
#Response sub-option 13 from option 3 MUST contain statuscode 0.
#Response MUST include option 13.
#Response option 13 MUST contain statuscode 0.

@v6 @dhcp6 @movingclient
Scenario: v6.movingclient.4

Test Setup:
Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::ff pool.
Server is configured with another subnet: 2001:db8:2::/64 with 2001:db8:2::1-2001:db8:2::10 pool.
Send server configuration using SSH and config-file.
DHCP server is started.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client sets ia_id value to 1000.
Client does include client-id.
Client does include IA-NA.
Client sends SOLICIT message.

Pass Criteria:
Server MUST respond with ADVERTISE message.
Response MUST include option 3.
Response option 3 MUST contain sub-option 5.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client saves IA_NA option from received message.
Client saves server-id option from received message.
Client adds saved options. And DONT Erase.
Client does include client-id.
Client sends REQUEST message.

RelayAgent sets ifaceid value to xyz.
RelayAgent does include interface-id.
RelayAgent sets linkaddr value to 2001:db8:1::1000.
RelayAgent forwards message encapsulated in 1 level.

Pass Criteria:
Server MUST respond with RELAYREPLY message.
Response MUST include option 9.
Response option 9 MUST contain Relayed Message.

Test Procedure:
Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
Client sets ia_id value to 1000.
Client adds saved options. And DONT Erase.
Client does include client-id.
Client sends RENEW message.

RelayAgent sets ifaceid value to abc.
RelayAgent does include interface-id.
RelayAgent sets linkaddr value to 2001:db8:2::2000.
RelayAgent forwards message encapsulated in 1 level.

Pass Criteria:
Server MUST respond with RELAYREPLY message.
Response MUST include option 9.
Response option 9 MUST contain Relayed Message.
Relayed Message MUST include option 1.
Relayed Message MUST include option 2.

#Response MUST include option 3.
#Response option 3 MUST contain sub-option 5.
