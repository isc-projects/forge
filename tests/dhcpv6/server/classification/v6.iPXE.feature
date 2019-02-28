Feature: DHCPv6 iPXE boot tests
  System tests for classification iPXE boot.

@v6 @iPXE
Scenario: v6.IPXE-1
  Test Setup:
  Server is configured with 2001:db8::/64 subnet with $(EMPTY) pool.
  Add class called a-ipxe.
  To class no 1 add parameter named: test with value: substring(option[15].hex,2,4) == 'iPXE'
  To class no 1 add option bootfile-url with value http://[2001:db8::1]/ubuntu.cfg.
  #Server is configured with client-classification option in subnet 0 with name a-ipxe.
  Send server configuration using SSH and config-file.
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
  Server is configured with 2001:db8::/64 subnet with $(EMPTY) pool.
  Add class called a-ipxe.
  To class no 1 add parameter named: test with value: option[61].hex == 0x0007
  To class no 1 add option bootfile-url with value http://[2001:db8::1]/ipxe.efi.
  #Server is configured with client-classification option in subnet 0 with name a-ipxe.
  Send server configuration using SSH and config-file.
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
  Server is configured with 2001:db8::/64 subnet with $(EMPTY) pool.

  Add class called a-ipxe.
  To class no 1 add parameter named: test with value: substring(option[15].hex,2,4) == 'iPXE'
  To class no 1 add option bootfile-url with value http://[2001:db8::1]/ubuntu.cfg.

  Add class called b-ipxe.
  To class no 2 add parameter named: test with value: option[61].hex == 0x0007
  To class no 2 add option bootfile-url with value http://[2001:db8::1]/ipxe.efi.

  Send server configuration using SSH and config-file.

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
