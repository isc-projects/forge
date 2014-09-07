Feature: DDNS without TSIG
    This feature is testing DHCPv6 + DDNS in cooperation with DNS server BIND9 without TSIG authorisation. It's primary
    target is DDNS forward and reverse update.

@v6 @ddns @notsig @forward_reverse_add
    Scenario: ddns.notsig.forw_and_rev.add-success-Sflag

    Test Setup:
    Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    DDNS server is configured with generated-prefix option set to six.
    DDNS server is configured with qualifying-suffix option set to example.com.
    Add forward DDNS with name six.example.com. and key EMPTY_KEY on address 2001:db8:1::1000 and port 53.
    Add reverse DDNS with name 1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. and key EMPTY_KEY on address 2001:db8:1::1000 and port 53.
    DHCP server is started.

    Use DNS set no. 1.
    DNS server is started.

    Test Procedure:
    Client for DNS Question Record uses address: sth6.six.example.com type AAAA class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include empty ANSWER part.

    Test Procedure:
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
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


@v6 @ddns @notsig @forward_reverse_add
    Scenario: ddns.notsig.forw_and_rev.add-fail-Sflag

    Test Setup:
    Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    DDNS server is configured with generated-prefix option set to six.
    DDNS server is configured with qualifying-suffix option set to example.com.
    Add forward DDNS with name six.example.com. and key EMPTY_KEY on address 2001:db8:1::1000 and port 53.
    Add reverse DDNS with name 1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. and key EMPTY_KEY on address 2001:db8:1::1000 and port 53.
    DHCP server is started.

    Use DNS set no. 1.
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
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 1.
    Response MUST include option 2.

    Test Procedure:
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client copies IA_NA option from received message.
    Client copies server-id option from received message.
    ## Update for different zone
    Client sets FQDN_domain_name value to sth6.six.com..
    Client sets FQDN_flags value to S.
    Client does include fqdn.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 1.
    Response MUST include option 2.
    Response MUST include option 39.
    Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    Response option 39 MUST contain fqdn sth6.six.com.

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

@v6 @ddns @notsig @forward_reverse_add
    Scenario: ddns.notsig.forw_and_rev.notenabled-Sflag

    Test Setup:
    Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to false.
    Add forward DDNS with name six.example.com. and key EMPTY_KEY on address 2001:db8:1::1000 and port 53.
    Add reverse DDNS with name 1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. and key EMPTY_KEY on address 2001:db8:1::1000 and port 53.
    DHCP server is started.

    Use DNS set no. 1.
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
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 1.
    Response MUST include option 2.
    Response MUST include option 39.
    Response option 39 MUST contain flags 6. #later make it 's' 'n' and 'o' 6 - NO
    Response option 39 MUST contain fqdn sth6.six.example.com.

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

@v6 @ddns @notsig @forward_update
    Scenario: ddns.notsig.forw_and_rev.update-success-Sflag

    Test Setup:
    Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    Add forward DDNS with name six.example.com. and key EMPTY_KEY on address 2001:db8:1::1000 and port 53.
    Add reverse DDNS with name 1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. and key EMPTY_KEY on address 2001:db8:1::1000 and port 53.
    DHCP server is started.

    Use DNS set no. 2.
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

    Test Setup:
    DHCP server is stopped.
    Clear leases.

    Test Setup:
    Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::51-2001:db8:1::51 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    Add forward DDNS with name six.example.com. and key EMPTY_KEY on address 2001:db8:1::1000 and port 53.
    Add reverse DDNS with name 1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. and key EMPTY_KEY on address 2001:db8:1::1000 and port 53.
    DHCP server is started.

    Test Procedure:
    Client for DNS Question Record uses address: sth6.six.example.com type AAAA class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include NOT empty ANSWER part.
    Received DNS part ANSWER MUST contain rdata with value 2001:db8:1::50.

    Test Procedure:
    Client for DNS Question Record uses address: 1.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. type PTR class IN.
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
    Received DNS part ANSWER MUST contain rdata with value 2001:db8:1::51.
    Received DNS part ANSWER MUST contain rrname with value sth6.six.example.com..

    Test Procedure:
    Client for DNS Question Record uses address: 1.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. type PTR class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include NOT empty ANSWER part.
    Received DNS part ANSWER MUST contain rdata with value sth6.six.example.com..
    Received DNS part ANSWER MUST contain rrname with value 1.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa..

@v6 @ddns @notsig @forward_reverse_add
    Scenario: ddns.notsig.forw_and_rev.two-dhci-Sflag

    Test Setup:
    Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::51-2001:db8:1::52 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    DDNS server is configured with generated-prefix option set to six.
    DDNS server is configured with qualifying-suffix option set to example.com.
    Add forward DDNS with name six.example.com. and key EMPTY_KEY on address 2001:db8:1::1000 and port 53.
    Add reverse DDNS with name 1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. and key EMPTY_KEY on address 2001:db8:1::1000 and port 53.
    DHCP server is started.

    Use DNS set no. 1.
    DNS server is started.

    Test Procedure:
    Client for DNS Question Record uses address: client1.six.example.com type AAAA class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include empty ANSWER part.

    Test Procedure:
    Client for DNS Question Record uses address: client2.six.example.com type AAAA class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include empty ANSWER part.

    ## Client 1 add
    Test Procedure:
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 1.
    Response MUST include option 2.

    Test Procedure:
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client saves into set no. 1 IA_NA option from received message.
    Client adds saved options in set no. 1. And DONT Erase.
    Client copies server-id option from received message.
    Client sets FQDN_domain_name value to client1.six.example.com..
    Client sets FQDN_flags value to S.
    Client does include fqdn.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 1.
    Response MUST include option 2.
    Response MUST include option 39.
    Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    Response option 39 MUST contain fqdn client1.six.example.com.

    Test Procedure:
    Client for DNS Question Record uses address: client1.six.example.com type AAAA class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include NOT empty ANSWER part.
    Received DNS part ANSWER MUST contain rdata with value 2001:db8:1::51.
    Received DNS part ANSWER MUST contain rrname with value client1.six.example.com..


    ## Client 2 add
    Test Procedure:
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:02.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 1.
    Response MUST include option 2.

    Test Procedure:
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:02.
    Client saves into set no. 2 IA_NA option from received message.
    Client adds saved options in set no. 2. And DONT Erase.
    Client copies server-id option from received message.
    Client sets FQDN_domain_name value to client2.six.example.com..
    Client sets FQDN_flags value to S.
    Client does include fqdn.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 1.
    Response MUST include option 2.
    Response MUST include option 39.
    Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    Response option 39 MUST contain fqdn client2.six.example.com.

    Test Procedure:
    Client for DNS Question Record uses address: client2.six.example.com type AAAA class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include NOT empty ANSWER part.
    Received DNS part ANSWER MUST contain rdata with value 2001:db8:1::52.
    Received DNS part ANSWER MUST contain rrname with value client2.six.example.com..

@v6 @ddns @notsig @forward_reverse_add
    Scenario: ddns.notsig.forw_and_rev.dhci-conflicts-Sflag

    Test Setup:
    Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::51-2001:db8:1::52 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    Add forward DDNS with name six.example.com. and key EMPTY_KEY on address 2001:db8:1::1000 and port 53.
    Add reverse DDNS with name 1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. and key EMPTY_KEY on address 2001:db8:1::1000 and port 53.
    DHCP server is started.

    Use DNS set no. 1.
    DNS server is started.

    Test Procedure:
    Client for DNS Question Record uses address: client1.six.example.com type AAAA class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include empty ANSWER part.

    Test Procedure:
    Client for DNS Question Record uses address: client2.six.example.com type AAAA class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include empty ANSWER part.

    ## Client 1 add
    Test Procedure:
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 1.
    Response MUST include option 2.

    Test Procedure:
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client saves into set no. 1 IA_NA option from received message.
    Client adds saved options in set no. 1. And DONT Erase.
    Client copies server-id option from received message.
    Client sets FQDN_domain_name value to client1.six.example.com..
    Client sets FQDN_flags value to S.
    Client does include fqdn.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 1.
    Response MUST include option 2.
    Response MUST include option 39.
    Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    Response option 39 MUST contain fqdn client1.six.example.com.

    Test Procedure:
    Client for DNS Question Record uses address: client1.six.example.com type AAAA class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include NOT empty ANSWER part.
    Received DNS part ANSWER MUST contain rdata with value 2001:db8:1::51.
    Received DNS part ANSWER MUST contain rrname with value client1.six.example.com..

    ## Client 2 add
    Test Procedure:
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:02.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 1.
    Response MUST include option 2.

    Test Procedure:
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:02.
    Client saves into set no. 2 IA_NA option from received message.
    Client saves into set no. 2 server-id option from received message.
    Client adds saved options in set no. 2. And DONT Erase.
    Client sets FQDN_domain_name value to client1.six.example.com..
    Client sets FQDN_flags value to S.
    Client does include fqdn.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 1.
    Response MUST include option 2.
    Response MUST include option 39.
    Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    Response option 39 MUST contain fqdn client1.six.example.com.

    Test Procedure:
    Client for DNS Question Record uses address: client1.six.example.com type AAAA class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include NOT empty ANSWER part.
    Received DNS part ANSWER MUST contain rdata with value 2001:db8:1::51.
    Received DNS part ANSWER MUST contain rrname with value client1.six.example.com..

    Test Procedure:
    Client for DNS Question Record uses address: client2.six.example.com type AAAA class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include empty ANSWER part.

    Test Procedure:
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:02.
    Client adds saved options in set no. 2. And DONT Erase.
    Client sets FQDN_domain_name value to client2.six.example.com..
    Client sets FQDN_flags value to S.
    Client does include fqdn.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 1.
    Response MUST include option 2.
    Response MUST include option 39.
    Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    Response option 39 MUST contain fqdn client2.six.example.com.

    Test Procedure:
    Client for DNS Question Record uses address: client2.six.example.com type AAAA class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include NOT empty ANSWER part.
    Received DNS part ANSWER MUST contain rdata with value 2001:db8:1::52.
    Received DNS part ANSWER MUST contain rrname with value client2.six.example.com..

    Test Procedure:
    Client for DNS Question Record uses address: 1.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. type PTR class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include NOT empty ANSWER part.
    Received DNS part ANSWER MUST contain rdata with value client1.six.example.com..
    Received DNS part ANSWER MUST contain rrname with value 1.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa..

    Test Procedure:
    Client for DNS Question Record uses address: 2.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. type PTR class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include NOT empty ANSWER part.
    Received DNS part ANSWER MUST contain rdata with value client2.six.example.com..
    Received DNS part ANSWER MUST contain rrname with value 2.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa..


@v6 @ddns @notsig @forward_reverse_add
    Scenario: ddns.notsig.forw_and_rev.add-success-withoutflag-override-client

    Test Setup:
    Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    DDNS server is configured with override-client-update option set to true.
    DDNS server is configured with qualifying-suffix option set to example.com.
    Add forward DDNS with name six.example.com. and key EMPTY_KEY on address 2001:db8:1::1000 and port 53.
    Add reverse DDNS with name 1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. and key EMPTY_KEY on address 2001:db8:1::1000 and port 53.
    DHCP server is started.

    Use DNS set no. 1.
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
    Client does include fqdn.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 1.
    Response MUST include option 2.
    Response MUST include option 39.
    Response option 39 MUST contain flags 3. #later make it 's' 'n' and 'o' 3 - SO
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

@v6 @ddns @notsig @reverse_add
    Scenario: ddns.notsig.rev.success-withoutflag

    Test Setup:
    Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    Add forward DDNS with name six.example.com. and key EMPTY_KEY on address 2001:db8:1::1000 and port 53.
    Add reverse DDNS with name 1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. and key EMPTY_KEY on address 2001:db8:1::1000 and port 53.
    DHCP server is started.

    Use DNS set no. 1.
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
    Client does include fqdn.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 1.
    Response MUST include option 2.
    Response MUST include option 39.
    Response option 39 MUST contain flags 0. #later make it 's' 'n' and 'o'
    Response option 39 MUST contain fqdn sth6.six.example.com.
    DNS log MUST contain line: adding an RR at '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa' PTR sth6.six.example.com.

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

@v6 @ddns @notsig @reverse_add
    Scenario: ddns.notsig.rev.withoutflag-notenabled

    Test Setup:
    Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to false.
    Add forward DDNS with name six.example.com. and key EMPTY_KEY on address 2001:db8:1::1000 and port 53.
    Add reverse DDNS with name 1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. and key EMPTY_KEY on address 2001:db8:1::1000 and port 53.
    DHCP server is started.

    Use DNS set no. 1.
    DNS server is started.

    Test Procedure:
    Client for DNS Question Record uses address: sth6.six.example.com type AAAA class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include empty ANSWER part.

    Test Procedure:
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
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
    Client does include fqdn.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 1.
    Response MUST include option 2.
    Response MUST include option 39.
    Response option 39 MUST contain flags 4. #later make it 's' 'n' and 'o' 4 -N
    Response option 39 MUST contain fqdn sth6.six.example.com.
    DNS log MUST NOT contain line: adding an RR at '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa' PTR sth6.six.example.com.

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

@v6 @ddns @notsig @reverse_add
    Scenario: ddns.notsig.rev.Nflag-override-no-update

    Test Setup:
    Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::50-2001:db8:1::50 pool.
    DDNS server is configured on 127.0.0.1 address and 53001 port.
    DDNS server is configured with enable-updates option set to true.
    DDNS server is configured with override-no-update option set to true.
    Add forward DDNS with name six.example.com. and key EMPTY_KEY on address 2001:db8:1::1000 and port 53.
    Add reverse DDNS with name 1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. and key EMPTY_KEY on address 2001:db8:1::1000 and port 53.
    DHCP server is started.

    Use DNS set no. 1.
    DNS server is started.

    Test Procedure:
    Client for DNS Question Record uses address: sth6.six.example.com type AAAA class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include empty ANSWER part.

    Test Procedure:
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
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
    Client sets FQDN_flags value to N.
    Client does include fqdn.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with REPLY message.
    Response MUST include option 1.
    Response MUST include option 2.
    Response MUST include option 39.
    Response option 39 MUST contain flags 3. #later make it 's' 'n' and 'o' 3 - SO
    Response option 39 MUST contain fqdn sth6.six.example.com.
    DNS log MUST contain line: adding an RR at '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa' PTR sth6.six.example.com.

    Test Procedure:
    Client for DNS Question Record uses address: sth6.six.example.com type AAAA class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include NOT empty ANSWER part.
    Received DNS part ANSWER MUST contain rdata with value 2001:db8:1::50.
    Received DNS part ANSWER MUST contain rrname with value sth6.six.example.com..

    Test Procedure:
    Client for DNS Question Record uses address: 0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa. type PTR class IN.
    Client sends DNS query.

    Pass Criteria:
    DNS server MUST respond with DNS query.
    Received DNS query MUST include NOT empty ANSWER part.
    Received DNS part ANSWER MUST contain rdata with value sth6.six.example.com..
    Received DNS part ANSWER MUST contain rrname with value 0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa..
