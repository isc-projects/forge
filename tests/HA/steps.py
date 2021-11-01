# Copyright (C) 2020 Internet Systems Consortium.
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND INTERNET SYSTEMS CONSORTIUM
# DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# INTERNET SYSTEMS CONSORTIUM BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
# FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
# WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# pylint: disable=invalid-name,line-too-long

import random
import misc
import srv_control
import srv_msg
from forge_cfg import world


HOT_STANDBY = {
    "mode": "hot-standby",
    "peers": [{
        "auto-failover": True,
        "name": "server1",
        "role": "primary",
        "url": f"http://{world.f_cfg.mgmt_address}:8000/"
    }, {
        "auto-failover": True,
        "name": "server2",
        "role": "standby",
        "url": f"http://{world.f_cfg.mgmt_address_2}:8000/"
    }],
    "state-machine": {
        "states": []
    }
}

LOAD_BALANCING = {
    "mode": "load-balancing",
    "peers": [{
        "auto-failover": True,
        "name": "server1",
        "role": "primary",
        "url": f"http://{world.f_cfg.mgmt_address}:8000/"
    }, {
        "auto-failover": True,
        "name": "server2",
        "role": "secondary",
        "url": f"http://{world.f_cfg.mgmt_address_2}:8000/"
    }],
    "state-machine": {
        "states": []
    }
}

PASSIVE_BACKUP = {
    "mode": "passive-backup",
    "peers": [{
        "auto-failover": True,
        "name": "server1",
        "role": "primary",
        "url": f"http://{world.f_cfg.mgmt_address}:8000/"
    }, {
        "auto-failover": True,
        "name": "server2",
        "role": "backup",
        "url": f"http://{world.f_cfg.mgmt_address_2}:8000/"
    }],
    "state-machine": {
        "states": []
    }
}


def send_heartbeat(dhcp_version='v6', exp_result=0, dest=world.f_cfg.mgmt_address, exp_failed=False):
    return send_command(cmd={"command": "ha-heartbeat"}, dhcp_version=dhcp_version, exp_result=exp_result,
                        dest=dest, exp_failed=exp_failed)


def send_command(cmd=None, dhcp_version='v6', exp_result=0, dest=world.f_cfg.mgmt_address, exp_failed=False):
    """
    send command to CA with http
    :param cmd: command, if not set ha-heartbeat will be send
    :param dhcp_version: dhcp version
    :param exp_result: expected result
    :param dest: address of remote server
    :param exp_failed: do we expect command to fail
    :return: json response
    """
    service = 'dhcp6' if dhcp_version == 'v6' else 'dhcp4'
    assert cmd is not None, "We can't send empty command"
    if "service" not in cmd:
        cmd.update({"service": [service]})
    result = srv_msg.send_ctrl_cmd_via_http(command=cmd, address=dest, exp_result=exp_result, exp_failed=exp_failed)
    if result is None:
        return None
    return result[0]


def wait_until_ha_state(state, dest=world.f_cfg.mgmt_address, retry=20, sleep=3, dhcp_version='v6'):
    """
    Send ha-heartbeat messages to server as long as we get expected state, HA tend to be slow so it's
    way of active sleep
    :param state: what state we are waiting for
    :param dest: management address of server
    :param retry: number of retries before we declare defeat
    :param sleep: sleep between retries
    :param dhcp_version: version of dhcp
    :return: last response
    """
    for _ in range(retry):
        srv_msg.forge_sleep(sleep, 'seconds')
        resp = send_heartbeat(dest=dest, dhcp_version=dhcp_version)
        if resp["arguments"]["state"] == state:
            return resp
    assert False, "After %d retries HA did NOT reach '%s' state" % (retry, state)
    return {}  # let's keep pylint error quiet


def _increase_mac(mac, rand=False):
    """
    Recalculate mac address by: keep first octet unchanged (we can change it in test to make sure that
    consecutive steps will generate different sets, change second octet always by 1, all the rest we can
    change by one or random number between 3 and 20. Used rand=True to generate test data
    :param mac: mac address as string
    :return: increased mac address as string
    """
    mac = mac.split(":")
    new_mac = (int(mac[0], 16),)
    new_mac += (int(mac[1], 16) + 1,)
    for i in range(2, 6):
        a = random.randint(3, 20) if rand else 1
        if int(mac[i], 16) + a > 255:
            mac[i] = 1
        new_mac += (int(mac[i], 16) + a,)
    return "%02x:%02x:%02x:%02x:%02x:%02x" % new_mac


def generate_leases(leases_count=1, iaid=1, iapd=1, dhcp_version='v6', mac="01:02:0c:03:0a:00"):
    """
    Function will perform message exchanges to get specified number of leases,
    will assert if at the end number of leases will be smaller
    :param leases_count: how many leases we want to generate
    :param iaid: how many v6 addresses we want in single exchange (ignored for v4)
    :param iapd: how many prefixes we want in single exchange (ignored for v4)
    :param dhcp_version: version of dhcp
    :param mac: mac we will start increase, to get different set of macs increase just first octet
    :return: list of leases generated
    """
    all_leases = []
    tmp = world.f_cfg.show_packets_from
    world.f_cfg.show_packets_from = ""
    if dhcp_version == 'v6':
        for _ in range(leases_count):
            mac = _increase_mac(mac)
            duid = "00:03:00:01:" + mac
            ia_1 = random.randint(2000, 7000)
            pd_1 = random.randint(7001, 9999)

            misc.test_procedure()
            srv_msg.client_sets_value('Client', 'DUID', duid)
            srv_msg.client_does_include('Client', 'client-id')

            for ia in range(iaid):
                this_iaid = ia_1 + ia
                srv_msg.client_sets_value('Client', 'ia_id', this_iaid)
                srv_msg.client_does_include('Client', 'IA-NA')
            for pd in range(iapd):
                this_iapd = pd_1 + pd
                srv_msg.client_sets_value('Client', 'ia_pd', this_iapd)
                srv_msg.client_does_include('Client', 'IA-PD')
            srv_msg.client_send_msg('SOLICIT')

            misc.pass_criteria()
            srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
            srv_msg.response_check_include_option(1)
            srv_msg.response_check_include_option(2)
            if iaid > 0:
                srv_msg.response_check_include_option(3)
            if iapd > 0:
                srv_msg.response_check_include_option(25)

            misc.test_procedure()
            srv_msg.client_sets_value('Client', 'DUID', duid)
            srv_msg.client_does_include('Client', 'client-id')

            # this should be copy not generated
            for ia in range(iaid):
                srv_msg.client_sets_value('Client', 'ia_id', ia_1 + ia)
                srv_msg.client_does_include('Client', 'IA-NA')

            for pd in range(iapd):
                srv_msg.client_sets_value('Client', 'ia_pd', pd_1 + pd)
                srv_msg.client_does_include('Client', 'IA-PD')

            srv_msg.client_copy_option('server-id')
            srv_msg.client_send_msg('REQUEST')

            misc.pass_criteria()
            # TODO check server-id!
            srv_msg.send_wait_for_message('MUST', 'REPLY')
            srv_msg.response_check_include_option(1)
            srv_msg.response_check_include_option(2)
            if iaid > 0:
                srv_msg.response_check_include_option(3)
                # srv_msg.response_check_include_option(4)
                # some times load balancing can't assign we cant check it for now
            if iapd > 0:
                srv_msg.response_check_include_option(25)
                # srv_msg.response_check_include_option(26)

            all_leases += srv_msg.get_all_leases()

    elif dhcp_version in ['v4', 'bootp']:
        # This is v4 DORA which we also check in BOOTP's case.

        # When testing BOOTP, send half (rounded downwards) of the leases with
        # v4 and half with BOOTP.
        if dhcp_version == 'bootp':
            leases_count = int(leases_count / 2)

        for _ in range(leases_count):
            mac = _increase_mac(mac)
            misc.test_procedure()
            srv_msg.client_sets_value('Client', 'chaddr', mac)
            srv_msg.client_requests_option(1)
            srv_msg.client_send_msg('DISCOVER')

            misc.pass_criteria()
            srv_msg.send_wait_for_message('MUST', 'OFFER')
            yiaddr = world.srvmsg[0].yiaddr

            misc.test_procedure()
            srv_msg.client_sets_value('Client', 'chaddr', mac)
            srv_msg.client_copy_option('server_id')
            srv_msg.client_does_include_with_value('requested_addr', yiaddr)
            srv_msg.client_requests_option(1)
            srv_msg.client_send_msg('REQUEST')

            misc.pass_criteria()
            srv_msg.send_wait_for_message('MUST', 'ACK')
            srv_msg.response_check_content('yiaddr', yiaddr)

            all_leases.append(srv_msg.get_all_leases())

    # In the end, test BOOTP as well, if enabled.
    if dhcp_version == 'bootp':
        for i in range(leases_count + 1, 2 * leases_count):
            assert i < 256
            srv_msg.BOOTP_REQUEST_and_BOOTP_REPLY('192.168.50.' + str(i), chaddr='00:01:02:03:04:%0.2x' % i)

    world.f_cfg.show_packets_from = tmp
    return all_leases


def send_increased_elapsed_time(msg_count, elapsed=3, dhcp_version='v6',
                                mac="05:02:0c:03:0a:00", duid="00:03:00:01:05:02:0c:03:0a:00"):
    """
    Send messages with increased elapsed time (v6) or secs field (v4) to simulate one node failure
    :param msg_count: how many messages send
    :param elapsed: value of time we are starting with
    :param dhcp_version: dhcp version
    :param mac: in load-balancing v4 we need to send specific mac addresses
    :param duid: in load-balancing v6 we need to send specific duids
    """
    tmp = world.f_cfg.show_packets_from
    world.f_cfg.show_packets_from = ""
    if dhcp_version == 'v6':
        # v6 is in milliseconds not seconds so let's multiply elapsed time
        elapsed *= 100
        for i in range(msg_count):
            if isinstance(duid, list):
                # if we have a list just take last one
                my_duid = duid[-1]
                duid = duid[:-1]
            else:
                # if list were not given calculate new
                mac = _increase_mac(duid[12:])
                my_duid = duid[:12] + mac
                duid = my_duid
            ia_1 = random.randint(1000, 1500)
            misc.test_procedure()
            srv_msg.client_sets_value('Client', 'DUID', my_duid)
            srv_msg.client_does_include('Client', 'client-id')
            srv_msg.client_sets_value('Client', 'ia_id', ia_1)
            srv_msg.client_does_include('Client', 'IA-NA')
            srv_msg.client_sets_value('Client', 'elapsedtime', elapsed + i)
            srv_msg.client_does_include('Client', 'time-elapsed')

            srv_msg.client_send_msg('SOLICIT')

            misc.pass_criteria()
            srv_msg.send_dont_wait_for_message()

    elif dhcp_version == 'v4':
        for i in range(msg_count):
            if isinstance(mac, list):
                my_mac = mac[-1]
                mac = mac[:-1]
            else:
                mac = _increase_mac(mac)
                my_mac = mac
            misc.test_procedure()
            srv_msg.client_sets_value('Client', 'chaddr', my_mac)
            srv_msg.client_sets_value('Client', 'secs', elapsed + i)
            srv_msg.client_requests_option(1)
            srv_msg.client_send_msg('DISCOVER')

            misc.pass_criteria()
            srv_msg.send_dont_wait_for_message()

    world.f_cfg.show_packets_from = tmp


def load_hook_libraries(dhcp_version, hook_order):
    if hook_order == 'alphabetical':
        if dhcp_version == 'bootp':
            srv_control.add_hooks('libdhcp_bootp.so')
        srv_control.add_ha_hook('libdhcp_ha.so')
        srv_control.add_hooks('libdhcp_lease_cmds.so')
    else:
        srv_control.add_hooks('libdhcp_lease_cmds.so')
        srv_control.add_ha_hook('libdhcp_ha.so')
        if dhcp_version == 'bootp':
            srv_control.add_hooks('libdhcp_bootp.so')
