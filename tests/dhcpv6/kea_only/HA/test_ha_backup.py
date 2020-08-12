"""Kea HA syncing"""

# pylint: disable=invalid-name,line-too-long
import random
import pytest
from forge_cfg import world

import srv_msg
import misc
import srv_control


@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.HA
@pytest.mark.HA_state
@pytest.mark.disabled
def test_v6_hooks_HA_page_size_sync_mulitple_NA():
    # HA SERVER 1
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ffff')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(MGMT_ADDRESS)')
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_hooks('libdhcp_ha.so')
    print (world.dhcp_cfg["hooks-libraries"])
    srv_control.add_parameter_to_hook("libdhcp_ha.so",
                                      {"this-server-name": "server1", "mode": "passive-backup"})
    srv_control.add_parameter_to_hook("libdhcp_ha.so",
                                      {"peers": [{"name":"server1",
                                                  "url":"http://$(MGMT_ADDRESS):8000/",
                                                  "role":"primary"},
                                                 {"name":"server2",
                                                  "url":"http://$(MGMT_ADDRESS_2):8000/",
                                                  "role":"backup"}]})

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    # HA SERVER 2
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ffff')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(MGMT_ADDRESS_2)')
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_hooks('libdhcp_ha.so')
    srv_control.add_parameter_to_hook("libdhcp_ha.so",
                                      {"this-server-name": "server2", "mode": "passive-backup"})
    srv_control.add_parameter_to_hook("libdhcp_ha.so",
                                      {"peers": [{"name": "server1",
                                                  "url": "http://$(MGMT_ADDRESS):8000/",
                                                  "role": "primary"},
                                                 {"name": "server2",
                                                  "url": "http://$(MGMT_ADDRESS_2):8000/",
                                                  "role": "backup"}]})

    srv_control.build_and_send_config_files_dest_addr('SSH', 'config-file', '$(MGMT_ADDRESS_2)')
    srv_control.remote_start_srv('DHCP', 'started', '$(MGMT_ADDRESS_2)')

    misc.test_procedure()
    srv_msg.forge_sleep('2', 'seconds')

    tmp = world.f_cfg.show_packets_from
    world.f_cfg.show_packets_from = ""
    duid = "00:03:00:01:ff:ff:ff:ff:ff:0"
    test_range = 5
    for each in range(9):
        ia_1 = random.randint(1, 9009)

        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'DUID', duid + str(each))
        srv_msg.client_does_include('Client', None, 'client-id')
        for each_ia in range(test_range):
            srv_msg.client_sets_value('Client', 'ia_id', ia_1 + each_ia)
            srv_msg.client_does_include('Client', None, 'IA-NA')

        for each_pd in range(test_range):
            srv_msg.client_sets_value('Client', 'ia_pd', ia_1 + each_pd)
            srv_msg.client_does_include('Client', None, 'IA-PD')
        srv_msg.client_send_msg('SOLICIT')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'DUID', duid + str(each))
        srv_msg.client_does_include('Client', None, 'client-id')

        for each_ia in range(test_range):
            srv_msg.client_sets_value('Client', 'ia_id', ia_1 + each_ia)
            srv_msg.client_does_include('Client', None, 'IA-NA')

        for each_pd in range(test_range):
            srv_msg.client_sets_value('Client', 'ia_pd', ia_1 + each_pd)
            srv_msg.client_does_include('Client', None, 'IA-PD')

        srv_msg.client_copy_option('server-id')
        srv_msg.client_send_msg('REQUEST')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', None, 'REPLY')
        srv_msg.response_check_include_option('Response', None, '2')

    srv_msg.forge_sleep('2', 'seconds')
    world.f_cfg.show_packets_from = tmp
    #
    # srv_msg.remote_log_includes_line('$(MGMT_ADDRESS_2)',
    #                                  '$(SOFTWARE_INSTALL_DIR)/var/log/kea.log',
    #                                  None,
    #                                  'DHCPSRV_MEMFILE_GET_ADDR6 obtaining IPv6 lease '
    #                                  'for address 2001:db8:2::aa0:0:0 and lease type IA_PD')
    # srv_msg.remote_log_includes_line('$(MGMT_ADDRESS_2)',
    #                                  '$(SOFTWARE_INSTALL_DIR)/var/log/kea.log',
    #                                  None,
    #                                  'DHCPSRV_MEMFILE_UPDATE_ADDR6 updating IPv6 lease for address 2001:db8:2::aa0:0:0')
    # srv_msg.remote_log_includes_line('$(MGMT_ADDRESS_2)',
    #                                  '$(SOFTWARE_INSTALL_DIR)/var/log/kea.log-CTRL2',
    #                                  None,
    #                                  'Bulk apply of 10 IPv6 leases completed.')
    # srv_control.start_srv('DHCP', 'stopped')
    # srv_msg.forge_sleep('2', 'seconds')
    #
    # tmp = world.f_cfg.show_packets_from
    # world.f_cfg.show_packets_from = ""
    # duid = "00:03:00:01:ff:ff:ff:ff:00:0"
    # for each in range(9):
    #     ia_1 = random.randint(1, 9009)
    #
    #     misc.test_procedure()
    #     srv_msg.client_sets_value('Client', 'DUID', duid + str(each))
    #     srv_msg.client_does_include('Client', None, 'client-id')
    #     for each_ia in range(test_range):
    #         srv_msg.client_sets_value('Client', 'ia_id', ia_1 + each_ia)
    #         srv_msg.client_does_include('Client', None, 'IA-NA')
    #
    #     for each_pd in range(test_range):
    #         srv_msg.client_sets_value('Client', 'ia_pd', ia_1 + each_pd)
    #         srv_msg.client_does_include('Client', None, 'IA-PD')
    #     srv_msg.client_send_msg('SOLICIT')
    #
    #     misc.pass_criteria()
    #     srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    #
    #     misc.test_procedure()
    #     srv_msg.client_sets_value('Client', 'DUID', duid + str(each))
    #     srv_msg.client_does_include('Client', None, 'client-id')
    #
    #     for each_ia in range(test_range):
    #         srv_msg.client_sets_value('Client', 'ia_id', ia_1 + each_ia)
    #         srv_msg.client_does_include('Client', None, 'IA-NA')
    #
    #     for each_pd in range(test_range):
    #         srv_msg.client_sets_value('Client', 'ia_pd', ia_1 + each_pd)
    #         srv_msg.client_does_include('Client', None, 'IA-PD')
    #
    #     srv_msg.client_copy_option('server-id')
    #     srv_msg.client_send_msg('REQUEST')
    #
    #     misc.pass_criteria()
    #     srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    #
    #     srv_msg.response_check_include_option('Response', None, '2')
    #     srv_msg.response_check_option_content('Response',
    #                                           '2',
    #                                           None,
    #                                           'duid',
    #                                           '00:01:00:02:52:7b:a8:f0:08:00:27:58:99:99')
    # srv_control.start_srv('DHCP', 'started')
    # srv_msg.forge_sleep('4', 'seconds')
    # # now we should have 180 leases in HEA server 1
