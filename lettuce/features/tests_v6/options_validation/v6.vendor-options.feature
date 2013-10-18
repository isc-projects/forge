
Feature: DHCPv6 vendor specific information
    This feature is designed for vendor specific information option (option code = 17).
    Testing suboption - option request and others.

@v6 @options @vendor
    Scenario: v6.vendor.options.tftp-servers

	Test Setup:
	Server is configured with 3000::/32 subnet with 3000::1-3000::2 pool.
	On space vendor-4491 server is configured with tftp-servers option with value 2001:558:ff18:16:10:253:175:76.
	Server is started.

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

@v6 @options @vendor
    Scenario: v6.vendor.options.config-file
    
	Test Setup:
	Server is configured with 3000::/32 subnet with 3000::1-3000::2 pool.
	On space vendor-4491 server is configured with config-file option with value normal_erouter_v6.cm.
	Server is started.

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

@v6 @options @vendor
    Scenario: v6.vendor.options.syslog-servers
    
	Test Setup:
	Server is configured with 3000::/32 subnet with 3000::1-3000::2 pool.
	On space vendor-4491 server is configured with syslog-servers option with value 2001:558:ff18:10:10:253:124:101.
	Server is started.

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

@v6 @options @vendor
    Scenario: v6.vendor.options.time-servers
	Test Setup:
	Server is configured with 3000::/32 subnet with 3000::1-3000::2 pool.
	On space vendor-4491 server is configured with time-servers option with value 2001:558:ff18:16:10:253:175:76.
	Server is started.

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

@v6 @options @vendor
    Scenario: v6.vendor.options.time-offset
	Test Setup:
	Server is configured with 3000::/32 subnet with 3000::1-3000::2 pool.
	On space vendor-4491 server is configured with time-offset option with value -18000.
	Server is started.

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


@v6 @options @vendor
    Scenario: v6.vendor.options.multiple

	Test Setup:
	Server is configured with 3000::/32 subnet with 3000::1-3000::2 pool.
	On space vendor-4491 server is configured with tftp-servers option with value 2001:558:ff18:16:10:253:175:76.
	On space vendor-4491 server is configured with config-file option with value normal_erouter_v6.cm.
	On space vendor-4491 server is configured with syslog-servers option with value 2001:558:ff18:10:10:253:124:101.
	On space vendor-4491 server is configured with time-servers option with value 2001:558:ff18:16:10:253:175:76.
	On space vendor-4491 server is configured with time-offset option with value -18000.
	Server is started.

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
	