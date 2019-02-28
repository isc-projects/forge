Feature: DDNS without TSIG
  This feature is testing DHCPv4 + DDNS in cooperation with DNS server BIND9 without TSIG authorisation. It's primary
  target is DDNS removing forward and reverse entries in time of releasing leases.

@v4 @ddns @notsig @forward_reverse_remove @hostname_sanitization
Scenario: ddns4.notsig-forw-and-rev-release-hostname-sanitization-replace-1

  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
  DDNS server is configured on 127.0.0.1 address and 53001 port.
  DDNS server is configured with enable-updates option set to true.
  DDNS server is configured with qualifying-suffix option set to example.com.
  DDNS server is configured with hostname-char-set option set to [^A-Za-z0-9.-].
  DDNS server is configured with hostname-char-replacement option set to x.
  Add forward DDNS with name four.example.com. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Add reverse DDNS with name 50.168.192.in-addr.arpa. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Use DNS set no. 20.
  DNS server is started.

  Test Procedure:
  Client for DNS Question Record uses address: xaax.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.10.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client saves into set no. 1 server_id option from received message.
  Client adds saved options in set no. 1. And DONT Erase.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client requests option 1.
  Client adds to the message hostname with value *aa$(WHITE_SPACE).four.example.com.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 12.
  Response option 12 MUST contain value xaax.four.example.com.

  Test Procedure:
  Client saves server_id option from received message.
  Client for DNS Question Record uses address: xaax.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include NOT empty ANSWER part.
  Received DNS part ANSWER MUST contain rdata with value 192.168.50.10.
  Received DNS part ANSWER MUST contain rrname with value xaax.four.example.com..

  Test Procedure:
  Client for DNS Question Record uses address: 10.50.168.192.in-addr.arpa. type PTR class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include NOT empty ANSWER part.
  Received DNS part ANSWER MUST contain rdata with value xaax.four.example.com..
  Received DNS part ANSWER MUST contain rrname with value 10.50.168.192.in-addr.arpa..

  Test Procedure:
  Client adds saved options in set no. 1. And DONT Erase.
  Client sets ciaddr value to 192.168.50.10.
  Client adds to the message hostname with value *aa$(WHITE_SPACE).four.example.com.
  Client sends RELEASE message.

  Pass Criteria:
  Server MUST NOT respond.

  Test Procedure:
  Client for DNS Question Record uses address: xaax.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client for DNS Question Record uses address: 10.50.168.192.in-addr.arpa. type PTR class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

@v4 @ddns @notsig @forward_reverse_remove @hostname_sanitization
Scenario: ddns4.notsig-forw-and-rev-release-fqdn-sanitization-replace-1

  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
  DDNS server is configured on 127.0.0.1 address and 53001 port.
  DDNS server is configured with enable-updates option set to true.
  DDNS server is configured with qualifying-suffix option set to example.com.
  DDNS server is configured with hostname-char-set option set to [^A-Za-z0-9.-].
  DDNS server is configured with hostname-char-replacement option set to x.
  Add forward DDNS with name four.example.com. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Add reverse DDNS with name 50.168.192.in-addr.arpa. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Use DNS set no. 20.
  DNS server is started.

  Test Procedure:
  Client for DNS Question Record uses address: xaax.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.10.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client saves into set no. 1 server_id option from received message.
  Client adds saved options in set no. 1. And DONT Erase.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client sets FQDN_domain_name value to *aa$(WHITE_SPACE).four.example.com..
  Client sets FQDN_flags value to S.
  Client does include fqdn.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 81.
  Response option 81 MUST contain flags 1. #later make it 's' 'n' and 'o'
  Response option 81 MUST contain fqdn xaax.four.example.com..

  Test Procedure:
  Client saves server_id option from received message.
  Client for DNS Question Record uses address: xaax.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include NOT empty ANSWER part.
  Received DNS part ANSWER MUST contain rdata with value 192.168.50.10.
  Received DNS part ANSWER MUST contain rrname with value xaax.four.example.com..

  Test Procedure:
  Client for DNS Question Record uses address: 10.50.168.192.in-addr.arpa. type PTR class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include NOT empty ANSWER part.
  Received DNS part ANSWER MUST contain rdata with value xaax.four.example.com..
  Received DNS part ANSWER MUST contain rrname with value 10.50.168.192.in-addr.arpa..

  Test Procedure:
  Client adds saved options in set no. 1. And DONT Erase.
  Client sets ciaddr value to 192.168.50.10.
  Client sets FQDN_domain_name value to *aa$(WHITE_SPACE).four.example.com..
  Client sets FQDN_flags value to S.
  Client does include fqdn.
  Client sends RELEASE message.

  Pass Criteria:
  Server MUST NOT respond.

  Test Procedure:
  Client for DNS Question Record uses address: xaax.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client for DNS Question Record uses address: 10.50.168.192.in-addr.arpa. type PTR class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

@v4 @ddns @notsig @forward_reverse_remove @hostname_sanitization
Scenario: ddns4.notsig-forw-and-rev-release-hostname-sanitization-replace-2

  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
  DDNS server is configured on 127.0.0.1 address and 53001 port.
  DDNS server is configured with enable-updates option set to true.
  DDNS server is configured with qualifying-suffix option set to example.com.
  DDNS server is configured with hostname-char-set option set to [^A-Za-z].
  DDNS server is configured with hostname-char-replacement option set to x.
  Add forward DDNS with name four.example.com. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Add reverse DDNS with name 50.168.192.in-addr.arpa. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:11.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.10.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:11.
  Client saves into set no. 1 server_id option from received message.
  Client adds saved options in set no. 1. And DONT Erase.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client requests option 1.
  Client adds to the message hostname with value *a$(WHITE_SPACE).8723()+.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 12.
  Response option 12 MUST contain value xaxxxxxxxxx.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:11.
  Client adds saved options in set no. 1. And DONT Erase.
  Client sets ciaddr value to 192.168.50.10.
  Client adds to the message hostname with value *a$(WHITE_SPACE).8723()+.
  Client sends RELEASE message.

  Pass Criteria:
  Server MUST NOT respond.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:22.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.10.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @ddns @notsig @forward_reverse_remove @hostname_sanitization
Scenario: ddns4.notsig-forw-and-rev-release-fqdn-sanitization-replace-2

  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
  DDNS server is configured on 127.0.0.1 address and 53001 port.
  DDNS server is configured with enable-updates option set to true.
  DDNS server is configured with qualifying-suffix option set to example.com.
  DDNS server is configured with hostname-char-set option set to [^A-Za-z].
  DDNS server is configured with hostname-char-replacement option set to x.
  Add forward DDNS with name four.example.com. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Add reverse DDNS with name 50.168.192.in-addr.arpa. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:11.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.10.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:11.
  Client saves into set no. 1 server_id option from received message.
  Client adds saved options in set no. 1. And DONT Erase.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client sets FQDN_domain_name value to *a$(WHITE_SPACE).8723()+..
  Client sets FQDN_flags value to S.
  Client does include fqdn.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 81.
  Response option 81 MUST contain flags 1. #later make it 's' 'n' and 'o'
  Response option 81 MUST contain fqdn xax.xxxxxxx..

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:11.
  Client adds saved options in set no. 1. And DONT Erase.
  Client sets ciaddr value to 192.168.50.10.
  Client sets FQDN_domain_name value to *a$(WHITE_SPACE).8723()+..
  Client sets FQDN_flags value to S.
  Client does include fqdn.
  Client sends RELEASE message.

  Pass Criteria:
  Server MUST NOT respond.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:22.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.10.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @ddns @notsig @forward_reverse_remove @hostname_sanitization
Scenario: ddns4.notsig-forw-and-rev-release-hostname-sanitization-omit-1

  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
  DDNS server is configured on 127.0.0.1 address and 53001 port.
  DDNS server is configured with enable-updates option set to true.
  DDNS server is configured with qualifying-suffix option set to example.com.
  DDNS server is configured with hostname-char-set option set to [^A-Za-z0-9.-].
  DDNS server is configured with hostname-char-replacement option set to $(EMPTY).
  Add forward DDNS with name four.example.com. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Add reverse DDNS with name 50.168.192.in-addr.arpa. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Use DNS set no. 20.
  DNS server is started.

  Test Procedure:
  Client for DNS Question Record uses address: aa.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.10.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client saves into set no. 1 server_id option from received message.
  Client adds saved options in set no. 1. And DONT Erase.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client requests option 1.
  Client adds to the message hostname with value $(WHITE_SPACE)*aa*.fo^ur.exa(mple.c)om.$(WHITE_SPACE).
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 12.
  Response option 12 MUST contain value aa.four.example.com..

  Test Procedure:
  Client saves server_id option from received message.
  Client for DNS Question Record uses address: aa.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include NOT empty ANSWER part.
  Received DNS part ANSWER MUST contain rdata with value 192.168.50.10.
  Received DNS part ANSWER MUST contain rrname with value aa.four.example.com..

  Test Procedure:
  Client for DNS Question Record uses address: 10.50.168.192.in-addr.arpa. type PTR class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include NOT empty ANSWER part.
  Received DNS part ANSWER MUST contain rdata with value aa.four.example.com..
  Received DNS part ANSWER MUST contain rrname with value 10.50.168.192.in-addr.arpa..

  Test Procedure:
  Client adds saved options in set no. 1. And DONT Erase.
  Client sets ciaddr value to 192.168.50.10.
  Client adds to the message hostname with value $(WHITE_SPACE)*aa*.fo^ur.exa(mple.c)om$(WHITE_SPACE).
  Client sends RELEASE message.

  Pass Criteria:
  Server MUST NOT respond.

  Test Procedure:
  Client for DNS Question Record uses address: aa.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client for DNS Question Record uses address: 10.50.168.192.in-addr.arpa. type PTR class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

@v4 @ddns @notsig @forward_reverse_remove @hostname_sanitization
Scenario: ddns4.notsig-forw-and-rev-release-fqdn-sanitization-omit-1

  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
  DDNS server is configured on 127.0.0.1 address and 53001 port.
  DDNS server is configured with enable-updates option set to true.
  DDNS server is configured with qualifying-suffix option set to example.com.
  DDNS server is configured with hostname-char-set option set to [^A-Za-z0-9.-].
  DDNS server is configured with hostname-char-replacement option set to $(EMPTY).
  Add forward DDNS with name four.example.com. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Add reverse DDNS with name 50.168.192.in-addr.arpa. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Use DNS set no. 20.
  DNS server is started.

  Test Procedure:
  Client for DNS Question Record uses address: aa.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.10.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client saves into set no. 1 server_id option from received message.
  Client adds saved options in set no. 1. And DONT Erase.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client sets FQDN_domain_name value to $(WHITE_SPACE)*aa*.fo^ur.exa(mple.c)om.^.
#  Client sets FQDN_domain_name value to aa.four.example.com.
  Client sets FQDN_flags value to S.
  Client does include fqdn.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 81.
  Response option 81 MUST contain flags 1. #later make it 's' 'n' and 'o'
  Response option 81 MUST contain fqdn aa.four.example.com..

  Test Procedure:
  Client saves server_id option from received message.
  Client for DNS Question Record uses address: aa.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include NOT empty ANSWER part.
  Received DNS part ANSWER MUST contain rdata with value 192.168.50.10.
  Received DNS part ANSWER MUST contain rrname with value aa.four.example.com..

  Test Procedure:
  Client for DNS Question Record uses address: 10.50.168.192.in-addr.arpa. type PTR class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include NOT empty ANSWER part.
  Received DNS part ANSWER MUST contain rdata with value aa.four.example.com..
  Received DNS part ANSWER MUST contain rrname with value 10.50.168.192.in-addr.arpa..

  Test Procedure:
  Client adds saved options in set no. 1. And DONT Erase.
  Client sets ciaddr value to 192.168.50.10.
  Client sets FQDN_domain_name value to $(WHITE_SPACE)*aa*.fo^ur.exa(mple.c)om..
  Client sets FQDN_flags value to S.
  Client does include fqdn.
  Client sends RELEASE message.

  Pass Criteria:
  Server MUST NOT respond.

  Test Procedure:
  Client for DNS Question Record uses address: aa.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client for DNS Question Record uses address: 10.50.168.192.in-addr.arpa. type PTR class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client for DNS Question Record uses address: aa.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client for DNS Question Record uses address: 10.50.168.192.in-addr.arpa. type PTR class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

@v4 @ddns @notsig @forward_reverse_remove @hostname_sanitization
Scenario: ddns4.notsig-forw-and-rev-release-hostname-sanitization-omit-identical-name
  # Two clients are using different hostnames which after sanitization end up being identical
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.11 pool.
  DDNS server is configured on 127.0.0.1 address and 53001 port.
  DDNS server is configured with enable-updates option set to true.
  DDNS server is configured with qualifying-suffix option set to example.com.
  DDNS server is configured with hostname-char-set option set to [^A-Za-z.-].
  DDNS server is configured with hostname-char-replacement option set to $(EMPTY).
  Add forward DDNS with name four.example.com. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Add reverse DDNS with name 50.168.192.in-addr.arpa. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Use DNS set no. 20.
  DNS server is started.

  Test Procedure:
  Client for DNS Question Record uses address: client.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client for DNS Question Record uses address: client1.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client for DNS Question Record uses address: client2.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:11.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.10.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:11.
  Client saves into set no. 1 server_id option from received message.
  Client adds saved options in set no. 1. And DONT Erase.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client requests option 1.
  Client adds to the message hostname with value client1.four.example.com.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 12.
  Response option 12 MUST contain value client.four.example.com.

  Test Procedure:
  Client saves server_id option from received message.
  Client for DNS Question Record uses address: client.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include NOT empty ANSWER part.
  Received DNS part ANSWER MUST contain rdata with value 192.168.50.10.
  Received DNS part ANSWER MUST contain rrname with value client.four.example.com..

  Test Procedure:
  Client for DNS Question Record uses address: 10.50.168.192.in-addr.arpa. type PTR class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include NOT empty ANSWER part.
  Received DNS part ANSWER MUST contain rdata with value client.four.example.com..
  Received DNS part ANSWER MUST contain rrname with value 10.50.168.192.in-addr.arpa..

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:22.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.11.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:22.
  Client saves into set no. 1 server_id option from received message.
  Client adds saved options in set no. 1. And DONT Erase.
  Client adds to the message requested_addr with value 192.168.50.11.
  Client requests option 1.
  Client adds to the message hostname with value client2.four.example.com.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.11.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 12.
  Response option 12 MUST contain value client.four.example.com.

  Test Procedure:
  Client for DNS Question Record uses address: client1.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client for DNS Question Record uses address: client2.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:11.
  Client adds saved options in set no. 1. And DONT Erase.
  Client sets ciaddr value to 192.168.50.10.
  Client adds to the message hostname with value client1.four.example.com.
  Client sends RELEASE message.

  Pass Criteria:
  Server MUST NOT respond.

  Test Procedure:
  Client for DNS Question Record uses address: client.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client for DNS Question Record uses address: 10.50.168.192.in-addr.arpa. type PTR class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

@v4 @ddns @notsig @forward_reverse_remove @hostname_sanitization
Scenario: ddns4.notsig-forw-and-rev-release-fqdn-sanitization-omit-identical-name
  # Two clients are using different hostnames which after sanitization end up being identical
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.11 pool.
  DDNS server is configured on 127.0.0.1 address and 53001 port.
  DDNS server is configured with enable-updates option set to true.
  DDNS server is configured with qualifying-suffix option set to example.com.
  DDNS server is configured with hostname-char-set option set to [^A-Za-z.-].
  DDNS server is configured with hostname-char-replacement option set to $(EMPTY).
  Add forward DDNS with name four.example.com. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Add reverse DDNS with name 50.168.192.in-addr.arpa. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Use DNS set no. 20.
  DNS server is started.

  Test Procedure:
  Client for DNS Question Record uses address: client.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client for DNS Question Record uses address: client1.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client for DNS Question Record uses address: client2.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:11.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.10.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:11.
  Client saves into set no. 1 server_id option from received message.
  Client adds saved options in set no. 1. And DONT Erase.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client sets FQDN_domain_name value to client1.four.example.com..
  Client sets FQDN_flags value to S.
  Client does include fqdn.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 81.
  Response option 81 MUST contain flags 1. #later make it 's' 'n' and 'o'
  Response option 81 MUST contain fqdn client.four.example.com..

  Test Procedure:
  Client saves server_id option from received message.
  Client for DNS Question Record uses address: client.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include NOT empty ANSWER part.
  Received DNS part ANSWER MUST contain rdata with value 192.168.50.10.
  Received DNS part ANSWER MUST contain rrname with value client.four.example.com..

  Test Procedure:
  Client for DNS Question Record uses address: 10.50.168.192.in-addr.arpa. type PTR class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include NOT empty ANSWER part.
  Received DNS part ANSWER MUST contain rdata with value client.four.example.com..
  Received DNS part ANSWER MUST contain rrname with value 10.50.168.192.in-addr.arpa..

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:22.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.11.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:22.
  Client saves into set no. 1 server_id option from received message.
  Client adds saved options in set no. 1. And DONT Erase.
  Client adds to the message requested_addr with value 192.168.50.11.
  Client sets FQDN_domain_name value to client2.four.example.com..
  Client sets FQDN_flags value to S.
  Client does include fqdn.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.11.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 81.
  Response option 81 MUST contain flags 1. #later make it 's' 'n' and 'o'
  Response option 81 MUST contain fqdn client.four.example.com..

  Test Procedure:
  Client for DNS Question Record uses address: client1.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client for DNS Question Record uses address: client2.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:11.
  Client adds saved options in set no. 1. And DONT Erase.
  Client sets ciaddr value to 192.168.50.10.
  Client sets FQDN_domain_name value to client1.four.example.com..
  Client sets FQDN_flags value to S.
  Client does include fqdn.
  Client sends RELEASE message.

  Pass Criteria:
  Server MUST NOT respond.

  Test Procedure:
  Client for DNS Question Record uses address: client.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client for DNS Question Record uses address: 10.50.168.192.in-addr.arpa. type PTR class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

@v4 @ddns @notsig @forward_reverse_remove @hostname_sanitization
Scenario: ddns4.notsig-forw-and-rev-release-hostname-sanitization-omit-2

  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
  DDNS server is configured on 127.0.0.1 address and 53001 port.
  DDNS server is configured with enable-updates option set to true.
  DDNS server is configured with qualifying-suffix option set to example.com.
  DDNS server is configured with hostname-char-set option set to [^A-Za-z].
  DDNS server is configured with hostname-char-replacement option set to $(EMPTY).
  Add forward DDNS with name four.example.com. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Add reverse DDNS with name 50.168.192.in-addr.arpa. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:11.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.10.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:11.
  Client saves into set no. 1 server_id option from received message.
  Client adds saved options in set no. 1. And DONT Erase.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client requests option 1.
  Client adds to the message hostname with value *a$(WHITE_SPACE).8723()+.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 12.
  Response option 12 MUST contain value a.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:11.
  Client adds saved options in set no. 1. And DONT Erase.
  Client sets ciaddr value to 192.168.50.10.
  Client adds to the message hostname with value *a$(WHITE_SPACE).8723()+.
  Client sends RELEASE message.

  Pass Criteria:
  Server MUST NOT respond.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:22.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.10.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @ddns @notsig @forward_reverse_remove @hostname_sanitization
Scenario: ddns4.notsig-forw-and-rev-release-fqdn-sanitization-omit-2

  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
  DDNS server is configured on 127.0.0.1 address and 53001 port.
  DDNS server is configured with enable-updates option set to true.
  DDNS server is configured with qualifying-suffix option set to example.com.
  DDNS server is configured with hostname-char-set option set to [^A-Za-z].
  DDNS server is configured with hostname-char-replacement option set to $(EMPTY).
  Add forward DDNS with name four.example.com. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Add reverse DDNS with name 50.168.192.in-addr.arpa. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:11.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.10.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:11.
  Client saves into set no. 1 server_id option from received message.
  Client adds saved options in set no. 1. And DONT Erase.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client sets FQDN_domain_name value to *a$(WHITE_SPACE).8723()+com.pl..
  Client sets FQDN_flags value to S.
  Client does include fqdn.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 81.
  Response option 81 MUST contain flags 1. #later make it 's' 'n' and 'o'
  Response option 81 MUST contain fqdn a.com.pl..

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:11.
  Client adds saved options in set no. 1. And DONT Erase.
  Client sets ciaddr value to 192.168.50.10.
  Client sets FQDN_domain_name value to *a$(WHITE_SPACE).8723()+..
  Client sets FQDN_flags value to S.
  Client does include fqdn.
  Client sends RELEASE message.

  Pass Criteria:
  Server MUST NOT respond.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:22.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.10.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @ddns @notsig @forward_reverse_remove @hostname_sanitization
Scenario: ddns4.notsig-forw-and-rev-release-hostname-sanitization-omit-3

  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
  DDNS server is configured on 127.0.0.1 address and 53001 port.
  DDNS server is configured with enable-updates option set to true.
  DDNS server is configured with qualifying-suffix option set to example.com.
  DDNS server is configured with hostname-char-set option set to [^A-Za-z].
  DDNS server is configured with hostname-char-replacement option set to $(EMPTY).
  Add forward DDNS with name four.example.com. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Add reverse DDNS with name 50.168.192.in-addr.arpa. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:11.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.10.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:11.
  Client saves into set no. 1 server_id option from received message.
  Client adds saved options in set no. 1. And DONT Erase.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client requests option 1.
  Client adds to the message hostname with value *$(WHITE_SPACE).8723()+.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST NOT include option 12.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:11.
  Client adds saved options in set no. 1. And DONT Erase.
  Client sets ciaddr value to 192.168.50.10.
  Client adds to the message hostname with value *$(WHITE_SPACE).8723()+.
  Client sends RELEASE message.

  Pass Criteria:
  Server MUST NOT respond.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:22.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.10.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @ddns @notsig @forward_reverse_remove @hostname_sanitization
Scenario: ddns4.notsig-forw-and-rev-release-hostname-sanitization-omit-3

  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
  DDNS server is configured on 127.0.0.1 address and 53001 port.
  DDNS server is configured with enable-updates option set to true.
  DDNS server is configured with qualifying-suffix option set to example.com.
  DDNS server is configured with hostname-char-set option set to [^A-Za-z].
  DDNS server is configured with hostname-char-replacement option set to $(EMPTY).
  Add forward DDNS with name four.example.com. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Add reverse DDNS with name 50.168.192.in-addr.arpa. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:11.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.10.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:11.
  Client saves into set no. 1 server_id option from received message.
  Client adds saved options in set no. 1. And DONT Erase.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client sets FQDN_domain_name value to *$(WHITE_SPACE).8723()+..
  Client sets FQDN_flags value to S.
  Client does include fqdn.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST NOT include option 12.
  Response MUST NOT include option 81.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:11.
  Client adds saved options in set no. 1. And DONT Erase.
  Client sets ciaddr value to 192.168.50.10.
  Client sets FQDN_domain_name value to *$(WHITE_SPACE).8723()+..
  Client sets FQDN_flags value to S.
  Client does include fqdn.
  Client sends RELEASE message.

  Pass Criteria:
  Server MUST NOT respond.

  Test Procedure:
  Client sets chaddr value to 00:1F:D0:00:00:22.
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.10.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @ddns @notsig @expire
Scenario: ddns4.notsig-expire-hostname-sanitization

  Test Setup:
  Time renew-timer is configured with value 3.
  Time rebind-timer is configured with value 4.
  Time valid-lifetime is configured with value 5.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
  DDNS server is configured on 127.0.0.1 address and 53001 port.
  DDNS server is configured with hostname-char-set option set to [^A-Za-z0-9.-].
  DDNS server is configured with hostname-char-replacement option set to x.
  DDNS server is configured with enable-updates option set to true.
  DDNS server is configured with generated-prefix option set to four.
  DDNS server is configured with qualifying-suffix option set to example.com.
  Add forward DDNS with name four.example.com. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Add reverse DDNS with name 50.168.192.in-addr.arpa. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Use DNS set no. 20.
  DNS server is started.

  Test Procedure:
  Client for DNS Question Record uses address: xaax.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client for DNS Question Record uses address: 10.50.168.192.in-addr.arpa. type PTR class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.10.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client adds to the message hostname with value ^aa$(WHITE_SPACE).four.example.com.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 12.
  Response option 12 MUST contain value xaax.four.example.com.

  Test Procedure:
  Client for DNS Question Record uses address: xaax.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include NOT empty ANSWER part.
  Received DNS part ANSWER MUST contain rdata with value 192.168.50.10.
  Received DNS part ANSWER MUST contain rrname with value xaax.four.example.com..

  Test Procedure:
  Client for DNS Question Record uses address: 10.50.168.192.in-addr.arpa. type PTR class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include NOT empty ANSWER part.
  Received DNS part ANSWER MUST contain rdata with value xaax.four.example.com..
  Received DNS part ANSWER MUST contain rrname with value 10.50.168.192.in-addr.arpa..

  Sleep for 10 seconds.

  Test Procedure:
  Client for DNS Question Record uses address: xaax.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client for DNS Question Record uses address: 10.50.168.192.in-addr.arpa. type PTR class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

@v4 @ddns @notsig @expire
Scenario: ddns4.notsig-expire-fqdn-sanitization

  Test Setup:
  Time renew-timer is configured with value 3.
  Time rebind-timer is configured with value 4.
  Time valid-lifetime is configured with value 5.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
  DDNS server is configured on 127.0.0.1 address and 53001 port.
  DDNS server is configured with hostname-char-set option set to [^A-Za-z0-9.-].
  DDNS server is configured with hostname-char-replacement option set to x.
  DDNS server is configured with enable-updates option set to true.
  DDNS server is configured with generated-prefix option set to four.
  DDNS server is configured with qualifying-suffix option set to example.com.
  Add forward DDNS with name four.example.com. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Add reverse DDNS with name 50.168.192.in-addr.arpa. and key EMPTY_KEY on address 192.168.50.252 and port 53.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Use DNS set no. 20.
  DNS server is started.

  Test Procedure:
  Client for DNS Question Record uses address: xaax.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client for DNS Question Record uses address: 10.50.168.192.in-addr.arpa. type PTR class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.10.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client sets FQDN_domain_name value to ^aa$(WHITE_SPACE).four.example.com..
  Client sets FQDN_flags value to S.
  Client does include fqdn.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.10.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 81.
  Response option 81 MUST contain flags 1. #later make it 's' 'n' and 'o'
  Response option 81 MUST contain fqdn xaax.four.example.com..

  Test Procedure:
  Client for DNS Question Record uses address: xaax.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include NOT empty ANSWER part.
  Received DNS part ANSWER MUST contain rdata with value 192.168.50.10.
  Received DNS part ANSWER MUST contain rrname with value xaax.four.example.com..

  Test Procedure:
  Client for DNS Question Record uses address: 10.50.168.192.in-addr.arpa. type PTR class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include NOT empty ANSWER part.
  Received DNS part ANSWER MUST contain rdata with value xaax.four.example.com..
  Received DNS part ANSWER MUST contain rrname with value 10.50.168.192.in-addr.arpa..

  Sleep for 10 seconds.

  Test Procedure:
  Client for DNS Question Record uses address: xaax.four.example.com type A class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client for DNS Question Record uses address: 10.50.168.192.in-addr.arpa. type PTR class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.
