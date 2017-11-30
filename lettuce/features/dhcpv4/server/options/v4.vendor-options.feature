
Feature: DHCPv4 vendor specific information
  This feature is designed for vendor specific information option.
  Testing suboption - option request and others.

@v4 @dhcp4 @options @vendor
  Scenario: v4.options.vendor-encapsulated-space

  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.
  On space vendor-encapsulated-options-space server is configured with a custom option foo/1 with type uint16 and value 66.
  Server is configured with vendor-encapsulated-options option with value $(EMPTY).
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client requests option 43.
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.
  Response MUST include option 43.
  # option 43 should have suboption code: 1 length: 2 with value 66 (hex:42)
  Response option 43 MUST contain value HEX:01020042.
