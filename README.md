ISC Forge
=========

ISC Forge is an open source DHCP conformance validation framework. It is a
joint project done by Internet Systems Consortium, a non profit company based
in Redwood City, California and students from Gdansk Univesity of Technology.

The goal of this project is to develop open source validation framework that
will be able to validate DHCPv4 and DHCPv6 implementations. Its primary focus
is on RFC compliance, but other validation aspects will be covered as well.

In principle the framework can be extended to cover any RFC compliant DHCP
software, but we're focusing on Kea. In various times, there was some partial
support added also for [ISC DHCP](https://gitlab.isc.org/isc-projects/dhcp) and
[Dibbler](https://klub.com.pl/dhcpv6/). Support for implementations other than
Kea is experimental at best.

The framework is written in Python and uses the following libraries:
- Scapy (for packet generation/parsing)
- Pytest (for test management)
- Fabric (for remote server configuration)

Participants
============
- Włodzimierz Wencel (ISC)
- Tomek Mrugalski (ISC, engineering manager)
- Andrei Pavel (ISC)
- Marcin Godzina (ISC)

Former participants
===================
- Michał Nowikowski (ISC)
- Stephen Morris (ISC, engineering manager)
- Marcin Siodelski (ISC)
- Thomas Markwalder (ISC)
- Rafał Jankowski (Gdansk University, DHCPv4 validation)
- Maciek Fijałkowski (Gdansk University, DHCPv6 validation)

Project homepage
================
http://gitlab.isc.org/isc-projects/forge

How to get the source code
==========================

git clone https://gitlab.isc.org/isc-projects/forge




