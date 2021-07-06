from .multi_server_functions import fabric_sudo_command, send_content
from forge_cfg import world


def init_and_start_krb():

    # /etc/krb5.conf
    ubuntu_krb5_conf = """[libdefaults]
	default_realm = EXAMPLE.COM
	kdc_timesync = 1
	ccache_type = 4
	forwardable = true
	proxiable = true
[realms]
	EXAMPLE.COM = {{
		kdc = {dns_addr}
		admin_server = {dns_addr}
	}}
"""
    fedora_krb5_conf = """includedir /etc/krb5.conf.d/

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
    spake_preauth_groups = edwards25519
    dns_canonicalize_hostname = fallback
    qualify_shortname = ""
    default_realm = EXAMPLE.COM
    default_ccache_name = KEYRING:persistent:%{{uid}}

[realms]
    EXAMPLE.COM = {{
        kdc = {dns_addr}
        admin_server = {dns_addr}
    }}
"""
    if world.server_system == 'redhat':
        krb5_conf = fedora_krb5_conf
    else:
        krb5_conf = ubuntu_krb5_conf
    krb5_conf = krb5_conf.format(dns_addr=world.f_cfg.dns4_addr)
    send_content('krb5.conf', '/etc/krb5.conf', krb5_conf, 'krb')

    # clean principals
    result = fabric_sudo_command('kadmin.local -q "getprincs"', ignore_errors=True)
    if result.succeeded:
        for princ in result.stdout.splitlines():
            if princ.startswith(('K/M', 'kadmin', 'kiprop', 'krbtgt')):
                continue
            fabric_sudo_command('kadmin.local -q "delprinc -force %s"' % princ)

    # add forge principal with DdU3Hjb2 as password
    fabric_sudo_command('kadmin.local -q "addprinc -pw DdU3Hjb2 forge@EXAMPLE.COM"')
    fabric_sudo_command('kadmin.local -q "addprinc -randkey DNS/dns.four.example.com@EXAMPLE.COM"')
    fabric_sudo_command('kadmin.local -q "ktadd -k /tmp/aaa.keytab DNS/dns.four.example.com@EXAMPLE.COM"')
    result = fabric_sudo_command('bash -c "cat /tmp/aaa.keytab | base64"')
    fabric_sudo_command('rm /tmp/aaa.keytab')

    if world.server_system == 'redhat':
        fabric_sudo_command('systemctl restart krb5kdc kadmin')
    else:
        fabric_sudo_command('systemctl restart krb5-admin-server.service')

    return result.stdout
