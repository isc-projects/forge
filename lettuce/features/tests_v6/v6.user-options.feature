
Feature: DHCPv6 custom options
    This is a simple DHCPv6 options validation. Its purpose is to check if
    requested options are assigned properly.

@v6 @options @user
    Scenario: v6.options.user.preference
	# Checks that server is able to serve sntp-servers option to clients.

	Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server is configured with custom option foo/100 with type uint8 and value 123.
    Server is started.

	Test Procedure:
	Client requests option 100.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 100.
	Response option 100 MUST contain uint8 123.

	References: v6.user-options, v6.oro, RFC3315 section 22.8

	Tags: v6 options preference automated
