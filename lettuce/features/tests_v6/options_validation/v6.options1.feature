
Feature: Standard DHCPv6 options part 1
    This is a simple DHCPv6 options validation. Its purpose is to check if
    requested options are assigned properly. Also testing information-request message.

@v6 @options @preference
    Scenario: v6.options.preference
	## Testing server ability to configure it with option
	## preference (code 7)with value 123, and ability to share that value 
	## with client via Advertise and Reply message.
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
	Server is configured with preference option with value 123.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 7.
	Response option 7 MUST contain value 123.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 7.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 7.
	Response option 7 MUST contain value 123.

	References: v6.options, v6.oro, RFC3315 section 22.8


@v6 @options @sip
    Scenario: v6.options.sip-domains
	## Testing server ability to configure it with option
	## SIP domains (code 21) with domains srv1.example.com 
	## and srv2.isc.org, and ability to share that 
	## with client via Advertise and Reply message.
	## 					Client		Server
	## request option	SOLICIT -->
	## sip-server-dns 			<--	ADVERTISE
	## request option	REQUEST -->
	## sip-server-dns			<--	REPLY
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					sip-server-dns option with domains
	##					srv1.example.com and srv2.isc.org

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with sip-server-dns option with value srv1.example.com,srv2.isc.org.
	Server is started.

	Test Procedure:
	Client requests option 21.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 21.
	Response option 21 MUST contain domains srv1.example.com,srv2.isc.org.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 21.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 21.
	Response option 21 MUST contain domains srv1.example.com,srv2.isc.org.

	References: v6.options RFC3319

@v6 @options @sip @rfc3319
    Scenario: v6.options.sip-servers
	## Testing server ability to configure it with option
	## SIP servers (code 22) with addresses 2001:db8::1 
	## and 2001:db8::2, and ability to share that 
	## with client via Advertise and Reply message.
	## 					Client		Server
	## request option	SOLICIT -->
	## sip-server-addr 			<--	ADVERTISE
	## request option	REQUEST -->
	## sip-server-addr			<--	REPLY
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					sip-server-addr option with addresses
	##					2001:db8::1 and 2001:db8::2

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with sip-server-addr option with value 2001:db8::1,2001:db8::2.
	Server is started.

	Test Procedure:
	Client requests option 22.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 22.
	Response option 22 MUST contain addresses 2001:db8::1,2001:db8::2.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 22.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 22.
	Response option 22 MUST contain addresses 2001:db8::1,2001:db8::2.

	References: v6.options RFC3319


@v6 @options @dns @rfc3646
    Scenario: v6.options.dns-servers
	## Testing server ability to configure it with option
	## DNS servers (code 23) with addresses 2001:db8::1 
	## and 2001:db8::2, and ability to share that 
	## with client via Advertise and Reply message.
	## 					Client		Server
	## request option	SOLICIT -->
	## dns-servers	 			<--	ADVERTISE
	## request option	REQUEST -->
	## dns-servers				<--	REPLY
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					dns-servers option with addresses
	##					2001:db8::1 and 2001:db8::2

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with dns-servers option with value 2001:db8::1,2001:db8::2.
	Server is started.

	Test Procedure:
	Client requests option 23.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 23.
	Response option 23 MUST contain addresses 2001:db8::1,2001:db8::2.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 23.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 23.
	Response option 23 MUST contain addresses 2001:db8::1,2001:db8::2.

	Test Procedure:

	References: v6.options, v6.oro, RFC3646

@v6 @options @rfc3646
    Scenario: v6.options.domains
	## Testing server ability to configure it with option
	## domains (code 24) with domains domain1.example.com 
	## and domain2.isc.org, and ability to share that 
	## with client via Advertise and Reply message.
	## 					Client		Server
	## request option	SOLICIT -->
	## domain-search 			<--	ADVERTISE
	## request option	REQUEST -->
	## domain-search			<--	REPLY
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					domain-search option with addresses
	##					domain1.example.com and domain2.isc.org

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with domain-search option with value domain1.example.com,domain2.isc.org.
	Server is started.

	Test Procedure:
	Client requests option 24.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 24.
	Response option 24 MUST contain domains domain1.example.com,domain2.isc.org.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 24.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 24.
	Response option 24 MUST contain domains domain1.example.com,domain2.isc.org.

	References: v6.options, v6.oro, RFC3646 

@v6 @options @nis @rfc3898
    Scenario: v6.options.nis-servers
	## Testing server ability to configure it with option
	## NIS servers (code 27) with addresses 2001:db8::abc, 3000::1
	## and 2000::1234, and ability to share that 
	## with client via Advertise and Reply message.
	## 					Client		Server
	## request option	SOLICIT -->
	## nis-servers	 			<--	ADVERTISE
	## request option	REQUEST -->
	## nis-servers				<--	REPLY
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					nis-servers option with addresses
	##					2001:db8::abc, 3000::1 and 2000::1234.

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with nis-servers option with value 2001:db8::abc,3000::1,2000::1234.
	Server is started.

	Test Procedure:
	Client requests option 27.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 27.
	Response option 27 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 27.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 27.
	Response option 27 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.

	References: v6.options, v6.oro, RFC3898

@v6 @options @nis @nisp @rfc3898
    Scenario: v6.options.nisp-servers
	## Testing server ability to configure it with option
	## NIS+ servers (code 28) with addresses 2001:db8::abc, 3000::1
	## and 2000::1234, and ability to share that 
	## with client via Advertise message.
	## 					Client		Server
	## request option	SOLICIT -->
	## nisp-servers	 			<--	ADVERTISE
	## Pass Criteria:
	## 				ADVERTISE MUST include option:
	##					nisp-servers option with addresses
	##					2001:db8::abc, 3000::1 and 2000::1234.
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with nisp-servers option with value 2001:db8::abc,3000::1,2000::1234.
	Server is started.

	Test Procedure:
	Client requests option 28.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 28.
	Response option 28 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.

	References: v6.options, v6.oro, RFC3898

	
@v6 @options @nis @rfc3898
    Scenario: v6.options.nisdomain
	## Testing server ability to configure it with option
	## NIS domain (code 29) with domains ntp.example.com and ability to share that 
	## with client via Advertise and Reply message.
	## 					Client		Server
	## request option	SOLICIT -->
	## domain-search 			<--	ADVERTISE
	## request option	REQUEST -->
	## domain-search			<--	REPLY
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					domain-search option with address ntp.example.com

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with nis-domain-name option with value ntp.example.com.
	Server is started.

	Test Procedure:
	Client requests option 29.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 29.
	Response option 29 MUST contain domain ntp.example.com.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 29.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 29.
	Response option 29 MUST contain domain ntp.example.com.

	References: v6.options, v6.oro, RFC3898


@v6 @options @rfc3898
    Scenario: v6.options.nispdomain
	## Testing server ability to configure it with option
	## NIS+ domain (code 30) with domain ntp.example.com, and ability to share that 
	## with client via Advertise and Reply message.
	## 					Client		Server
	## request option	SOLICIT -->
	## nisp-domain-name 			<--	ADVERTISE
	## request option	REQUEST -->
	## nisp-domain-name			<--	REPLY
	## Pass Criteria:
	## 				ADVERTISE MUST include option:
	##					nisp-domain-name option with address ntp.example.com

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with nisp-domain-name option with value ntp.example.com.
	Server is started.

	Test Procedure:
	Client requests option 30.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 30.
	Response option 30 MUST contain domain ntp.example.com.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 30.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 30.
	Response option 30 MUST contain domain ntp.example.com.
	References: v6.options, v6.oro, RFC3898 

@v6 @options @sntp @rfc4075
    Scenario: v6.options.sntp-servers
	## Testing server ability to configure it with option
	## SNTP servers (code 31) with addresses 2001:db8::abc, 3000::1
	## and 2000::1234, and ability to share that 
	## with client via Advertise and Reply message.
	## 					Client		Server
	## request option	SOLICIT -->
	## sntp-servers	 			<--	ADVERTISE
	## request option	REQUEST -->
	## sntp-servers				<--	REPLY
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					sntp-servers option with addresses
	##					2001:db8::abc, 3000::1 and 2000::1234.

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with sntp-servers option with value 2001:db8::abc,3000::1,2000::1234.
	Server is started.

	Test Procedure:
	Client requests option 31.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 31.
	Response option 31 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 31.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 31.
	Response option 31 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.

	References: v6.options, v6.oro, RFC4075
	
@v6 @options @rfc4242
    Scenario: v6.options.info-refresh
	## Testing server ability to configure it with option
	## information refresh time (code 32) with value 12345678 and ability to share that 
	## with client via Advertise and Reply message.
	## 					Client		Server
	## request option	SOLICIT -->
	## information-refresh-time	<--	ADVERTISE
	## request option	REQUEST -->
	## information-refresh-time <--	REPLY
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					information-refresh-time option with value 12345678

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with information-refresh-time option with value 12345678.
	Server is started.

	Test Procedure:
	Client requests option 32.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 32.
	Response option 32 MUST contain value 12345678.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 32.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 32.
	Response option 32 MUST contain value 12345678.
	
	References: v6.options, v6.oro, RFC4242

@v6 @options
    Scenario: v6.options.multiple
	## Testing server ability to configure it with option multiple options:
	## preference (code 7), SIP domain (code 21), DNS servers (code 23), domains (code 24)
	## with client via Advertise and Reply message.
	## 					Client		Server
	## request option	SOLICIT -->
	## all requested opts		<--	ADVERTISE
	## request option	REQUEST -->
	## all requested opts	 	<--	REPLY
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					preference option value 123
	##					SIP domain with domains srv1.example.com and srv2.isc.org.
	##					DNS servers with addresses 2001:db8::1 and 2001:db8::2
	##					domain-search with addresses domain1.example.com and domain2.isc.org
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with preference option with value 123.
	Server is configured with sip-server-dns option with value srv1.example.com,srv2.isc.org.
	Server is configured with dns-servers option with value 2001:db8::1,2001:db8::2.
	Server is configured with domain-search option with value domain1.example.com,domain2.isc.org.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client requests option 21.
	Client requests option 23.
	Client requests option 24.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 7.
	Response MUST include option 21.
	Response MUST include option 23.
	Response MUST include option 24.
	Response option 7 MUST contain value 123.
	Response option 21 MUST contain addresses srv1.example.com,srv2.isc.org.
	Response option 23 MUST contain addresses 2001:db8::1,2001:db8::2.
	Response option 24 MUST contain domains domain1.example.com,domain2.isc.org.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 7.
	Client requests option 21.
	Client requests option 23.
	Client requests option 24.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 7.
	Response MUST include option 21.
	Response MUST include option 23.
	Response MUST include option 24.
	Response option 7 MUST contain value 123.
	Response option 21 MUST contain addresses srv1.example.com,srv2.isc.org.
	Response option 23 MUST contain addresses 2001:db8::1,2001:db8::2.
	Response option 24 MUST contain domains domain1.example.com,domain2.isc.org.

	References: v6.options, v6.oro, RFC3315 section 22.8

@v6 @options @dns @rfc3646
    Scenario: v6.options.negative
	## Testing if server does not return option that it was not configured with.
	## Server configured with option 23, requesting option 24.
	## Testing Advertise and Reply message.
	## 					Client		Server
	## request option	SOLICIT -->
	## does not include code 24	<--	ADVERTISE
	## request option	REQUEST -->
	## does not include code 24	<--	REPLY
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include not option:
	##					domain and dns-servers
	##
	## request option 23 REQUEST -->
	## does include code 23		<--	REPLY
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					dns-servers	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with dns-servers option with value 2001:db8::1,2001:db8::2.
	Server is started.

	Test Procedure:
	# dns-servers is option 23. 24 is domain.
	Client requests option 24.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST NOT include option 23.
	Response MUST NOT include option 24.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 24.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST NOT include option 23.
	Response MUST NOT include option 24.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 23.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 23.
	Response option 23 MUST contain addresses 2001:db8::1,2001:db8::2.
	Response MUST NOT include option 24.
	References: v6.options, v6.oro, RFC3646