Feature: Kea All Hooks
  Tests of integration of all hooks

@v4 @hook
Scenario: v4.all.hooks-start

Test Setup:
Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
# flex id
Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by flex-id 'docsis3.0'.
For host reservation entry no. 0 in subnet 0 add address with value 192.168.50.10.
Add to config file line: "host-reservation-identifiers": [ "flex-id","hw-address" ]
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so.
To hook no. 1 add parameter named identifier-expression with value: option[60].hex
# legal log
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_stat_cmds.so.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_subnet_cmds.so.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cache.so.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_lease_cmds.so.

Add High-Availability hook library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_ha.so.
To HA hook configuration add this-server-name with value: "server1"
To HA hook configuration add mode with value: "load-balancing"
To HA hook configuration add heartbeat-delay with value: 1000
To HA hook configuration add max-response-delay with value: 1001
To HA hook configuration add max-unacked-clients with value: 0
To HA hook configuration add max-ack-delay with value: 0

To HA hook configuration add peers with value: {"name":"server1","url":"http://$(MGMT_ADDRESS):8080/","role":"primary","auto-failover":true}
To HA hook configuration add peers with value: {"name":"server2","url":"http://$(MGMT_ADDRESS_2):8080/","role":"secondary","auto-failover":true}

Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Send server configuration using SSH and config-file.

DHCP server is started.
Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command": "list-commands","arguments": {}}

@v4 @hook
Scenario: v4.all.hooks-test-cooperation

Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.

Test Setup:
Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.10 pool.
# flex id
Reserve hostname reserved-hostname in subnet 0 for host uniquely identified by flex-id 'docsis3.0'.
For host reservation entry no. 0 in subnet 0 add address with value 192.168.50.10.
Add to config file line: "host-reservation-identifiers": [ "flex-id","hw-address" ]
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_flex_id.so.
To hook no. 1 add parameter named identifier-expression with value: option[60].hex
# legal log
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_legal_log.so.
Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_lease_cmds.so.
#Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cmds.so.
#Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_stat_cmds.so.
#Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_subnet_cmds.so.
#Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_host_cache.so.
##
#Add High-Availability hook library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_ha.so.
#To HA hook configuration add this-server-name with value: "server1"
#To HA hook configuration add mode with value: "load-balancing"
#To HA hook configuration add heartbeat-delay with value: 1000
#To HA hook configuration add max-response-delay with value: 1001
#To HA hook configuration add max-unacked-clients with value: 0
#To HA hook configuration add max-ack-delay with value: 0
#
#To HA hook configuration add peers with value: {"name":"server1","url":"http://$(MGMT_ADDRESS):8080/","role":"primary","auto-failover":true}
#To HA hook configuration add peers with value: {"name":"server2","url":"http://$(MGMT_ADDRESS_2):8080/","role":"secondary","auto-failover":true}

Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Server has control agent configured on HTTP connection with address $(MGMT_ADDRESS):8080 and socket unix path: $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
Send server configuration using SSH and config-file.

DHCP server is started.

#Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command": "list-commands","arguments": {}}
#JSON response in arguments MUST include value: build-report
#JSON response in arguments MUST include value: cache-clear
#JSON response in arguments MUST include value: cache-flush
#JSON response in arguments MUST include value: cache-get
#JSON response in arguments MUST include value: cache-insert
#JSON response in arguments MUST include value: cache-load
#JSON response in arguments MUST include value: cache-remove
#JSON response in arguments MUST include value: cache-write
#JSON response in arguments MUST include value: config-get
#JSON response in arguments MUST include value: config-reload
#JSON response in arguments MUST include value: config-set
#JSON response in arguments MUST include value: config-test
#JSON response in arguments MUST include value: config-write
#JSON response in arguments MUST include value: dhcp-disable
#JSON response in arguments MUST include value: dhcp-enable
#JSON response in arguments MUST include value: ha-continue
#JSON response in arguments MUST include value: ha-heartbeat
#JSON response in arguments MUST include value: ha-scopes
#JSON response in arguments MUST include value: ha-sync
#JSON response in arguments MUST include value: lease4-add
#JSON response in arguments MUST include value: lease4-del
#JSON response in arguments MUST include value: lease4-get
#JSON response in arguments MUST include value: lease4-get-all
#JSON response in arguments MUST include value: lease4-get-page
#JSON response in arguments MUST include value: lease4-update
#JSON response in arguments MUST include value: lease4-wipe
#JSON response in arguments MUST include value: lease6-add
#JSON response in arguments MUST include value: lease6-del
#JSON response in arguments MUST include value: lease6-get
#JSON response in arguments MUST include value: lease6-get-all
#JSON response in arguments MUST include value: lease6-get-page
#JSON response in arguments MUST include value: lease6-update
#JSON response in arguments MUST include value: lease6-wipe
#JSON response in arguments MUST include value: leases-reclaim
#JSON response in arguments MUST include value: libreload
#JSON response in arguments MUST include value: list-commands
#JSON response in arguments MUST include value: network4-add
#JSON response in arguments MUST include value: network4-del
#JSON response in arguments MUST include value: network4-get
#JSON response in arguments MUST include value: network4-list
#JSON response in arguments MUST include value: network4-subnet-add
#JSON response in arguments MUST include value: network4-subnet-del
#JSON response in arguments MUST include value: network6-add
#JSON response in arguments MUST include value: network6-del
#JSON response in arguments MUST include value: network6-get
#JSON response in arguments MUST include value: network6-list
#JSON response in arguments MUST include value: network6-subnet-add
#JSON response in arguments MUST include value: network6-subnet-del
#JSON response in arguments MUST include value: reservation-add
#JSON response in arguments MUST include value: reservation-del
#JSON response in arguments MUST include value: reservation-get
#JSON response in arguments MUST include value: shutdown
#JSON response in arguments MUST include value: stat-lease4-get
#JSON response in arguments MUST include value: stat-lease6-get
#JSON response in arguments MUST include value: statistic-get
#JSON response in arguments MUST include value: statistic-get-all
#JSON response in arguments MUST include value: statistic-remove
#JSON response in arguments MUST include value: statistic-remove-all
#JSON response in arguments MUST include value: statistic-reset
#JSON response in arguments MUST include value: statistic-reset-all
#JSON response in arguments MUST include value: subnet4-add
#JSON response in arguments MUST include value: subnet4-del
#JSON response in arguments MUST include value: subnet4-get
#JSON response in arguments MUST include value: subnet4-list
#JSON response in arguments MUST include value: subnet6-add
#JSON response in arguments MUST include value: subnet6-del
#JSON response in arguments MUST include value: subnet6-get
#JSON response in arguments MUST include value: subnet6-list
#JSON response in arguments MUST include value: version-get

# ha command
#Using existing HTTP $(MGMT_ADDRESS):8080 connection send: {"command": "ha-heartbeat","service":["dhcp4"],"arguments": {} }
#JSON response in arguments MUST include value: "state": "partner-down"

# flex-id
Test Procedure:
Client adds to the message vendor_class_id with value docsis3.0.
Client sets chaddr value to ff:01:02:03:ff:04.
Client sends DISCOVER message.

Pass Criteria:
Server MUST respond with OFFER message.
Response MUST contain yiaddr 192.168.50.10.

# legal log
Test Procedure:
Client sets chaddr value to ff:01:02:03:ff:04.
Client adds to the message client_id with value 00010203040506.
Client requests option 1.
Client sends DISCOVER message.

Pass Criteria:
Server MUST respond with OFFER message.
Response MUST contain yiaddr 192.168.50.1.
Response MUST include option 1.
Response MUST include option 54.
Response MUST include option 61.
Response option 1 MUST contain value 255.255.255.0.
Response option 61 MUST contain value 00010203040506.

Test Procedure:
Client adds to the message client_id with value 00010203040506.
Client sets chaddr value to ff:01:02:03:ff:04.
Client copies server_id option from received message.
Client adds to the message requested_addr with value 192.168.50.1.
Client requests option 1.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with ACK message.
Response MUST contain yiaddr 192.168.50.1.
Response MUST include option 1.
Response MUST include option 54.
Response MUST include option 61.
Response option 1 MUST contain value 255.255.255.0.
Response option 61 MUST contain value 00010203040506.

Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.

File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: Address: 192.168.50.1 has been assigned for 1 hrs 6 mins 40
File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: to a device with hardware address: hwtype=1 ff:01:02:03:ff:04, client-id: 00:01:02:03:04:05:06

# lease commands
Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"lease4-add","arguments":{"ip-address": "192.168.50.10","hostname": "newhostname.example.org","hw-address": "1a:1b:1c:1d:1e:1f","subnet-id":1,"valid-lft":500000}}
File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: Administrator added a lease of address: 192.168.50.10 to a device with hardware address: 1a:1b:1c:1d:1e:1f for 5 days 18 hrs 53 mins 20 secs

#
#Test Procedure:
#Client sets chaddr value to 1a:1b:1c:1d:1e:1f.
#Client sets ciaddr value to 192.168.50.10.
#Client copies server_id option from received message.
#Client sends REQUEST message.
#
#Pass Criteria:
#Server MUST respond with ACK message.
#Response MUST contain yiaddr 192.168.50.10.
#Response MUST include option 54.
#Response option 54 MUST contain value $(SRV4_ADDR).


Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.