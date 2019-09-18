Feature: billing class
        testing billing class 


@v4 @dhcpd @keyword
Scenario: v4.dhcpd.billing_class_limit

Test Setup:
Run configuration command:  ping-check off;
Run configuration command:  ddns-updates off;
Run configuration command:  max-lease-time 50;
Run configuration command:  default-lease-time 50;
Run configuration command:  subnet 192.168.50.0 netmask 255.255.255.0 {
Run configuration command:      authoritative;
Run configuration command:      pool {
Run configuration command:          range 192.168.50.100 192.168.50.101;
Run configuration command:      }
Run configuration command:  }
Run configuration command:  class "vnd1001" {
Run configuration command:      match if (option vendor-class-identifier = "vnd1001");
Run configuration command:      lease limit 1;
Run configuration command:  }

Run configuration command:  class "vendor-classes" 
Run configuration command:  { 
Run configuration command:      match option vendor-class-identifier; 
Run configuration command:  }

Run configuration command:  subclass "vendor-classes" "4491" {
Run configuration command:      vendor-option-space vendor-4491;
Run configuration command:      lease limit 1;
Run configuration command:  }

Send server configuration using SSH and config-file.
DHCP Server is started.


Test Procedure:
Sleep for 1 seconds.
#Client sets chaddr value to 00:00:00:00:00:11.
Client adds to the message client_id with value 72656331323334.
Client adds to the message vendor_class_id with value vnd1001.
Client sends DISCOVER message.

Pass Criteria:
Server MUST respond with OFFER message.
Response MUST contain yiaddr 192.168.50.100.

Test Procedure:
Client adds to the message client_id with value 72656331323334.
Client adds to the message vendor_class_id with value vnd1001.
Client copies server_id option from received message.
Client adds to the message requested_addr with value 192.168.50.100.
Client sends REQUEST message.

Pass Criteria:
Server MUST respond with ACK message.
Response MUST contain yiaddr 192.168.50.100. 



Test Procedure:
Sleep for 1 seconds.
#Client sets chaddr value to 00:00:00:00:00:22.
Client adds to the message client_id with value 72656331323335.
Client adds to the message vendor_class_id with value vnd1001.
Client sends DISCOVER message.

Pass Criteria:
Server MUST NOT respond.
DHCP log contains 1 of line: no available billing: lease limit reached in all matching classes (last: 'vnd1001')
