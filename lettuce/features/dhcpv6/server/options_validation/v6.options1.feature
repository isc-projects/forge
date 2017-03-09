
Feature: Standard DHCPv6 options part 1
    This is a simple DHCPv6 options validation. Its purpose is to check if
    requested options are assigned properly. Also testing information-request message.

@v6 @dhcp6 @options @preference
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
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 7.
	Response option 7 MUST contain prefval 123.

	Test Procedure:
	Client does include client-id.
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client requests option 7.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 7.
	Response option 7 MUST contain value 123.

	References: v6.options, v6.oro, RFC3315 section 22.8


@v6 @dhcp6 @options @sip
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
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
	Client requests option 21.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 21.
	Response option 21 MUST contain sipdomains srv1.example.com,srv2.isc.org.

	Test Procedure:
	Client does include client-id.
    Client does include IA-NA.
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client requests option 21.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 21.
	Response option 21 MUST contain domains srv1.example.com,srv2.isc.org.

	References: v6.options RFC3319

@v6 @dhcp6 @options @sip @rfc3319
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
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 22.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 22.
	Response option 22 MUST contain addresses 2001:db8::1,2001:db8::2.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client requests option 22.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 22.
	Response option 22 MUST contain addresses 2001:db8::1,2001:db8::2.

	References: v6.options RFC3319


@v6 @dhcp6 @options @dns @rfc3646
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
	Send server configuration using SSH and config-file.
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

@v6 @dhcp6 @options @rfc3646
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
	Send server configuration using SSH and config-file.
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

@v6 @dhcp6 @options @nis @rfc3898
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
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 27.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 27.
	Response option 27 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 27.
	Client copies IA_NA option from received message.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 27.
	Response option 27 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.

	References: v6.options, v6.oro, RFC3898

@v6 @dhcp6 @options @nis @nisp @rfc3898
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
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 28.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 28.
	Response option 28 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.

	References: v6.options, v6.oro, RFC3898

	
@v6 @dhcp6 @options @nis @rfc3898
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
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 29.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 29.
	Response option 29 MUST contain domain ntp.example.com.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client requests option 29.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 29.
	Response option 29 MUST contain domain ntp.example.com.

	References: v6.options, v6.oro, RFC3898


@v6 @dhcp6 @options @rfc3898
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
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 30.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 30.
	Response option 30 MUST contain domain ntp.example.com.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client requests option 30.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 30.
	Response option 30 MUST contain domain ntp.example.com.
	References: v6.options, v6.oro, RFC3898 

@v6 @dhcp6 @options @sntp @rfc4075
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
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 31.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 31.
	Response option 31 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client requests option 31.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 31.
	Response option 31 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.

	References: v6.options, v6.oro, RFC4075
	
@v6 @dhcp6 @options @rfc4242
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
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 32.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 32.
	Response option 32 MUST contain value 12345678.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client requests option 32.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 32.
	Response option 32 MUST contain value 12345678.
	
	References: v6.options, v6.oro, RFC4242

@v6 @dhcp6 @options
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
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client requests option 21.
	Client requests option 23.
	Client requests option 24.
	Client does include client-id.
    Client does include IA-NA.
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
	Client copies IA_NA option from received message.
	Client requests option 7.
	Client requests option 21.
	Client requests option 23.
	Client requests option 24.
	Client does include client-id.
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

@v6 @dhcp6 @options @dns @rfc3646
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
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	# dns-servers is option 23. 24 is domain.
	Client requests option 24.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST NOT include option 23.
	Response MUST NOT include option 24.
	
	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client requests option 24.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST NOT include option 23.
	Response MUST NOT include option 24.

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
	Response MUST NOT include option 24.
	References: v6.options, v6.oro, RFC3646


@v6 @dhcp6 @options
    Scenario: v6.options.unicast
	## Testing server ability to configure it with option
	## unicast (code 12) with value 3000::66 and ability to share that
	## with client via Advertise and Reply message.
	## 					Client		Server
	## request option	SOLICIT -->
	## unicast              	<--	ADVERTISE
	## request option	REQUEST -->
	## unicast                 <--	REPLY
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					unicast option with value 3000::66

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with unicast option with value 3000::66.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 12.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 12.
	Response option 12 MUST contain srvaddr 3000::66.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client requests option 12.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 12.
	Response option 12 MUST contain srvaddr 3000::66.

@v6 @dhcp6 @options
    Scenario: v6.options.bcmcs-server-dns
	## Testing server ability to configure it with option
	## bcmcs-server-dns (code 33) with value very.good.domain.name.com and ability to share that
	## with client via Advertise and Reply message.
	## 					Client		Server
	## request option	SOLICIT -->
	## bcmcs-server-dns              	<--	ADVERTISE
	## request option	REQUEST -->
	## bcmcs-server-dns                 <--	REPLY
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					bcmcs-server-dns option with value very.good.domain.name.com

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with bcmcs-server-dns option with value very.good.domain.name.com.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 33.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 33.
	Response option 33 MUST contain bcmcsdomains very.good.domain.name.com.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client requests option 33.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 33.
	Response option 33 MUST contain bcmcsdomains very.good.domain.name.com.

  @v6 @dhcp6 @options
    Scenario: v6.options.bcmcs-server-addr
	## Testing server ability to configure it with option
	## bcmcs-server-addr (code 34) with value 3000::66 and ability to share that
	## with client via Advertise and Reply message.
	## 					Client		Server
	## request option	SOLICIT -->
	## bcmcs-server-addr              	<--	ADVERTISE
	## request option	REQUEST -->
	## bcmcs-server-addr                 <--	REPLY
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					bcmcs-server-addr option with value 3000::66

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with bcmcs-server-addr option with value 3000::66,3000::77.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 34.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 34.
	Response option 34 MUST contain bcmcsservers 3000::66,3000::77.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client requests option 34.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 34.
	Response option 34 MUST contain bcmcsservers 3000::66,3000::77.

  @v6 @dhcp6 @options
    Scenario: v6.options.pana-agent
	## Testing server ability to configure it with option
	## pana-agent (code 40) with value 3000::66 and ability to share that
	## with client via Advertise and Reply message.
	## 					Client		Server
	## request option	SOLICIT -->
	## pana-agent             	<--	ADVERTISE
	## request option	REQUEST -->
	## pana-agent                 <--	REPLY
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					pana-agent option with value 3000::66

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with pana-agent option with value 3000::66,3000::77.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 40.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 40.
	Response option 40 MUST contain paaaddr 3000::66,3000::77.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client requests option 40.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 40.
	Response option 40 MUST contain paaaddr 3000::66,3000::77.

    References: RFC5192

@v6 @dhcp6 @options
    Scenario: v6.options.new-posix-timezone
	## Testing server ability to configure it with option
	## new-posix-timezone (code 41) with value EST5EDT4,M3.2.0/02:00,M11.1.0/02:00 and ability to share that
	## with client via Advertise and Reply message.
	## 					Client		Server
	## request option	SOLICIT -->
	## new-posix-timezone              	<--	ADVERTISE
	## request option	REQUEST -->
	## new-posix-timezone                 <--	REPLY
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					new-posix-timezone option with value EST5EDT4,M3.2.0/02:00,M11.1.0/02:00

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with new-posix-timezone option with value EST5EDT4\\,M3.2.0/02:00\\,M11.1.0/02:00.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 41.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 41.
	Response option 41 MUST contain optdata EST5EDT4,M3.2.0/02:00,M11.1.0/02:00.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client requests option 41.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 41.
	Response option 41 MUST contain optdata EST5EDT4,M3.2.0/02:00,M11.1.0/02:00.

@v6 @dhcp6 @options
    Scenario: v6.options.new-tzdb-timezone
	## Testing server ability to configure it with option
	## new-tzdb-timezone (code 42) with value Europe/Zurich and ability to share that
	## with client via Advertise and Reply message.
	## 					Client		Server
	## request option	SOLICIT -->
	## new-tzdb-timezone              	<--	ADVERTISE
	## request option	REQUEST -->
	## new-tzdb-timezone                 <--	REPLY
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					new-tzdb-timezone option with value Europe/Zurich

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with new-tzdb-timezone option with value Europe/Zurich.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 42.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 42.
	Response option 42 MUST contain optdata Europe/Zurich.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client requests option 42.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 42.
	Response option 42 MUST contain optdata Europe/Zurich.


@v6 @dhcp6 @options
    Scenario: v6.options.bootfile-url
	## Testing server ability to configure it with option
	## bootfile-url (code 59) with value http://www.kea.isc.org and ability to share that
	## with client via Advertise and Reply message.
	## 					Client		Server
	## request option	SOLICIT -->
	## bootfile-url              	<--	ADVERTISE
	## request option	REQUEST -->
	## bootfile-url                 <--	REPLY
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					new-tzdb-timezone option with value http://www.kea.isc.org

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with bootfile-url option with value http://www.kea.isc.org.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 59.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 59.
	Response option 59 MUST contain optdata http://www.kea.isc.org.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client requests option 59.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 59.
	Response option 59 MUST contain optdata http://www.kea.isc.org.

@v6 @dhcp6 @options
    Scenario: v6.options.bootfile-param
	## Testing server ability to configure it with option
	## bootfile-param (code 60) with value 000B48656C6C6F20776F726C64 and ability to share that
    ## 000B48656C6C6F20776F726C64 = length 11 "Hello world length 3 "foo"
	## with client via Advertise and Reply message.
	## 					Client		Server
	## request option	SOLICIT -->
	## bootfile-param              	<--	ADVERTISE
	## request option	REQUEST -->
	## bootfile-param                 <--	REPLY
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					bootfile-param option with value 000B48656C6C6F20776F726C64

	Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server is configured with bootfile-param option with value 000B48656C6C6F20776F726C640003666F6F.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
	Client requests option 60.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 60.
	#Response option 60 MUST contain optdata ??.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client requests option 60.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 60.
	#Response option 60 MUST contain optdata ??.


@v6 @dhcp6 @options @disabled
    # Kea works against the RFC spec.
    Scenario: v6.options.lq-client-link
	## Testing server ability to configure it with option
	## lq-client-link (code 48) with value 3000::66 and ability to share that
	## with client via Advertise and Reply message.
	## 					Client		Server
	## request option	SOLICIT -->
	## lq-client-link             	<--	ADVERTISE
	## request option	REQUEST -->
	## lq-client-link                 <--	REPLY
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					lq-client-link option with value 3000::66

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is configured with lq-client-link option with value 3000::66,3000::77.
	Send server configuration using SSH and config-file.
DHCP server is started.

	Test Procedure:
	Client requests option 48.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 48.
	Response option 48 MUST contain link-address 3000::66,3000::77.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client requests option 48.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 48.
	Response option 48 MUST contain link-address 3000::66,3000::77.

    References: RFC5007


@v6 @dhcp6 @options
    Scenario: v6.options.erp-local-domain-name
	## Testing server ability to configure it with option
	## erp-local-domain-name (code 65) with value erp-domain.isc.org and ability to share that
	## with client via Advertise and Reply message.
	## 					Client		Server
	## request option	SOLICIT -->
	## erp-local-domain-name       	<--	ADVERTISE
	## request option	REQUEST -->
	## erp-local-domain-name        <--	REPLY
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					erp-local-domain-name option with value erp-domain.isc.org

	Test Setup:
    Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    Server is configured with erp-local-domain-name option with value erp-domain.isc.org.
    Send server configuration using SSH and config-file.
DHCP server is started.

    Test Procedure:
	Client requests option 65.
	Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 65.
	Response option 65 MUST contain erpdomain erp-domain.isc.org.

	Test Procedure:
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client requests option 65.
	Client does include client-id.
    Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 65.
	Response option 65 MUST contain erpdomain erp-domain.isc.org.