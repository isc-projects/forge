"""DDNS with GSS-TSIG"""

# pylint: disable=invalid-name,line-too-long

import subprocess

import pytest

import misc
import srv_msg
import srv_control
from forge_cfg import world
from softwaresupport import krb
from softwaresupport.multi_server_functions import fabric_sudo_command, fabric_run_command
from softwaresupport.bind9_server.functions import upload_dns_keytab

def run(cmd, input=None):
    subprocess.run(cmd, shell=True, check=True, timeout=60, input=input)


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.tsig
@pytest.mark.gss
@pytest.mark.forward_reverse_add
def test_ddns4_gss_tsig_sha1_forw_and_rev():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_ddns_server_options('generated-prefix', 'four')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    # srv_control.add_forward_ddns('four.example.com.', 'forge.sha1.key')
    # srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'forge.sha1.key')
    # srv_control.add_keys('forge.sha1.key', 'HMAC-SHA1', 'PN4xKZ/jDobCMlo4rpr70w==')
    srv_control.ddns_add_gss_tsig()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    dns_keytab = krb.init_and_start_krb()

    srv_control.use_dns_set_number(33)
    upload_dns_keytab(dns_keytab)
    srv_control.start_srv('DNS', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('aa.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    # misc.pass_criteria()
    # srv_msg.send_wait_for_query('MUST')
    # srv_msg.dns_option('ANSWER', expect_include=False)

    # misc.test_procedure()
    # srv_msg.client_requests_option(1)
    # srv_msg.client_send_msg('DISCOVER')

    # misc.pass_criteria()
    # srv_msg.send_wait_for_message('MUST', 'OFFER')
    # srv_msg.response_check_include_option(1)
    # srv_msg.response_check_content('yiaddr', '192.168.50.10')
    # srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    # misc.test_procedure()
    # srv_msg.client_copy_option('server_id')
    # srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    # srv_msg.client_requests_option(1)
    # srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'aa.four.example.com.')
    # srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    # srv_msg.client_does_include('Client', 'fqdn')
    # srv_msg.client_send_msg('REQUEST')

    # misc.pass_criteria()
    # srv_msg.send_wait_for_message('MUST', 'ACK')
    # srv_msg.response_check_content('yiaddr', '192.168.50.10')
    # srv_msg.response_check_include_option(1)
    # srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    # srv_msg.response_check_include_option(81)
    # srv_msg.response_check_option_content(81, 'flags', 1)
    # srv_msg.response_check_option_content(81, 'fqdn', 'aa.four.example.com.')

    # misc.test_procedure()
    # srv_msg.dns_question_record('aa.four.example.com', 'A', 'IN')
    # srv_msg.client_send_dns_query()

    # misc.pass_criteria()
    # srv_msg.send_wait_for_query('MUST')
    # srv_msg.dns_option('ANSWER')
    # srv_msg.dns_option_content('ANSWER', 'rdata', '192.168.50.10')
    # srv_msg.dns_option_content('ANSWER', 'rrname', 'aa.four.example.com.')

    # misc.test_procedure()
    # srv_msg.dns_question_record('10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    # srv_msg.client_send_dns_query()

    # misc.pass_criteria()
    # srv_msg.send_wait_for_query('MUST')
    # srv_msg.dns_option('ANSWER')
    # srv_msg.dns_option_content('ANSWER', 'rdata', 'aa.four.example.com.')
    # srv_msg.dns_option_content('ANSWER', 'rrname', '10.50.168.192.in-addr.arpa.')

    fabric_run_command('kdestroy -A')
    fabric_run_command('bash -c "printf DdU3Hjb2 | kinit forge@EXAMPLE.COM"')

    script = 'gsstsig\\nserver %s\\nupdate add four.example.com. 120 TXT "Hello from Kerberos"\\nsend\\n' % world.f_cfg.dns4_addr
    fabric_run_command("printf '%s' | nsupdate -g" % script)
