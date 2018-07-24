Feature: Kea Control Channel - socket
  Tests for Kea Command Control Channel using unix socket to pass commands.

  @v6 @controlchannel @kea_onlyn
  Scenario: control.channel.socket.dhcp-disable-timer
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::1.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "dhcp-disable", "arguments": {"max-period": 5}}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST NOT respond.

  Sleep for 7 seconds.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

@v6 @controlchannel @kea_only
  Scenario: control.channel.socket.dhcp-disable
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::1.
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "dhcp-disable" }

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST NOT respond.

@v6 @controlchannel @kea_only
  Scenario: control.channel.socket.dhcp-disable-and-enable
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::1.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "dhcp-disable" }

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST NOT respond.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "dhcp-enable" }

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  
@v6 @controlchannel @kea_only
  Scenario: control.channel.socket.config-set-basic
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::1.

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Generate server configuration file.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "config-set","arguments":  $(SERVER_CONFIG) }

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.

@v6 @controlchannel @kea_only
  Scenario: control.channel.socket.change-socket-during-reconfigure
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::1.

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket2.
  Generate server configuration file.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "config-set","arguments":  $(SERVER_CONFIG) }

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "list-commands","arguments": {}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket2 send {"command": "list-commands","arguments": {}}

@v6 @controlchannel @kea_only
Scenario: control.channel.socket.after-restart-load-config-file

  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::1.

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Generate server configuration file.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "config-set","arguments":  $(SERVER_CONFIG) }

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.

  DHCP server is restarted.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::1.

@v6 @controlchannel @kea_only @disabled
Scenario: control.channel.socket.big-config-file
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::1.

  Test Setup:
  Server is configured with 2001:db8:1:1::/64 subnet with 2001:db8:1:1::1-2001:db8:1:1::1 pool.
  Server is configured with another subnet: 2001:db8:1:2::/64 with 2001:db8:1:2::1-2001:db8:1:2::1 pool.
  Server is configured with another subnet: 2001:db8:1:3::/64 with 2001:db8:1:3::1-2001:db8:1:3::1 pool.
  Server is configured with another subnet: 2001:db8:1:4::/64 with 2001:db8:1:4::1-2001:db8:1:4::1 pool.
  Server is configured with another subnet: 2001:db8:1:5::/64 with 2001:db8:1:5::1-2001:db8:1:5::1 pool.
  Server is configured with another subnet: 2001:db8:1:6::/64 with 2001:db8:1:6::1-2001:db8:1:6::1 pool.
  Server is configured with another subnet: 2001:db8:1:7::/64 with 2001:db8:1:7::1-2001:db8:1:7::1 pool.
  Server is configured with another subnet: 2001:db8:1:8::/64 with 2001:db8:1:8::1-2001:db8:1:8::1 pool.
  Server is configured with another subnet: 2001:db8:1:9::/64 with 2001:db8:1:9::1-2001:db8:1:9::1 pool.
  Server is configured with another subnet: 2001:db8:1:10::/64 with 2001:db8:1:10::1-2001:db8:1:10::1 pool.
  Server is configured with another subnet: 2001:db8:1:11::/64 with 2001:db8:1:11::1-2001:db8:1:11::1 pool.
  Server is configured with another subnet: 2001:db8:1:12::/64 with 2001:db8:1:12::1-2001:db8:1:12::1 pool.
  Server is configured with another subnet: 2001:db8:1:13::/64 with 2001:db8:1:13::1-2001:db8:1:13::1 pool.
  Server is configured with another subnet: 2001:db8:1:14::/64 with 2001:db8:1:14::1-2001:db8:1:14::1 pool.
  Server is configured with another subnet: 2001:db8:1:15::/64 with 2001:db8:1:15::1-2001:db8:1:15::1 pool.
  Server is configured with another subnet: 2001:db8:1:16::/64 with 2001:db8:1:16::1-2001:db8:1:16::1 pool.
  Server is configured with another subnet: 2001:db8:1:17::/64 with 2001:db8:1:17::1-2001:db8:1:17::1 pool.
  Server is configured with another subnet: 2001:db8:1:18::/64 with 2001:db8:1:18::1-2001:db8:1:18::1 pool.
  Server is configured with another subnet: 2001:db8:1:19::/64 with 2001:db8:1:19::1-2001:db8:1:19::1 pool.
  Server is configured with another subnet: 2001:db8:1:20::/64 with 2001:db8:1:20::1-2001:db8:1:20::1 pool.
  Server is configured with another subnet: 2001:db8:1:21::/64 with 2001:db8:1:21::1-2001:db8:1:21::1 pool.
  Server is configured with another subnet: 2001:db8:1:22::/64 with 2001:db8:1:22::1-2001:db8:1:22::1 pool.
  Server is configured with another subnet: 2001:db8:1:23::/64 with 2001:db8:1:23::1-2001:db8:1:23::1 pool.
  Server is configured with another subnet: 2001:db8:1:24::/64 with 2001:db8:1:24::1-2001:db8:1:24::1 pool.
  Server is configured with another subnet: 2001:db8:1:25::/64 with 2001:db8:1:25::1-2001:db8:1:25::1 pool.

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
  Server is configured with custom option foo/100 with type uint8 and value 123.

  Server is configured with preference option in subnet 0 with value 123.
  Server is configured with sip-server-dns option in subnet 0 with value srv1.example.com,srv2.isc.org.
  Server is configured with dns-servers option in subnet 0 with value 2001:db8::1,2001:db8::2.
  Server is configured with domain-search option in subnet 0 with value domain1.example.com,domain2.isc.org.
  Server is configured with sip-server-addr option in subnet 0 with value 2001:db8::1,2001:db8::2.
  Server is configured with nisp-servers option in subnet 0 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-servers option in subnet 0 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-domain-name option in subnet 0 with value ntp.example.com.
  Server is configured with nisp-domain-name option in subnet 0 with value ntp.example.com.
  Server is configured with sntp-servers option in subnet 0 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with information-refresh-time option in subnet 0 with value 12345678.
  Server is configured with unicast option in subnet 0 with value 3000::66.
  Server is configured with bcmcs-server-dns option in subnet 0 with value very.good.domain.name.com.
  Server is configured with bcmcs-server-addr option in subnet 0 with value 3000::66,3000::77.
  Server is configured with pana-agent option in subnet 0 with value 3000::66,3000::77.
  Server is configured with new-posix-timezone option in subnet 0 with value EST5EDT4.
  Server is configured with new-tzdb-timezone option in subnet 0 with value Europe/Zurich.
  Server is configured with bootfile-url option in subnet 0 with value http://www.kea.isc.org.
  Server is configured with bootfile-param option in subnet 0 with value 000B48656C6C6F20776F726C640003666F6F.
  Server is configured with erp-local-domain-name option in subnet 0 with value erp-domain.isc.org.
  Server is configured with domain-search option in subnet 0 with value subnet.example.com.
  Server is configured with custom option foo/101 with type uint8 and value 123.

  Server is configured with custom option foo/109 with type uint16 and value 12313.
  Server is configured with custom option foo/111 with type uint16 and value 12313.
  Server is configured with custom option foo/112 with type uint16 and value 12312.
  Server is configured with custom option foo/113 with type uint16 and value 12313.
  Server is configured with custom option foo/114 with type uint16 and value 12311.
  Server is configured with custom option foo/115 with type uint16 and value 1231.
  Server is configured with custom option foo/116 with type uint16 and value 12313.
  Server is configured with custom option foo/117 with type uint16 and value 1231.
  Server is configured with custom option foo/118 with type uint16 and value 1231.
  Server is configured with custom option foo/119 with type uint16 and value 1231.
  Server is configured with custom option foo/120 with type uint16 and value 1231.
  Server is configured with custom option foo/121 with type uint16 and value 12313.
  Server is configured with custom option foo/122 with type uint16 and value 1231.

  Server is configured with custom option fowqrgfo/123 with type string and value 123123123456789edrftgyhujikrctvybnui23.
  Server is configured with custom option fowefwefwvro/124 with type string and value 12312312!@#$%^&*(*&^%$JKHBGV<&IMUNTY3.
  Server is configured with custom option fowerwerfvro/125 with type string and value 12312312<IMU^N%$^HGB$VTBYNU&I2.
  Server is configured with custom option foogretnbu8oimu/126 with type string and value 123123122@#%$#^$&%*I*KJHNBV3.
  Server is configured with custom option foo/127 with type string and value 123123123J%^$HBYU*N(KIJMNUTYBRT1.
  Server is configured with custom option fojumnygbfcdo/128 with type string and value 123123J&%MNY$TBERVF+{\"?PO:><JKMHJ123.
  Server is configured with custom option fbtrbrtn78980oo/129 with type string and value 12312312<IMU^TNYRBFVD3.
  Server is configured with custom option foo8iumjyhgnfv/130 with type string and value 1231231<I&MYUTNYHFGVD23.
  Server is configured with custom option foumhnbo/131 with type string and value 123123123.
  Server is configured with custom option fomunhygbvo/132 with type string and value 123123123.
  Server is configured with custom option fmuhnoo/133 with type string and value 123123123.
  Server is configured with custom option fomunhgo/134 with type string and value 123123123.
  Server is configured with custom option foimujhno/135 with type string and value 123123123.
  Server is configured with custom option dawfwrbrbumobt/136 with type string and value 1231231wsedrftgyhujikolp;lokijhgfdszswxdecfvgtbyhnujuyhtgf5rdew23e4r5t6y7u81234567890-=!@#$%^&*()_+{:>}|?><23.
  Server is configured with custom option dawfwrbrbumobt/137 with type string and value 123123123wrexcrvtbuynium435678ui8oikmnbgvfcder5t6y7u8iko,mjnbvcfdxse34r567yu8ijkmn.
  Server is configured with custom option dawfwrbrbumobt/138 with type string and value 12312312i87654e3wsdxcfvgyh7u8ijkmolplk,9j8unbyg6tfr54edswzedcfrtghyujikmolkoiujhyt65rfdesw3.
  Server is configured with custom option dawfwrbrbumobt/139 with type string and value 12312312@!#$R%^TY&*UI()OP_P_)O(*&U^%TR%$#E@Q!3.
  Server is configured with custom option dawfwrbrbumobt/140 with type string and value 1231231wsedrftgyhujikolp;lokijhgfdszswxdecfvgtbyhnujuyhtgf5rdew23e4r5t6y7u81234567890-=!@#$%^&*()_+{:>}|?><23.
  Server is configured with custom option dawfwrbrbumobt/141 with type string and value 123123123wrexcrvtbuynium435678ui8oikmnbgvfcder5t6y7u8iko,mjnbvcfdxse34r567yu8ijkmn.
  Server is configured with custom option dawfwrbrbumobt/142 with type string and value 12312312i87654e3wsdxcfvgyh7u8ijkmolplk,9j8unbyg6tfr54edswzedcfrtghyujikmolkoiujhyt65rfdesw3.
  Server is configured with custom option dawfwrbrbumobt/143 with type string and value 12312312@!#$R%^TY&*UI()OP_P_)O(*&U^%TR%$#E@Q!3.
  Server is configured with custom option dawfwrbrbumobt/144 with type string and value 1231231wsedrftgyhujikolp;lokijhgfdszswxdecfvgtbyhnujuyhtgf5rdew23e4r5t6y7u81234567890-=!@#$%^&*()_+{:>}|?><23.
  Server is configured with custom option dawfwrbrbumobt/145 with type string and value 123123123wrexcrvtbuynium435678ui8oikmnbgvfcder5t6y7u8iko,mjnbvcfdxse34r567yu8ijkmn.
  Server is configured with custom option dawfwrbrbumobt/146 with type string and value 12312312i87654e3wsdxcfvgyh7u8ijkmolplk,9j8unbyg6tfr54edswzedcfrtghyujikmolkoiujhyt65rfdesw3.
  Server is configured with custom option dawfwrbrbumobt/147 with type string and value 12312312@!#$R%^TY&*UI()OP_P_)O(*&U^%TR%$#E@Q!3.
  Server is configured with custom option dawfwrbrbumobt/148 with type string and value 1231231wsedrftgyhujikolp;lokijhgfdszswxdecfvgtbyhnujuyhtgf5rdew23e4r5t6y7u81234567890-=!@#$%^&*()_+{:>}|?><23.
  Server is configured with custom option dawfwrbrbumobt/149 with type string and value 123123123wrexcrvtbuynium435678ui8oikmnbgvfcder5t6y7u8iko,mjnbvcfdxse34r567yu8ijkmn.
  Server is configured with custom option dawfwrbrbumobt/150 with type string and value 12312312i87654e3wsdxcfvgyh7u8ijkmolplk,9j8unbyg6tfr54edswzedcfrtghyujikmolkoiujhyt65rfdesw3.
  Server is configured with custom option dawfwrbrbumobt/151 with type string and value 12312312@!#$R%^TY&*UI()OP_P_)O(*&U^%TR%$#E@Q!3.

  #Server is configured with custom option dawfwrbrbumobt/152 with type string and value 12312312@!#$R%^TY&*UI()OP_P_)O(*&U^%TR%$#E@Q!3.
  #Server is configured with custom option dawfwrbrbumobt/153 with type string and value 1231231wsedrftgyhujikolp;lokijhgfdszswxdecfvgtbyhnujuyhtgf5rdew23e4r5t6y7u81234567890-=!@#$%^&*()_+{:>}|?><23.
  #Server is configured with custom option dawfwrbrbumobt/154 with type string and value 123123123wrexcrvtbuynium435678ui8oikmnbgvfcder5t6y7u8iko,mjnbvcfdxse34r567yu8ijkmn.
  #Server is configured with custom option dawfwrbrbumobt/155 with type string and value 12312312i87654e3wsdxcfvgyh7u8ijkmolplk,9j8unbyg6tfr54edswzedcfrtghyujikmolkoiujhyt65rfdesw3.
  #Server is configured with custom option dawfwrbrbumobt/156 with type string and value 12312312@!#$R%^TY&*UI()OP_P_)O(*&U^%TR%$#E@Q!3.
  #Server is configured with custom option dawfwrbrbumobt/157 with type string and value 1231231wsedrftgyhujikolp;lokijhgfdszswxdecfvgtbyhnujuyhtgf5rdew23e4r5t6y7u81234567890-=!@#$%^&*()_+{:>}|?><23.
  #Server is configured with custom option dawfwrbrbumobt/158 with type string and value 123123123wrexcrvtbuynium435678ui8oikmnbgvfcder5t6y7u8iko,mjnbvcfdxse34r567yu8ijkmn.
  #Server is configured with custom option dawfwrbrbumobt/159 with type string and value 12312312i87654e3wsdxcfvgyh7u8ijkmolplk,9j8unbyg6tfr54edswzedcfrtghyujikmolkoiujhyt65rfdesw3.
  #Server is configured with custom option dawfwrbrbumobt/160 with type string and value 12312312@!#$R%^TY&*UI()OP_P_)O(*&U^%TR%$#E@Q!3.
  #
  #Server is configured with custom option dawfwrbrbumobt/161 with type string and value 12312312@!#$R%^TY&*UI()OP_P_)O(*&U^%TR%$#E@Q!3.
  #Server is configured with custom option dawfwrbrbumobt/162 with type string and value 1231231wsedrftgyhujikolp;lokijhgfdszswxdecfvgtbyhnujuyhtgf5rdew23e4r5t6y7u81234567890-=!@#$%^&*()_+{:>}|?><23.
  #Server is configured with custom option dawfwrbrbumobt/163 with type string and value 123123123wrexcrvtbuynium435678ui8oikmnbgvfcder5t6y7u8iko,mjnbvcfdxse34r567yu8ijkmn.
  #Server is configured with custom option dawfwrbrbumobt/164 with type string and value 12312312i87654e3wsdxcfvgyh7u8ijkmolplk,9j8unbyg6tfr54edswzedcfrtghyujikmolkoiujhyt65rfdesw3.
  #Server is configured with custom option dawfwrbrbumobt/165 with type string and value 12312312@!#$R%^TY&*UI()OP_P_)O(*&U^%TR%$#E@Q!3.
  #Server is configured with custom option dawfwrbrbumobt/166 with type string and value 1231231wsedrftgyhujikolp;lokijhgfdszswxdecfvgtbyhnujuyhtgf5rdew23e4r5t6y7u81234567890-=!@#$%^&*()_+{:>}|?><23.
  #Server is configured with custom option dawfwrbrbumobt/167 with type string and value 123123123wrexcrvtbuynium435678ui8oikmnbgvfcder5t6y7u8iko,mjnbvcfdxse34r567yu8ijkmn.
  #Server is configured with custom option dawfwrbrbumobt/168 with type string and value 12312312i87654e3wsdxcfvgyh7u8ijkmolplk,9j8unbyg6tfr54edswzedcfrtghyujikmolkoiujhyt65rfdesw3.
  #Server is configured with custom option dawfwrbrbumobt/169 with type string and value 12312312@!#$R%^TY&*UI()OP_P_)O(*&U^%TR%$#E@Q!3.



  #Server is configured with preference option in subnet 1 with value 123.
  #Server is configured with sip-server-dns option in subnet 1 with value srv1.example.com,srv2.isc.org.
  #Server is configured with dns-servers option in subnet 1 with value 2001:db8::1,2001:db8::2.
  #Server is configured with domain-search option in subnet 1 with value domain1.example.com,domain2.isc.org.
  #Server is configured with sip-server-addr option in subnet 1 with value 2001:db8::1,2001:db8::2.
  #Server is configured with nisp-servers option in subnet 1 with value 2001:db8::abc,3000::1,2000::1234.
  #Server is configured with nis-servers option in subnet 1 with value 2001:db8::abc,3000::1,2000::1234.
  #Server is configured with nis-domain-name option in subnet 1 with value ntp.example.com.
  #Server is configured with nisp-domain-name option in subnet 1 with value ntp.example.com.
  #Server is configured with sntp-servers option in subnet 1 with value 2001:db8::abc,3000::1,2000::1234.
  #Server is configured with information-refresh-time option in subnet 1 with value 12345678.
  #Server is configured with unicast option in subnet 1 with value 3000::66.
  #Server is configured with bcmcs-server-dns option in subnet 1 with value very.good.domain.name.com.
  #Server is configured with bcmcs-server-addr option in subnet 1 with value 3000::66,3000::77.
  #Server is configured with pana-agent option in subnet 1 with value 3000::66,3000::77.
  #Server is configured with new-posix-timezone option in subnet 1 with value EST5EDT4.
  #Server is configured with new-tzdb-timezone option in subnet 1 with value Europe/Zurich.
  #Server is configured with bootfile-url option in subnet 1 with value http://www.kea.isc.org.
  #Server is configured with bootfile-param option in subnet 1 with value 000B48656C6C6F20776F726C640003666F6F.
  #Server is configured with erp-local-domain-name option in subnet 1 with value erp-domain.isc.org.
  #Server is configured with domain-search option in subnet 0 with value subnet.example.com.
  #Server is configured with custom option foo/102 with type uint8 and value 123.

  #Server is configured with preference option in subnet 2 with value 123.
  #Server is configured with sip-server-dns option in subnet 2 with value srv1.example.com,srv2.isc.org.
  #Server is configured with dns-servers option in subnet 2 with value 2001:db8::1,2001:db8::2.
  #Server is configured with domain-search option in subnet 2 with value domain1.example.com,domain2.isc.org.
  #Server is configured with sip-server-addr option in subnet 2 with value 2001:db8::1,2001:db8::2.
  #Server is configured with nisp-servers option in subnet 2 with value 2001:db8::abc,3000::1,2000::1234.
  #Server is configured with nis-servers option in subnet 2 with value 2001:db8::abc,3000::1,2000::1234.
  #Server is configured with nis-domain-name option in subnet 2 with value ntp.example.com.
  #Server is configured with nisp-domain-name option in subnet 2 with value ntp.example.com.
  #Server is configured with sntp-servers option in subnet 2 with value 2001:db8::abc,3000::1,2000::1234.
  #Server is configured with information-refresh-time option in subnet 2 with value 12345678.
  #Server is configured with unicast option in subnet 2 with value 3000::66.
  #Server is configured with bcmcs-server-dns option in subnet 2 with value very.good.domain.name.com.
  #Server is configured with bcmcs-server-addr option in subnet 2 with value 3000::66,3000::77.
  #Server is configured with pana-agent option in subnet 2 with value 3000::66,3000::77.
  #Server is configured with new-posix-timezone option in subnet 2 with value EST5EDT4.
  #Server is configured with new-tzdb-timezone option in subnet 2 with value Europe/Zurich.
  #Server is configured with bootfile-url option in subnet 2 with value http://www.kea.isc.org.
  #Server is configured with bootfile-param option in subnet 2 with value 000B48656C6C6F20776F726C640003666F6F.
  #Server is configured with erp-local-domain-name option in subnet 2 with value erp-domain.isc.org.
  #Server is configured with domain-search option in subnet 0 with value subnet.example.com.
  #Server is configured with custom option foo/103 with type uint8 and value 123.

  #  Server is configured with preference option in subnet 3 with value 123.
  #Server is configured with sip-server-dns option in subnet 3 with value srv1.example.com,srv2.isc.org.
  #Server is configured with dns-servers option in subnet 3 with value 2001:db8::1,2001:db8::2.
  #Server is configured with domain-search option in subnet 3 with value domain1.example.com,domain2.isc.org.
  #Server is configured with sip-server-addr option in subnet 3 with value 2001:db8::1,2001:db8::2.
  #Server is configured with nisp-servers option in subnet 3 with value 2001:db8::abc,3000::1,2000::1234.
  #Server is configured with nis-servers option in subnet 3 with value 2001:db8::abc,3000::1,2000::1234.
  #Server is configured with nis-domain-name option in subnet 3 with value ntp.example.com.
  #Server is configured with nisp-domain-name option in subnet 3 with value ntp.example.com.
  #Server is configured with sntp-servers option in subnet 3 with value 2001:db8::abc,3000::1,2000::1234.
  #Server is configured with information-refresh-time option in subnet 3 with value 12345678.
  #Server is configured with unicast option in subnet 3 with value 3000::66.
  #Server is configured with bcmcs-server-dns option in subnet 3 with value very.good.domain.name.com.
  #Server is configured with bcmcs-server-addr option in subnet 3 with value 3000::66,3000::77.
  #Server is configured with pana-agent option in subnet 3 with value 3000::66,3000::77.
  #Server is configured with new-posix-timezone option in subnet 3 with value EST5EDT4.
  #Server is configured with new-tzdb-timezone option in subnet 3 with value Europe/Zurich.
  #Server is configured with bootfile-url option in subnet 3 with value http://www.kea.isc.org.
  #Server is configured with bootfile-param option in subnet 3 with value 000B48656C6C6F20776F726C640003666F6F.
  #Server is configured with erp-local-domain-name option in subnet 3 with value erp-domain.isc.org.
  #Server is configured with domain-search option in subnet 0 with value subnet.example.com.
  #Server is configured with custom option foo/104 with type uint8 and value 123.
  #
  #
  #Server is configured with preference option in subnet 4 with value 123.
  #Server is configured with sip-server-dns option in subnet 4 with value srv1.example.com,srv2.isc.org.
  #Server is configured with dns-servers option in subnet 4 with value 2001:db8::1,2001:db8::2.
  #Server is configured with domain-search option in subnet 4 with value domain1.example.com,domain2.isc.org.
  #Server is configured with sip-server-addr option in subnet 4 with value 2001:db8::1,2001:db8::2.
  #Server is configured with nisp-servers option in subnet 4 with value 2001:db8::abc,3000::1,2000::1234.
  #Server is configured with nis-servers option in subnet 4 with value 2001:db8::abc,3000::1,2000::1234.
  #Server is configured with nis-domain-name option in subnet 4 with value ntp.example.com.
  #Server is configured with nisp-domain-name option in subnet 4 with value ntp.example.com.
  #Server is configured with sntp-servers option in subnet 4 with value 2001:db8::abc,3000::1,2000::1234.
  #Server is configured with information-refresh-time option in subnet 4 with value 12345678.
  #Server is configured with unicast option in subnet 4 with value 3000::66.
  #Server is configured with bcmcs-server-dns option in subnet 4 with value very.good.domain.name.com.
  #Server is configured with bcmcs-server-addr option in subnet 4 with value 3000::66,3000::77.
  #Server is configured with pana-agent option in subnet 4 with value 3000::66,3000::77.
  #Server is configured with new-posix-timezone option in subnet 4 with value EST5EDT4.
  #Server is configured with new-tzdb-timezone option in subnet 4 with value Europe/Zurich.
  #Server is configured with bootfile-url option in subnet 4 with value http://www.kea.isc.org.
  #Server is configured with bootfile-param option in subnet 4 with value 000B48656C6C6F20776F726C640003666F6F.
  #Server is configured with erp-local-domain-name option in subnet 4 with value erp-domain.isc.org.
  #Server is configured with domain-search option in subnet 0 with value subnet.example.com.
  #Server is configured with custom option foo/105 with type uint8 and value 123.


  Server is configured with preference option in subnet 5 with value 123.
  Server is configured with sip-server-dns option in subnet 5 with value srv1.example.com,srv2.isc.org.
  Server is configured with dns-servers option in subnet 5 with value 2001:db8::1,2001:db8::2.
  Server is configured with domain-search option in subnet 5 with value domain1.example.com,domain2.isc.org.
  Server is configured with sip-server-addr option in subnet 5 with value 2001:db8::1,2001:db8::2.
  Server is configured with nisp-servers option in subnet 5 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-servers option in subnet 5 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-domain-name option in subnet 5 with value ntp.example.com.
  Server is configured with nisp-domain-name option in subnet 5 with value ntp.example.com.
  Server is configured with sntp-servers option in subnet 5 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with information-refresh-time option in subnet 5 with value 12345678.
  Server is configured with unicast option in subnet 5 with value 3000::66.
  Server is configured with bcmcs-server-dns option in subnet 5 with value very.good.domain.name.com.
  Server is configured with bcmcs-server-addr option in subnet 5 with value 3000::66,3000::77.
  Server is configured with pana-agent option in subnet 5 with value 3000::66,3000::77.
  Server is configured with new-posix-timezone option in subnet 5 with value EST5EDT4.
  Server is configured with new-tzdb-timezone option in subnet 5 with value Europe/Zurich.
  Server is configured with bootfile-url option in subnet 5 with value http://www.kea.isc.org.
  Server is configured with bootfile-param option in subnet 5 with value 000B48656C6C6F20776F726C640003666F6F.
  Server is configured with erp-local-domain-name option in subnet 5 with value erp-domain.isc.org.
  Server is configured with domain-search option in subnet 0 with value subnet.example.com.
  Server is configured with custom option foo/106 with type uint8 and value 123.

  Server is configured with preference option in subnet 6 with value 123.
  Server is configured with sip-server-dns option in subnet 6 with value srv1.example.com,srv2.isc.org.
  Server is configured with dns-servers option in subnet 6 with value 2001:db8::1,2001:db8::2.
  Server is configured with domain-search option in subnet 6 with value domain1.example.com,domain2.isc.org.
  Server is configured with sip-server-addr option in subnet 6 with value 2001:db8::1,2001:db8::2.
  Server is configured with nisp-servers option in subnet 6 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-servers option in subnet 6 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-domain-name option in subnet 6 with value ntp.example.com.
  Server is configured with nisp-domain-name option in subnet 6 with value ntp.example.com.
  Server is configured with sntp-servers option in subnet 6 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with information-refresh-time option in subnet 6 with value 12345678.
  Server is configured with unicast option in subnet 6 with value 3000::66.
  Server is configured with bcmcs-server-dns option in subnet 6 with value very.good.domain.name.com.
  Server is configured with bcmcs-server-addr option in subnet 6 with value 3000::66,3000::77.
  Server is configured with pana-agent option in subnet 6 with value 3000::66,3000::77.
  Server is configured with new-posix-timezone option in subnet 6 with value EST5EDT4.
  Server is configured with new-tzdb-timezone option in subnet 6 with value Europe/Zurich.
  Server is configured with bootfile-url option in subnet 6 with value http://www.kea.isc.org.
  Server is configured with bootfile-param option in subnet 6 with value 000B48656C6C6F20776F726C640003666F6F.
  Server is configured with erp-local-domain-name option in subnet 6 with value erp-domain.isc.org.
  Server is configured with domain-search option in subnet 0 with value subnet.example.com.
  Server is configured with custom option foo/108 with type uint8 and value 123.

  Server is configured with preference option in subnet 7 with value 123.
  Server is configured with sip-server-dns option in subnet 7 with value srv1.example.com,srv2.isc.org.
  Server is configured with dns-servers option in subnet 7 with value 2001:db8::1,2001:db8::2.
  Server is configured with domain-search option in subnet 7 with value domain1.example.com,domain2.isc.org.
  Server is configured with sip-server-addr option in subnet 7 with value 2001:db8::1,2001:db8::2.
  Server is configured with nisp-servers option in subnet 7 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-servers option in subnet 7 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-domain-name option in subnet 7 with value ntp.example.com.
  Server is configured with nisp-domain-name option in subnet 7 with value ntp.example.com.
  Server is configured with sntp-servers option in subnet 7 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with information-refresh-time option in subnet 7 with value 12345678.
  Server is configured with unicast option in subnet 7 with value 3000::66.
  Server is configured with bcmcs-server-dns option in subnet 7 with value very.good.domain.name.com.
  Server is configured with bcmcs-server-addr option in subnet 7 with value 3000::66,3000::77.
  Server is configured with pana-agent option in subnet 7 with value 3000::66,3000::77.
  Server is configured with new-posix-timezone option in subnet 7 with value EST5EDT4.
  Server is configured with new-tzdb-timezone option in subnet 7 with value Europe/Zurich.
  Server is configured with bootfile-url option in subnet 7 with value http://www.kea.isc.org.
  Server is configured with bootfile-param option in subnet 7 with value 000B48656C6C6F20776F726C640003666F6F.
  Server is configured with erp-local-domain-name option in subnet 7 with value erp-domain.isc.org.
  Server is configured with domain-search option in subnet 0 with value subnet.example.com.
  Server is configured with custom option foo/107 with type uint8 and value 123.

  Server is configured with preference option in subnet 8 with value 123.
  Server is configured with sip-server-dns option in subnet 8 with value srv1.example.com,srv2.isc.org.
  Server is configured with dns-servers option in subnet 8 with value 2001:db8::1,2001:db8::2.
  Server is configured with domain-search option in subnet 8 with value domain1.example.com,domain2.isc.org.
  Server is configured with sip-server-addr option in subnet 8 with value 2001:db8::1,2001:db8::2.
  Server is configured with nisp-servers option in subnet 8 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-servers option in subnet 8 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-domain-name option in subnet 8 with value ntp.example.com.
  Server is configured with nisp-domain-name option in subnet 8 with value ntp.example.com.
  Server is configured with sntp-servers option in subnet 8 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with information-refresh-time option in subnet 8 with value 12345678.
  Server is configured with unicast option in subnet 8 with value 3000::66.
  Server is configured with bcmcs-server-dns option in subnet 8 with value very.good.domain.name.com.
  Server is configured with bcmcs-server-addr option in subnet 8 with value 3000::66,3000::77.
  Server is configured with pana-agent option in subnet 8 with value 3000::66,3000::77.
  Server is configured with new-posix-timezone option in subnet 8 with value EST5EDT4.
  Server is configured with new-tzdb-timezone option in subnet 8 with value Europe/Zurich.
  Server is configured with bootfile-url option in subnet 8 with value http://www.kea.isc.org.
  Server is configured with bootfile-param option in subnet 8 with value 000B48656C6C6F20776F726C640003666F6F.
  Server is configured with erp-local-domain-name option in subnet 8 with value erp-domain.isc.org.
  Server is configured with domain-search option in subnet 8 with value subnet.example.com.


  Server is configured with preference option in subnet 9 with value 123.
  Server is configured with sip-server-dns option in subnet 9 with value srv1.example.com,srv2.isc.org.
  Server is configured with dns-servers option in subnet 9 with value 2001:db8::1,2001:db8::2.
  Server is configured with domain-search option in subnet 9 with value domain1.example.com,domain2.isc.org.
  Server is configured with sip-server-addr option in subnet 9 with value 2001:db8::1,2001:db8::2.
  Server is configured with nisp-servers option in subnet 9 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-servers option in subnet 9 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-domain-name option in subnet 9 with value ntp.example.com.
  Server is configured with nisp-domain-name option in subnet 9 with value ntp.example.com.
  Server is configured with sntp-servers option in subnet 9 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with information-refresh-time option in subnet 9 with value 12345678.
  Server is configured with unicast option in subnet 9 with value 3000::66.
  Server is configured with bcmcs-server-dns option in subnet 9 with value very.good.domain.name.com.
  Server is configured with bcmcs-server-addr option in subnet 9 with value 3000::66,3000::77.
  Server is configured with pana-agent option in subnet 9 with value 3000::66,3000::77.
  Server is configured with new-posix-timezone option in subnet 9 with value EST5EDT4.
  Server is configured with new-tzdb-timezone option in subnet 9 with value Europe/Zurich.
  Server is configured with bootfile-url option in subnet 9 with value http://www.kea.isc.org.
  Server is configured with bootfile-param option in subnet 9 with value 000B48656C6C6F20776F726C640003666F6F.
  Server is configured with erp-local-domain-name option in subnet 9 with value erp-domain.isc.org.
  Server is configured with domain-search option in subnet 9 with value subnet.example.com.

  Server is configured with preference option in subnet 10 with value 123.
  Server is configured with sip-server-dns option in subnet 10 with value srv1.example.com,srv2.isc.org.
  Server is configured with dns-servers option in subnet 10 with value 2001:db8::1,2001:db8::2.
  Server is configured with domain-search option in subnet 10 with value domain1.example.com,domain2.isc.org.
  Server is configured with sip-server-addr option in subnet 10 with value 2001:db8::1,2001:db8::2.
  Server is configured with nisp-servers option in subnet 10 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-servers option in subnet 10 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-domain-name option in subnet 10 with value ntp.example.com.
  Server is configured with nisp-domain-name option in subnet 10 with value ntp.example.com.
  Server is configured with sntp-servers option in subnet 10 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with information-refresh-time option in subnet 10 with value 12345678.
  Server is configured with unicast option in subnet 10 with value 3000::66.
  Server is configured with bcmcs-server-dns option in subnet 10 with value very.good.domain.name.com.
  Server is configured with bcmcs-server-addr option in subnet 10 with value 3000::66,3000::77.
  Server is configured with pana-agent option in subnet 10 with value 3000::66,3000::77.
  Server is configured with new-posix-timezone option in subnet 10 with value EST5EDT4.
  Server is configured with new-tzdb-timezone option in subnet 10 with value Europe/Zurich.
  Server is configured with bootfile-url option in subnet 10 with value http://www.kea.isc.org.
  Server is configured with bootfile-param option in subnet 10 with value 000B48656C6C6F20776F726C640003666F6F.
  Server is configured with erp-local-domain-name option in subnet 10 with value erp-domain.isc.org.
  Server is configured with domain-search option in subnet 10 with value subnet.example.com.

  Server is configured with preference option in subnet 11 with value 123.
  Server is configured with sip-server-dns option in subnet 11 with value srv1.example.com,srv2.isc.org.
  Server is configured with dns-servers option in subnet 11 with value 2001:db8::1,2001:db8::2.
  Server is configured with domain-search option in subnet 11 with value domain1.example.com,domain2.isc.org.
  Server is configured with sip-server-addr option in subnet 11 with value 2001:db8::1,2001:db8::2.
  Server is configured with nisp-servers option in subnet 11 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-servers option in subnet 11 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-domain-name option in subnet 11 with value ntp.example.com.
  Server is configured with nisp-domain-name option in subnet 11 with value ntp.example.com.
  Server is configured with sntp-servers option in subnet 11 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with information-refresh-time option in subnet 11 with value 12345678.
  Server is configured with unicast option in subnet 11 with value 3000::66.
  Server is configured with bcmcs-server-dns option in subnet 11 with value very.good.domain.name.com.
  Server is configured with bcmcs-server-addr option in subnet 11 with value 3000::66,3000::77.
  Server is configured with pana-agent option in subnet 11 with value 3000::66,3000::77.
  Server is configured with new-posix-timezone option in subnet 11 with value EST5EDT4.
  Server is configured with new-tzdb-timezone option in subnet 11 with value Europe/Zurich.
  Server is configured with bootfile-url option in subnet 11 with value http://www.kea.isc.org.
  Server is configured with bootfile-param option in subnet 11 with value 000B48656C6C6F20776F726C640003666F6F.
  Server is configured with erp-local-domain-name option in subnet 11 with value erp-domain.isc.org.
  Server is configured with domain-search option in subnet 11 with value subnet.example.com.
  Server is configured with preference option in subnet 12 with value 123.
  Server is configured with sip-server-dns option in subnet 12 with value srv1.example.com,srv2.isc.org.
  Server is configured with dns-servers option in subnet 12 with value 2001:db8::1,2001:db8::2.
  Server is configured with domain-search option in subnet 12 with value domain1.example.com,domain2.isc.org.
  Server is configured with sip-server-addr option in subnet 12 with value 2001:db8::1,2001:db8::2.
  Server is configured with nisp-servers option in subnet 12 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-servers option in subnet 12 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-domain-name option in subnet 12 with value ntp.example.com.
  Server is configured with nisp-domain-name option in subnet 12 with value ntp.example.com.
  Server is configured with sntp-servers option in subnet 12 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with information-refresh-time option in subnet 12 with value 12345678.
  Server is configured with unicast option in subnet 12 with value 3000::66.
  Server is configured with bcmcs-server-dns option in subnet 12 with value very.good.domain.name.com.
  Server is configured with bcmcs-server-addr option in subnet 12 with value 3000::66,3000::77.
  Server is configured with pana-agent option in subnet 12 with value 3000::66,3000::77.
  Server is configured with new-posix-timezone option in subnet 12 with value EST5EDT4.
  Server is configured with new-tzdb-timezone option in subnet 12 with value Europe/Zurich.
  Server is configured with bootfile-url option in subnet 12 with value http://www.kea.isc.org.
  Server is configured with bootfile-param option in subnet 12 with value 000B48656C6C6F20776F726C640003666F6F.
  Server is configured with erp-local-domain-name option in subnet 12 with value erp-domain.isc.org.
  Server is configured with domain-search option in subnet 12 with value subnet.example.com.


  Server is configured with preference option in subnet 13 with value 123.
  Server is configured with sip-server-dns option in subnet 13 with value srv1.example.com,srv2.isc.org.
  Server is configured with dns-servers option in subnet 13 with value 2001:db8::1,2001:db8::2.
  Server is configured with domain-search option in subnet 13 with value domain1.example.com,domain2.isc.org.
  Server is configured with sip-server-addr option in subnet 13 with value 2001:db8::1,2001:db8::2.
  Server is configured with nisp-servers option in subnet 13 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-servers option in subnet 13 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-domain-name option in subnet 13 with value ntp.example.com.
  Server is configured with nisp-domain-name option in subnet 13 with value ntp.example.com.
  Server is configured with sntp-servers option in subnet 13 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with information-refresh-time option in subnet 13 with value 12345678.
  Server is configured with unicast option in subnet 13 with value 3000::66.
  Server is configured with bcmcs-server-dns option in subnet 13 with value very.good.domain.name.com.
  Server is configured with bcmcs-server-addr option in subnet 13 with value 3000::66,3000::77.
  Server is configured with pana-agent option in subnet 13 with value 3000::66,3000::77.
  Server is configured with new-posix-timezone option in subnet 13 with value EST5EDT4.
  Server is configured with new-tzdb-timezone option in subnet 13 with value Europe/Zurich.
  Server is configured with bootfile-url option in subnet 13 with value http://www.kea.isc.org.
  Server is configured with bootfile-param option in subnet 13 with value 000B48656C6C6F20776F726C640003666F6F.
  Server is configured with erp-local-domain-name option in subnet 13 with value erp-domain.isc.org.
  Server is configured with domain-search option in subnet 13 with value subnet.example.com.
  Server is configured with preference option in subnet 14 with value 123.
  Server is configured with sip-server-dns option in subnet 14 with value srv1.example.com,srv2.isc.org.
  Server is configured with dns-servers option in subnet 14 with value 2001:db8::1,2001:db8::2.
  Server is configured with domain-search option in subnet 14 with value domain1.example.com,domain2.isc.org.
  Server is configured with sip-server-addr option in subnet 14 with value 2001:db8::1,2001:db8::2.
  Server is configured with nisp-servers option in subnet 14 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-servers option in subnet 14 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-domain-name option in subnet 14 with value ntp.example.com.
  Server is configured with nisp-domain-name option in subnet 14 with value ntp.example.com.
  Server is configured with sntp-servers option in subnet 14 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with information-refresh-time option in subnet 14 with value 12345678.
  Server is configured with unicast option in subnet 14 with value 3000::66.
  Server is configured with bcmcs-server-dns option in subnet 14 with value very.good.domain.name.com.
  Server is configured with bcmcs-server-addr option in subnet 14 with value 3000::66,3000::77.
  Server is configured with pana-agent option in subnet 14 with value 3000::66,3000::77.
  Server is configured with new-posix-timezone option in subnet 14 with value EST5EDT4.
  Server is configured with new-tzdb-timezone option in subnet 14 with value Europe/Zurich.
  Server is configured with bootfile-url option in subnet 14 with value http://www.kea.isc.org.
  Server is configured with bootfile-param option in subnet 14 with value 000B48656C6C6F20776F726C640003666F6F.
  Server is configured with erp-local-domain-name option in subnet 14 with value erp-domain.isc.org.
  Server is configured with domain-search option in subnet 14 with value subnet.example.com.
  Server is configured with preference option in subnet 15 with value 123.
  Server is configured with sip-server-dns option in subnet 15 with value srv1.example.com,srv2.isc.org.
  Server is configured with dns-servers option in subnet 15 with value 2001:db8::1,2001:db8::2.
  Server is configured with domain-search option in subnet 15 with value domain1.example.com,domain2.isc.org.
  Server is configured with sip-server-addr option in subnet 15 with value 2001:db8::1,2001:db8::2.
  Server is configured with nisp-servers option in subnet 15 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-servers option in subnet 15 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-domain-name option in subnet 15 with value ntp.example.com.
  Server is configured with nisp-domain-name option in subnet 15 with value ntp.example.com.
  Server is configured with sntp-servers option in subnet 15 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with information-refresh-time option in subnet 15 with value 12345678.
  Server is configured with unicast option in subnet 15 with value 3000::66.
  Server is configured with bcmcs-server-dns option in subnet 15 with value very.good.domain.name.com.
  Server is configured with bcmcs-server-addr option in subnet 15 with value 3000::66,3000::77.
  Server is configured with pana-agent option in subnet 15 with value 3000::66,3000::77.
  Server is configured with new-posix-timezone option in subnet 15 with value EST5EDT4.
  Server is configured with new-tzdb-timezone option in subnet 15 with value Europe/Zurich.
  Server is configured with bootfile-url option in subnet 15 with value http://www.kea.isc.org.
  Server is configured with bootfile-param option in subnet 15 with value 000B48656C6C6F20776F726C640003666F6F.
  Server is configured with erp-local-domain-name option in subnet 15 with value erp-domain.isc.org.
  Server is configured with domain-search option in subnet 15 with value subnet.example.com.
  Server is configured with preference option in subnet 16 with value 123.
  Server is configured with sip-server-dns option in subnet 16 with value srv1.example.com,srv2.isc.org.
  Server is configured with dns-servers option in subnet 16 with value 2001:db8::1,2001:db8::2.
  Server is configured with domain-search option in subnet 16 with value domain1.example.com,domain2.isc.org.
  Server is configured with sip-server-addr option in subnet 16 with value 2001:db8::1,2001:db8::2.
  Server is configured with nisp-servers option in subnet 16 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-servers option in subnet 16 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-domain-name option in subnet 16 with value ntp.example.com.
  Server is configured with nisp-domain-name option in subnet 16 with value ntp.example.com.
  Server is configured with sntp-servers option in subnet 16 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with information-refresh-time option in subnet 16 with value 12345678.
  Server is configured with unicast option in subnet 16 with value 3000::66.
  Server is configured with bcmcs-server-dns option in subnet 16 with value very.good.domain.name.com.
  Server is configured with bcmcs-server-addr option in subnet 16 with value 3000::66,3000::77.
  Server is configured with pana-agent option in subnet 16 with value 3000::66,3000::77.
  Server is configured with new-posix-timezone option in subnet 16 with value EST5EDT4.
  Server is configured with new-tzdb-timezone option in subnet 16 with value Europe/Zurich.
  Server is configured with bootfile-url option in subnet 16 with value http://www.kea.isc.org.
  Server is configured with bootfile-param option in subnet 16 with value 000B48656C6C6F20776F726C640003666F6F.
  Server is configured with erp-local-domain-name option in subnet 16 with value erp-domain.isc.org.
  Server is configured with domain-search option in subnet 16 with value subnet.example.com.
  Server is configured with preference option in subnet 17 with value 123.
  Server is configured with sip-server-dns option in subnet 17 with value srv1.example.com,srv2.isc.org.
  Server is configured with dns-servers option in subnet 17 with value 2001:db8::1,2001:db8::2.
  Server is configured with domain-search option in subnet 17 with value domain1.example.com,domain2.isc.org.
  Server is configured with sip-server-addr option in subnet 17 with value 2001:db8::1,2001:db8::2.
  Server is configured with nisp-servers option in subnet 17 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-servers option in subnet 17 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-domain-name option in subnet 17 with value ntp.example.com.
  Server is configured with nisp-domain-name option in subnet 17 with value ntp.example.com.
  Server is configured with sntp-servers option in subnet 17 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with information-refresh-time option in subnet 17 with value 12345678.
  Server is configured with unicast option in subnet 17 with value 3000::66.
  Server is configured with bcmcs-server-dns option in subnet 17 with value very.good.domain.name.com.
  Server is configured with bcmcs-server-addr option in subnet 17 with value 3000::66,3000::77.
  Server is configured with pana-agent option in subnet 17 with value 3000::66,3000::77.
  Server is configured with new-posix-timezone option in subnet 17 with value EST5EDT4.
  Server is configured with new-tzdb-timezone option in subnet 17 with value Europe/Zurich.
  Server is configured with bootfile-url option in subnet 17 with value http://www.kea.isc.org.
  Server is configured with bootfile-param option in subnet 17 with value 000B48656C6C6F20776F726C640003666F6F.
  Server is configured with erp-local-domain-name option in subnet 17 with value erp-domain.isc.org.
  Server is configured with domain-search option in subnet 17 with value subnet.example.com.
  Server is configured with preference option in subnet 18 with value 123.
  Server is configured with sip-server-dns option in subnet 18 with value srv1.example.com,srv2.isc.org.
  Server is configured with dns-servers option in subnet 18 with value 2001:db8::1,2001:db8::2.
  Server is configured with domain-search option in subnet 18 with value domain1.example.com,domain2.isc.org.
  Server is configured with sip-server-addr option in subnet 18 with value 2001:db8::1,2001:db8::2.
  Server is configured with nisp-servers option in subnet 18 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-servers option in subnet 18 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-domain-name option in subnet 18 with value ntp.example.com.
  Server is configured with nisp-domain-name option in subnet 18 with value ntp.example.com.
  Server is configured with sntp-servers option in subnet 18 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with information-refresh-time option in subnet 18 with value 12345678.
  Server is configured with unicast option in subnet 18 with value 3000::66.
  Server is configured with bcmcs-server-dns option in subnet 18 with value very.good.domain.name.com.
  Server is configured with bcmcs-server-addr option in subnet 18 with value 3000::66,3000::77.
  Server is configured with pana-agent option in subnet 18 with value 3000::66,3000::77.
  Server is configured with new-posix-timezone option in subnet 18 with value EST5EDT4.
  Server is configured with new-tzdb-timezone option in subnet 18 with value Europe/Zurich.
  Server is configured with bootfile-url option in subnet 18 with value http://www.kea.isc.org.
  Server is configured with bootfile-param option in subnet 18 with value 000B48656C6C6F20776F726C640003666F6F.
  Server is configured with erp-local-domain-name option in subnet 18 with value erp-domain.isc.org.
  Server is configured with domain-search option in subnet 18 with value subnet.example.com.
  Server is configured with preference option in subnet 19 with value 123.
  Server is configured with sip-server-dns option in subnet 19 with value srv1.example.com,srv2.isc.org.
  Server is configured with dns-servers option in subnet 19 with value 2001:db8::1,2001:db8::2.
  Server is configured with domain-search option in subnet 19 with value domain1.example.com,domain2.isc.org.
  Server is configured with sip-server-addr option in subnet 19 with value 2001:db8::1,2001:db8::2.
  Server is configured with nisp-servers option in subnet 19 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-servers option in subnet 19 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-domain-name option in subnet 19 with value ntp.example.com.
  Server is configured with nisp-domain-name option in subnet 19 with value ntp.example.com.
  Server is configured with sntp-servers option in subnet 19 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with information-refresh-time option in subnet 19 with value 12345678.
  Server is configured with unicast option in subnet 19 with value 3000::66.
  Server is configured with bcmcs-server-dns option in subnet 19 with value very.good.domain.name.com.
  Server is configured with bcmcs-server-addr option in subnet 19 with value 3000::66,3000::77.
  Server is configured with pana-agent option in subnet 19 with value 3000::66,3000::77.
  Server is configured with new-posix-timezone option in subnet 19 with value EST5EDT4.
  Server is configured with new-tzdb-timezone option in subnet 19 with value Europe/Zurich.
  Server is configured with bootfile-url option in subnet 19 with value http://www.kea.isc.org.
  Server is configured with bootfile-param option in subnet 19 with value 000B48656C6C6F20776F726C640003666F6F.
  Server is configured with erp-local-domain-name option in subnet 19 with value erp-domain.isc.org.
  Server is configured with domain-search option in subnet 19 with value subnet.example.com.

  Server is configured with preference option in subnet 20 with value 123.
  Server is configured with sip-server-dns option in subnet 20 with value srv1.example.com,srv2.isc.org.
  Server is configured with dns-servers option in subnet 20 with value 2001:db8::1,2001:db8::2.
  Server is configured with domain-search option in subnet 20 with value domain1.example.com,domain2.isc.org.
  Server is configured with sip-server-addr option in subnet 20 with value 2001:db8::1,2001:db8::2.
  Server is configured with nisp-servers option in subnet 20 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-servers option in subnet 20 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-domain-name option in subnet 20 with value ntp.example.com.
  Server is configured with nisp-domain-name option in subnet 20 with value ntp.example.com.
  Server is configured with sntp-servers option in subnet 20 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with information-refresh-time option in subnet 20 with value 12345678.
  Server is configured with unicast option in subnet 20 with value 3000::66.
  Server is configured with bcmcs-server-dns option in subnet 20 with value very.good.domain.name.com.
  Server is configured with bcmcs-server-addr option in subnet 20 with value 3000::66,3000::77.
  Server is configured with pana-agent option in subnet 20 with value 3000::66,3000::77.
  Server is configured with new-posix-timezone option in subnet 20 with value EST5EDT4.
  Server is configured with new-tzdb-timezone option in subnet 20 with value Europe/Zurich.
  Server is configured with bootfile-url option in subnet 20 with value http://www.kea.isc.org.
  Server is configured with bootfile-param option in subnet 20 with value 000B48656C6C6F20776F726C640003666F6F.
  Server is configured with erp-local-domain-name option in subnet 20 with value erp-domain.isc.org.
  Server is configured with domain-search option in subnet 20 with value subnet.example.com.
  Server is configured with preference option in subnet 21 with value 123.
  Server is configured with sip-server-dns option in subnet 21 with value srv1.example.com,srv2.isc.org.
  Server is configured with dns-servers option in subnet 21 with value 2001:db8::1,2001:db8::2.
  Server is configured with domain-search option in subnet 21 with value domain1.example.com,domain2.isc.org.
  Server is configured with sip-server-addr option in subnet 21 with value 2001:db8::1,2001:db8::2.
  Server is configured with nisp-servers option in subnet 21 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-servers option in subnet 21 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-domain-name option in subnet 21 with value ntp.example.com.
  Server is configured with nisp-domain-name option in subnet 21 with value ntp.example.com.
  Server is configured with sntp-servers option in subnet 21 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with information-refresh-time option in subnet 21 with value 12345678.
  Server is configured with unicast option in subnet 21 with value 3000::66.
  Server is configured with bcmcs-server-dns option in subnet 21 with value very.good.domain.name.com.
  Server is configured with bcmcs-server-addr option in subnet 21 with value 3000::66,3000::77.
  Server is configured with pana-agent option in subnet 21 with value 3000::66,3000::77.
  Server is configured with new-posix-timezone option in subnet 21 with value EST5EDT4.
  Server is configured with new-tzdb-timezone option in subnet 21 with value Europe/Zurich.
  Server is configured with bootfile-url option in subnet 21 with value http://www.kea.isc.org.
  Server is configured with bootfile-param option in subnet 21 with value 000B48656C6C6F20776F726C640003666F6F.
  Server is configured with erp-local-domain-name option in subnet 21 with value erp-domain.isc.org.
  Server is configured with domain-search option in subnet 21 with value subnet.example.com.
  Server is configured with preference option in subnet 22 with value 123.
  Server is configured with sip-server-dns option in subnet 22 with value srv1.example.com,srv2.isc.org.
  Server is configured with dns-servers option in subnet 22 with value 2001:db8::1,2001:db8::2.
  Server is configured with domain-search option in subnet 22 with value domain1.example.com,domain2.isc.org.
  Server is configured with sip-server-addr option in subnet 22 with value 2001:db8::1,2001:db8::2.
  Server is configured with nisp-servers option in subnet 22 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-servers option in subnet 22 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-domain-name option in subnet 22 with value ntp.example.com.
  Server is configured with nisp-domain-name option in subnet 22 with value ntp.example.com.
  Server is configured with sntp-servers option in subnet 22 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with information-refresh-time option in subnet 22 with value 12345678.
  Server is configured with unicast option in subnet 22 with value 3000::66.
  Server is configured with bcmcs-server-dns option in subnet 22 with value very.good.domain.name.com.
  Server is configured with bcmcs-server-addr option in subnet 22 with value 3000::66,3000::77.
  Server is configured with pana-agent option in subnet 22 with value 3000::66,3000::77.
  Server is configured with new-posix-timezone option in subnet 22 with value EST5EDT4.
  Server is configured with new-tzdb-timezone option in subnet 22 with value Europe/Zurich.
  Server is configured with bootfile-url option in subnet 22 with value http://www.kea.isc.org.
  Server is configured with bootfile-param option in subnet 22 with value 000B48656C6C6F20776F726C640003666F6F.
  Server is configured with erp-local-domain-name option in subnet 22 with value erp-domain.isc.org.
  Server is configured with domain-search option in subnet 22 with value subnet.example.com.
  Server is configured with preference option in subnet 23 with value 123.
  Server is configured with sip-server-dns option in subnet 23 with value srv1.example.com,srv2.isc.org.
  Server is configured with dns-servers option in subnet 23 with value 2001:db8::1,2001:db8::2.
  Server is configured with domain-search option in subnet 23 with value domain1.example.com,domain2.isc.org.
  Server is configured with sip-server-addr option in subnet 23 with value 2001:db8::1,2001:db8::2.
  Server is configured with nisp-servers option in subnet 23 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-servers option in subnet 23 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-domain-name option in subnet 23 with value ntp.example.com.
  Server is configured with nisp-domain-name option in subnet 23 with value ntp.example.com.
  Server is configured with sntp-servers option in subnet 23 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with information-refresh-time option in subnet 23 with value 12345678.
  Server is configured with unicast option in subnet 23 with value 3000::66.
  Server is configured with bcmcs-server-dns option in subnet 23 with value very.good.domain.name.com.
  Server is configured with bcmcs-server-addr option in subnet 23 with value 3000::66,3000::77.
  Server is configured with pana-agent option in subnet 23 with value 3000::66,3000::77.
  Server is configured with new-posix-timezone option in subnet 23 with value EST5EDT4.
  Server is configured with new-tzdb-timezone option in subnet 23 with value Europe/Zurich.
  Server is configured with bootfile-url option in subnet 23 with value http://www.kea.isc.org.
  Server is configured with bootfile-param option in subnet 23 with value 000B48656C6C6F20776F726C640003666F6F.
  Server is configured with erp-local-domain-name option in subnet 23 with value erp-domain.isc.org.
  Server is configured with domain-search option in subnet 23 with value subnet.example.com.
  Server is configured with preference option in subnet 24 with value 123.
  Server is configured with sip-server-dns option in subnet 24 with value srv1.example.com,srv2.isc.org.
  Server is configured with dns-servers option in subnet 24 with value 2001:db8::1,2001:db8::2.
  Server is configured with domain-search option in subnet 24 with value domain1.example.com,domain2.isc.org.
  Server is configured with sip-server-addr option in subnet 24 with value 2001:db8::1,2001:db8::2.
  Server is configured with nisp-servers option in subnet 24 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-servers option in subnet 24 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with nis-domain-name option in subnet 24 with value ntp.example.com.
  Server is configured with nisp-domain-name option in subnet 24 with value ntp.example.com.
  Server is configured with sntp-servers option in subnet 24 with value 2001:db8::abc,3000::1,2000::1234.
  Server is configured with information-refresh-time option in subnet 24 with value 12345678.
  Server is configured with unicast option in subnet 24 with value 3000::66.
  Server is configured with bcmcs-server-dns option in subnet 24 with value very.good.domain.name.com.
  Server is configured with bcmcs-server-addr option in subnet 24 with value 3000::66,3000::77.
  Server is configured with pana-agent option in subnet 24 with value 3000::66,3000::77.
  Server is configured with new-posix-timezone option in subnet 24 with value EST5EDT4.
  Server is configured with new-tzdb-timezone option in subnet 24 with value Europe/Zurich.
  Server is configured with bootfile-url option in subnet 24 with value http://www.kea.isc.org.
  Server is configured with bootfile-param option in subnet 24 with value 000B48656C6C6F20776F726C640003666F6F.
  Server is configured with erp-local-domain-name option in subnet 24 with value erp-domain.isc.org.
  Server is configured with domain-search option in subnet 24 with value subnet.example.com.
  On space vendor-4491 server is configured with tftp-servers option with value 2001:558:ff18:16:10:253:175:76.
  On space vendor-4491 server is configured with config-file option with value normal_erouter_v6.cm.
  On space vendor-4491 server is configured with syslog-servers option with value 2001:558:ff18:10:10:253:124:101.
  On space vendor-4491 server is configured with time-servers option with value 2001:558:ff18:16:10:253:175:76.
  On space vendor-4491 server is configured with time-offset option with value -10000.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.



  Server logging system is configured with logger type kea-dhcp6.dhcp6, severity INFO, severity level None and log file kea.log.
  Server logging system is configured with logger type kea-dhcp6.dhcpsrv, severity INFO, severity level None and log file kea.log.
  Server logging system is configured with logger type kea-dhcp6.options, severity DEBUG, severity level 99 and log file kea.log.
  Server logging system is configured with logger type kea-dhcp6.packets, severity DEBUG, severity level 99 and log file kea.log.
  Server logging system is configured with logger type kea-dhcp6.leases, severity WARN, severity level None and log file kea.log.
  Server logging system is configured with logger type kea-dhcp6.alloc-engine, severity DEBUG, severity level 50 and log file kea.log.
  Server logging system is configured with logger type kea-dhcp6.bad-packets, severity DEBUG, severity level 25 and log file kea.log.
  Server logging system is configured with logger type kea-dhcp6.options, severity INFO, severity level None and log file kea.log.
  Generate server configuration file.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "config-set","arguments":  $(SERVER_CONFIG) }

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1:1::1.

  DHCP server is restarted.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::1.
