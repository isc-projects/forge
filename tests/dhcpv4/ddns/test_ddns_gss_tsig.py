"""DDNS with GSS-TSIG"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_msg
import srv_control
from forge_cfg import world
from softwaresupport import krb
from softwaresupport.multi_server_functions import fabric_sudo_command


def _send_through_socket(cmd, socket_name=world.f_cfg.run_join('ddns_control_socket'), exp_result=0, exp_failed=False):
    return srv_msg.send_ctrl_cmd_via_socket(command=cmd, socket_name=socket_name,
                                            exp_result=exp_result, exp_failed=exp_failed)


def _check_dns_record(fqdn, rdata=None, dns_addr=None):
    # this time we are using v4 address to communicate to DNS so no need to change this
    misc.test_procedure()
    srv_msg.dns_question_record(fqdn, 'A' if world.proto == 'v4' else 'AAAA', 'IN')
    srv_msg.client_send_dns_query(dns_addr=dns_addr)

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST')
    if rdata is None:
        srv_msg.dns_option('ANSWER', expect_include=False)
    else:
        srv_msg.dns_option_content('ANSWER', 'rdata', rdata)
        srv_msg.dns_option_content('ANSWER', 'rrname', fqdn)


def _get_lease(addr, fqdn, mac, suffix="example.com"):
    srv_msg.clean_saved_options()
    misc.test_procedure()

    if world.proto == 'v4':
        srv_msg.client_requests_option(1)
        srv_msg.client_sets_value('Client', 'chaddr', mac)
        srv_msg.client_send_msg('DISCOVER')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'OFFER')
        srv_msg.response_check_include_option(1)
        srv_msg.client_sets_value('Client', 'chaddr', mac)
        srv_msg.response_check_content('yiaddr', addr)
        srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'chaddr', mac)
        srv_msg.client_copy_option('server_id')
        srv_msg.client_does_include_with_value('requested_addr', addr)
        srv_msg.client_requests_option(1)
        srv_msg.client_sets_value('Client', 'FQDN_domain_name', fqdn)
        srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
        srv_msg.client_does_include('Client', 'fqdn')
        srv_msg.client_send_msg('REQUEST')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'ACK')
        srv_msg.client_save_option('server_id')  # needed for release
        srv_msg.response_check_content('yiaddr', addr)
        srv_msg.response_check_include_option(1)
        srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
        srv_msg.response_check_include_option(81)
        srv_msg.response_check_option_content(81, 'flags', 1)
        srv_msg.response_check_option_content(81, 'fqdn', f'{fqdn}' if suffix in fqdn else f'{fqdn}.{suffix}.')
    else:
        srv_msg.client_sets_value('Client', 'DUID', f'00:03:00:01:{mac}')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_does_include('Client', 'IA-NA')
        srv_msg.client_send_msg('SOLICIT')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
        srv_msg.response_check_include_option(1)
        srv_msg.response_check_include_option(2)

        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'DUID', f'00:03:00:01:{mac}')
        srv_msg.client_copy_option('IA_NA')
        srv_msg.client_copy_option('server-id')
        srv_msg.client_sets_value('Client', 'FQDN_domain_name', f'{fqdn}')
        srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
        srv_msg.client_does_include('Client', 'fqdn')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_send_msg('REQUEST')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'REPLY')
        srv_msg.client_save_option('IA_NA')  # needed for release
        srv_msg.client_save_option('server-id')  # needed for release
        srv_msg.response_check_include_option(1)
        srv_msg.response_check_include_option(2)
        srv_msg.response_check_include_option(39)
        srv_msg.response_check_option_content(39, 'flags', 'S')
        srv_msg.response_check_option_content(39, 'fqdn', f'{fqdn}' if suffix in fqdn else f'{fqdn}.{suffix}.')


def _release_lease(addr, mac):
    misc.test_procedure()
    if world.proto == 'v4':
        srv_msg.client_add_saved_option(erase=True)
        srv_msg.client_sets_value('Client', 'chaddr', mac)
        srv_msg.client_sets_value('Client', 'ciaddr', addr)
        srv_msg.client_send_msg('RELEASE')

        misc.pass_criteria()
        srv_msg.send_dont_wait_for_message()
    else:
        srv_msg.client_sets_value('Client', 'DUID', f'00:03:00:01:{mac}')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_add_saved_option(erase=True)
        srv_msg.client_send_msg('RELEASE')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'REPLY')
        srv_msg.response_check_include_option(1)
        srv_msg.response_check_include_option(2)


def _delete_lease(extra_param=None, exp_result=0):
    cmd = dict(command=f"lease{world.proto[1]}-del", arguments={})
    if isinstance(extra_param, dict):
        cmd["arguments"].update(extra_param)
    return srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result, channel='socket')


def _do_we_have_usable_key(index=0, server_id='server1'):
    for _ in range(5):
        cmd = dict(command="gss-tsig-get", arguments={"server-id": server_id})
        response = _send_through_socket(cmd)
        assert response["arguments"]["keys"][index]["status"] != "in error",\
            f'Key negotiation filed with status: {response["arguments"]["keys"][0]["tkey-status"]}'
        if response["arguments"]["keys"][index]["status"] == "usable":
            # if all is as we expected we can continue with a test
            return response["arguments"]["keys"][index]["name"]
        srv_msg.forge_sleep(1)
    assert False, "After 5 seconds we don't have valid key, it might be environment issue, please debug this."

# IMPORTANT NOTE
# HOW TO MANUALLY DEBUG THOSE TESTS WITHOUT LOCAL WINDOWS SERVER
# connect to VPN
# start windows with specific security group
# copy globally accessible IPv4 address of started vm
# use this address as "dns_addr" in all tests


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.tsig
@pytest.mark.gss
@pytest.mark.parametrize("system_and_domain", [('linux', 'example.com'), ('windows', '2019'), ('windows', '2016')])
def test_ddns_gss_tsig_manual_expiration(system_and_domain):
    """
    Simple scenario to check if we are just able to add and remove records from forward and reverse zones with
    automatically and manually generated key.

    This test also is running in v4 and v6 mode, to check updates, other tests are focused on key management
    rather than updates so those can be run in v4 only.
    """
    dns_system, my_domain = system_and_domain
    if world.proto == 'v6' and dns_system == 'windows':
        # TODO figure out why dns pkts with AAAA are dropped by windows
        pytest.skip("Windows DNS do not respond to AAAA question, manually checked - it worked nice")

    tkey_lifetime = 30
    srv_msg.forge_sleep(tkey_lifetime+5)
    if dns_system == 'windows':
        my_domain = f"win{my_domain}ad.aws.isc.org"
    dns_addr = ""

    if dns_system == 'windows':
        # THIS IS THE SECTION NEEDED FOR MANUAL DEBUG
        # dns_addr = "<global addr of vm running windows 2019>"
        # if "2016" in my_domain:
        #     dns_addr = "<global addr of vm running windows 2016>"
        dns_addr = world.f_cfg.win_dns_addr_2016
        if "2019" in my_domain:
            dns_addr = world.f_cfg.win_dns_addr_2019
        world.f_cfg.win_dns_addr = dns_addr
        world.f_cfg.dns4_addr = dns_addr
        krb.init_and_start_krb(dns_addr, my_domain)
        fabric_sudo_command(f'bash -c "kinit -k -t /tmp/forge{my_domain[3:7]}.keytab DHCP/forge.{my_domain}"')
    else:
        dns_addr = world.f_cfg.dns4_addr
        krb.init_and_start_krb(dns_addr, my_domain)
        krb.manage_kerb(procedure='restart')
        fabric_sudo_command(f'bash -c "kinit -k -t /tmp/dhcp.keytab DHCP/admin.{my_domain}"')
        fabric_sudo_command('klist')
        fabric_sudo_command('kadmin.local -q "getprincs"', ignore_errors=True)
        srv_control.use_dns_set_number(33 if world.proto == 'v4' else 34, override_dns_addr=dns_addr)
        srv_control.start_srv('DNS', 'started')

    # couple configurable values used for kea configuration and further testing
    server_id = "server1"
    key_name = ""

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24' if world.proto == 'v4' else '2001:db8:1::/64',
                                  '192.168.50.21-192.168.50.23' if world.proto == 'v4' else '2001:db8:1::51-2001:db8:1::53')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.ddns_open_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_ddns_server_options('qualifying-suffix', my_domain)
    srv_control.add_forward_ddns(f'{my_domain}.', 'EMPTY_KEY', ip_address=dns_addr)
    # windows needs four additional 0 in reverse zone
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.' if world.proto == 'v4' else '1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.' if dns_system == 'linux' else '0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                 'EMPTY_KEY', ip_address=dns_addr)

    if dns_system == 'linux':
        srv_control.ddns_add_gss_tsig(dns_addr, dns_system, tkey_lifetime=tkey_lifetime, server_id=server_id)
    else:
        srv_control.ddns_add_gss_tsig(dns_addr, dns_system, tkey_lifetime=tkey_lifetime, server_id=server_id,
                                      server_principal=f"DNS/kdc.{my_domain}@{my_domain.upper()}")
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    key_name = _do_we_have_usable_key()

    # get 1st lease, dns updated with new key
    addr = "192.168.50.21" if world.proto == 'v4' else "2001:db8:1::51"
    _get_lease(addr, f"name1.{my_domain}.", "01:01:01:01:01:11", suffix=my_domain)

    # srv_msg./wait_for_message_in_log('FQDN: [name1.example.com.]', log_file='kea.log_ddns')
    srv_msg.forge_sleep(1)
    _check_dns_record(f"name1.{my_domain}.", rdata=addr, dns_addr=dns_addr)

    # expire key
    cmd = dict(command="gss-tsig-key-expire", arguments={"key-name": key_name})
    response = _send_through_socket(cmd)
    assert response["text"] == f"GSS-TSIG key '{key_name}' expired"

    # get another lease, dns should NOT be updated
    addr2 = "192.168.50.22" if world.proto == 'v4' else "2001:db8:1::52"
    _get_lease(addr2, f"name2.{my_domain}.", "01:01:01:01:01:22", suffix=my_domain)
    srv_msg.forge_sleep(1)
    _check_dns_record(f"name2.{my_domain}.", dns_addr=dns_addr)

    cmd = dict(command="gss-tsig-rekey", arguments={"server-id": server_id})
    response = _send_through_socket(cmd)
    assert response["text"] == f"GSS-TSIG server[{server_id}] rekeyed"

    # purge one that is expired
    cmd = dict(command="gss-tsig-purge", arguments={"server-id": server_id})
    response = _send_through_socket(cmd)
    assert response["text"] == f"1 purged keys for GSS-TSIG server[{server_id}]"

    _do_we_have_usable_key()

    # resend update for second lease
    cmd = dict(command=f"lease{world.proto[1]}-resend-ddns", arguments={"ip-address": addr2})
    response = _send_through_socket(cmd, socket_name=None)  # with socket_name=None default will be used
    assert response["text"] == f"NCR generated for: {addr2}, hostname: name2.{my_domain}."

    # get 3rd lease, dns updated with new key
    addr = "192.168.50.23" if world.proto == 'v4' else "2001:db8:1::53"
    _get_lease(addr, f"name3.{my_domain}.", "01:01:01:01:01:33", suffix=my_domain)
    srv_msg.forge_sleep(1)
    _check_dns_record(f"name3.{my_domain}.", rdata=addr, dns_addr=dns_addr)
    _check_dns_record(f"name2.{my_domain}.", rdata=addr2, dns_addr=dns_addr)

    # release 3rd address should result in removing dns entry
    _release_lease(addr, "01:01:01:01:01:33")
    srv_msg.forge_sleep(2)  # slow down a bit
    _check_dns_record(f"name3.{my_domain}.", dns_addr=dns_addr)

    # second address removed via command
    _delete_lease(extra_param={"ip-address": f"{addr2}", "update-ddns": True}, exp_result=0)
    srv_msg.forge_sleep(2)
    _check_dns_record(f"name2.{my_domain}.", dns_addr=dns_addr)


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.tsig
@pytest.mark.gss
@pytest.mark.forward_reverse_add
@pytest.mark.parametrize("fallback", [False, True])
def test_ddns4_gss_tsig_fallback(fallback):
    """
    This test will check just fallback procedure and just on linux, to be sure that we didn't send
    updates we have to check DNS server logs (I've also looked into traffic between kea-ddns
    and bind 9 using tcpdump)
    """

    # this is a problem, for some reason deleting principal and all files is not enough to regenerate keys.
    # for now I will keep it that way
    srv_msg.forge_sleep(40)

    dns_addr = world.f_cfg.dns4_addr
    #
    # dns_keytab, dhcp_keytab = krb.init_and_start_krb(dns_addr)
    krb.init_and_start_krb(dns_addr, 'example.com')
    krb.manage_kerb(procedure='restart')
    fabric_sudo_command('bash -c "kinit -k -t /tmp/dhcp.keytab DHCP/admin.example.com"')
    fabric_sudo_command('klist')
    fabric_sudo_command('kadmin.local -q "getprincs"', ignore_errors=True)
    srv_control.use_dns_set_number(33)
    srv_control.start_srv('DNS', 'started')

    # couple configurable values used for kea configuration and further testing
    server_id = "server1"
    tkey_lifetime = 40

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.40-192.168.50.43')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.ddns_open_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_ddns_server_options('generated-prefix', 'four')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.ddns_add_gss_tsig(dns_addr, 'linux', tkey_lifetime=tkey_lifetime, server_id=server_id, fallback=fallback)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # let's wait for negotiations of the key:
    for _ in range(3):
        cmd = dict(command="gss-tsig-get", arguments={"server-id": server_id})
        response = _send_through_socket(cmd)
        assert response["arguments"]["keys"][0]["status"] != "in error",\
            f'Key negotiation filed with status: {response["arguments"]["keys"][0]["tkey-status"]}'
        if response["arguments"]["keys"][0]["status"] == "usable":
            # now we know that key is assigned we can check other values:
            key_name = response["arguments"]["keys"][0]["name"]  # let's save it for later
            assert response["arguments"]["fallback"] is fallback  # this needs to be False!
            break
        srv_msg.forge_sleep(1)
    else:
        assert False, "After 5 seconds we don't have valid key, it might be environment issue, please debug this."
    #
    _get_lease("192.168.50.40", "thiswillbeindns", "01:01:01:01:01:22")
    _check_dns_record("thiswillbeindns.example.com.", rdata="192.168.50.40", dns_addr=dns_addr)

    # let's expire key
    cmd = dict(command="gss-tsig-key-expire", arguments={"key-name": key_name})
    response = _send_through_socket(cmd)
    assert response["text"] == f"GSS-TSIG key '{key_name}' expired"

    # new exchange, we expect that DNS update won't be successful
    # but with fallback set to True we will try to update DNS with set to False
    # we wont. Update will be declined to we are looking for specific logs
    _get_lease("192.168.50.41", "thiswontbeindns", "01:01:01:01:01:11")
    # update will fail no matter of fallback value
    _check_dns_record("thiswontbeindns.example.com.", dns_addr=dns_addr)
    # but logs will differ
    if fallback:
        srv_msg.log_contains("update 'example.com/IN' denied", log_file="/tmp/dns.log")
    else:
        srv_msg.log_doesnt_contain("update 'example.com/IN' denied", log_file="/tmp/dns.log")


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.tsig
@pytest.mark.gss
@pytest.mark.forward_reverse_add
# @pytest.mark.parametrize("system_domain", [('linux', 'example.com'), ('windows', '2019'), ('windows', '2016')])
@pytest.mark.parametrize("system_domain", [('linux', 'example.com')])
# @pytest.mark.parametrize("system_domain", [('windows', '2019'), ('windows', '2016')])
# @pytest.mark.parametrize("system_domain", [('windows', '2019')])
def test_ddns4_gss_tsig_complex_scenario(system_domain):
    """
    This test checks multiple features related to GSS-TSIG on linux, windows 2016 and 2019.
    - Automatically negotiate new key.
    - Adding entry to forward an reverse zones using traffic and lease4-resend-ddns command.
    - Removing entry from forward and reverse zones using traffic and lease4-del command.
    - Manually expiring key and rekey.
    - Basic statistics (although something weird is in update counts, needs more investigation).
    - getting keys by server name, key name, list and all
    """
    srv_msg.forge_sleep(50)
    dns_system, my_domain = system_domain
    if dns_system == 'windows':
        my_domain = f"win{my_domain}ad.aws.isc.org"
    dns_addr = ""

    if dns_system == 'windows':
        # THIS IS THE SECTION NEEDED FOR MANUAL DEBUG
        # dns_addr = "<global addr of vm running windows 2019>"
        # if "2016" in my_domain:
        #     dns_addr = "<global addr of vm running windows 2016>"
        dns_addr = "54.224.249.185"
        if "2016" in my_domain:
            dns_addr = "54.242.20.19"
        world.f_cfg.win_dns_addr = dns_addr
        world.f_cfg.dns4_addr = dns_addr
        krb.init_and_start_krb(dns_addr, my_domain)
        fabric_sudo_command(f'bash -c "kinit -k -t /tmp/forge{my_domain[3:7]}.keytab DHCP/forge.{my_domain}"')
    else:
        dns_addr = world.f_cfg.dns4_addr
        krb.init_and_start_krb(dns_addr, my_domain)
        krb.manage_kerb(procedure='restart')
        fabric_sudo_command(f'bash -c "kinit -k -t /tmp/dhcp.keytab DHCP/admin.{my_domain}"')
        fabric_sudo_command('klist')
        fabric_sudo_command('kadmin.local -q "getprincs"', ignore_errors=True)
        srv_control.use_dns_set_number(33)
        srv_control.start_srv('DNS', 'started')

    # couple configurable values used for kea configuration and further testing
    server_id = "server1"
    tkey_lifetime = 50
    key_name = ""

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.12')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('$(SRV4_ADDR)')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.ddns_open_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_ddns_server_options('qualifying-suffix', my_domain)
    srv_control.add_forward_ddns(f'{my_domain}.', 'EMPTY_KEY', ip_address=dns_addr)
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY', ip_address=dns_addr)
    if dns_system == 'linux':
        srv_control.ddns_add_gss_tsig(dns_addr, dns_system, tkey_lifetime=tkey_lifetime, server_id=server_id)
    else:
        srv_control.ddns_add_gss_tsig(dns_addr, dns_system, tkey_lifetime=tkey_lifetime, server_id=server_id,
                                      server_principal=f"DNS/kdc.{my_domain}@{my_domain.upper()}")
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # let's wait for negotiations of the key:
    for _ in range(5):
        cmd = dict(command="gss-tsig-get", arguments={"server-id": server_id})
        response = _send_through_socket(cmd)
        assert response["arguments"]["keys"][0]["status"] != "in error",\
            f'Key negotiation filed with status: {response["arguments"]["keys"][0]["tkey-status"]}'
        if response["arguments"]["keys"][0]["status"] == "usable":
            # now we know that key is assigned we can check other values:
            key_name = response["arguments"]["keys"][0]["name"]  # let's save it for later
            assert response["arguments"]["id"] == server_id
            assert response["arguments"]["fallback"] is False
            assert response["arguments"]["ip-address"] == dns_addr
            assert response["arguments"]["tkey-protocol"] == "TCP"
            assert response["arguments"]["tkey-lifetime"] == tkey_lifetime
            assert response["arguments"]["keys"][0]["server-id"] == server_id
            assert len(response["arguments"]["keys"]) == 1
            # values calculated in functions_ddns.py:
            assert response["arguments"]["rekey-interval"] == tkey_lifetime - int(tkey_lifetime * 0.1)
            assert response["arguments"]["retry-interval"] == tkey_lifetime - int(tkey_lifetime * 0.2)
            if dns_system == "linux":
                assert response["arguments"]["client-principal"] == f"DHCP/admin.{my_domain}@{my_domain.upper()}"
                assert response["arguments"]["server-principal"] == f"DNS/server.{my_domain}@{my_domain.upper()}"
            else:
                assert response["arguments"]["server-principal"] == f"DNS/kdc.{my_domain}@{my_domain.upper()}"
                # pass
            # if all is as we expected we can continue with a test
            break
        srv_msg.forge_sleep(1)
    else:
        assert False, "After 5 seconds we don't have valid key, it might be environment issue, please debug this."

    # statistics
    cmd = dict(command="statistic-get-all", arguments={})
    stats_1 = _send_through_socket(cmd)["arguments"]
    # one key created
    assert stats_1[f"server[{server_id}].gss-tsig-key-created"][0][0] == 1
    assert stats_1["gss-tsig-key-created"][0][0] == 1

    _get_lease("192.168.50.10", "abc", "01:01:01:01:01:11", suffix=my_domain)
    _check_dns_record(f"abc.{my_domain}.", rdata="192.168.50.10", dns_addr=dns_addr)

    # check stats for single key, we made update for forward and reverse dns for one lease so we expect value 2
    cmd = dict(command="statistic-get", arguments={"name": f"key[{key_name}].update-success"})
    single_stat = _send_through_socket(cmd)["arguments"]
    assert single_stat[f"key[{key_name}].update-success"][0][0] == 2

    # check global number of updates
    cmd = dict(command="statistic-get", arguments={"name": "update-success"})
    single_stat = _send_through_socket(cmd)["arguments"]
    assert single_stat["update-success"][0][0] == 2

    cmd = dict(command="list-commands", arguments={})
    response = _send_through_socket(cmd)

    for cmd in ["gss-tsig-get",
                "gss-tsig-get-all",
                "gss-tsig-key-del",
                "gss-tsig-key-expire",
                "gss-tsig-key-get",
                "gss-tsig-list",
                "gss-tsig-purge",
                "gss-tsig-purge-all",
                "gss-tsig-rekey",
                "gss-tsig-rekey-all"]:
        assert cmd in response["arguments"]
    # get key by name
    cmd = dict(command="gss-tsig-key-get", arguments={"key-name": key_name})
    response = _send_through_socket(cmd)
    assert response["arguments"]["name"] == key_name
    assert response["arguments"]["server-id"] == server_id
    assert response["arguments"]["status"] == "usable"
    assert response["text"] == f"GSS-TSIG key '{key_name}' found"

    # let's expire key
    cmd = dict(command="gss-tsig-key-expire", arguments={"key-name": key_name})
    response = _send_through_socket(cmd)
    assert response["text"] == f"GSS-TSIG key '{key_name}' expired"

    # new exchange, we expect that DNS update won't be successful
    _get_lease("192.168.50.11", "abcfqdn", "01:01:01:01:01:22", suffix=my_domain)
    _check_dns_record(f"abcfqdn.{my_domain}.", dns_addr=dns_addr)

    # check also logs
    srv_msg.log_contains("KEY_LOOKUP_NONE hooks library lookup for a key: found no usable key", log_file="kea.log_ddns")

    # get list of all keys, check if we got back one key with correct name
    cmd = dict(command="gss-tsig-list", arguments={})
    response = _send_through_socket(cmd)
    assert len(response["arguments"]["gss-tsig-keys"]) == 1
    assert response["arguments"]["gss-tsig-keys"][0] == key_name

    # manual rekey (second key for statistics)
    cmd = dict(command="gss-tsig-rekey", arguments={"server-id": server_id})
    response = _send_through_socket(cmd)
    assert response["text"] == f"GSS-TSIG server[{server_id}] rekeyed"

    second_key_name = ""
    # AD is a bit slower so now we need to wait for new key to be ready to use:
    for _ in range(5):
        cmd = dict(command="gss-tsig-get", arguments={"server-id": server_id})
        response = _send_through_socket(cmd)
        assert response["arguments"]["keys"][1]["status"] != "in error",\
            f'Key negotiation filed with status: {response["arguments"]["keys"][0]["tkey-status"]}'
        if response["arguments"]["keys"][1]["status"] == "usable":
            # now we know that key is assigned we can check other values:
            second_key_name = response["arguments"]["keys"][1]["name"]  # let's save it for later
            # if all is as we expected we can continue with a test
            break
        srv_msg.forge_sleep(1)
    else:
        assert False, "After 5 seconds we don't have valid key, it might be environment issue, please debug this."

    # get list of all keys, check if we got back one key with correct name
    cmd = dict(command="gss-tsig-list", arguments={})
    response = _send_through_socket(cmd)
    assert len(response["arguments"]["gss-tsig-keys"]) == 2
    assert key_name in response["arguments"]["gss-tsig-keys"]
    assert second_key_name in response["arguments"]["gss-tsig-keys"]

    # since we have new key we can resend ddns update
    cmd = dict(command="lease4-resend-ddns", arguments={"ip-address": "192.168.50.11"})
    response = _send_through_socket(cmd, socket_name=None)  # with socket_name=None default will be used
    assert response["text"] == f"NCR generated for: 192.168.50.11, hostname: abcfqdn.{my_domain}."

    # and expect to have record
    srv_msg.forge_sleep(2)
    _check_dns_record(f"abcfqdn.{my_domain}.", rdata="192.168.50.11", dns_addr=dns_addr)

    cmd = dict(command="statistic-get", arguments={"name": f"key[{key_name}].update-success"})
    single_stat = _send_through_socket(cmd)["arguments"]
    # assert single_stat[f"key[{key_name}].update-success"][0][0] == 2

    cmd = dict(command="statistic-get", arguments={"name": f"key[{second_key_name}].update-success"})
    single_stat = _send_through_socket(cmd)["arguments"]
    # assert single_stat[f"key[{second_key_name}].update-success"][0][0] == 2

    cmd = dict(command="statistic-get", arguments={"name": "update-success"})
    single_stat = _send_through_socket(cmd)["arguments"]
    # assert single_stat["update-success"][0][0] == 4

    # check new key
    cmd = dict(command="gss-tsig-get-all", arguments={})
    response = _send_through_socket(cmd)
    if dns_system == 'linux':
        assert response["arguments"]["gss-tsig-servers"][0]["client-principal"] == f"DHCP/admin.{my_domain}@{my_domain.upper()}"
        assert response["arguments"]["gss-tsig-servers"][0]["server-principal"] == f"DNS/server.{my_domain}@{my_domain.upper()}"
    else:
        assert response["arguments"]["gss-tsig-servers"][0]["server-principal"] == f"DNS/kdc.{my_domain}@{my_domain.upper()}"
    key_list = response["arguments"]["gss-tsig-servers"][0]["keys"]
    new_key_name = ""
    assert len(key_list) == 2
    for k in key_list:
        if k["status"] == "usable":
            new_key_name = k["name"]
        if k["name"] == key_name:
            # old key should be expired
            assert k["status"] == "expired"

    # rekeyed all servers, (third key for statistics)
    cmd = dict(command="gss-tsig-rekey-all", arguments={})
    response = _send_through_socket(cmd)

    #  as result one more key
    cmd = dict(command="gss-tsig-get-all", arguments={})
    response = _send_through_socket(cmd)
    assert len(response["arguments"]["gss-tsig-servers"][0]["keys"]) == 3

    # purge one that is expired (one less on the list)
    cmd = dict(command="gss-tsig-purge", arguments={"server-id": server_id})
    response = _send_through_socket(cmd)
    assert response["text"] == f"1 purged keys for GSS-TSIG server[{server_id}]"

    # get removed key
    cmd = dict(command="gss-tsig-key-get", arguments={"key-name": key_name})
    response = _send_through_socket(cmd, exp_result=3)
    assert response["text"] == f"GSS-TSIG key '{key_name}' not found"

    # get new key
    cmd = dict(command="gss-tsig-key-get", arguments={"key-name": new_key_name})
    response = _send_through_socket(cmd)
    assert response["arguments"]["name"] == new_key_name
    assert response["arguments"]["server-id"] == server_id
    assert response["arguments"]["status"] == "usable"
    assert response["text"] == f"GSS-TSIG key '{new_key_name}' found"

    # one key removed
    cmd = dict(command="gss-tsig-get-all", arguments={})
    response = _send_through_socket(cmd)
    assert len(response["arguments"]["gss-tsig-servers"][0]["keys"]) == 2

    # rekeyed all servers (fourth key for statistics)
    cmd = dict(command="gss-tsig-rekey-all", arguments={})
    response = _send_through_socket(cmd)

    # one key removed, one added we are again with 3 keys on the list
    cmd = dict(command="gss-tsig-get-all", arguments={})
    response = _send_through_socket(cmd)
    assert len(response["arguments"]["gss-tsig-servers"][0]["keys"]) == 3

    # now we have 3 keys, let's get new lease
    _get_lease("192.168.50.12", "a", "01:01:01:01:01:33", suffix=my_domain)
    _check_dns_record(f"a.{my_domain}.", rdata="192.168.50.12", dns_addr=dns_addr)

    cmd = dict(command="statistic-get", arguments={"name": "update-success"})
    single_stat = _send_through_socket(cmd)["arguments"]
    # assert single_stat["update-success"][0][0] == 6

    # now let's release
    _release_lease("192.168.50.12", "01:01:01:01:01:33")
    _check_dns_record(f"a.{my_domain}.", dns_addr=dns_addr)
    _check_dns_record(f"abcfqdn.{my_domain}.", rdata="192.168.50.11", dns_addr=dns_addr)

    # now let's remove first remove, and check if dns is update correctly
    _delete_lease(extra_param={"ip-address": "192.168.50.11", "update-ddns": True}, exp_result=0)
    _check_dns_record(f"abcfqdn.{my_domain}.", dns_addr=dns_addr)

    # get statistics and compare those with previous set
    cmd = dict(command="statistic-get-all", arguments={})
    stats_2 = _send_through_socket(cmd)["arguments"]
    assert stats_2[f"server[{server_id}].gss-tsig-key-created"][0][0] == 4
    # assert stats_2["gss-tsig-key-created"][0][0] == 4
    # assert stats_2["update-success"][0][0] == 12
