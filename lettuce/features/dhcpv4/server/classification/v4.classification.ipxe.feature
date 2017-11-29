Feature: Client Classification DHCPv4
  iPXE In Kea4

@v4 @dhcp4 @classification
Scenario: v4.client.classification.iPXE-client-arch
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.

  Add class called ipxe_efi_x64.
  To class no 1 add parameter named: test with value: option[93].hex == 0x0009
  To class no 1 add parameter named: next-server with value: 192.0.2.254
  To class no 1 add parameter named: server-hostname with value: hal9000
  To class no 1 add parameter named: boot-file-name with value: /dev/null
  Server is configured with client-classification option in subnet 0 with name ipxe_efi_x64.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message client_id with value ff:01:11:11:11:11:11:22.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client adds to the message pxe_client_architecture with value 9.
  Client adds to the message pxe_client_network_interface with value 320.
  Client adds to the message pxe_client_machine_identifier with value 123456789a.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.
  Response MUST contain siaddr 192.0.2.254.
  Response MUST contain file /dev/null.
  Response MUST contain sname hal9000.

@v4 @dhcp4 @classification
Scenario: v4.client.classification.iPXE-client-inter
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.

  Add class called ipxe_efi_x64.
  To class no 1 add parameter named: test with value: option[94].hex == 0x030200
  To class no 1 add parameter named: next-server with value: 192.0.2.254
  To class no 1 add parameter named: server-hostname with value: hal9000
  To class no 1 add parameter named: boot-file-name with value: /dev/null
  Server is configured with client-classification option in subnet 0 with name ipxe_efi_x64.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message client_id with value ff:01:11:11:11:11:11:22.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client adds to the message pxe_client_architecture with value 9.
  Client adds to the message pxe_client_network_interface with value 320.
  Client adds to the message pxe_client_machine_identifier with value 123456789a.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.
  Response MUST contain siaddr 192.0.2.254.
  Response MUST contain file /dev/null.
  Response MUST contain sname hal9000.

@v4 @dhcp4 @classification
Scenario: v4.client.classification.iPXE-machine-ident
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.

  Add class called ipxe_efi_x64.
  To class no 1 add parameter named: test with value: option[97].hex == 0x0102030405060708090a
  To class no 1 add parameter named: next-server with value: 192.0.2.254
  To class no 1 add parameter named: server-hostname with value: hal9000
  To class no 1 add parameter named: boot-file-name with value: /dev/null
  Server is configured with client-classification option in subnet 0 with name ipxe_efi_x64.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message client_id with value ff:01:11:11:11:11:11:22.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client adds to the message pxe_client_architecture with value 9.
  Client adds to the message pxe_client_network_interface with value 320.
  Client adds to the message pxe_client_machine_identifier with value 123456789a.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.
  Response MUST contain siaddr 192.0.2.254.
  Response MUST contain file /dev/null.
  Response MUST contain sname hal9000.


#
#      208: "pxelinux_magic",
#    209: "pxelinux_configuration_file",
#    210: "pxelinux_path_prefix",
#    211: "pxelinux_reboot_time",