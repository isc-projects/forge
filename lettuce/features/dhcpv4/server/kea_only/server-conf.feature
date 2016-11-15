Feature: Kea features
  Various tests of simple Kea features.

@v4 @kea_only
  Scenario: v4.echo.client.id
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Add configuration parameter echo-client-id with value False to global configuration.
  DHCP server is started.

  Test Procedure:
  Client requests option 1.
  Client adds to the message client_id with value 00010203040506.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST NOT include option 61.

  Test Procedure:
  Client adds to the message client_id with value 00010203040506.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.1.
  Client requests option 1.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response MUST NOT include option 61.