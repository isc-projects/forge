ISC Forge
=========

ISC Forge is an open-source DHCP conformance validation framework. It started as a joint project
done by Internet Systems Consortium, a non-profit company based in Redwood City, California, and
students from Gdansk University of Technology. Currently, Forge is maintained and developed by ISC.

The goal of this project is to develop an automated, open-source DHCPv4 and DHCPv6 validation
framework. The primary focus is on RFC compliance, but other validation aspects are also covered.

In principle, the framework can be extended to cover any RFC compliant DHCP
software, but we're focusing on Kea. In various times, there was some partial
support added also for [ISC DHCP](https://gitlab.isc.org/isc-projects/dhcp) and
[Dibbler](https://klub.com.pl/dhcpv6/). Support for implementations other than
Kea is experimental at best.

The framework is written in Python and uses the following libraries:

- Scapy (for packet generation/parsing)
- Pytest (for test management)
- Fabric (for remote server configuration)

Current team
------------

- Włodzimierz Wencel (ISC)
- Tomek Mrugalski (ISC, engineering manager)
- Andrei Pavel (ISC)
- Marcin Godzina (ISC)

The list is in roughly chronological order.

Former participants
-------------------

- Rafał Jankowski (Gdansk University, DHCPv4 validation)
- Maciek Fijałkowski (Gdansk University, DHCPv6 validation)
- Thomas Markwalder (ISC)
- Marcin Siodelski (ISC)
- Stephen Morris (ISC, engineering manager)
- Michał Nowikowski (ISC)

The list is roughly chronological order of the last activity.

Getting in touch
----------------

For questions, ideas, and bug reports, please get in touch with us via kea-dev mailing list,
available on <https://lists.isc.org/mailman/listinfo/kea-dev>. You may also open tickets and send
patches on gitlab. See project homepage for details. Before sending patches, please read the coding
guidelines.

Project homepage
----------------

<http://gitlab.isc.org/isc-projects/forge>

Getting the source code
-----------------------

```shell
git clone https://gitlab.isc.org/isc-projects/forge
```

Other useful documentation
--------------------------

- [Installation](doc/install.md) - a quick overview of Forge installation
- [Usage](doc/usage.md) - how to use Forge once installed
- Working Examples - step-by-step instructions for setting up Forge with Kea and running some tests.
  - [Manual VM set up](doc/example_manual.md)
  - [Automatic Incus set up](doc/example_automatic.md)
- [Coding Guidelines](doc/coding-guidelines.md) - various tips for developers and contributors.
