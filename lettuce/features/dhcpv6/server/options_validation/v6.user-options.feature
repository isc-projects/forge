
Feature: DHCPv6 custom options
    This is a simple DHCPv6 options validation. Its purpose is to check if
    requested custom options are assigned properly.

@v6 @dhcp6 @options @user
    Scenario: v6.options.user.preference
	## Testing server ability to configure it with user custom option
	## in this case: option code 100, value unit8 123. 
	## with client via Advertise and Reply message.
	## 					Client		Server
	## request option	SOLICIT -->
	## custom option 			<--	ADVERTISE
	## request option	REQUEST -->
	## custom option			<--	REPLY
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					custom option with value 123

	Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server is configured with custom option foo/100 with type uint8 and value 123.
    DHCP server is started.

	Test Procedure:
	Client requests option 100.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 100.
	Response option 100 MUST contain uint8 123.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 100.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 100.
	Response option 100 MUST contain uint8 123.

	References: RFC3315 section 22.8
