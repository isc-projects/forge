# Copyright (C) 2013-2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# This file include all operations needed for installing, configuring and managing kerberos server
# as well as authenticating to it. It's windows part is based on preconfigured windows systems
# in kea internal testing network. On contrary to all other configuration procedures in forge
# all operations here can be execute just on one system, primary accessible via MGMT_ADDRESS

# pylint: disable=consider-using-f-string
# pylint: disable=f-string-without-interpolation
# pylint: disable=line-too-long
"""Manage kerberos operations."""

import os
import time

from src.forge_cfg import world
from .multi_server_functions import fabric_sudo_command, send_content, fabric_download_file, fabric_send_file


def kinit(my_domain):
    """Execute kinit on debian/redhat based systems in various configurations.

    :param my_domain: string with domain name
    :type my_domain: str
    """
    fabric_sudo_command('cat /etc/krb5.conf')
    if world.server_system == 'debian':
        fabric_sudo_command('cat /etc/krb5kdc/kdc.conf')

    manage_kerb(procedure='restart')
    if world.server_system == 'debian' and world.f_cfg.install_method == 'native':
        # kea is running using user _kea this is for now only one distinction
        # all the rest is divided between windows and linux
        if 'win' in my_domain:
            fabric_sudo_command(f'bash -c "sudo -u _kea kinit -k -t /tmp/forge{my_domain[3:7]}.keytab DHCP/forge.{my_domain}"')
        else:
            fabric_sudo_command(f'bash -c "sudo -u _kea kinit -k -t /tmp/dhcp.keytab DHCP/admin.{my_domain}"')
        fabric_sudo_command('sudo -u _kea klist', ignore_errors=True)
    elif 'win' in my_domain:
        fabric_sudo_command(f'bash -c "kinit -k -t /tmp/forge{my_domain[3:7]}.keytab DHCP/forge.{my_domain}"')
        fabric_sudo_command('klist')
    else:
        fabric_sudo_command(f'bash -c "kinit -k -t /tmp/dhcp.keytab DHCP/admin.{my_domain}"')
        fabric_sudo_command('klist')
    fabric_sudo_command('kadmin.local -q "getprincs"', ignore_errors=True)


def manage_kerb(procedure='stop', ignore=False):
    """Manage kerberos via systemctl on redhat and ubuntu.

    :param procedure: can be start, stop or restart (disable and enable not recommended)
    :type procedure: str
    :param ignore: decide if possible systemctl error should be ignored
    :type ignore: bool
    """
    if world.server_system == 'redhat':
        fabric_sudo_command(f'systemctl {procedure} krb5kdc kadmin', ignore_errors=ignore)
        if procedure in ["start", "restart"]:
            fabric_sudo_command('systemctl status krb5kdc kadmin', ignore_errors=ignore)
    else:
        fabric_sudo_command(f'systemctl {procedure} krb5-admin-server.service', ignore_errors=ignore)
        if procedure in ["start", "restart"]:
            fabric_sudo_command('systemctl status krb5-admin-server.service', ignore_errors=ignore)
    time.sleep(2)


def clean_principals():
    """Remove all non default principals."""
    result = fabric_sudo_command('kadmin.local -q "getprincs"', ignore_errors=True)
    if result.succeeded:
        for princ in result.stdout.splitlines():
            if princ.startswith(('Authenticating', 'K/M', 'kadmin', 'kiprop', 'krbtgt')):
                continue
            fabric_sudo_command('kadmin.local -q "delprinc -force %s"' % princ)


def install_krb(dns_addr, domain, key_life=2):
    """Remove, install and configure (default configuration) kerberos on ubuntu/redhat based system.

    :param dns_addr: string with ip address of dns system
    :type dns_addr: str
    :param domain: sting with domain name in which we should authenticate
    :type domain: str
    :param key_life: int, lifetime of a key in seconds
    :type key_life: int
    """
    clean_principals()
    krb_destroy()
    manage_kerb()
    if world.server_system == 'debian':
        manage_kerb(ignore=True)  # stop all, do not care about error
        fabric_sudo_command('apt-get purge -y krb5-kdc krb5-admin-server libkrb5-dev dnsutils krb5-user', ignore_errors=True)
        fabric_sudo_command('rm -rf /var/lib/krb5kdc /etc/krb5kdc /etc/krb5kdc/kadm5.acl /var/tmp/DNS_0 /var/tmp/kadmin_0 /tmp/krb5cc_0 /tmp/krb5*')
        fabric_sudo_command('sudo DEBIAN_FRONTEND=noninteractive apt install -y krb5-kdc krb5-admin-server libkrb5-dev dnsutils krb5-user')
        fabric_sudo_command('rm -rf /tmp/krb5cc_0 /tmp/krb5* /etc/krb5.conf /etc/krb5kdc/kdc.conf')
        kdc_conf = f"""[kdcdefaults]
            kdc_ports = 750,88
            extra_addresses = {dns_addr}

        [realms]
            {domain.upper()} = {{
                database_name = /var/lib/krb5kdc/principal
                default_ccache_name = FILE:/tmp/krb5cc_%{{uid}}
                admin_keytab = FILE:/etc/krb5kdc/kadm5.keytab
                acl_file = /etc/krb5kdc/kadm5.acl
                key_stash_file = /etc/krb5kdc/stash
                kdc_ports = 750,88
                max_life = 0h {key_life}m 0s
                max_renewable_life = 0d 0h {key_life}m 0s
                master_key_type = des3-hmac-sha1
                # supported_enctypes = aes256-cts:normal aes128-cts:normal
                default_principal_flags = +preauth
            }}

                """
        send_content('kdc.conf', '/etc/krb5kdc/kdc.conf', kdc_conf, 'krb')

    fabric_sudo_command('rm -rf /tmp/*.keytab')
    # /etc/krb5.conf
    krb5_conf = f"""[libdefaults]
            default_realm = {domain.upper()}
            kdc_timesync = 1
            ccache_type = 4
            forwardable = true
            proxiable = true
    [realms]
            {domain.upper()} = {{
                kdc = {dns_addr}
                admin_server = {dns_addr}
            }}
    [logging]
        default = FILE:/var/log/krb5libs.log
        kdc = FILE:/var/log/krb5kdc.log
        admin_server = FILE:/var/log/kadmind.log
    """

    send_content('krb5.conf', '/etc/krb5.conf', krb5_conf, 'krb')

    cmd = "sudo test -e /var/lib/krb5kdc/principal || printf '123\\n123' | sudo krb5_newrealm"
    if world.server_system == 'redhat':
        cmd = "sudo test -e /var/kerberos/krb5kdc/principal || printf '123\\n123' | sudo kdb5_util create -s"
    fabric_sudo_command(cmd)


def krb_destroy():
    """Execute kdestroy -A."""
    fabric_sudo_command('kdestroy -A', ignore_errors=True)


def init_and_start_krb(dns_addr, domain, key_life=2):
    """Initialize and start kerberos with OS specific configuration files.

    :param dns_addr: string with ip address of DNS server
    :type dns_addr: str
    :param domain: string with domain name
    :type domain: str
    :param key_life: int with key life time in seconds
    :type key_life: int
    """
    install_krb(dns_addr, domain, key_life)
    # /etc/krb5.conf
    ubuntu_krb5_conf = f"""[libdefaults]
    default_realm = {domain.upper()}
    kdc_timesync = 1
    ccache_type = 4
    forwardable = true
    proxiable = true
[realms]
    {domain.upper()} = {{
        kdc = {dns_addr}
        admin_server = {dns_addr}
    }}
"""
    fedora_krb5_conf = f"""includedir /etc/krb5.conf.d/

[logging]
    default = FILE:/var/log/krb5libs.log
    kdc = FILE:/var/log/krb5kdc.log
    admin_server = FILE:/var/log/kadmind.log

[libdefaults]
    dns_lookup_realm = false
    ticket_lifetime = {key_life}m
    renew_lifetime = {key_life}m
    forwardable = true
    rdns = false
    pkinit_anchors = FILE:/etc/pki/tls/certs/ca-bundle.crt
    master_key_type = des3-hmac-sha1
    spake_preauth_groups = edwards25519
    dns_canonicalize_hostname = fallback
    qualify_shortname = ""
    default_realm = {domain.upper()}
    default_ccache_name = KEYRING:persistent:%{{uid}}

[realms]
    {domain.upper()} = {{
        kdc = {dns_addr}
        admin_server = {dns_addr}
    }}
"""
    krb5_conf = ubuntu_krb5_conf
    if world.server_system == 'redhat':
        krb5_conf = fedora_krb5_conf

    send_content('krb5.conf', '/etc/krb5.conf', krb5_conf, 'krb')

    kadm5_path = '/etc/krb5kdc/kadm5.acl' if world.server_system == 'debian' else '/var/kerberos/krb5kdc/kadm5.acl'
    if 'win' in domain:
        # on each configured windows system there is keytab generated, e.g command used:
        # PS C:\Users\Administrator> ktpass -out /Users/forge/forge.keytab -mapUser forge +rndPass -mapOp set +DumpSalt -crypto AES256-SHA1 -ptype KRB5_NT_PRINCIPAL -princ DHCP/forge.win2019ad.aws.isc.org@WIN2019AD.AWS.ISC.ORG
        # PS C:\Users\Administrator> ktpass -out /Users/forge/forge.keytab -mapUser forge +rndPass -mapOp set +DumpSalt -crypto AES256-SHA1 -ptype KRB5_NT_PRINCIPAL -princ DHCP/forge.win2016ad.aws.isc.org@WIN2016AD.AWS.ISC.ORG
        # so we need to download keytabs before test for both 2016 and 2019, if something goes wrong in the future
        # we can add step here to generate this. Due to AWS setup if you are running those tests locally
        # you have to download those yourself because ssh connection will be blocked

        fabric_download_file("..\\forge\\forge.keytab",
                             os.path.join(world.cfg["test_result_dir"], f"forge{domain[3:7]}.keytab"),
                             destination_host=dns_addr,
                             user_loc='wlodek',
                             # Issue: [B106:hardcoded_password_funcarg]
                             # Possible hardcoded password: 'DdU3Hjb2'
                             password_loc='DdU3Hjb2',  # nosec B106
                             use_sudo=False)
        # than we can upload this to system that is running kea
        fabric_sudo_command("rm -rf /tmp/*.keytab")
        fabric_send_file(os.path.join(world.cfg["test_result_dir"], f"forge{domain[3:7]}.keytab"),
                         f"/tmp/forge{domain[3:7]}.keytab")

    else:
        clean_principals()
        kadm5 = f"DHCP/admin.{domain}@{domain.upper()}      *\n"
        send_content('kadm5.acl', kadm5_path, kadm5, 'krb')

        fabric_sudo_command('kadmin.local -q "addprinc -randkey DNS/server.example.com"')
        fabric_sudo_command('kadmin.local -q "addprinc -pw 123 DHCP/admin.example.com"')
        fabric_sudo_command('kadmin.local -q "ktadd -k /tmp/dns.keytab DNS/server.example.com"')
        fabric_sudo_command('kadmin.local -q "ktadd -k /tmp/dhcp.keytab DHCP/admin.example.com"')

    if 'win' not in domain:
        # we don't use dns.keytab with AD
        if world.f_cfg.dns_data_path.startswith('/etc'):
            # when installed from pkg
            fabric_sudo_command('chmod 440 /tmp/dns.keytab')
            if world.server_system == 'redhat':
                fabric_sudo_command('chown named:named /tmp/dns.keytab')
                fabric_sudo_command(f'chown root:named {kadm5_path}')
                fabric_sudo_command('chown root:named /etc/krb5.conf')
            else:
                fabric_sudo_command('chown root:bind /tmp/dns.keytab')
                fabric_sudo_command(f'chown root:bind {kadm5_path}')
        else:
            # when compiled and installed from sources
            fabric_sudo_command('chmod 440 /tmp/dns.keytab')
            fabric_sudo_command('chown root:root /tmp/dns.keytab')
            fabric_sudo_command(f'chown root:root {kadm5_path}')

    keytab_file = "/tmp/dhcp.keytab" if "win" not in domain else f"/tmp/forge{domain[3:7]}.keytab"

    fabric_sudo_command(f'chmod 440 {keytab_file}')
    if world.server_system == 'debian' and world.f_cfg.install_method == 'native':
        fabric_sudo_command(f'chown root:_kea {keytab_file}')
    else:
        fabric_sudo_command(f'chown root:root {keytab_file}')
