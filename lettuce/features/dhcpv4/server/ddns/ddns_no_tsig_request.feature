Feature: DDNS without TSIG
    This feature is testing DHCPv4 + DDNS in cooperation with DNS server BIND9 without TSIG authorisation. It's primary
    target is DDNS forward and reverse update. Testing ASCII format in domain names.

@v4 @ddns @notsig @forward_reverse_add
    Scenario: ddns4.notsig.forw_and_rev.add-success-Sflag

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
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


@v4 @ddns @notsig @forward_reverse_add
    Scenario: ddns4.notsig.forw_and_rev.add-fail-Sflag

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
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
    Client sets FQDN_domain_name value to aa.four.exae.com..
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
    Response option 81 MUST contain fqdn aa.four.exae.com..

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


@v4 @ddns @notsig @forward_reverse_add
    Scenario: ddns4.notsig.forw_and_rev.notenabled-Sflag

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to false.
    DDNS server is configured with generated-prefix option set to four.
    DDNS server is configured with qualifying-suffix option set to example.com.
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
    #Response option 81 MUST contain flags 10. #later make it 's' 'n' and 'o' should be 10
    Response option 81 MUST contain fqdn aa.four.example.com..

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

@v4 @ddns @notsig @forward_update
    Scenario: ddns4.notsig.forw_and_rev.update-success-Sflag

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
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

    Test Setup:
    DHCP server is stopped.
    Clear leases.

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.11-192.168.50.11 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    DDNS server is configured with generated-prefix option set to four.
    DDNS server is configured with qualifying-suffix option set to example.com.
    Add forward DDNS with name four.example.com. and key EMPTY_KEY on address 192.168.50.252 and port 53.
    Add reverse DDNS with name 50.168.192.in-addr.arpa. and key EMPTY_KEY on address 192.168.50.252 and port 53.
    Send server configuration using SSH and config-file.
DHCP server is started.

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

    Test Procedure:
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.11.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.11.
    Client requests option 1.
    Client sets FQDN_domain_name value to aa.four.example.com..
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
    Response option 81 MUST contain fqdn aa.four.example.com..

    Test Procedure:
    Client for DNS Question Record uses address: aa.four.example.com type A class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include NOT empty ANSWER part.
    Received DNS part ANSWER MUST contain rdata with value 192.168.50.11.
    Received DNS part ANSWER MUST contain rrname with value aa.four.example.com..

    Test Procedure:
    Client for DNS Question Record uses address: 11.50.168.192.in-addr.arpa. type PTR class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include NOT empty ANSWER part.
    Received DNS part ANSWER MUST contain rdata with value aa.four.example.com..
    Received DNS part ANSWER MUST contain rrname with value 11.50.168.192.in-addr.arpa..

@v4 @ddns @notsig @forward_reverse_add
    Scenario: ddns4.notsig.forw_and_rev.two-dhci-Sflag

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.11 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
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
    Client sets chaddr value to 00:00:00:00:00:11.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.10.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:11.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.10.
    Client requests option 1.
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
    Response option 81 MUST contain fqdn client1.four.example.com..

    Test Procedure:
    Client for DNS Question Record uses address: client1.four.example.com type A class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include NOT empty ANSWER part.
    Received DNS part ANSWER MUST contain rdata with value 192.168.50.10.
    Received DNS part ANSWER MUST contain rrname with value client1.four.example.com..


    ## Client 2 add
    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:12.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.11.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:12.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.11.
    Client requests option 1.
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
    Response option 81 MUST contain fqdn client2.four.example.com..

    Test Procedure:
    Client for DNS Question Record uses address: client2.four.example.com type A class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include NOT empty ANSWER part.
    Received DNS part ANSWER MUST contain rdata with value 192.168.50.11.
    Received DNS part ANSWER MUST contain rrname with value client2.four.example.com..


@v4 @ddns @notsig @forward_reverse_add
    Scenario: ddns4.notsig.forw_and_rev.dhci-conflicts-Sflag

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.11 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
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
    Client for DNS Question Record uses address: client1.four.example.com type A class IN.
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
    Client for DNS Question Record uses address: client2.four.example.com type A class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include empty ANSWER part.

    Test Procedure:
    Client for DNS Question Record uses address: 11.50.168.192.in-addr.arpa. type PTR class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include empty ANSWER part.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:11.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.10.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:11.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.10.
    Client requests option 1.
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
    Response option 81 MUST contain fqdn client1.four.example.com..

    Test Procedure:
    Client for DNS Question Record uses address: client1.four.example.com type A class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include NOT empty ANSWER part.
    Received DNS part ANSWER MUST contain rdata with value 192.168.50.10.
    Received DNS part ANSWER MUST contain rrname with value client1.four.example.com..

    Test Procedure:
    Client for DNS Question Record uses address: 10.50.168.192.in-addr.arpa. type PTR class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include NOT empty ANSWER part.
    Received DNS part ANSWER MUST contain rdata with value client1.four.example.com..
    Received DNS part ANSWER MUST contain rrname with value 10.50.168.192.in-addr.arpa..

    ## Client 2 add
    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:12.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.11.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:12.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.11.
    Client requests option 1.
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
    Response option 81 MUST contain fqdn client2.four.example.com..

    Test Procedure:
    Client for DNS Question Record uses address: client2.four.example.com type A class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include NOT empty ANSWER part.
    Received DNS part ANSWER MUST contain rdata with value 192.168.50.11.
    Received DNS part ANSWER MUST contain rrname with value client2.four.example.com..

    Test Procedure:
    Client for DNS Question Record uses address: 11.50.168.192.in-addr.arpa. type PTR class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include NOT empty ANSWER part.
    Received DNS part ANSWER MUST contain rdata with value client2.four.example.com..
    Received DNS part ANSWER MUST contain rrname with value 11.50.168.192.in-addr.arpa..

    ## Client 2 try to update client's 1 domain
    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:12.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.11.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client sets chaddr value to 00:00:00:00:00:12.
    Client copies server_id option from received message.
    Client adds to the message requested_addr with value 192.168.50.11.
    Client requests option 1.
    Client sets FQDN_domain_name value to client1.four.example.com..
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
    Response option 81 MUST contain fqdn client1.four.example.com..

    ## address and domain name should not be changed!
    Test Procedure:
    Client for DNS Question Record uses address: client1.four.example.com type A class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include NOT empty ANSWER part.
    Received DNS part ANSWER MUST contain rdata with value 192.168.50.10.
    Received DNS part ANSWER MUST contain rrname with value client1.four.example.com..

    Test Procedure:
    Client for DNS Question Record uses address: 10.50.168.192.in-addr.arpa. type PTR class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include NOT empty ANSWER part.
    Received DNS part ANSWER MUST contain rdata with value client1.four.example.com..
    Received DNS part ANSWER MUST contain rrname with value 10.50.168.192.in-addr.arpa..

    Test Procedure:
    Client for DNS Question Record uses address: client2.four.example.com type A class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include empty ANSWER part.

    Test Procedure:
    Client for DNS Question Record uses address: 11.50.168.192.in-addr.arpa. type PTR class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include empty ANSWER part.


@v4 @ddns @notsig @forward_reverse_add
    Scenario: ddns4.notsig.forw_and_rev.add-success-withoutflag-override-client

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with override-client-update option set to true.
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
    Client does include fqdn.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.10.
	Response MUST include option 1.
    Response option 1 MUST contain value 255.255.255.0.
    Response MUST include option 81.
    Response option 81 MUST contain flags 3. #later make it 's' 'n' and 'o'
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


@v4 @ddns @notsig @reverse_add
    Scenario: ddns4.notsig.rev.success-withoutflag

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
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
    Client does include fqdn.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.10.
	Response MUST include option 1.
    Response option 1 MUST contain value 255.255.255.0.
    Response MUST include option 81.
    Response option 81 MUST contain flags 0. #later make it 's' 'n' and 'o'
    Response option 81 MUST contain fqdn aa.four.example.com..

    Test Procedure:
    Client for DNS Question Record uses address: 10.50.168.192.in-addr.arpa. type PTR class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include NOT empty ANSWER part.
    Received DNS part ANSWER MUST contain rdata with value aa.four.example.com..
    Received DNS part ANSWER MUST contain rrname with value 10.50.168.192.in-addr.arpa..

    Test Procedure:
    Client for DNS Question Record uses address: aa.four.example.com type A class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include empty ANSWER part.


@v4 @ddns @notsig @reverse_add
    Scenario: ddns4.notsig.rev.withoutflag-notenabled

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to false.
    DDNS server is configured with generated-prefix option set to four.
    DDNS server is configured with qualifying-suffix option set to example.com.
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
    Client requests option 1.
    Client sets FQDN_domain_name value to aa.four.example.com..
    Client does include fqdn.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.10.
	Response MUST include option 1.
    Response option 1 MUST contain value 255.255.255.0.
    Response MUST include option 81.
    #Response option 81 MUST contain flags 0. #later make it 's' 'n' and 'o' should be 10
    Response option 81 MUST contain fqdn aa.four.example.com..

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

@v4 @ddns @notsig @reverse_add
    Scenario: ddns4.notsig.rev.Nflag-override-no-update

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.10-192.168.50.10 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with override-no-update option set to true.
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
    Client sets FQDN_flags value to N.
    Client sets FQDN_domain_name value to aa.four.example.com..
    Client does include fqdn.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.10.
	Response MUST include option 1.
    Response option 1 MUST contain value 255.255.255.0.
    Response MUST include option 81.
    Response option 81 MUST contain flags 3. #later make it 's' 'n' and 'o'
    Response option 81 MUST contain fqdn aa.four.example.com..

    Test Procedure:
    Client for DNS Question Record uses address: 10.50.168.192.in-addr.arpa. type PTR class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include NOT empty ANSWER part.
    Received DNS part ANSWER MUST contain rdata with value aa.four.example.com..
    Received DNS part ANSWER MUST contain rrname with value 10.50.168.192.in-addr.arpa..

    Test Procedure:
    Client for DNS Question Record uses address: aa.four.example.com. type A class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include NOT empty ANSWER part.
    Received DNS part ANSWER MUST contain rdata with value 192.168.50.10.
    Received DNS part ANSWER MUST contain rrname with value aa.four.example.com..
