# Copyright (C) 2013 Internet Systems Consortium.
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

# Author: Wlodzimierz Wencel

config_file_set = {
    #number : [named.conf, rndc.conf, fwd.db, rev.db ]
    1: ["""
options {
    directory "${data_path}";  // Working directory
    listen-on-v6 port ${dns_port} { ${dns_addr}; };
    allow-query-cache { none; };       // Do not allow access to cache
    allow-update { any; };              // This is the default
    allow-query { any; };              // This is the default
    recursion no;                      // Do not provide recursive service
};

zone "1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa" {
     type master;
     file "rev.db";
     notify no;
     allow-update { any; };              // This is the default
     allow-query { any; };              // This is the default

};

zone "six.example.com" {
     type master;
     file "fwd.db";
     notify no;
     allow-update { any; };              // This is the default
     allow-transfer { any; };
     allow-query { any; };              // This is the default

};

#Use with the following in named.conf, adjusting the allow list as needed:
key "rndc-key" {
    algorithm hmac-md5;
    secret "+kOEcvxPTCPxzGqB5n5FeA==";
};
controls {
    inet 127.0.0.1 port 53001
    allow { 127.0.0.1; } keys { "rndc-key"; };
};
logging{
  channel simple_log {
    file "/tmp/dns.log";
    severity debug 99;
    print-time yes;
    print-severity yes;
    print-category yes;
  };
  category default{
    simple_log;
  };
  category queries{
    simple_log;
  };
};
""", """
key "rndc-key" {
	algorithm hmac-md5;
	secret "+kOEcvxPTCPxzGqB5n5FeA==";
};

options {
	default-key "rndc-key";
	default-server 127.0.0.1;
	default-port 953;
};
""", """$ORIGIN .
$TTL 86400	; 1 day
six.example.com		IN SOA	dns6-1.six.example.com. mail.six.example.com. (
				107        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				2592000    ; expire (4 weeks 2 days)
				3600       ; minimum (1 hour)
				)
			NS	dns6-1.six.example.com.
$ORIGIN six.example.com.
dns6-1			AAAA	2001:db8:1::1
nanny6			AAAA	2001:db8:1::10
""", """$ORIGIN .
$TTL 3600	; 1 hour
1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa IN SOA	dns6-1.six.example.com. mail.six.example.com. (
				102        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				604800     ; expire (1 week)
				3600       ; minimum (1 hour)
				)
			NS	dns6-1.six.example.com.
$ORIGIN 1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.
0			PTR	nanny6.six.exmaple.com.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.
"""],
    2: ["""
options {
    directory "${data_path}";  // Working directory
    listen-on-v6 port ${dns_port} { ${dns_addr}; };
    allow-query-cache { none; };       // Do not allow access to cache
    allow-update { any; };              // This is the default
    allow-query { any; };              // This is the default
    recursion no;                      // Do not provide recursive service
};

zone "1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa" {
     type master;
     file "rev.db";
     notify no;
     allow-update { any; };              // This is the default
     allow-query { any; };              // This is the default

};

zone "six.example.com" {
     type master;
     file "fwd.db";
     notify no;
     allow-update { any; };              // This is the default
     allow-transfer { any; };
     allow-query { any; };              // This is the default

};

#Use with the following in named.conf, adjusting the allow list as needed:
key "rndc-key" {
    algorithm hmac-md5;
    secret "+kOEcvxPTCPxzGqB5n5FeA==";
};
controls {
    inet 127.0.0.1 port 53001
    allow { 127.0.0.1; } keys { "rndc-key"; };
};
logging{
  channel simple_log {
    file "/tmp/dns.log";
    severity debug 99;
    print-time yes;
    print-severity yes;
    print-category yes;
  };
  category default{
    simple_log;
  };
  category queries{
    simple_log;
  };
};
""", """
key "rndc-key" {
	algorithm hmac-md5;
	secret "+kOEcvxPTCPxzGqB5n5FeA==";
};

options {
	default-key "rndc-key";
	default-server 127.0.0.1;
	default-port 953;
};
""", """$ORIGIN .
$TTL 86400	; 1 day
six.example.com		IN SOA	dns6-1.six.example.com. mail.six.example.com. (
				107        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				2592000    ; expire (4 weeks 2 days)
				3600       ; minimum (1 hour)
				)
			NS	dns6-1.six.example.com.
$ORIGIN six.example.com.
dns6-1			AAAA	2001:db8:1::1
""", """$ORIGIN .
$TTL 3600	; 1 hour
1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa IN SOA	dns6-1.six.example.com. mail.six.example.com. (
				102        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				604800     ; expire (1 week)
				3600       ; minimum (1 hour)
				)
			NS	dns6-1.six.example.com.
$ORIGIN 1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.
0			PTR	dns6-1.six.example.com.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.
"""],
3: ["""
options {
    directory "${data_path}";  // Working directory
    listen-on-v6 port ${dns_port} { ${dns_addr}; };
    allow-query-cache { none; };       // Do not allow access to cache
    allow-update { any; };              // This is the default
    allow-query { any; };              // This is the default
    recursion no;                      // Do not provide recursive service
};

zone "1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa" {
     type master;
     file "rev.db";
     notify no;
     allow-update { key forge.sha1.key; };
     allow-query { any; };

};

zone "six.example.com" {
     type master;
     file "fwd.db";
     notify no;
     allow-update { key forge.sha1.key; };
     allow-query { any; };

};

key "forge.sha1.key" {
    algorithm hmac-sha1;
    secret "PN4xKZ/jDobCMlo4rpr70w==";
};

#Use with the following in named.conf, adjusting the allow list as needed:
key "rndc-key" {
    algorithm hmac-md5;
    secret "+kOEcvxPTCPxzGqB5n5FeA==";
};
controls {
    inet 127.0.0.1 port 53001
    allow { 127.0.0.1; } keys { "rndc-key"; };
};
logging{
  channel simple_log {
    file "/tmp/dns.log";
    severity debug 99;
    print-time yes;
    print-severity yes;
    print-category yes;
  };
  category default{
    simple_log;
  };
  category queries{
    simple_log;
  };
};
""", """
key "rndc-key" {
	algorithm hmac-md5;
	secret "+kOEcvxPTCPxzGqB5n5FeA==";
};

options {
	default-key "rndc-key";
	default-server 127.0.0.1;
	default-port 953;
};
""", """$ORIGIN .
$TTL 86400	; 1 day
six.example.com		IN SOA	dns6-1.six.example.com. mail.six.example.com. (
				107        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				2592000    ; expire (4 weeks 2 days)
				3600       ; minimum (1 hour)
				)
			NS	dns6-1.six.example.com.
$ORIGIN six.example.com.
dns6-1			AAAA	2001:db8:1::1
nanny6			AAAA	2001:db8:1::10
""", """$ORIGIN .
$TTL 3600	; 1 hour
1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa IN SOA	dns6-1.six.example.com. mail.six.example.com. (
				102        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				604800     ; expire (1 week)
				3600       ; minimum (1 hour)
				)
			NS	dns6-1.six.example.com.
$ORIGIN 1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.
0			PTR	nanny6.six.exmaple.com.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.
"""],
4: ["""
options {
    directory "${data_path}";  // Working directory
    listen-on-v6 port ${dns_port} { ${dns_addr}; };
    allow-query-cache { none; };       // Do not allow access to cache
    allow-update { any; };              // This is the default
    allow-query { any; };              // This is the default
    recursion no;                      // Do not provide recursive service
};

zone "1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa" {
     type master;
     file "rev.db";
     notify no;
     allow-update { key forge.sha224.key; };
     allow-query { any; };

};

zone "six.example.com" {
     type master;
     file "fwd.db";
     notify no;
     allow-update { key forge.sha224.key; };
     allow-query { any; };

};

key "forge.sha224.key" {
    algorithm hmac-sha224;
    secret "TxAiO5TRKkFyHSCa4erQZQ==";
};

#Use with the following in named.conf, adjusting the allow list as needed:
key "rndc-key" {
    algorithm hmac-md5;
    secret "+kOEcvxPTCPxzGqB5n5FeA==";
};
controls {
    inet 127.0.0.1 port 53001
    allow { 127.0.0.1; } keys { "rndc-key"; };
};
logging{
  channel simple_log {
    file "/tmp/dns.log";
    severity debug 99;
    print-time yes;
    print-severity yes;
    print-category yes;
  };
  category default{
    simple_log;
  };
  category queries{
    simple_log;
  };
};
""", """
key "rndc-key" {
	algorithm hmac-md5;
	secret "+kOEcvxPTCPxzGqB5n5FeA==";
};

options {
	default-key "rndc-key";
	default-server 127.0.0.1;
	default-port 953;
};
""", """$ORIGIN .
$TTL 86400	; 1 day
six.example.com		IN SOA	dns6-1.six.example.com. mail.six.example.com. (
				107        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				2592000    ; expire (4 weeks 2 days)
				3600       ; minimum (1 hour)
				)
			NS	dns6-1.six.example.com.
$ORIGIN six.example.com.
dns6-1			AAAA	2001:db8:1::1
nanny6			AAAA	2001:db8:1::10
""", """$ORIGIN .
$TTL 3600	; 1 hour
1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa IN SOA	dns6-1.six.example.com. mail.six.example.com. (
				102        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				604800     ; expire (1 week)
				3600       ; minimum (1 hour)
				)
			NS	dns6-1.six.example.com.
$ORIGIN 1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.
0			PTR	nanny6.six.exmaple.com.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.
"""],
5: ["""
options {
    directory "${data_path}";  // Working directory
    listen-on-v6 port ${dns_port} { ${dns_addr}; };
    allow-query-cache { none; };       // Do not allow access to cache
    allow-update { any; };              // This is the default
    allow-query { any; };              // This is the default
    recursion no;                      // Do not provide recursive service
};

zone "1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa" {
     type master;
     file "rev.db";
     notify no;
     allow-update { key forge.sha256.key; };
     allow-query { any; };

};

zone "six.example.com" {
     type master;
     file "fwd.db";
     notify no;
     allow-update { key forge.sha256.key; };
     allow-query { any; };

};

key "forge.sha256.key" {
    algorithm hmac-sha256;
    secret "5AYMijv0rhZJyQqK/caV7g==";
};

#Use with the following in named.conf, adjusting the allow list as needed:
key "rndc-key" {
    algorithm hmac-md5;
    secret "+kOEcvxPTCPxzGqB5n5FeA==";
};
controls {
    inet 127.0.0.1 port 53001
    allow { 127.0.0.1; } keys { "rndc-key"; };
};
logging{
  channel simple_log {
    file "/tmp/dns.log";
    severity debug 99;
    print-time yes;
    print-severity yes;
    print-category yes;
  };
  category default{
    simple_log;
  };
  category queries{
    simple_log;
  };
};
""", """
key "rndc-key" {
	algorithm hmac-md5;
	secret "+kOEcvxPTCPxzGqB5n5FeA==";
};

options {
	default-key "rndc-key";
	default-server 127.0.0.1;
	default-port 953;
};
""", """$ORIGIN .
$TTL 86400	; 1 day
six.example.com		IN SOA	dns6-1.six.example.com. mail.six.example.com. (
				107        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				2592000    ; expire (4 weeks 2 days)
				3600       ; minimum (1 hour)
				)
			NS	dns6-1.six.example.com.
$ORIGIN six.example.com.
dns6-1			AAAA	2001:db8:1::1
nanny6			AAAA	2001:db8:1::10
""", """$ORIGIN .
$TTL 3600	; 1 hour
1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa IN SOA	dns6-1.six.example.com. mail.six.example.com. (
				102        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				604800     ; expire (1 week)
				3600       ; minimum (1 hour)
				)
			NS	dns6-1.six.example.com.
$ORIGIN 1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.
0			PTR	nanny6.six.exmaple.com.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.
"""],
6: ["""
options {
    directory "${data_path}";  // Working directory
    listen-on-v6 port ${dns_port} { ${dns_addr}; };
    allow-query-cache { none; };       // Do not allow access to cache
    allow-update { any; };              // This is the default
    allow-query { any; };              // This is the default
    recursion no;                      // Do not provide recursive service
};

zone "1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa" {
     type master;
     file "rev.db";
     notify no;
     allow-update { key forge.sha384.key; };
     allow-query { any; };

};

zone "six.example.com" {
     type master;
     file "fwd.db";
     notify no;
     allow-update { key forge.sha384.key; };
     allow-query { any; };

};

key "forge.sha384.key" {
    algorithm hmac-sha384;
    secret "21upyvp7zcG0S2PB4+kuQQ==";
};

#Use with the following in named.conf, adjusting the allow list as needed:
key "rndc-key" {
    algorithm hmac-md5;
    secret "+kOEcvxPTCPxzGqB5n5FeA==";
};
controls {
    inet 127.0.0.1 port 53001
    allow { 127.0.0.1; } keys { "rndc-key"; };
};
logging{
  channel simple_log {
    file "/tmp/dns.log";
    severity debug 99;
    print-time yes;
    print-severity yes;
    print-category yes;
  };
  category default{
    simple_log;
  };
  category queries{
    simple_log;
  };
};
""", """
key "rndc-key" {
	algorithm hmac-md5;
	secret "+kOEcvxPTCPxzGqB5n5FeA==";
};

options {
	default-key "rndc-key";
	default-server 127.0.0.1;
	default-port 953;
};
""", """$ORIGIN .
$TTL 86400	; 1 day
six.example.com		IN SOA	dns6-1.six.example.com. mail.six.example.com. (
				107        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				2592000    ; expire (4 weeks 2 days)
				3600       ; minimum (1 hour)
				)
			NS	dns6-1.six.example.com.
$ORIGIN six.example.com.
dns6-1			AAAA	2001:db8:1::1
nanny6			AAAA	2001:db8:1::10
""", """$ORIGIN .
$TTL 3600	; 1 hour
1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa IN SOA	dns6-1.six.example.com. mail.six.example.com. (
				102        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				604800     ; expire (1 week)
				3600       ; minimum (1 hour)
				)
			NS	dns6-1.six.example.com.
$ORIGIN 1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.
0			PTR	nanny6.six.exmaple.com.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.
"""],
6: ["""
options {
    directory "${data_path}";  // Working directory
    listen-on-v6 port ${dns_port} { ${dns_addr}; };
    allow-query-cache { none; };       // Do not allow access to cache
    allow-update { any; };              // This is the default
    allow-query { any; };              // This is the default
    recursion no;                      // Do not provide recursive service
};

zone "1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa" {
     type master;
     file "rev.db";
     notify no;
     allow-update { key forge.sha384.key; };
     allow-query { any; };

};

zone "six.example.com" {
     type master;
     file "fwd.db";
     notify no;
     allow-update { key forge.sha384.key; };
     allow-query { any; };

};

key "forge.sha384.key" {
    algorithm hmac-sha384;
    secret "21upyvp7zcG0S2PB4+kuQQ==";
};

#Use with the following in named.conf, adjusting the allow list as needed:
key "rndc-key" {
    algorithm hmac-md5;
    secret "+kOEcvxPTCPxzGqB5n5FeA==";
};
controls {
    inet 127.0.0.1 port 53001
    allow { 127.0.0.1; } keys { "rndc-key"; };
};
logging{
  channel simple_log {
    file "/tmp/dns.log";
    severity debug 99;
    print-time yes;
    print-severity yes;
    print-category yes;
  };
  category default{
    simple_log;
  };
  category queries{
    simple_log;
  };
};
""", """
key "rndc-key" {
	algorithm hmac-md5;
	secret "+kOEcvxPTCPxzGqB5n5FeA==";
};

options {
	default-key "rndc-key";
	default-server 127.0.0.1;
	default-port 953;
};
""", """$ORIGIN .
$TTL 86400	; 1 day
six.example.com		IN SOA	dns6-1.six.example.com. mail.six.example.com. (
				107        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				2592000    ; expire (4 weeks 2 days)
				3600       ; minimum (1 hour)
				)
			NS	dns6-1.six.example.com.
$ORIGIN six.example.com.
dns6-1			AAAA	2001:db8:1::1
nanny6			AAAA	2001:db8:1::10
""", """$ORIGIN .
$TTL 3600	; 1 hour
1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa IN SOA	dns6-1.six.example.com. mail.six.example.com. (
				102        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				604800     ; expire (1 week)
				3600       ; minimum (1 hour)
				)
			NS	dns6-1.six.example.com.
$ORIGIN 1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.
0			PTR	nanny6.six.exmaple.com.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.
"""],
7: ["""
options {
    directory "${data_path}";  // Working directory
    listen-on-v6 port ${dns_port} { ${dns_addr}; };
    allow-query-cache { none; };       // Do not allow access to cache
    allow-update { any; };              // This is the default
    allow-query { any; };              // This is the default
    recursion no;                      // Do not provide recursive service
};

zone "1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa" {
     type master;
     file "rev.db";
     notify no;
     allow-update { key forge.sha512.key; };
     allow-query { any; };

};

zone "six.example.com" {
     type master;
     file "fwd.db";
     notify no;
     allow-update { key forge.sha512.key; };
     allow-query { any; };

};

key "forge.sha512.key" {
    algorithm hmac-sha512;
    secret "jBng5D6QL4f8cfLUUwE7OQ==";
};

#Use with the following in named.conf, adjusting the allow list as needed:
key "rndc-key" {
    algorithm hmac-md5;
    secret "+kOEcvxPTCPxzGqB5n5FeA==";
};
controls {
    inet 127.0.0.1 port 53001
    allow { 127.0.0.1; } keys { "rndc-key"; };
};
logging{
  channel simple_log {
    file "/tmp/dns.log";
    severity debug 99;
    print-time yes;
    print-severity yes;
    print-category yes;
  };
  category default{
    simple_log;
  };
  category queries{
    simple_log;
  };
};
""", """
key "rndc-key" {
	algorithm hmac-md5;
	secret "+kOEcvxPTCPxzGqB5n5FeA==";
};

options {
	default-key "rndc-key";
	default-server 127.0.0.1;
	default-port 953;
};
""", """$ORIGIN .
$TTL 86400	; 1 day
six.example.com		IN SOA	dns6-1.six.example.com. mail.six.example.com. (
				107        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				2592000    ; expire (4 weeks 2 days)
				3600       ; minimum (1 hour)
				)
			NS	dns6-1.six.example.com.
$ORIGIN six.example.com.
dns6-1			AAAA	2001:db8:1::1
nanny6			AAAA	2001:db8:1::10
""", """$ORIGIN .
$TTL 3600	; 1 hour
1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa IN SOA	dns6-1.six.example.com. mail.six.example.com. (
				102        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				604800     ; expire (1 week)
				3600       ; minimum (1 hour)
				)
			NS	dns6-1.six.example.com.
$ORIGIN 1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.
0			PTR	nanny6.six.exmaple.com.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.
"""],
8: ["""
options {
    directory "${data_path}";  // Working directory
    listen-on-v6 port ${dns_port} { ${dns_addr}; };
    allow-query-cache { none; };       // Do not allow access to cache
    allow-update { any; };              // This is the default
    allow-query { any; };              // This is the default
    recursion no;                      // Do not provide recursive service
};

zone "1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa" {
     type master;
     file "rev.db";
     notify no;
     allow-update { key forge.md5.key; };
     allow-query { any; };

};

zone "six.example.com" {
     type master;
     file "fwd.db";
     notify no;
     allow-update { key forge.md5.key; };
     allow-query { any; };

};

key "forge.md5.key" {
    algorithm hmac-md5;
    secret "bX3Hs+fG/tThidQPuhK1mA==";
};

#Use with the following in named.conf, adjusting the allow list as needed:
key "rndc-key" {
    algorithm hmac-md5;
    secret "+kOEcvxPTCPxzGqB5n5FeA==";
};
controls {
    inet 127.0.0.1 port 53001
    allow { 127.0.0.1; } keys { "rndc-key"; };
};
logging{
  channel simple_log {
    file "/tmp/dns.log";
    severity debug 99;
    print-time yes;
    print-severity yes;
    print-category yes;
  };
  category default{
    simple_log;
  };
  category queries{
    simple_log;
  };
};
""", """
key "rndc-key" {
	algorithm hmac-md5;
	secret "+kOEcvxPTCPxzGqB5n5FeA==";
};

options {
	default-key "rndc-key";
	default-server 127.0.0.1;
	default-port 953;
};
""", """$ORIGIN .
$TTL 86400	; 1 day
six.example.com		IN SOA	dns6-1.six.example.com. mail.six.example.com. (
				107        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				2592000    ; expire (4 weeks 2 days)
				3600       ; minimum (1 hour)
				)
			NS	dns6-1.six.example.com.
$ORIGIN six.example.com.
dns6-1			AAAA	2001:db8:1::1
nanny6			AAAA	2001:db8:1::10
""", """$ORIGIN .
$TTL 3600	; 1 hour
1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa IN SOA	dns6-1.six.example.com. mail.six.example.com. (
				102        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				604800     ; expire (1 week)
				3600       ; minimum (1 hour)
				)
			NS	dns6-1.six.example.com.
$ORIGIN 1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.
0			PTR	nanny6.six.exmaple.com.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.
"""],
9: ["""
options {
    directory "${data_path}";  // Working directory
    listen-on-v6 port ${dns_port} { ${dns_addr}; };
    allow-query-cache { none; };       // Do not allow access to cache
    allow-update { any; };              // This is the default
    allow-query { any; };              // This is the default
    recursion no;                      // Do not provide recursive service
};

zone "1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa" {
     type master;
     file "rev.db";
     notify no;
     allow-update { key forge.sha512.key; };
     allow-query { any; };

};

zone "six.example.com" {
     type master;
     file "fwd.db";
     notify no;
     allow-update { key forge.md5.key; };
     allow-query { any; };

};
key "forge.sha512.key" {
    algorithm hmac-sha512;
    secret "jBng5D6QL4f8cfLUUwE7OQ==";
};

key "forge.md5.key" {
    algorithm hmac-md5;
    secret "bX3Hs+fG/tThidQPuhK1mA==";
};

#Use with the following in named.conf, adjusting the allow list as needed:
key "rndc-key" {
    algorithm hmac-md5;
    secret "+kOEcvxPTCPxzGqB5n5FeA==";
};
controls {
    inet 127.0.0.1 port 53001
    allow { 127.0.0.1; } keys { "rndc-key"; };
};
logging{
  channel simple_log {
    file "/tmp/dns.log";
    severity debug 99;
    print-time yes;
    print-severity yes;
    print-category yes;
  };
  category default{
    simple_log;
  };
  category queries{
    simple_log;
  };
};
""", """
key "rndc-key" {
	algorithm hmac-md5;
	secret "+kOEcvxPTCPxzGqB5n5FeA==";
};

options {
	default-key "rndc-key";
	default-server 127.0.0.1;
	default-port 953;
};
""", """$ORIGIN .
$TTL 86400	; 1 day
six.example.com		IN SOA	dns6-1.six.example.com. mail.six.example.com. (
				107        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				2592000    ; expire (4 weeks 2 days)
				3600       ; minimum (1 hour)
				)
			NS	dns6-1.six.example.com.
$ORIGIN six.example.com.
dns6-1			AAAA	2001:db8:1::1
nanny6			AAAA	2001:db8:1::10
""", """$ORIGIN .
$TTL 3600	; 1 hour
1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa IN SOA	dns6-1.six.example.com. mail.six.example.com. (
				102        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				604800     ; expire (1 week)
				3600       ; minimum (1 hour)
				)
			NS	dns6-1.six.example.com.
$ORIGIN 1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.
0			PTR	nanny6.six.exmaple.com.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.
"""],

    10: ["", "", "", ""],
    11: ["", "", "", ""],
    12: ["", "", "", ""],
    13: ["", "", "", ""],
    14: ["", "", "", ""],
    15: ["", "", "", ""],

    ## v4 configs!
20: ["""
options {
    directory "${data_path}";  // Working directory
    listen-on port ${dns_port} { ${dns_addr}; };
    allow-query-cache { none; };       // Do not allow access to cache
    allow-update { any; };              // This is the default
    allow-query { any; };              // This is the default
    recursion no;                      // Do not provide recursive service
};

zone "50.168.192.in-addr.arpa." {
     type master;
     file "rev.db";
     notify no;
     allow-update { any; };              // This is the default
     allow-query { any; };              // This is the default

};

zone "four.example.com" {
     type master;
     file "fwd.db";
     notify no;
     allow-update { any; };              // This is the default
     allow-transfer { any; };
     allow-query { any; };              // This is the default

};

#Use with the following in named.conf, adjusting the allow list as needed:
key "rndc-key" {
    algorithm hmac-md5;
    secret "+kOEcvxPTCPxzGqB5n5FeA==";
};
controls {
    inet 127.0.0.1 port 53001  allow { 127.0.0.1; } keys { "rndc-key"; };
};
logging{
  channel simple_log {
    file "/tmp/dns.log";
    severity debug 99;
    print-time yes;
    print-severity yes;
    print-category yes;
  };
  category default{
    simple_log;
  };
  category queries{
    simple_log;
  };
};
""", """
key "rndc-key" {
	algorithm hmac-md5;
	secret "+kOEcvxPTCPxzGqB5n5FeA==";
};

options {
	default-key "rndc-key";
	default-server 127.0.0.1;
	default-port 953;
};
""", """$ORIGIN .
$TTL 86400	; 1 day
four.example.com	IN SOA	dns.four.example.com. mail.four.example.com. (
				106        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				2592000    ; expire (4 weeks 2 days)
				3600       ; minimum (1 hour)
				)
			NS	dns.four.example.com.
$ORIGIN four.example.com.
dns			A	172.16.1.1
""", """$TTL 1h	; Default TTL
@ IN SOA dns1.four.example.com. hostmaster.example.com. (
	100	; serial
	1h		; slave refresh interval
	15m		; slave retry interval
	1w		; slave copy expire time
	1h		; NXDOMAIN cache time
	)

	NS	dns1.four.example.com.

$ORIGIN 50.168.192.in-addr.arpa.

1 	IN	PTR      dns1.four.example.com.
"""],

21: ["""
options {
    directory "${data_path}";  // Working directory
    listen-on port ${dns_port} { ${dns_addr}; };
    allow-query-cache { none; };       // Do not allow access to cache
    allow-update { any; };              // This is the default
    allow-query { any; };              // This is the default
    recursion no;                      // Do not provide recursive service
};

zone "50.168.192.in-addr.arpa." {
     type master;
     file "rev.db";
     notify no;
     allow-update { key forge.sha1.key; };
     allow-query { any; };              // This is the default

};

zone "four.example.com" {
     type master;
     file "fwd.db";
     notify no;
     allow-update { key forge.sha1.key; };
     allow-transfer { any; };
     allow-query { any; };              // This is the default

};

key "forge.sha1.key" {
    algorithm hmac-sha1;
    secret "PN4xKZ/jDobCMlo4rpr70w==";
};

#Use with the following in named.conf, adjusting the allow list as needed:
key "rndc-key" {
    algorithm hmac-md5;
    secret "+kOEcvxPTCPxzGqB5n5FeA==";
};

controls {
    inet 127.0.0.1 port 53001  allow { 127.0.0.1; } keys { "rndc-key"; };
};

logging{
  channel simple_log {
    file "/tmp/dns.log";
    severity debug 99;
    print-time yes;
    print-severity yes;
    print-category yes;
  };
  category default{
    simple_log;
  };
  category queries{
    simple_log;
  };
};
""", """
key "rndc-key" {
	algorithm hmac-md5;
	secret "+kOEcvxPTCPxzGqB5n5FeA==";
};

options {
	default-key "rndc-key";
	default-server 127.0.0.1;
	default-port 953;
};
""", """$ORIGIN .
$TTL 86400	; 1 day
four.example.com	IN SOA	dns.four.example.com. mail.four.example.com. (
				106        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				2592000    ; expire (4 weeks 2 days)
				3600       ; minimum (1 hour)
				)
			NS	dns.four.example.com.
$ORIGIN four.example.com.
dns			A	172.16.1.1
""", """$TTL 1h	; Default TTL
@ IN SOA dns1.four.example.com. hostmaster.example.com. (
	100	; serial
	1h		; slave refresh interval
	15m		; slave retry interval
	1w		; slave copy expire time
	1h		; NXDOMAIN cache time
	)

	NS	dns1.four.example.com.

$ORIGIN 50.168.192.in-addr.arpa.

1 	IN	PTR      dns1.four.example.com.
"""],
22: ["""
options {
    directory "${data_path}";  // Working directory
    listen-on port ${dns_port} { ${dns_addr}; };
    allow-query-cache { none; };       // Do not allow access to cache
    allow-update { any; };              // This is the default
    allow-query { any; };              // This is the default
    recursion no;                      // Do not provide recursive service
};

zone "50.168.192.in-addr.arpa." {
     type master;
     file "rev.db";
     notify no;
     allow-update { key forge.sha224.key; };
     allow-query { any; };              // This is the default

};

zone "four.example.com" {
     type master;
     file "fwd.db";
     notify no;
     allow-update { key forge.sha224.key; };
     allow-transfer { any; };
     allow-query { any; };              // This is the default

};

key "forge.sha224.key" {
    algorithm hmac-sha224;
    secret "TxAiO5TRKkFyHSCa4erQZQ==";
};

#Use with the following in named.conf, adjusting the allow list as needed:
key "rndc-key" {
    algorithm hmac-md5;
    secret "+kOEcvxPTCPxzGqB5n5FeA==";
};

controls {
    inet 127.0.0.1 port 53001  allow { 127.0.0.1; } keys { "rndc-key"; };
};

logging{
  channel simple_log {
    file "/tmp/dns.log";
    severity debug 99;
    print-time yes;
    print-severity yes;
    print-category yes;
  };
  category default{
    simple_log;
  };
  category queries{
    simple_log;
  };
};
""", """
key "rndc-key" {
	algorithm hmac-md5;
	secret "+kOEcvxPTCPxzGqB5n5FeA==";
};

options {
	default-key "rndc-key";
	default-server 127.0.0.1;
	default-port 953;
};
""", """$ORIGIN .
$TTL 86400	; 1 day
four.example.com	IN SOA	dns.four.example.com. mail.four.example.com. (
				106        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				2592000    ; expire (4 weeks 2 days)
				3600       ; minimum (1 hour)
				)
			NS	dns.four.example.com.
$ORIGIN four.example.com.
dns			A	172.16.1.1
""", """$TTL 1h	; Default TTL
@ IN SOA dns1.four.example.com. hostmaster.example.com. (
	100	; serial
	1h		; slave refresh interval
	15m		; slave retry interval
	1w		; slave copy expire time
	1h		; NXDOMAIN cache time
	)

	NS	dns1.four.example.com.

$ORIGIN 50.168.192.in-addr.arpa.

1 	IN	PTR      dns1.four.example.com.
"""],
23: ["""
options {
    directory "${data_path}";  // Working directory
    listen-on port ${dns_port} { ${dns_addr}; };
    allow-query-cache { none; };       // Do not allow access to cache
    allow-update { any; };              // This is the default
    allow-query { any; };              // This is the default
    recursion no;                      // Do not provide recursive service
};

zone "50.168.192.in-addr.arpa." {
     type master;
     file "rev.db";
     notify no;
     allow-update { key forge.sha256.key; };
     allow-query { any; };              // This is the default

};

zone "four.example.com" {
     type master;
     file "fwd.db";
     notify no;
     allow-update { key forge.sha256.key; };
     allow-transfer { any; };
     allow-query { any; };              // This is the default

};

key "forge.sha256.key" {
    algorithm hmac-sha256;
    secret "5AYMijv0rhZJyQqK/caV7g==";
};

#Use with the following in named.conf, adjusting the allow list as needed:
key "rndc-key" {
    algorithm hmac-md5;
    secret "+kOEcvxPTCPxzGqB5n5FeA==";
};

controls {
    inet 127.0.0.1 port 53001  allow { 127.0.0.1; } keys { "rndc-key"; };
};

logging{
  channel simple_log {
    file "/tmp/dns.log";
    severity debug 99;
    print-time yes;
    print-severity yes;
    print-category yes;
  };
  category default{
    simple_log;
  };
  category queries{
    simple_log;
  };
};
""", """
key "rndc-key" {
	algorithm hmac-md5;
	secret "+kOEcvxPTCPxzGqB5n5FeA==";
};

options {
	default-key "rndc-key";
	default-server 127.0.0.1;
	default-port 953;
};
""", """$ORIGIN .
$TTL 86400	; 1 day
four.example.com	IN SOA	dns.four.example.com. mail.four.example.com. (
				106        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				2592000    ; expire (4 weeks 2 days)
				3600       ; minimum (1 hour)
				)
			NS	dns.four.example.com.
$ORIGIN four.example.com.
dns			A	172.16.1.1
""", """$TTL 1h	; Default TTL
@ IN SOA dns1.four.example.com. hostmaster.example.com. (
	100	; serial
	1h		; slave refresh interval
	15m		; slave retry interval
	1w		; slave copy expire time
	1h		; NXDOMAIN cache time
	)

	NS	dns1.four.example.com.

$ORIGIN 50.168.192.in-addr.arpa.

1 	IN	PTR      dns1.four.example.com.
"""],
24: ["""
options {
    directory "${data_path}";  // Working directory
    listen-on port ${dns_port} { ${dns_addr}; };
    allow-query-cache { none; };       // Do not allow access to cache
    allow-update { any; };              // This is the default
    allow-query { any; };              // This is the default
    recursion no;                      // Do not provide recursive service
};

zone "50.168.192.in-addr.arpa." {
     type master;
     file "rev.db";
     notify no;
     allow-update { key forge.sha384.key; };
     allow-query { any; };              // This is the default

};

zone "four.example.com" {
     type master;
     file "fwd.db";
     notify no;
     allow-update { key forge.sha384.key; };
     allow-transfer { any; };
     allow-query { any; };              // This is the default

};

key "forge.sha384.key" {
    algorithm hmac-sha384;
    secret "21upyvp7zcG0S2PB4+kuQQ==";
};

#Use with the following in named.conf, adjusting the allow list as needed:
key "rndc-key" {
    algorithm hmac-md5;
    secret "+kOEcvxPTCPxzGqB5n5FeA==";
};

controls {
    inet 127.0.0.1 port 53001  allow { 127.0.0.1; } keys { "rndc-key"; };
};

logging{
  channel simple_log {
    file "/tmp/dns.log";
    severity debug 99;
    print-time yes;
    print-severity yes;
    print-category yes;
  };
  category default{
    simple_log;
  };
  category queries{
    simple_log;
  };
};
""", """
key "rndc-key" {
	algorithm hmac-md5;
	secret "+kOEcvxPTCPxzGqB5n5FeA==";
};

options {
	default-key "rndc-key";
	default-server 127.0.0.1;
	default-port 953;
};
""", """$ORIGIN .
$TTL 86400	; 1 day
four.example.com	IN SOA	dns.four.example.com. mail.four.example.com. (
				106        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				2592000    ; expire (4 weeks 2 days)
				3600       ; minimum (1 hour)
				)
			NS	dns.four.example.com.
$ORIGIN four.example.com.
dns			A	172.16.1.1
""", """$TTL 1h	; Default TTL
@ IN SOA dns1.four.example.com. hostmaster.example.com. (
	100	; serial
	1h		; slave refresh interval
	15m		; slave retry interval
	1w		; slave copy expire time
	1h		; NXDOMAIN cache time
	)

	NS	dns1.four.example.com.

$ORIGIN 50.168.192.in-addr.arpa.

1 	IN	PTR      dns1.four.example.com.
"""],
25: ["""
options {
    directory "${data_path}";  // Working directory
    listen-on port ${dns_port} { ${dns_addr}; };
    allow-query-cache { none; };       // Do not allow access to cache
    allow-update { any; };              // This is the default
    allow-query { any; };              // This is the default
    recursion no;                      // Do not provide recursive service
};

zone "50.168.192.in-addr.arpa." {
     type master;
     file "rev.db";
     notify no;
     allow-update { key forge.sha512.key; };
     allow-query { any; };              // This is the default

};

zone "four.example.com" {
     type master;
     file "fwd.db";
     notify no;
     allow-update { key forge.sha512.key; };
     allow-transfer { any; };
     allow-query { any; };              // This is the default

};

key "forge.sha512.key" {
    algorithm hmac-sha512;
    secret "jBng5D6QL4f8cfLUUwE7OQ==";
};

#Use with the following in named.conf, adjusting the allow list as needed:
key "rndc-key" {
    algorithm hmac-md5;
    secret "+kOEcvxPTCPxzGqB5n5FeA==";
};

controls {
    inet 127.0.0.1 port 53001  allow { 127.0.0.1; } keys { "rndc-key"; };
};

logging{
  channel simple_log {
    file "/tmp/dns.log";
    severity debug 99;
    print-time yes;
    print-severity yes;
    print-category yes;
  };
  category default{
    simple_log;
  };
  category queries{
    simple_log;
  };
};
""", """
key "rndc-key" {
	algorithm hmac-md5;
	secret "+kOEcvxPTCPxzGqB5n5FeA==";
};

options {
	default-key "rndc-key";
	default-server 127.0.0.1;
	default-port 953;
};
""", """$ORIGIN .
$TTL 86400	; 1 day
four.example.com	IN SOA	dns.four.example.com. mail.four.example.com. (
				106        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				2592000    ; expire (4 weeks 2 days)
				3600       ; minimum (1 hour)
				)
			NS	dns.four.example.com.
$ORIGIN four.example.com.
dns			A	172.16.1.1
""", """$TTL 1h	; Default TTL
@ IN SOA dns1.four.example.com. hostmaster.example.com. (
	100	; serial
	1h		; slave refresh interval
	15m		; slave retry interval
	1w		; slave copy expire time
	1h		; NXDOMAIN cache time
	)

	NS	dns1.four.example.com.

$ORIGIN 50.168.192.in-addr.arpa.

1 	IN	PTR      dns1.four.example.com.
"""],
26: ["""
options {
    directory "${data_path}";  // Working directory
    listen-on port ${dns_port} { ${dns_addr}; };
    allow-query-cache { none; };       // Do not allow access to cache
    allow-update { any; };              // This is the default
    allow-query { any; };              // This is the default
    recursion no;                      // Do not provide recursive service
};

zone "50.168.192.in-addr.arpa." {
     type master;
     file "rev.db";
     notify no;
     allow-update { key forge.md5.key; };
     allow-query { any; };              // This is the default

};

zone "four.example.com" {
     type master;
     file "fwd.db";
     notify no;
     allow-update { key forge.md5.key; };
     allow-transfer { any; };
     allow-query { any; };              // This is the default

};

key "forge.md5.key" {
    algorithm hmac-md5;
    secret "bX3Hs+fG/tThidQPuhK1mA==";
};

#Use with the following in named.conf, adjusting the allow list as needed:
key "rndc-key" {
    algorithm hmac-md5;
    secret "+kOEcvxPTCPxzGqB5n5FeA==";
};

controls {
    inet 127.0.0.1 port 53001  allow { 127.0.0.1; } keys { "rndc-key"; };
};

logging{
  channel simple_log {
    file "/tmp/dns.log";
    severity debug 99;
    print-time yes;
    print-severity yes;
    print-category yes;
  };
  category default{
    simple_log;
  };
  category queries{
    simple_log;
  };
};
""", """
key "rndc-key" {
	algorithm hmac-md5;
	secret "+kOEcvxPTCPxzGqB5n5FeA==";
};

options {
	default-key "rndc-key";
	default-server 127.0.0.1;
	default-port 953;
};
""", """$ORIGIN .
$TTL 86400	; 1 day
four.example.com	IN SOA	dns.four.example.com. mail.four.example.com. (
				106        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				2592000    ; expire (4 weeks 2 days)
				3600       ; minimum (1 hour)
				)
			NS	dns.four.example.com.
$ORIGIN four.example.com.
dns			A	172.16.1.1
""", """$TTL 1h	; Default TTL
@ IN SOA dns1.four.example.com. hostmaster.example.com. (
	100	; serial
	1h		; slave refresh interval
	15m		; slave retry interval
	1w		; slave copy expire time
	1h		; NXDOMAIN cache time
	)

	NS	dns1.four.example.com.

$ORIGIN 50.168.192.in-addr.arpa.

1 	IN	PTR      dns1.four.example.com.
"""],
27: ["""
options {
    directory "${data_path}";  // Working directory
    listen-on port ${dns_port} { ${dns_addr}; };
    allow-query-cache { none; };       // Do not allow access to cache
    allow-update { any; };              // This is the default
    allow-query { any; };              // This is the default
    recursion no;                      // Do not provide recursive service
};

zone "50.168.192.in-addr.arpa." {
     type master;
     file "rev.db";
     notify no;
     allow-update { key forge.sha512.key; };
     allow-query { any; };              // This is the default

};

zone "four.example.com" {
     type master;
     file "fwd.db";
     notify no;
     allow-update { key forge.md5.key; };
     allow-transfer { any; };
     allow-query { any; };              // This is the default

};

key "forge.md5.key" {
    algorithm hmac-md5;
    secret "bX3Hs+fG/tThidQPuhK1mA==";
};

key "forge.sha512.key" {
    algorithm hmac-sha512;
    secret "jBng5D6QL4f8cfLUUwE7OQ==";
};

#Use with the following in named.conf, adjusting the allow list as needed:
key "rndc-key" {
    algorithm hmac-md5;
    secret "+kOEcvxPTCPxzGqB5n5FeA==";
};

controls {
    inet 127.0.0.1 port 53001  allow { 127.0.0.1; } keys { "rndc-key"; };
};

logging{
  channel simple_log {
    file "/tmp/dns.log";
    severity debug 99;
    print-time yes;
    print-severity yes;
    print-category yes;
  };
  category default{
    simple_log;
  };
  category queries{
    simple_log;
  };
};
""", """
key "rndc-key" {
	algorithm hmac-md5;
	secret "+kOEcvxPTCPxzGqB5n5FeA==";
};

options {
	default-key "rndc-key";
	default-server 127.0.0.1;
	default-port 953;
};
""", """$ORIGIN .
$TTL 86400	; 1 day
four.example.com	IN SOA	dns.four.example.com. mail.four.example.com. (
				106        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				2592000    ; expire (4 weeks 2 days)
				3600       ; minimum (1 hour)
				)
			NS	dns.four.example.com.
$ORIGIN four.example.com.
dns			A	172.16.1.1
""", """$TTL 1h	; Default TTL
@ IN SOA dns1.four.example.com. hostmaster.example.com. (
	100	; serial
	1h		; slave refresh interval
	15m		; slave retry interval
	1w		; slave copy expire time
	1h		; NXDOMAIN cache time
	)

	NS	dns1.four.example.com.

$ORIGIN 50.168.192.in-addr.arpa.

1 	IN	PTR      dns1.four.example.com.
"""]





}
#["filename","""file""","filename","file"]












keys = '''/* $Id: bind.keys,v 1.7 2011/01/03 23:45:07 each Exp $ */
# The bind.keys file is used to override the built-in DNSSEC trust anchors
# which are included as part of BIND 9.  As of the current release, the only
# trust anchors it contains are those for the DNS root zone ("."), and for
# the ISC DNSSEC Lookaside Validation zone ("dlv.isc.org").  Trust anchors
# for any other zones MUST be configured elsewhere; if they are configured
# here, they will not be recognized or used by named.
#
# The built-in trust anchors are provided for convenience of configuration.
# They are not activated within named.conf unless specifically switched on.
# To use the built-in root key, set "dnssec-validation auto;" in
# named.conf options.  To use the built-in DLV key, set
# "dnssec-lookaside auto;".  Without these options being set,
# the keys in this file are ignored.
#
# This file is NOT expected to be user-configured.
#
# These keys are current as of January 2011.  If any key fails to
# initialize correctly, it may have expired.  In that event you should
# replace this file with a current version.  The latest version of
# bind.keys can always be obtained from ISC at https://www.isc.org/bind-keys.

managed-keys {
	# ISC DLV: See https://www.isc.org/solutions/dlv for details.
        # NOTE: This key is activated by setting "dnssec-lookaside auto;"
        # in named.conf.
	dlv.isc.org. initial-key 257 3 5 "BEAAAAPHMu/5onzrEE7z1egmhg/WPO0+juoZrW3euWEn4MxDCE1+lLy2
		brhQv5rN32RKtMzX6Mj70jdzeND4XknW58dnJNPCxn8+jAGl2FZLK8t+
		1uq4W+nnA3qO2+DL+k6BD4mewMLbIYFwe0PG73Te9fZ2kJb56dhgMde5
		ymX4BI/oQ+cAK50/xvJv00Frf8kw6ucMTwFlgPe+jnGxPPEmHAte/URk
		Y62ZfkLoBAADLHQ9IrS2tryAe7mbBZVcOwIeU/Rw/mRx/vwwMCTgNboM
		QKtUdvNXDrYJDSHZws3xiRXF1Rf+al9UmZfSav/4NWLKjHzpT59k/VSt
		TDN0YUuWrBNh";

	# ROOT KEY: See https://data.iana.org/root-anchors/root-anchors.xml
	# for current trust anchor information.
        # NOTE: This key is activated by setting "dnssec-validation auto;"
        # in named.conf.
	. initial-key 257 3 8 "AwEAAagAIKlVZrpC6Ia7gEzahOR+9W29euxhJhVVLOyQbSEW0O8gcCjF
		FVQUTf6v58fLjwBd0YI0EzrAcQqBGCzh/RStIoO8g0NfnfL2MTJRkxoX
		bfDaUeVPQuYEhg37NZWAJQ9VnMVDxP/VHL496M/QZxkjf5/Efucp2gaD
		X6RS6CXpoY68LsvPVjR0ZSwzz1apAzvN9dlzEheX7ICJBBtuA6G3LQpz
		W5hOA2hzCTMjJPJ8LbqF6dsV6DoBQzgul0sGIcGOYl7OyQdXfZ57relS
		Qageu+ipAdTTJ25AsRTAoub8ONGcLmqrAmRLKBP1dfwhYB4N7knNnulq
		QxA+Uk1ihz0=";
};'''
