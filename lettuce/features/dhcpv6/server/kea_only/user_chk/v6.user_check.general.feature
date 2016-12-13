Feature: Kea6 User Check Hook Library 
    Testing KEA's User Check Hook Library - NOTE TEST IS ONLY SUPPORTED BY KEA

# All of these tests rely on the Kea only behavior of setting the first subnet's
# interface value equal to SERVER_IFACE.  If SERVER_IFACE is not blank, Forge
# automatically addes "config set Dhcp6/subnet[0]/interface <SERVER_IFACE>"
# to the server configuration.

@v6 @dhcp6 @kea_only @user_check  @IA_NA
    Scenario: user_check.hook-IA_NA-no_registry
    # Without a user registry and multiple subnets 
    # Subnet selection will use subnet interface for subnet selection hint

    Test Setup:
    Client removes file from server located in: /tmp/user_chk_registry.txt.
    Client removes file from server located in: /tmp/user_chk_outcome.txt.
    Server is configured with 3000::/64 subnet with 3000::5-3000::5 pool.
    Server is configured with another subnet: 1000::/64 with 1000::5-1000::5 pool.
    Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/libdhcp_user_chk.so.
    DHCP server is started.
    
    Test Procedure:
    Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::5.

@v6 @dhcp6 @kea_only @user_check  @IA_NA
    Scenario: user_check.hook-IA_NA-with_registry_unknown_user
    # With a user registry and multiple subnets
    # an unknown user should get last subnet

    Test Setup:
    Client sends local file stored in: features/dhcpv6/server/kea_only/user_chk/registry_1.txt to server, to location: /tmp/user_chk_registry.txt.
    Client removes file from server located in: /tmp/user_chk_outcome.txt.
    Server is configured with 3000::/64 subnet with 3000::5-3000::5 pool.
    Server is configured with another subnet: 1000::/64 with 1000::5-1000::5 pool.
    Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/libdhcp_user_chk.so.
    DHCP server is started.
    
    Test Procedure:
    # Send a query from an unregistered user
    Client sets DUID value to 00:03:00:01:ff:ff:ff:ff:ff:01.
    Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 1000::5.
    # Check the outcome file for correct content
    Client download file from server stored in: /tmp/user_chk_outcome.txt.
    Client compares downloaded file from server with local file stored in: features/dhcpv6/server/kea_only/user_chk/outcome_1.txt.

@v6 @dhcp6 @kea_only @user_check  @IA_NA
    Scenario: user_check.hook-IA_NA-with_registry_known_user
    # With a user registry and multiple subnets
    # an known user should get first subnet

    Test Setup:
    Client sends local file stored in: features/dhcpv6/server/kea_only/user_chk/registry_1.txt to server, to location: /tmp/user_chk_registry.txt.
    Client removes file from server located in: /tmp/user_chk_outcome.txt.
    Server is configured with 3000::/64 subnet with 3000::5-3000::5 pool.
    Server is configured with another subnet: 1000::/64 with 1000::5-1000::5 pool.
    Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/libdhcp_user_chk.so.
    DHCP server is started.
    
    Test Procedure:
    # Send a query from a registered user
    Client sets DUID value to 00:03:00:01:11:02:03:04:05:06.
    Client does include client-id.
    Client does include IA-NA.
    Client sends SOLICIT message.

    Pass Criteria:
    Server MUST respond with ADVERTISE message.
    Response MUST include option 3.
    Response option 3 MUST contain sub-option 5.
    Response sub-option 5 from option 3 MUST contain address 3000::5.
    # Check the outcome file for correct content
    Client download file from server stored in: /tmp/user_chk_outcome.txt.
    Client compares downloaded file from server with local file stored in: features/dhcpv6/server/kea_only/user_chk/outcome_2.txt.
