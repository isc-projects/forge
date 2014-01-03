Feature: Kea6 User Check Hook Library
    Testing KEA's User Check Hook Library - NOTE TEST IS ONLY SUPPORTED BY KEA

# All of these tests rely on the Kea only behavior of setting the first subnet's
# interface value equal to SERVER_IFACE.  If SERVER_IFACE is not blank, Forge
# automatically addes "config set Dhcp6/subnet[0]/interface <SERVER_IFACE>"
# to the server configuration.

@v6 @kea_only @user_check @vendor_options
    Scenario: user_check.vendor_options.all

    # Install the requisite user registry file onto the server and then 
    # Configure the server with two subnets.  The first subnet will be used 
    # for registeted users, the second for unregistered users.  
    Test Setup:
    Client sends local file stored in: features/tests_v6/kea_only/user_chk/registry_1.txt to server, to location: /tmp/user_chk_registry.txt.
    Client removes file from server located in: /tmp/user_chk_outcome.txt.
    Server is configured with 3000::/64 subnet with 3000::5-3000::20 pool.
    Server is configured with another subnet: 1000:1::/64 with 1000:1::5-1000:1::5 pool on interface eth3.
    Run configuration command: config add Dhcp6/hooks-libraries
    Run configuration command: config set Dhcp6/hooks-libraries[0] $(SERVER_INSTALL_DIR)/lib/libdhcp_user_chk.so
    On space vendor-4491 server is configured with tftp-servers option with value 7000::1.
    On space vendor-4491 server is configured with config-file option with value bootfile.from.server.
    Server is started.

    #
    # Send a query from an unknown user
    #
    Test Procedure:
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client sets enterprisenum value to 4491.
    Client does include vendor-class.
    Client adds suboption for vendor specific information with code: 1 and data: 32.
    Client adds suboption for vendor specific information with code: 1 and data: 33.
    Client does include vendor-specific-info.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response option 3 MUST contain sub-option 5.
    # We don't really care about the address value
    # Options should come from default user in registry
    Response option 17 MUST contain sub-option 32.
    #   Response sub-option 32 from option 17 MUST contain tftp-servers 9000::1.
    Response option 17 MUST contain sub-option 33.
    Response sub-option 33 from option 17 MUST contain config-file bootfile.from.default.

    #
    # Send a query from a registered user with no properties
    #
    Test Procedure:
    Client sets DUID value to 00:03:00:01:11:02:03:04:05:06.
    Client sets enterprisenum value to 4491.
    Client does include vendor-class.
    Client adds suboption for vendor specific information with code: 1 and data: 32.
    Client adds suboption for vendor specific information with code: 1 and data: 33.
    Client does include vendor-specific-info.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response option 3 MUST contain sub-option 5.
    # We don't really care about the address value
    # Options should come from server config
    Response option 17 MUST contain sub-option 32.
    #    Response sub-option 32 from option 17 MUST contain tftp-servers 7000::1.
    Response option 17 MUST contain sub-option 33.
   	Response sub-option 33 from option 17 MUST contain config-file bootfile.from.server.

    #
    # Send a query from a registered user who supplies only bootfile
    #
    Test Procedure:
    Client sets DUID value to 00:03:00:01:22:02:03:04:05:06.
    Client sets enterprisenum value to 4491.
    Client does include vendor-class.
    Client adds suboption for vendor specific information with code: 1 and data: 32.
    Client adds suboption for vendor specific information with code: 1 and data: 33.
    Client does include vendor-specific-info.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response option 3 MUST contain sub-option 5.
    # We don't really care about the address value
    # bootfile should be from user, tftp server from server config
    Response option 17 MUST contain sub-option 32.
    #   Response sub-option 32 from option 17 MUST contain tftp-servers 7000::1.
    Response option 17 MUST contain sub-option 33.
   	Response sub-option 33 from option 17 MUST contain config-file bootfile.from.user.

    #
    # Send a query from a registered user who supplies only tftp server
    #
    Test Procedure:
    Client sets DUID value to 00:03:00:01:33:02:03:04:05:06.
    Client sets enterprisenum value to 4491.
    Client does include vendor-class.
    Client adds suboption for vendor specific information with code: 1 and data: 32.
    Client adds suboption for vendor specific information with code: 1 and data: 33.
    Client does include vendor-specific-info.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response option 3 MUST contain sub-option 5.
    # We don't really care about the address value
    # bootfile should be from server config, tftp server from user
    Response option 17 MUST contain sub-option 32.
   	#   Response sub-option 32 from option 17 MUST contain tftp-servers 8000::1.
    Response option 17 MUST contain sub-option 33.
   	Response sub-option 33 from option 17 MUST contain config-file bootfile.from.server.

    Test Procedure:
    # Send a query from a registered user who supplies both tftp server and bootfile
    Client sets DUID value to 00:03:00:01:44:02:03:04:05:06.
    Client sets enterprisenum value to 4491.
    Client does include vendor-class.
    Client adds suboption for vendor specific information with code: 1 and data: 32.
    Client adds suboption for vendor specific information with code: 1 and data: 33.
    Client does include vendor-specific-info.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response option 3 MUST contain sub-option 5.
    # We don't really care about the address value
    # tftp server and bootfile should be from user
    Response option 17 MUST contain sub-option 32.
   	#   Response sub-option 32 from option 17 MUST contain tftp-servers 8002::1.
    Response option 17 MUST contain sub-option 33.
  	Response sub-option 33 from option 17 MUST contain config-file bootfile.from.user-2.
