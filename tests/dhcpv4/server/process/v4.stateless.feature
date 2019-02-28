Feature: DHCPv4 Stateless clients


@v4 @stateless
  Scenario: v4.stateless.with-subnet-empty-pool
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with $(EMPTY) pool.
  Server is configured with subnet-mask option with value 255.255.255.0.
  Server is configured with time-offset option with value 50.
  Server is configured with routers option with value 100.100.100.10,50.50.50.5.
  Send server configuration using SSH and config-file.
DHCP server is started.

  Test Procedure:
  Client requests option 1.
  Client requests option 2.
  Client requests option 3.
  Client sets ciaddr value to $(CIADDR).
  Client sends INFORM message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 0.0.0.0.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 2.
  Response option 2 MUST contain value 50.
  Response MUST include option 3.
  Response option 3 MUST contain value 100.100.100.10.
  Response option 3 MUST contain value 50.50.50.5.
