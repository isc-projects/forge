Feature: DDNS without TSIG
    This feature is testing DHCPv6 + DDNS in cooperation with DNS server BIND9 without TSIG authorisation. It's primary
    target is DDNS forward and reverse update.

@v6 @ddns @tsig @forward_reverse_add
    Scenario: ddns6.tsig.sha1-forw_and_rev
    Test Setup:
    Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    DDNS server is configured with generated-prefix option set to six.
    DDNS server is configured with qualifying-suffix option set to example.com.
    Add forward DDNS with name six.example.com. and key forge.sha1.key on address 2001:db8:1::1000 and port 53.
    Add reverse DDNS with name 1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. and key forge.sha1.key on address 2001:db8:1::1000 and port 53.
    Add DDNS key named forge.sha1.key based on HMAC-SHA1 with secret value PN4xKZ/jDobCMlo4rpr70w==.
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
    Client copies IA_NA option from received message.
    Client copies server-id option from received message.
    Client sets FQDN_domain_name value to sth6.six.example.com..
    Client sets FQDN_flags value to S.
    Client does include fqdn.
    Client does include client-id.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 1.
    Response MUST include option 2.
    Response MUST include option 39.
    Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    Response option 39 MUST contain fqdn sth6.six.example.com.

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

@v6 @ddns @tsig @forward_reverse_add
    Scenario: ddns6.tsig.sha224-forw_and_rev

    Test Setup:
    Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    DDNS server is configured with generated-prefix option set to six.
    DDNS server is configured with qualifying-suffix option set to example.com.
    Add forward DDNS with name six.example.com. and key forge.sha224.key on address 2001:db8:1::1000 and port 53.
    Add reverse DDNS with name 1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. and key forge.sha224.key on address 2001:db8:1::1000 and port 53.
    Add DDNS key named forge.sha224.key based on HMAC-SHA224 with secret value TxAiO5TRKkFyHSCa4erQZQ==.
    DHCP server is started.

    Use DNS set no. 4.
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
    Client copies IA_NA option from received message.
    Client copies server-id option from received message.
    Client sets FQDN_domain_name value to sth6.six.example.com..
    Client sets FQDN_flags value to S.
    Client does include fqdn.
    Client does include client-id.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 1.
    Response MUST include option 2.
    Response MUST include option 39.
    Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    Response option 39 MUST contain fqdn sth6.six.example.com.

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

@v6 @ddns @tsig @forward_reverse_add
    Scenario: ddns6.tsig.sha256-forw_and_rev

    Test Setup:
    Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    DDNS server is configured with generated-prefix option set to six.
    DDNS server is configured with qualifying-suffix option set to example.com.
    Add forward DDNS with name six.example.com. and key forge.sha256.key on address 2001:db8:1::1000 and port 53.
    Add reverse DDNS with name 1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. and key forge.sha256.key on address 2001:db8:1::1000 and port 53.
    Add DDNS key named forge.sha256.key based on HMAC-SHA256 with secret value 5AYMijv0rhZJyQqK/caV7g==.
    DHCP server is started.

    Use DNS set no. 5.
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
    Client copies IA_NA option from received message.
    Client copies server-id option from received message.
    Client sets FQDN_domain_name value to sth6.six.example.com..
    Client sets FQDN_flags value to S.
    Client does include fqdn.
    Client does include client-id.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 1.
    Response MUST include option 2.
    Response MUST include option 39.
    Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    Response option 39 MUST contain fqdn sth6.six.example.com.

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

@v6 @ddns @tsig @forward_reverse_add
    Scenario: ddns6.tsig.sha384-forw_and_rev

    Test Setup:
    Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    DDNS server is configured with generated-prefix option set to six.
    DDNS server is configured with qualifying-suffix option set to example.com.
    Add forward DDNS with name six.example.com. and key forge.sha384.key on address 2001:db8:1::1000 and port 53.
    Add reverse DDNS with name 1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. and key forge.sha384.key on address 2001:db8:1::1000 and port 53.
    Add DDNS key named forge.sha384.key based on HMAC-SHA384 with secret value 21upyvp7zcG0S2PB4+kuQQ==.
    DHCP server is started.

    Use DNS set no. 6.
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
    Client copies IA_NA option from received message.
    Client copies server-id option from received message.
    Client sets FQDN_domain_name value to sth6.six.example.com..
    Client sets FQDN_flags value to S.
    Client does include fqdn.
    Client does include client-id.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 1.
    Response MUST include option 2.
    Response MUST include option 39.
    Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    Response option 39 MUST contain fqdn sth6.six.example.com.

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

@v6 @ddns @tsig @forward_reverse_add
    Scenario: ddns6.tsig.sha512-forw_and_rev

    Test Setup:
    Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    DDNS server is configured with generated-prefix option set to six.
    DDNS server is configured with qualifying-suffix option set to example.com.
    Add forward DDNS with name six.example.com. and key forge.sha512.key on address 2001:db8:1::1000 and port 53.
    Add reverse DDNS with name 1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. and key forge.sha512.key on address 2001:db8:1::1000 and port 53.
    Add DDNS key named forge.sha512.key based on HMAC-SHA512 with secret value jBng5D6QL4f8cfLUUwE7OQ==.
    DHCP server is started.

    Use DNS set no. 7.
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
    Client copies IA_NA option from received message.
    Client copies server-id option from received message.
    Client sets FQDN_domain_name value to sth6.six.example.com..
    Client sets FQDN_flags value to S.
    Client does include fqdn.
    Client does include client-id.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 1.
    Response MUST include option 2.
    Response MUST include option 39.
    Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    Response option 39 MUST contain fqdn sth6.six.example.com.

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

@v6 @ddns @tsig @forward_reverse_add
    Scenario: ddns6.tsig.md5-forw_and_rev

    Test Setup:
    Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    DDNS server is configured with generated-prefix option set to six.
    DDNS server is configured with qualifying-suffix option set to example.com.
    Add forward DDNS with name six.example.com. and key forge.md5.key on address 2001:db8:1::1000 and port 53.
    Add reverse DDNS with name 1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. and key forge.md5.key on address 2001:db8:1::1000 and port 53.
    Add DDNS key named forge.md5.key based on HMAC-MD5 with secret value bX3Hs+fG/tThidQPuhK1mA==.
    DHCP server is started.

    Use DNS set no. 8.
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
    Client copies IA_NA option from received message.
    Client copies server-id option from received message.
    Client sets FQDN_domain_name value to sth6.six.example.com..
    Client sets FQDN_flags value to S.
    Client does include fqdn.
    Client does include client-id.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 1.
    Response MUST include option 2.
    Response MUST include option 39.
    Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    Response option 39 MUST contain fqdn sth6.six.example.com.

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

@v6 @ddns @tsig @forward_reverse_add
    Scenario: ddns6.tsig.multi-key-forw_and_rev

    Test Setup:
    Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    DDNS server is configured with generated-prefix option set to six.
    DDNS server is configured with qualifying-suffix option set to example.com.
    Add forward DDNS with name six.example.com. and key forge.md5.key on address 2001:db8:1::1000 and port 53.
    Add reverse DDNS with name 1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. and key forge.sha512.key on address 2001:db8:1::1000 and port 53.
    Add DDNS key named forge.sha512.key based on HMAC-SHA512 with secret value jBng5D6QL4f8cfLUUwE7OQ==.
    Add DDNS key named forge.md5.key based on HMAC-MD5 with secret value bX3Hs+fG/tThidQPuhK1mA==.
    DHCP server is started.

    Use DNS set no. 9.
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
    Client copies IA_NA option from received message.
    Client copies server-id option from received message.
    Client sets FQDN_domain_name value to sth6.six.example.com..
    Client sets FQDN_flags value to S.
    Client does include fqdn.
    Client does include client-id.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 1.
    Response MUST include option 2.
    Response MUST include option 39.
    Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    Response option 39 MUST contain fqdn sth6.six.example.com.

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
