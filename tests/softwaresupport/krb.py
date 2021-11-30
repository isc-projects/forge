import os
from .multi_server_functions import fabric_sudo_command, send_content, fabric_download_file
from forge_cfg import world


def manage_kerb(procedure='stop'):
    if world.server_system == 'redhat':
        fabric_sudo_command(f'systemctl {procedure} krb5kdc kadmin')
    else:
        fabric_sudo_command(f'systemctl {procedure} krb5-admin-server.service')

    if procedure in ["start", "restart"]:
        if world.server_system == 'redhat':
            fabric_sudo_command('systemctl status krb5kdc kadmin')
        else:
            fabric_sudo_command('systemctl status krb5-admin-server.service')


def install_krb(dns_addr, domain, key_life=2):
    result = fabric_sudo_command('kadmin.local -q "getprincs"', ignore_errors=True)
    if result.succeeded:
        for princ in result.stdout.splitlines():
            if princ.startswith(('K/M', 'kadmin', 'kiprop', 'krbtgt')):
                continue
            fabric_sudo_command('kadmin.local -q "delprinc -force %s"' % princ)

    fabric_sudo_command('kdestroy -A', ignore_errors=True)
    manage_kerb()

    fabric_sudo_command('apt-get purge -y krb5-kdc krb5-admin-server libkrb5-dev dnsutils krb5-user')
    fabric_sudo_command('rm -rf /var/lib/krb5kdc /etc/krb5kdc /etc/krb5kdc/kadm5.acl /var/tmp/DNS_0 /var/tmp/kadmin_0 /tmp/krb5cc_0 /tmp/krb5*')
    fabric_sudo_command('rm -rf /tmp/dhcp.keytab /tmp/dns.keytab /tmp/krb5cc_0 /tmp/krb5*')
    fabric_sudo_command('sudo DEBIAN_FRONTEND=noninteractive apt install -y krb5-kdc krb5-admin-server libkrb5-dev dnsutils krb5-user')

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
    cmd = "sudo test -e /var/lib/krb5kdc/principal || printf '123\\n123' | sudo krb5_newrealm"
    fabric_sudo_command(cmd)

    manage_kerb(procedure='restart')


def init_and_start_krb(dns_addr, domain, key_life=2):
    install_krb(dns_addr, key_life)
    fabric_sudo_command('kdestroy -A', ignore_errors=True)
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
    ticket_lifetime = 24h
    renew_lifetime = 7d
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
    if world.server_system == 'redhat':
        krb5_conf = fedora_krb5_conf
    else:
        krb5_conf = ubuntu_krb5_conf
    send_content('krb5.conf', '/etc/krb5.conf', krb5_conf, 'krb')

    if 'win' in domain:
        # on each configured windows system there is keatab generated, e.g command used:
        # PS C:\Users\Administrator> ktpass -out /Users/forge/forge.keytab -mapUser forge +rndPass -mapOp set +DumpSalt -crypto AES256-SHA1 -ptype KRB5_NT_PRINCIPAL -princ DHCP/forge.win2019ad.aws.isc.org@WIN2019AD.AWS.ISC.ORG
        # so we need to download keytabs before test for both 2016 and 2019, if something goes wrong in the future
        # we can add step here to generate this. Due to AWS setup if you are running those tests locally
        # you have to download those yourself because ssh connection will be blocked
        if not os.path.exists(f"/tmp/forge{domain[3:7]}.keytab"):
            fabric_download_file("\\Users\\forge\\forge.keytab", f"/tmp/forge{domain[3:7]}.keytab",
                                 destination_host=dns_addr,
                                 user_loc='forge',
                                 password_loc='DdU3Hjb2')

    else:
        # clean principals
        result = fabric_sudo_command('kadmin.local -q "getprincs"', ignore_errors=True)
        if result.succeeded:
            for princ in result.stdout.splitlines():
                if princ.startswith(('K/M', 'kadmin', 'kiprop', 'krbtgt')):
                    continue
                fabric_sudo_command('kadmin.local -q "delprinc -force %s"' % princ)
        kadm5 = f"DHCP/admin.{domain}@{domain.upper()}      *\n"
        send_content('kadm5.acl', '/etc/krb5kdc/kadm5.acl', kadm5, 'krb')

        fabric_sudo_command('kadmin.local -q "addprinc -randkey DNS/server.example.com"')
        fabric_sudo_command('kadmin.local -q "addprinc -pw 123 DHCP/admin.example.com"')
        fabric_sudo_command('kadmin.local -q "ktadd -k /tmp/dns.keytab DNS/server.example.com"')
        fabric_sudo_command('kadmin.local -q "ktadd -k /tmp/dhcp.keytab DHCP/admin.example.com"')

    manage_kerb()
