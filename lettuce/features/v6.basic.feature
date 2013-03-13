
Feature: Standard DHCPv6 message types
    This is a simple DHCPv6 message validation. Its purpose is to check if presence of message types from RFC 3315 section 5.3
    @nowe
    Scenario: v6.basic.message.advertise

    	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 48.
	Client sends SOLICIT message and expect ADVERTISE response.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	References: RFC3315 section 5.3


    Scenario: v6.basic.message.reply.valid

    	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message and expect ADVERTISE response.
	Server MUST respond with ADVERTISE message.
	Client sends REQUEST message and expect REPLY response.

	Pass Criteria:
	Server MUST respond with REPLY message.
	References: RFC3315 section 5.3

  
    Scenario: v6.basic.message.reply.invalid

    	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message and expect ADVERTISE response.
	Server MUST respond with ADVERTISE message.
	Client requests option 7.
	Client sends REQUEST message and expect REPLY response.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 5.3

