Feature: Kea6 User Check Hook Library
  Testing KEA's User Check Hook Library - NOTE TEST IS ONLY SUPPORTED BY KEA

# All of these tests rely on the Kea only behavior of setting the first subnet's
# interface value equal to SERVER_IFACE.  If SERVER_IFACE is not blank, Forge
# automatically addes "config set Dhcp6/subnet[0]/interface <SERVER_IFACE>"
# to the server configuration.

@v4 @dhcp4 @kea_only @user_check
  Scenario: user_check.IA_NA.no_registry-logging
  # Without a user registry and multiple subnets
  # Subnet selection will use subnet interface for subnet selection hint

  Test Setup:
  Client removes file from server located in: /tmp/user_chk_registry.txt.
  Client removes file from server located in: /tmp/user_chk_outcome.txt.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.5 pool.
  Server is configured with another subnet: 10.0.0.0/24 with 10.0.0.5-10.0.0.5 pool.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_user_chk.so.
  Server logging system is configured with logger type kea-dhcp4.callouts, severity ERROR, severity level None and log file kea.log.
  Server logging system is configured with logger type kea-dhcp4.hooks, severity ERROR, severity level None and log file kea.log.
  Send server configuration using SSH and config-file.
  DHCP server failed to start. During configuration process.
#  DHCP server is started.
#
#  Test Procedure:
#  Client requests option 1.
#  Client sends DISCOVER message.
#
#  Pass Criteria:
#  Server MUST respond with OFFER message.
#  Response MUST include option 1.
#  Response MUST contain yiaddr 192.168.50.5.
#  Response option 1 MUST contain value 255.255.255.0.
#
#  Test Procedure:
#  Client copies server_id option from received message.
#  Client adds to the message requested_addr with value 192.168.50.5.
#  Client requests option 1.
#  Client sends REQUEST message.
#
#  Pass Criteria:
#  Server MUST respond with ACK message.
#  Client download file from server stored in: /tmp/user_chk_outcome.txt.
#  Client download file from server stored in: /tmp/user_chk_registry.txt.
#  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp4.hooks
#  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST contain line or phrase: ERROR \[kea-dhcp4.hooks
#  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST NOT contain line or phrase: DEBUG \[kea-dhcp4.callouts


@v4 @dhcp4 @kea_only @user_check
  Scenario: user_check.IA_NA.with_registry_unknown_user-logging
  # With a user registry and multiple subnets
  # an unknown user should get last subnet

  Test Setup:
  Client sends local file stored in: features/dhcpv4/server/kea_only/user_chk/registry_1.txt to server, to location: /tmp/user_chk_registry.txt.
  Client removes file from server located in: /tmp/user_chk_outcome.txt.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.5 pool.
  Server is configured with another subnet: 10.0.0.0/24 with 10.0.0.5-10.0.0.5 pool.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_user_chk.so.
  Server logging system is configured with logger type kea-dhcp4.callouts, severity DEBUG, severity level 99 and log file kea.log.
  Server logging system is configured with logger type kea-dhcp4.hooks, severity INFO, severity level None and log file kea.log.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client requests option 1.
  Client sets chaddr value to 0c:0e:0a:01:ff:01.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 10.0.0.5.
  Response option 1 MUST contain value 255.255.255.0.

  # Check the outcome file for correct content
  Client download file from server stored in: /tmp/user_chk_outcome.txt.
  Client compares downloaded file from server with local file stored in: features/dhcpv4/server/kea_only/user_chk/outcome_1.txt.
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST contain line or phrase: INFO  \[kea-dhcp4.hooks
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp4.callouts

@v4 @dhcp4 @kea_only @user_check
  Scenario: user_check.IA_NA.with_registry_unknown_user-logging-2
  # With a user registry and multiple subnets
  # an unknown user should get last subnet

  Test Setup:
  Client sends local file stored in: features/dhcpv4/server/kea_only/user_chk/registry_1.txt to server, to location: /tmp/user_chk_registry.txt.
  Client removes file from server located in: /tmp/user_chk_outcome.txt.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.5 pool.
  Server is configured with another subnet: 10.0.0.0/24 with 10.0.0.5-10.0.0.5 pool.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_user_chk.so.
  #Server logging system is configured with logger type kea-dhcp4.callouts, severity DEBUG, severity level 99 and log file kea.log.
  #Server logging system is configured with logger type kea-dhcp4.hooks, severity INFO, severity level None and log file kea.log.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client requests option 1.
  Client sets chaddr value to 0c:0e:0a:01:ff:01.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 10.0.0.5.
  Response option 1 MUST contain value 255.255.255.0.

  # Check the outcome file for correct content
  Client download file from server stored in: /tmp/user_chk_outcome.txt.
  Client compares downloaded file from server with local file stored in: features/dhcpv4/server/kea_only/user_chk/outcome_1.txt.
  #File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST contain line or phrase: INFO  \[kea-dhcp4.hooks
  #File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp4.callouts

  Test Setup:
  Client sends local file stored in: features/dhcpv4/server/kea_only/user_chk/registry_1.txt to server, to location: /tmp/user_chk_registry.txt.
  Client removes file from server located in: /tmp/user_chk_outcome.txt.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.5 pool.
  Server is configured with another subnet: 10.0.0.0/24 with 10.0.0.5-10.0.0.5 pool.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_user_chk.so.
  #Server logging system is configured with logger type kea-dhcp4.callouts, severity DEBUG, severity level 99 and log file kea.log.
  #Server logging system is configured with logger type kea-dhcp4.hooks, severity INFO, severity level None and log file kea.log.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client requests option 1.
  Client sets chaddr value to 0c:0e:0a:01:ff:01.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 10.0.0.5.
  Response option 1 MUST contain value 255.255.255.0.

  # Check the outcome file for correct content
  Client download file from server stored in: /tmp/user_chk_outcome.txt.
  Client compares downloaded file from server with local file stored in: features/dhcpv4/server/kea_only/user_chk/outcome_1.txt.
  #File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST contain line or phrase: INFO  \[kea-dhcp4.hooks
  #File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST contain line or phrase: DEBUG \[kea-dhcp4.callouts