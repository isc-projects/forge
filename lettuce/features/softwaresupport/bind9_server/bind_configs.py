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
	directory "/home/test/dns/namedb";  // Working #directory
	listen-on port 53 {192.168.59.150;};
	allow-query-cache { none; };       // Do not allow access to cache
	allow-update { any; };              // This is the default
	allow-query { any; };              // This is the default
	recursion no;                      // Do not provide recursive service
};

// Provide a reverse mapping for v4
zone "2.0.192.in-addr.arpa" {
     type master;
     file "rev.db";
     notify no;
};

key "rndc-key" {
 	algorithm hmac-md5;
	secret "y4Ztg2jvErIp/9KZ5ZKtIg==";
};

controls {
	inet 127.0.0.1 port 953
 		allow { 127.0.0.1; } keys { "rndc-key"; };
};




// We are the master server for four.example.com
zone "four.example.com" {
     type master;
     file "fwd.db";
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

""",
"""
key "rndc-key" {
	algorithm hmac-md5;
	secret "y4Ztg2jvErIp/9KZ5ZKtIg==";
};

options {
	default-key "rndc-key";
	default-server 127.0.0.1;
	default-port 953;
};
""",
"""
$ORIGIN .
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
hoot			A	192.0.2.10
nanny			A	192.0.2.11
			AAAA	2001:db8:1::11
$TTL 4000	; 1 hour 6 minutes 40 seconds
one			A	192.0.2.200
			DHCID	( AAABJv4/px6+FWdByTnTSqrFrtCvQ388N2GhndyTH3SS
				IpM= ) ; 48704 177 32
""",
"""
$ORIGIN .
$TTL 3600	; 1 hour
2.0.192.in-addr.arpa	IN SOA	dns1.four.example.com. hostmaster.example.com. (
				102        ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				604800     ; expire (1 week)
				3600       ; minimum (1 hour)
				)
			NS	dns1.four.example.com.
$ORIGIN 2.0.192.in-addr.arpa.
1			PTR	dns1.four.example.com.
10			PTR	hoot.four.example.com.
$TTL 4000	; 1 hour 6 minutes 40 seconds
100			PTR	one.four.example.com.
			DHCID	( AAABJv4/px6+FWdByTnTSqrFrtCvQ388N2GhndyTH3SS
				IpM= ) ; 48643 0 32
$TTL 3600	; 1 hour
11			PTR	hooter.four.example.com.
$TTL 4000	; 1 hour 6 minutes 40 seconds
200			PTR	one.four.example.com.
			DHCID	( AAABJv4/px6+FWdByTnTSqrFrtCvQ388N2GhndyTH3SS
				IpM= ) ; 48856 1 32
"""],
    2: ["", "", "", ""],
    3: ["", "", "", ""],
    4: ["", "", "", ""],
    5: ["", "", "", ""],
    6: ["", "", "", ""],
    7: ["", "", "", ""],
    8: ["", "", "", ""],
    9: ["", "", "", ""],
    10: ["", "", "", ""],
    11: ["", "", "", ""],
    12: ["", "", "", ""],
    13: ["", "", "", ""],
    14: ["", "", "", ""],
    15: ["", "", "", ""]
}