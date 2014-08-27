
Feature: Standard DHCPv6 options part 2
    This is a simple DHCPv6 options validation. Its purpose is to check if
    requested options are assigned properly. Also testing information-request message.

@v6 @dhcp6 @options @preference
    Scenario: v6.options.inforequest.preference
	## Testing server ability to configure it with option
	## preference (code 7)with value 123, and ability to share that value 
	## with client via Reply message as a respond to INFOREQUEST.
	## 						Client		Server
	## request option	INFOREQUEST -->
	## preference value 123			<--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					Preference option with value 123
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with preference option with value 123.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 7.
	Response option 7 MUST contain value 123.

	References: RFC3315 section 22.8

@v6 @dhcp6 @options @sip
    Scenario: v6.options.inforequest.sip-domains
	## Testing server ability to configure it with option
	## SIP domains (code 21) with domains srv1.example.com 
	## and srv2.isc.org, and ability to share that 
	## with client via Reply message as a respond to INFOREQUEST.
	## 						Client		Server
	## request option	INFOREQUEST -->
	## sip-server-dns				<--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					sip-server-dns option with domains
	##					srv1.example.com and srv2.isc.org
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with sip-server-dns option with value srv1.example.com,srv2.isc.org.
	DHCP server is started.

	Test Procedure:
	Client requests option 21.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 21.
	Response option 21 MUST contain domains srv1.example.com,srv2.isc.org.

	References: RFC3319

@v6 @dhcp6 @options @sip @rfc3319
    Scenario: v6.options.inforequest.sip-servers
	## Testing server ability to configure it with option
	## SIP servers (code 22) with addresses 2001:db8::1 
	## and 2001:db8::2, and ability to share that 
	## with client via Reply message as a respond to INFOREQUEST.
	## 						Client		Server
	## request option	INFOREQUEST -->
	## sip-server-addr				<--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					sip-server-addr option with addresses
	##					2001:db8::1 and 2001:db8::2
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with sip-server-addr option with value 2001:db8::1,2001:db8::2.
	DHCP server is started.

	Test Procedure:
	Client requests option 22.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 22.
	Response option 22 MUST contain addresses 2001:db8::1,2001:db8::2.

	References: RFC3319


@v6 @dhcp6 @options @dns @rfc3646
    Scenario: v6.options.inforequest.dns-servers
	## Testing server ability to configure it with option
	## DNS servers (code 23) with addresses 2001:db8::1 
	## and 2001:db8::2, and ability to share that 
	## with client via Reply message as a respond to INFOREQUEST.
	## 						Client		Server
	## request option	INFOREQUEST -->
	## dns-servers					<--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					dns-servers option with addresses
	##					2001:db8::1 and 2001:db8::2

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with dns-servers option with value 2001:db8::1,2001:db8::2.
	DHCP server is started.

	Test Procedure:
	Client requests option 23.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 23.
	Response option 23 MUST contain addresses 2001:db8::1,2001:db8::2.

	Test Procedure:

	References: v6.options, v6.oro, RFC3646

@v6 @dhcp6 @options @rfc3646
    Scenario: v6.options.inforequest.domains
	## Testing server ability to configure it with option
	## domains (code 24) with domains domain1.example.com 
	## and domain2.isc.org, and ability to share that 
	## with client via Reply message as a respond to INFOREQUEST.
	## 						Client		Server
	## request option	INFOREQUEST -->
	## domain-search				<--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					domain-search option with addresses
	##					domain1.example.com and domain2.isc.org

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with domain-search option with value domain1.example.com,domain2.isc.org.
	DHCP server is started.

	Test Procedure:
	Client requests option 24.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 24.
	Response option 24 MUST contain domains domain1.example.com,domain2.isc.org.

	References: RFC3646 

@v6 @dhcp6 @options @nis @rfc3898
    Scenario: v6.options.inforequest.nis-servers
	## Testing server ability to configure it with option
	## NIS servers (code 27) with addresses 2001:db8::abc, 3000::1
	## and 2000::1234, and ability to share that 
	## with client via Reply message as a respond to INFOREQUEST.
	## 						Client		Server
	## request option	INFOREQUEST -->
	## nis-servers					<--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					nis-servers option with addresses
	##					2001:db8::abc, 3000::1 and 2000::1234.

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with nis-servers option with value 2001:db8::abc,3000::1,2000::1234.
	DHCP server is started.

	Test Procedure:
	Client requests option 27.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 27.
	Response option 27 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.

	References: RFC3898

@v6 @dhcp6 @options @nis @nisp @rfc3898
    Scenario: v6.options.inforequest.nisp-servers
	## Testing server ability to configure it with option
	## NIS+ servers (code 28) with addresses 2001:db8::abc, 3000::1
	## and 2000::1234, and ability to share that 
	## with client via Reply message as a respond to INFOREQUEST.
	## 						Client		Server
	## request option	INFOREQUEST -->
	## nisp-servers				<--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					nisp-servers option with addresses
	##					2001:db8::abc, 3000::1 and 2000::1234.

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with nisp-servers option with value 2001:db8::abc,3000::1,2000::1234.
	DHCP server is started.

	Test Procedure:
	Client requests option 28.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 28.
	Response option 28 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.

	References: RFC3898

	
@v6 @dhcp6 @options @nis @rfc3898
    Scenario: v6.options.inforequest.nisdomain
	## Testing server ability to configure it with option
	## NIS domain (code 29) with domains ntp.example.com and ability to share that 
	## with client via Reply message as a respond to INFOREQUEST.
	## 						Client		Server
	## request option	INFOREQUEST -->
	## domain-search				<--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					domain-search option with address ntp.example.com


	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with nis-domain-name option with value ntp.example.com.
	DHCP server is started.

	Test Procedure:
	Client requests option 29.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 29.
	Response option 29 MUST contain domain ntp.example.com.

	References: RFC3898


@v6 @dhcp6 @options @rfc3898
    Scenario: v6.options.inforequest.nispdomain
	## Testing server ability to configure it with option
	## NIS+ domain (code 30) with domain ntp.example.com, and ability to share that 
	## with client via Reply message as a respond to INFOREQUEST.
	## 						Client		Server
	## request option	INFOREQUEST -->
	## nisp-domain-name				<--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					nisp-domain-name option with address ntp.example.com

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with nisp-domain-name option with value ntp.example.com.
	DHCP server is started.

	Test Procedure:
	Client requests option 30.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 30.
	Response option 30 MUST contain domain ntp.example.com.

	References: RFC3898 

@v6 @dhcp6 @options @sntp @rfc4075
    Scenario: v6.options.inforequest.sntp-servers
	## Testing server ability to configure it with option
	## SNTP servers (code 31) with addresses 2001:db8::abc, 3000::1
	## and 2000::1234, and ability to share that 
	## with client via Reply message as a respond to INFOREQUEST.
	## 						Client		Server
	## request option	INFOREQUEST -->
	## sntp-servers				<--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					sntp-servers option with addresses
	##					2001:db8::abc, 3000::1 and 2000::1234.

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with sntp-servers option with value 2001:db8::abc,3000::1,2000::1234.
	DHCP server is started.

	Test Procedure:
	Client requests option 31.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 31.
	Response option 31 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.

	References: RFC4075
	
@v6 @dhcp6 @options @rfc4242
    Scenario: v6.options.inforequest.info-refresh
	## Testing server ability to configure it with option
	## information refresh time (code 32) with value 12345678 and ability to share that 
	## with client via Reply message as a respond to INFOREQUEST.
	## 						Client		Server
	## request option	INFOREQUEST -->
	## information-refresh-time		<--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					information-refresh-time option with value 12345678

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with information-refresh-time option with value 12345678.
	DHCP server is started.

	Test Procedure:
	Client requests option 32.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 32.
	Response option 32 MUST contain value 12345678.
	
	References: RFC4242

@v6 @dhcp6 @options
    Scenario: v6.options.inforequest.multiple
	## Testing server ability to configure it with option multiple options:
	## preference (code 7), SIP domain (code 21), DNS servers (code 23), domains (code 24)
	## with client via Reply message as a respond to INFOREQUEST.
	## 						Client		Server
	## request option	INFOREQUEST -->
	## all requested opts			<--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
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
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client requests option 21.
	Client requests option 23.
	Client requests option 24.
	Client sends INFOREQUEST message.

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

	References: RFC3315 section 22.8

@v6 @dhcp6 @options @dns @rfc3646
    Scenario: v6.options.inforequest.negative
	## Testing if server does not return option that it was not configured with.
	## Server configured with option 23, requesting option 24.
	## Testing Reply message as a respond to INFOREQUEST.
	## 						Client		Server
	## request option	INFOREQUEST -->
	## does not include code 24		<--	REPLY
	## Pass Criteria:
	## 				REPLY MUST NOT include option:
	##					domain and dns-servers
	##
	## request option	INFOREQUEST -->
	## does include code 23			<--	REPLY
	## Pass Criteria:
	## 				REPLY MUST NOT include option:
	##					domain and dns-servers
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with dns-servers option with value 2001:db8::1,2001:db8::2.
	DHCP server is started.

	Test Procedure:
	Client requests option 24.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST NOT include option 23.
	Response MUST NOT include option 24.
	

	Test Procedure:
	Client requests option 23.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 23.

	References: RFC3646
