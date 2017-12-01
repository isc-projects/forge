
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

@v4 @dhcp4 @options @vendor @private
  Scenario: v4.options.vendor-encapsulated-space-private-iPXE

  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.
  On space APC server is configured with a custom option cookie/1 with type string and value global-value.
  On space PXE server is configured with a custom option mtftp-ip/1 with type ipv4-address and value 0.0.0.0.

  Add class called APC.
  To class no 1 add parameter named: test with value: option[vendor-class-identifier].text == 'APC'
  To class no 1 add parameter named: option-def with value: [{"name":"vendor-encapsulated-options","code":43,"type":"empty","encapsulate":"APC"}]
  To class no 1 add parameter named: option-data with value: [{"name":"cookie","space":"APC","data":"1APC"},{"name": "vendor-encapsulated-options"}]

  Add class called PXE.
  To class no 2 add parameter named: test with value: option[vendor-class-identifier].text == 'PXE'
  To class no 2 add parameter named: option-def with value: [{"name": "vendor-encapsulated-options","code":43,"type": "empty","encapsulate": "PXE"}]
  To class no 2 add parameter named: option-data with value: [{"name": "mtftp-ip","space": "PXE","data": "1.2.3.4"},{"name": "vendor-encapsulated-options"}]

  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client requests option 43.
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client adds to the message vendor_class_id with value PXE.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 43.
  # option 43 should have suboption code: 1 length: 4 with value(v4 address) 1.2.3.4
  Response option 43 MUST contain value HEX:010401020304.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client requests option 43.
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client adds to the message vendor_class_id with value APC.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 43.
  # option 43 should have suboption code: 1 length: 4 with value 1APC hex:31415043, entire option 43 has length 6
  Response option 43 MUST contain value HEX:010431415043.