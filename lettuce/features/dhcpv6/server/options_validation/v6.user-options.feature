Feature: DHCPv6 custom options
    This is a simple DHCPv6 options validation. Its purpose is to check if
    requested custom options are assigned properly.

@v6 @dhcp6 @options @user
  Scenario: v6.options.user-defined-option
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
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 100.

  Test Procedure:
  Client copies server-id option from received message.
  Client copies IA_NA option from received message.
  Client requests option 100.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 100.
  References: RFC3315 section 22.8

@v6 @dhcp6 @options
  Scenario: v6.options.all

  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
  Server is configured with preference option with value 123.
  Server is configured with sip-server-dns option with value srv1.example.com,srv2.isc.org.
  Server is configured with dns-servers option with value 2001:db8::1,2001:db8::2.
  Server is configured with domain-search option with value domain1.example.com,domain2.isc.org.
  Server is configured with sip-server-addr option with value 2001:db8::1,2001:db8::2.
  Server is configured with nisp-servers option with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-servers option with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-domain-name option with value ntp.example.com.
  Server is configured with nisp-domain-name option with value ntp.example.com.
  Server is configured with sntp-servers option with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with information-refresh-time option with value 12345678.
  Server is configured with unicast option with value 3000::66.
  Server is configured with bcmcs-server-dns option with value very.good.domain.name.com.
  Server is configured with bcmcs-server-addr option with value 3000::66,3000::77.
  Server is configured with pana-agent option with value 3000::66,3000::77.
  Server is configured with new-posix-timezone option with value EST5EDT4.
  Server is configured with new-tzdb-timezone option with value Europe/Zurich.
  Server is configured with bootfile-url option with value http://www.kea.isc.org.
  Server is configured with bootfile-param option with value 000B48656C6C6F20776F726C640003666F6F.
  Server is configured with erp-local-domain-name option with value erp-domain.isc.org.
  Server is configured with domain-search option in subnet 0 with value subnet.example.com.
  Server is configured with custom option foo/100 with type uint8 and value 123.
  On space vendor-4491 server is configured with tftp-servers option with value 2001:558:ff18:16:10:253:175:76.
  On space vendor-4491 server is configured with config-file option with value normal_erouter_v6.cm.
  On space vendor-4491 server is configured with syslog-servers option with value 2001:558:ff18:10:10:253:124:101.
  On space vendor-4491 server is configured with time-servers option with value 2001:558:ff18:16:10:253:175:76.
  On space vendor-4491 server is configured with time-offset option with value -10000.
  DHCP server is started.

  Test Procedure:
  Client requests option 7.
  Client requests option 12.
  Client requests option 21.
  Client requests option 22.
  Client requests option 23.
  Client requests option 24.
  Client requests option 27.
  Client requests option 28.
  Client requests option 29.
  Client requests option 30.
  Client requests option 31.
  Client requests option 32.
  Client requests option 33.
  Client requests option 34.
  Client requests option 40.
  Client requests option 41.
  Client requests option 42.
  Client requests option 59.
  Client requests option 60.
  Client requests option 65.
  Client requests option 100.
  Client sends INFOREQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 7.
  Response option 7 MUST contain value 123.
  Response MUST include option 12.
  Response option 12 MUST contain srvaddr 3000::66.
  Response MUST include option 21.
  Response option 21 MUST contain addresses srv1.example.com,srv2.isc.org.
  Response MUST include option 22.
  Response option 22 MUST contain addresses 2001:db8::1,2001:db8::2.
  Response MUST include option 23.
  Response option 23 MUST contain addresses 2001:db8::1,2001:db8::2.
  Response MUST include option 24.
  Response MUST include option 27.
  Response option 27 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.
  Response MUST include option 28.
  Response option 28 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.
  Response MUST include option 29.
  Response option 29 MUST contain domain ntp.example.com.
  Response MUST include option 30.
  Response option 30 MUST contain domain ntp.example.com.
  Response MUST include option 31.
  Response option 31 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.
  Response MUST include option 32.
  Response option 32 MUST contain value 12345678.
  Response MUST include option 33.
  Response option 33 MUST contain bcmcsdomains very.good.domain.name.com.
  Response MUST include option 34.
  Response option 34 MUST contain bcmcsservers 3000::66,3000::77.
  Response MUST include option 40.
  Response option 40 MUST contain paaaddr 3000::66,3000::77.
  Response MUST include option 41.
  Response option 41 MUST contain optdata EST5EDT4.
  Response MUST include option 42.
  Response option 42 MUST contain optdata Europe/Zurich.
  Response MUST include option 59.
  Response option 59 MUST contain optdata http://www.kea.isc.org.
  Response MUST include option 65.
  Response option 65 MUST contain erpdomain erp-domain.isc.org.

  Test Procedure:
  Client requests option 7.
  Client requests option 12.
  Client requests option 21.
  Client requests option 22.
  Client requests option 23.
  Client requests option 24.
  Client requests option 27.
  Client requests option 28.
  Client requests option 29.
  Client requests option 30.
  Client requests option 31.
  Client requests option 32.
  Client requests option 33.
  Client requests option 34.
  Client requests option 40.
  Client requests option 41.
  Client requests option 42.
  Client requests option 59.
  Client requests option 60.
  Client requests option 65.
  Client requests option 100.
  Client sets enterprisenum value to 4491.
  Client does include vendor-class.
  Client adds suboption for vendor specific information with code: 1 and data: 32.
  Client adds suboption for vendor specific information with code: 1 and data: 33.
  Client adds suboption for vendor specific information with code: 1 and data: 34.
  Client adds suboption for vendor specific information with code: 1 and data: 37.
  Client adds suboption for vendor specific information with code: 1 and data: 38.
  Client does include vendor-specific-info.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 17.
  Response option 17 MUST contain sub-option 32.
  Response option 17 MUST contain sub-option 33.
  Response option 17 MUST contain sub-option 34.
  Response option 17 MUST contain sub-option 37.
  Response option 17 MUST contain sub-option 38.
  Response MUST include option 7.
  Response option 7 MUST contain value 123.
  Response MUST include option 12.
  Response option 12 MUST contain srvaddr 3000::66.
  Response MUST include option 21.
  Response option 21 MUST contain addresses srv1.example.com,srv2.isc.org.
  Response MUST include option 22.
  Response option 22 MUST contain addresses 2001:db8::1,2001:db8::2.
  Response MUST include option 23.
  Response option 23 MUST contain addresses 2001:db8::1,2001:db8::2.
  Response MUST include option 24.
  Response option 24 MUST contain domains subnet.example.com.
  Response MUST include option 27.
  Response option 27 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.
  Response MUST include option 28.
  Response option 28 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.
  Response MUST include option 29.
  Response option 29 MUST contain domain ntp.example.com.
  Response MUST include option 30.
  Response option 30 MUST contain domain ntp.example.com.
  Response MUST include option 31.
  Response option 31 MUST contain addresses 2001:db8::abc,3000::1,2000::1234.
  Response MUST include option 32.
  Response option 32 MUST contain value 12345678.
  Response MUST include option 33.
  Response option 33 MUST contain bcmcsdomains very.good.domain.name.com.
  Response MUST include option 34.
  Response option 34 MUST contain bcmcsservers 3000::66,3000::77.
  Response MUST include option 40.
  Response option 40 MUST contain paaaddr 3000::66,3000::77.
  Response MUST include option 41.
  Response option 41 MUST contain optdata EST5EDT4.
  Response MUST include option 42.
  Response option 42 MUST contain optdata Europe/Zurich.
  Response MUST include option 59.
  Response option 59 MUST contain optdata http://www.kea.isc.org.
  Response MUST include option 65.
  Response option 65 MUST contain erpdomain erp-domain.isc.org.
