Feature: DDNS without TSIG
  This feature is testing DHCPv6 + DDNS in cooperation with DNS server BIND9 with TSIG authorisation. It's primary
  target is DDNS removing forward and reverse entries in time of releasing leases.

@v6 @ddns @tsig @forward_reverse_remove
Scenario: ddns6.tsig-sha1-forw_and_rev-release

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  DDNS server is configured on 127.0.0.1 address and 53001 port.
  DDNS server is configured with ddns-update-style option set to interim.
  #DDNS server is configured with generated-prefix option set to six.
  #DDNS server is configured with qualifying-suffix option set to example.com.
  Add forward DDNS with name six.example.com. and key forge.sha1.key on address 2001:db8:1::1000 and port 53.
  Add reverse DDNS with name 1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. and key forge.sha1.key on address 2001:db8:1::1000 and port 53.
  Add DDNS key named forge.sha1.key based on HMAC-SHA1 with secret value PN4xKZ/jDobCMlo4rpr70w==.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Use DNS set no. 3.
  DNS server is started.

  Test Procedure:
  Client for DNS Question Record uses address: sth6.six.example.com type AAAA class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
  Client saves into set no. 1 IA_NA option from received message.
  Client saves into set no. 1 server-id option from received message.
  Client adds saved options in set no. 1. And DONT Erase.
  Client sets FQDN_domain_name value to sth6.six.example.com..
  Client sets FQDN_flags value to S.
  Client does include fqdn.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  #Response MUST include option 39.
  #Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
  #Response option 39 MUST contain fqdn sth6.six.example.com.

  Test Procedure:
  Client for DNS Question Record uses address: sth6.six.example.com type AAAA class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include NOT empty ANSWER part.
  Received DNS part ANSWER MUST contain rdata with value 2001:db8:1::50.

  Test Procedure:
  Client for DNS Question Record uses address: 0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. type PTR class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include NOT empty ANSWER part.
  Received DNS part ANSWER MUST contain rdata with value sth6.six.example.com..
  Received DNS part ANSWER MUST contain rrname with value 0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa..

  Test Procedure:
  Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
  Client adds saved options in set no. 1. And DONT Erase.
  Client does include client-id.
  Client sends RELEASE message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.

  Test Procedure:
  Client for DNS Question Record uses address: sth6.six.example.com type AAAA class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client for DNS Question Record uses address: 0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. type PTR class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

@v6 @ddns @tsig @forward_reverse_remove
Scenario: ddns6.tsig-forw_and_rev-release-notenabled

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  DDNS server is configured on 127.0.0.1 address and 53001 port.
  DDNS server is configured with ddns-update-style option set to interim.
  #DDNS server is configured with generated-prefix option set to six.
  #DDNS server is configured with qualifying-suffix option set to example.com.
  Add forward DDNS with name six.example.com. and key forge.sha1.key on address 2001:db8:1::1000 and port 53.
  Add reverse DDNS with name 1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. and key forge.sha1.key on address 2001:db8:1::1000 and port 53.
  Add DDNS key named forge.sha1.key based on HMAC-SHA1 with secret value PN4xKZ/jDobCMlo4rpr70w==.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Use DNS set no. 3.
  DNS server is started.

  Test Procedure:
  Client for DNS Question Record uses address: sth6.six.example.com type AAAA class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
  Client saves into set no. 1 IA_NA option from received message.
  Client saves into set no. 1 server-id option from received message.
  Client adds saved options in set no. 1. And DONT Erase.
  Client sets FQDN_domain_name value to sth6.six.example.com..
  Client sets FQDN_flags value to S.
  Client does include fqdn.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  #Response MUST include option 39.
  #Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
  #Response option 39 MUST contain fqdn sth6.six.example.com.

  Test Procedure:
  Client for DNS Question Record uses address: sth6.six.example.com type AAAA class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include NOT empty ANSWER part.
  Received DNS part ANSWER MUST contain rdata with value 2001:db8:1::50.

  Test Procedure:
  Client for DNS Question Record uses address: 0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. type PTR class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include NOT empty ANSWER part.
  Received DNS part ANSWER MUST contain rdata with value sth6.six.example.com..
  Received DNS part ANSWER MUST contain rrname with value 0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa..

  Test Procedure:
  DHCP server is stopped.

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  DDNS server is configured on 127.0.0.1 address and 53001 port.
  #DDNS server is configured with ddns-update-style option set to off.
  #DDNS server is configured with generated-prefix option set to six.
  #DDNS server is configured with qualifying-suffix option set to example.com.
  Add forward DDNS with name six.example.com. and key forge.sha1.key on address 2001:db8:1::1000 and port 53.
  Add reverse DDNS with name 1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. and key forge.sha1.key on address 2001:db8:1::1000 and port 53.
  Add DDNS key named forge.sha1.key based on HMAC-SHA1 with secret value PN4xKZ/jDobCMlo4rpr70w==.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
  Client adds saved options in set no. 1. And DONT Erase.
  Client does include client-id.
  Client sends RELEASE message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.

  Test Procedure:
  Client for DNS Question Record uses address: sth6.six.example.com type AAAA class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include NOT empty ANSWER part.
  Received DNS part ANSWER MUST contain rdata with value 2001:db8:1::50.

  Test Procedure:
  Client for DNS Question Record uses address: 0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. type PTR class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include NOT empty ANSWER part.
  Received DNS part ANSWER MUST contain rdata with value sth6.six.example.com..
  Received DNS part ANSWER MUST contain rrname with value 0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa..

@v6 @ddns @tsig @reverse_remove
Scenario: ddns6.tsig-sha1-rev-release

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
  DDNS server is configured on 127.0.0.1 address and 53001 port.
  DDNS server is configured with ddns-update-style option set to interim.
  #DDNS server is configured with generated-prefix option set to six.
  #DDNS server is configured with qualifying-suffix option set to example.com.
  Add forward DDNS with name six.example.com. and key forge.sha1.key on address 2001:db8:1::1000 and port 53.
  Add reverse DDNS with name 1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. and key forge.sha1.key on address 2001:db8:1::1000 and port 53.
  Add DDNS key named forge.sha1.key based on HMAC-SHA1 with secret value PN4xKZ/jDobCMlo4rpr70w==.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Use DNS set no. 3.
  DNS server is started.

  Test Procedure:
  Client for DNS Question Record uses address: sth6.six.example.com type AAAA class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client for DNS Question Record uses address: 0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. type PTR class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
  Client saves into set no. 1 IA_NA option from received message.
  Client saves into set no. 1 server-id option from received message.
  Client adds saved options in set no. 1. And DONT Erase.
  Client sets FQDN_domain_name value to sth6.six.example.com..
  Client does include fqdn.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  #Response MUST include option 39.
  #Response option 39 MUST contain flags 0. #later make it 's' 'n' and 'o'
  #Response option 39 MUST contain fqdn sth6.six.example.com.

  Test Procedure:
  Client for DNS Question Record uses address: sth6.six.example.com type AAAA class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client for DNS Question Record uses address: 0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. type PTR class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include NOT empty ANSWER part.
  Received DNS part ANSWER MUST contain rdata with value sth6.six.example.com..
  Received DNS part ANSWER MUST contain rrname with value 0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa..

  Test Procedure:
  Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
  Client adds saved options in set no. 1. And DONT Erase.
  Client does include client-id.
  Client sends RELEASE message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.

  Test Procedure:
  Client for DNS Question Record uses address: sth6.six.example.com type AAAA class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

  Test Procedure:
  Client for DNS Question Record uses address: 0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. type PTR class IN.
  Client sends DNS query.

  Pass Criteria:
  DNS server MUST respond with DNS query.
  Received DNS query MUST include empty ANSWER part.

