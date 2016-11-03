Feature: DHCPv6 options defined in subnet
    This is a simple DHCPv6 options validation. Its purpose is to check if
    requested options are assigned properly.

@v6 @dhcp6 @options @subnet
    Scenario: v6.options.subnet.preference
	## Testing server ability to configure it with option
	## preference (code 7) with value 123 per subnet(to override global)
	## and ability to share that value with client via Advertise and Reply message.
	## 					Client		Server
	## request option	SOLICIT -->
	## preference value 123		<--	ADVERTISE
	## request option	REQUEST -->
	## preference value 123		<--	REPLY
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					Preference option with value 123

	Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server is configured with preference option in subnet 0 with value 123.
    DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 7.
	Response option 7 MUST contain value 123.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client requests option 7.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 7.
	Response option 7 MUST contain value 123.

	References: v6.options, v6.oro, RFC3315 section 22.8

@v6 @dhcp6 @options @subnet @rfc3646
    Scenario: v6.options.subnet.dns-servers
	## Testing server ability to configure it with option
	## DNS servers (code 23) with addresses 2001:db8::1 per subnet(to override global)
	## and ability to share that value with client via Advertise and Reply message.
	## 					Client		Server
	## request option	SOLICIT -->
	## dns-servers				<--	ADVERTISE
	## request option	REQUEST -->
	## dns-servers				<--	REPLY
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					dns-servers option with addresses
	##					2001:db8::1 and 2001:db8::2

	Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server is configured with dns-servers option in subnet 0 with value 2001:db8::1,2001:db8::2.
    DHCP server is started.

	Test Procedure:
	Client requests option 23.
	Client does include client-id.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 23.
	Response option 23 MUST contain addresses 2001:db8::1,2001:db8::2.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client requests option 23.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 23.
	Response option 23 MUST contain addresses 2001:db8::1,2001:db8::2.
	
	References: v6.options, v6.oro, RFC3646

@v6 @dhcp6 @options @subnet @rfc3646
    Scenario: v6.options.subnet.domains
	## Testing server ability to configure it with option
	## domains (code 24) with domains domain1.example.com 
	## and domain2.isc.org, per subnet(to override global)
	## and ability to share that value with client via Advertise and Reply message.
	## 					Client		Server
	## request option	SOLICIT -->
	## domain-search			<--	ADVERTISE
	## request option	REQUEST -->
	## domain-search			<--	REPLY
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					domain-search option with addresses
	##					domain1.example.com and domain2.isc.org
	Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server is configured with domain-search option in subnet 0 with value domain1.example.com,domain2.isc.org.
    DHCP server is started.

	Test Procedure:
	Client requests option 24.
	Client does include client-id.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 24.
	Response option 24 MUST contain domains domain1.example.com,domain2.isc.org.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client requests option 24.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 24.
	Response option 24 MUST contain domains domain1.example.com,domain2.isc.org.
	
	References: v6.options, v6.oro, RFC3646 

@v6 @dhcp6 @options @subnet @rfc3646
    Scenario: v6.options.subnet.override
	## Testing server ability to configure it with option
	## domains (code 24) with domains subnet.example.com per subnet
	## (to override global which is also configured with domain global.example.com)
	## and ability to share that value with client via Advertise and Reply message.
	## 					Client		Server
	## request option	SOLICIT -->
	## domain-search			<--	ADVERTISE
	## request option	REQUEST -->
	## domain-search			<--	REPLY
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					domain-search option with addresses
	##					subnet.example.com
	## 				REPLY/ADVERTISE MUST NOT include option:
	##					domain-search option with addresses
	##					global.example.com	
	Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server is configured with domain-search option with value global.example.com.
    Server is configured with domain-search option in subnet 0 with value subnet.example.com.
    DHCP server is started.

	Test Procedure:
	Client requests option 24.
	Client does include client-id.
    Client does include IA-NA.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 24.
	Response option 24 MUST contain domains subnet.example.com.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client requests option 24.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 24.
	Response option 24 MUST contain domains subnet.example.com.
	
	References: v6.options, v6.oro, RFC3646 
