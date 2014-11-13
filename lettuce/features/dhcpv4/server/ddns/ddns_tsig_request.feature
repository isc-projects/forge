Feature: DDNS without TSIG
    This feature is testing DHCPv6 + DDNS in cooperation with DNS server BIND9 without TSIG authorisation. It's primary
    target is DDNS forward and reverse update.

@v4 @ddns @tsig @forward_reverse_add
    Scenario: ddns4.tsig.sha1-forw_and_rev
    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    Add forward DDNS with name four.example.com. and key forge.sha1.key on address 192.168.50.252 and port 53.
    Add reverse DDNS with name 50.168.192.in-addr.arpa. and key forge.sha1.key on address 192.168.50.252 and port 53.
    Add DDNS key named forge.sha1.key based on HMAC-SHA1 with secret value PN4xKZ/jDobCMlo4rpr70w==.
    DHCP server is started.

    Use DNS set no. 21.
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
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.10.
    Client requests option 1.
    Client sets FQDN_domain_name value to aa.four.example.com..
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

@v4 @ddns @tsig @forward_reverse_add
    Scenario: ddns4.tsig.sha224-forw_and_rev

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    Add forward DDNS with name four.example.com. and key forge.sha224.key on address 192.168.50.252 and port 53.
    Add reverse DDNS with name 50.168.192.in-addr.arpa. and key forge.sha224.key on address 192.168.50.252 and port 53.
    Add DDNS key named forge.sha224.key based on HMAC-SHA224 with secret value TxAiO5TRKkFyHSCa4erQZQ==.
    DHCP server is started.

    Use DNS set no. 22.
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
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.10.
    Client requests option 1.
    Client sets FQDN_domain_name value to aa.four.example.com..
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

@v4 @ddns @tsig @forward_reverse_add
    Scenario: ddns4.tsig.sha256-forw_and_rev

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    Add forward DDNS with name four.example.com. and key forge.sha256.key on address 192.168.50.252 and port 53.
    Add reverse DDNS with name 50.168.192.in-addr.arpa. and key forge.sha256.key on address 192.168.50.252 and port 53.
    Add DDNS key named forge.sha256.key based on HMAC-SHA256 with secret value 5AYMijv0rhZJyQqK/caV7g==.
    DHCP server is started.

    Use DNS set no. 23.
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
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.10.
    Client requests option 1.
    Client sets FQDN_domain_name value to aa.four.example.com..
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

@v4 @ddns @tsig @forward_reverse_add
    Scenario: ddns4.tsig.sha384-forw_and_rev

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    Add forward DDNS with name four.example.com. and key forge.sha384.key on address 192.168.50.252 and port 53.
    Add reverse DDNS with name 50.168.192.in-addr.arpa. and key forge.sha384.key on address 192.168.50.252 and port 53.
    Add DDNS key named forge.sha384.key based on HMAC-SHA384 with secret value 21upyvp7zcG0S2PB4+kuQQ==.
    DHCP server is started.

    Use DNS set no. 24.
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
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.10.
    Client requests option 1.
    Client sets FQDN_domain_name value to aa.four.example.com..
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

@v4 @ddns @tsig @forward_reverse_add
    Scenario: ddns4.tsig.sha512-forw_and_rev

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    Add forward DDNS with name four.example.com. and key forge.sha512.key on address 192.168.50.252 and port 53.
    Add reverse DDNS with name 50.168.192.in-addr.arpa. and key forge.sha512.key on address 192.168.50.252 and port 53.
    Add DDNS key named forge.sha512.key based on HMAC-SHA512 with secret value jBng5D6QL4f8cfLUUwE7OQ==.
    DHCP server is started.

    Use DNS set no. 25.
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
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.10.
    Client requests option 1.
    Client sets FQDN_domain_name value to aa.four.example.com..
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

@v4 @ddns @tsig @forward_reverse_add
    Scenario: ddns4.tsig.md5-forw_and_rev

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    Add forward DDNS with name four.example.com. and key forge.md5.key on address 192.168.50.252 and port 53.
    Add reverse DDNS with name 50.168.192.in-addr.arpa. and key forge.md5.key on address 192.168.50.252 and port 53.
    Add DDNS key named forge.md5.key based on HMAC-MD5 with secret value bX3Hs+fG/tThidQPuhK1mA==.
    DHCP server is started.

    Use DNS set no. 26.
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
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.10.
    Client requests option 1.
    Client sets FQDN_domain_name value to aa.four.example.com..
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

@v4 @ddns @tsig @forward_reverse_add
    Scenario: ddns4.tsig.multi-key-forw_and_rev

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    Add forward DDNS with name four.example.com. and key forge.md5.key on address 192.168.50.252 and port 53.
    Add reverse DDNS with name 50.168.192.in-addr.arpa. and key forge.sha512.key on address 192.168.50.252 and port 53.
    Add DDNS key named forge.sha512.key based on HMAC-SHA512 with secret value jBng5D6QL4f8cfLUUwE7OQ==.
    Add DDNS key named forge.md5.key based on HMAC-MD5 with secret value bX3Hs+fG/tThidQPuhK1mA==.
    DHCP server is started.

    Use DNS set no. 27.
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
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.10.
    Client requests option 1.
    Client sets FQDN_domain_name value to aa.four.example.com..
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
