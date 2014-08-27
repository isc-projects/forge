
Feature: DHCPv6 vendor specific information
    This feature is designed for vendor specific information option (option code = 17).
    Testing suboption - option request and others.

@v6 @dhcp6 @options @vendor
    Scenario: v6.vendor.options.tftp-servers
	## Testing server ability to configure it with vendor-specific options
	## and share it with user.
	## In this case: for vendor id vendor-4491 set option tftp-servers with value: 2001:558::76
	## Send vendor class and vendor specific information option (with option request).
	## Vendor tests are beta version.
	## with client via Advertise message.
	## 							 Client		Server
	## vendor-class
	## specific-info-req (32)	SOLICIT -->
	## vendor-spec-info 				<--	ADVERTISE
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					vendor specific information (code 17) with suboption
	##					TFTP Server address (code 32)
	Test Setup:
	Server is configured with 3000::/32 subnet with 3000::1-3000::2 pool.
	On space vendor-4491 server is configured with tftp-servers option with value 2001:558::76.
	DHCP server is started.

	Client sets enterprisenum value to 4491.
	Client does include vendor-class.
	Client adds suboption for vendor specific information with code: 1 and data: 32.
	Client does include vendor-specific-info.
	
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 17.
	Response option 17 MUST contain sub-option 32.
	
	References: RFC3315 section 22.17

@v6 @dhcp6 @options @vendor
    Scenario: v6.vendor.options.config-file
	## Testing server ability to configure it with vendor-specific options
	## and share it with user.
	## In this case: for vendor id vendor-4491 set option config-file with value normal_erouter_v6.cm.
	## Send vendor class and vendor specific information option (with option request).
	## Vendor tests are beta version.
	## with client via Advertise message.
	## 							 Client		Server
	## vendor-class
	## specific-info-req (33)	SOLICIT -->
	## vendor-spec-info 				<--	ADVERTISE
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					vendor specific information (code 17) with suboption
	##					Configuration file name (code 33)    
	Test Setup:
	Server is configured with 3000::/32 subnet with 3000::1-3000::2 pool.
	On space vendor-4491 server is configured with config-file option with value normal_erouter_v6.cm.
	DHCP server is started.

	Client sets enterprisenum value to 4491.
	Client does include vendor-class.
	Client adds suboption for vendor specific information with code: 1 and data: 33.
	Client does include vendor-specific-info.
	
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 17.
	Response option 17 MUST contain sub-option 33.

	References: RFC3315 section 22.17

@v6 @dhcp6 @options @vendor
    Scenario: v6.vendor.options.syslog-servers
 	## Testing server ability to configure it with vendor-specific options
	## and share it with user.
	## In this case: for vendor id vendor-4491 set option syslog-servers with address 2001::101.
	## Send vendor class and vendor specific information option (with option request).
	## Vendor tests are beta version.
	## with client via Advertise message.
	## 							 Client		Server
	## vendor-class
	## specific-info-req (34)	SOLICIT -->
	## vendor-spec-info 				<--	ADVERTISE
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					vendor specific information (code 17) with suboption
	##					sys log servers (code 34)       
	Test Setup:
	Server is configured with 3000::/32 subnet with 3000::1-3000::2 pool.
	On space vendor-4491 server is configured with syslog-servers option with value 2001::101.
	DHCP server is started.

	Client sets enterprisenum value to 4491.
	Client does include vendor-class.
	Client adds suboption for vendor specific information with code: 1 and data: 34.
	Client does include vendor-specific-info.
	
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 17.
	Response option 17 MUST contain sub-option 34.
	
	References: RFC3315 section 22.17

@v6 @dhcp6 @options @vendor
    Scenario: v6.vendor.options.time-servers
 	## Testing server ability to configure it with vendor-specific options
	## and share it with user.
	## In this case: for vendor id vendor-4491 set option time-servers option with value 2001::76.
	## Send vendor class and vendor specific information option (with option request).
	## Vendor tests are beta version.
	## with client via Advertise message.
	## 							 Client		Server
	## vendor-class
	## specific-info-req (37)	SOLICIT -->
	## vendor-spec-info 				<--	ADVERTISE
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					vendor specific information (code 17) with suboption
	##					time protocol servers (code 37)
	
	Test Setup:
	Server is configured with 3000::/32 subnet with 3000::1-3000::2 pool.
	On space vendor-4491 server is configured with time-servers option with value 2001::76.
	DHCP server is started.

	Client sets enterprisenum value to 4491.
	Client does include vendor-class.
	Client adds suboption for vendor specific information with code: 1 and data: 37.
	Client does include vendor-specific-info.
	
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 17.
	Response option 17 MUST contain sub-option 37.
	
	References: RFC3315 section 22.17

@v6 @dhcp6 @options @vendor
    Scenario: v6.vendor.options.time-offset
 	## Testing server ability to configure it with vendor-specific options
	## and share it with user.
	## In this case: for vendor id vendor-4491 set option time-offset with value -18000
	## Send vendor class and vendor specific information option (with option request).
	## Vendor tests are beta version.
	## with client via Advertise message.
	## 							 Client		Server
	## vendor-class
	## specific-info-req (38)	SOLICIT -->
	## vendor-spec-info 				<--	ADVERTISE
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					vendor specific information (code 17) with suboption
	##					time offset (code 38)
	Test Setup:
	Server is configured with 3000::/32 subnet with 3000::1-3000::2 pool.
	On space vendor-4491 server is configured with time-offset option with value -18000.
	DHCP server is started.

	Client sets enterprisenum value to 4491.
	Client does include vendor-class.
	Client adds suboption for vendor specific information with code: 1 and data: 38.
	Client does include vendor-specific-info.
	
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 17.
	Response option 17 MUST contain sub-option 38.
	
	References: RFC3315 section 22.17
	References: RFC3315 section 22.17


@v6 @dhcp6 @options @vendor
    Scenario: v6.vendor.options.multiple
 	## Testing server ability to configure it with vendor-specific options
	## and share it with user.
	## In this case: for vendor id vendor-4491 set option time-offset with value -18000
	## and for vendor id vendor-4491 set option tftp-servers with value: 2001:558:ff18:16:10:253:175:76
	## and for vendor id vendor-4491 set option config-file with value normal_erouter_v6.cm
	## and for vendor id vendor-4491 set option syslog-servers with address 2001:558:ff18:10:10:253:124:101
	## and for vendor id vendor-4491 set option time-servers option with value 2001:558:ff18:16:10:253:175:76
	## and for vendor id vendor-4491 set option time-offset with value -10000
	## Send vendor class and vendor specific information option (with option request).
	## Vendor tests are beta version.
	## with client via Advertise message.
	## 							 Client		Server
	## vendor-class
	## specific-info-req (all codes)SOLICIT -->
	## vendor-spec-info 				<--	ADVERTISE
	## Pass Criteria:
	## 				REPLY/ADVERTISE MUST include option:
	##					vendor specific information (code 17) with suboption
	##					TFTP Server address (code 32)
	##					Configuration file name (code 33)
	##					sys log servers (code 34)
	##					time offset (code 38)
	##					time protocol servers (code 37)
	
	Test Setup:
	Server is configured with 3000::/32 subnet with 3000::1-3000::2 pool.
	On space vendor-4491 server is configured with tftp-servers option with value 2001:558:ff18:16:10:253:175:76.
	On space vendor-4491 server is configured with config-file option with value normal_erouter_v6.cm.
	On space vendor-4491 server is configured with syslog-servers option with value 2001:558:ff18:10:10:253:124:101.
	On space vendor-4491 server is configured with time-servers option with value 2001:558:ff18:16:10:253:175:76.
	On space vendor-4491 server is configured with time-offset option with value -10000.
	DHCP server is started.

	Client sets enterprisenum value to 4491.
	Client does include vendor-class.
	Client adds suboption for vendor specific information with code: 1 and data: 32.
	Client adds suboption for vendor specific information with code: 1 and data: 33.
	Client adds suboption for vendor specific information with code: 1 and data: 34.
	Client adds suboption for vendor specific information with code: 1 and data: 37.
	Client adds suboption for vendor specific information with code: 1 and data: 38.
	Client does include vendor-specific-info.
	
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 17.
	Response option 17 MUST contain sub-option 32.
	Response option 17 MUST contain sub-option 33.
	Response option 17 MUST contain sub-option 34.
	Response option 17 MUST contain sub-option 37.
	Response option 17 MUST contain sub-option 38.
	
	References: RFC3315 section 22.17
	