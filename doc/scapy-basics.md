This is a collection of loose notes about Scapy, with some
command examples. I (tomek) use it as scratchbook for various
things. Unless you want to learn how scapy works, you can safely
ignore it.





dhcp_discover = Ether(dst="ff:ff:ff:ff:ff:ff")/IP(src="0.0.0.0",dst="255.255.255.255")/UDP(sport=68,dport=67)/BOOTP(chaddr=hw)/DHCP(options=[("message-type","discover"),("param_req_list", "abc"), "end"])
sendp(dhcp_discover, iface="eth1")

ans, unans = srp(dhcp_discover, multi=True)

---
conf.checkIPaddr = False
conf.iface="eth1"
fam,hw = get_if_raw_hwaddr(conf.iface)
discover = Ether(dst="ff:ff:ff:ff:ff:ff")/IP(src="0.0.0.0",dst="255.255.255.255")
discover /= UDP(sport=68,dport=67)/BOOTP(chaddr=hw)
options = [("message-type","discover"),("param_req_list","a"),("router", "1.2.3.4"), "end"]
sendp(discover/DHCP(options = options), iface="eth1")
ans, unans = srp(discover/DHCP(options=options), iface="eth1", multi=True)
