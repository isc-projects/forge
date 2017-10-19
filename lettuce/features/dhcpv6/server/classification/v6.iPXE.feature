Feature: DHCPv6 iPXE boot tests
  System tests for classification iPXE boot.

@v6 @iPXE
Scenario: v6.IPXE-1
  Test Setup:
  Client sends local file stored in: features/dhcpv6/server/classification/ipxe2.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/kea.conf.
  Client sends local file stored in: features/dhcpv6/server/classification/ipxe-ctrl.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/keactrl.conf.
  DHCP server is started.

  Test Procedure:
  Client sets archtypes value to 7.
  Client does include client-arch-type.
  Client does include client-id.
  Client does include IA-NA.
  Client sets user_class_data value to iPXE.
  Client does include user-class.
  Client requests option 59.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 59.
  Response option 59 MUST contain optdata http://[2001:db8::1]/ubuntu.cfg.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

@v6 @iPXE
Scenario: v6.IPXE-2
  Test Setup:
  Client sends local file stored in: features/dhcpv6/server/classification/ipxe3.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/kea.conf.
  Client sends local file stored in: features/dhcpv6/server/classification/ipxe-ctrl.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/keactrl.conf.
  DHCP server is started.


  Test Procedure:
  Client sets archtypes value to 7.
  Client does include client-arch-type.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 59.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 59.
  Response option 59 MUST contain optdata http://[2001:db8::1]/ipxe.efi.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

@v6 @iPXE
Scenario: v6.IPXE-combined
  Test Setup:
  Client sends local file stored in: features/dhcpv6/server/classification/ipxe.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/kea.conf.
  Client sends local file stored in: features/dhcpv6/server/classification/ipxe-ctrl.conf to server, to location: $(SOFTWARE_INSTALL_DIR)etc/kea/keactrl.conf.
  DHCP server is started.


  Test Procedure:
  Client sets archtypes value to 7.
  Client does include client-arch-type.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 59.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 59.
  Response option 59 MUST contain optdata http://[2001:db8::1]/ipxe.efi.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Test Procedure:
  Client sets archtypes value to 7.
  Client does include client-arch-type.
  Client does include client-id.
  Client does include IA-NA.
  Client sets user_class_data value to iPXE.
  Client does include user-class.
  Client requests option 59.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 59.
  Response option 59 MUST contain optdata http://[2001:db8::1]/ubuntu.cfg.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.
