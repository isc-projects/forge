* 33.	[func]		godfryd

	Implemented tests for class_cmds hook in Kea.
	(gitlab !9)

* 32.	[func]		godfryd

	Implemented better logging.
	(gitlab !2)

* 31.	[func]		godfryd

	Added support for pytest. Many cleanups.
	(gitlab !5)

* 30.	[func]		wlodek

	Implemented new tests for reservation-get-all and reservation-get-page
	commands.
	(gitlab !7)

* 29.	[bug]		wlodek

	Fixes for multiple tests.
	(gitlab !8)

* 28.	[func]		godfryd

	Preparation for pytest support, as an intended replacement for lettuce
	that is no longer being developed.
	(gitlab !1)

* 27.	[func]		wlodek

	Imlemented new tests for lease retrieval page by page.
	(gitlab !3)

Code migrated from github (http://github.com/isc-projects/forge)
            to gitlab (http://gitlab.isc.org/isc-projects/forge)

* 26.	[func]		Maciej Fijalkowski

	Experimental DHCP client tests.
	(github, 70 commits)

* 25.	[func]		thomas

	user_chk hook library tests, improved support for isc-dhcp v6,
	several smaller improvements.
	(github, 14 commits)

* 24.	[build]		marcin

	Several improvements: logging, scapy patch, v6 option tests,
	better results reporting.
	(github, 16 commits)

* 23.	[func]	wlodek

	Support for DNS and DDNS added.
	(no backwards compatibility)

* 22.	[func]	wlodek

	- copy log files for Kea servers

* 21.	[func]	wlodek

    - configuration server timers (e.g. renew-timer)

* 20.	[func] 	wlodek

	- support for vendor option tests

* 19. [func]	maciek

	- support for changing multiple values

* 18. [bug]	wlodek

	- parsing received message more accurate
	- added new patch for Scapy!

* 17.	[func]	wlodek

	- support for Prefix Delegation (RFC 3633)

* 16.	[bug]	wlodek

	- multiple copy-from-received message procedure now fully functional

* 15.	[func]	wlodek

	- multiple IA options in msg

* 14.	[bug]	wlodek

	- Scapy statuscode fixed, all tests now operational

* 13.	[bug]	wlodek

	- IA_NA option fixed
	- double option bug fixed

* 12.	[func]	wlodek

	- config generation for Dibbler (v6)
	- automatic start/stop Dibbler (v6)

* 11.	[bug]	wlodek

	- removed - character from directory names.

* 10.	[func]	wlodek

	- config generation for ISC-DHCPv6
	- automatic start/stop ISC-DHCPv6

* 9. 	[func]	wlodek

	- new type of tests, Scenario Outline
	- reports for Scenario Outline

* 8.	[func]	wlodek

	- first version of UserHelp in using Forge (set of all available
	test sets, features, test names) and building new tests

* 7.	[func]	wlodek

	new functions in run_test.py:
	-l for listing all features (for specific IP version)
	-s for choosing test set based on directory name

* 6. [bug] wlodek

	- options -v4 and -v6 in run_test.py are operational

* 5. [func] wlodek

	- building basic relay-forward message
	- relay-forward message tests

* 4. [doc] tomek

	Initial documentation added. Many overlapping and redundant copies
	of readme/todo/notes sorted out.

* 3. [func] wlodek

	- configuration checker (when starting by run_test.py)
	- configuration in different file
	- basic tests
	- building all dhcpv6 messages and scapy patch (InforRequest is
	  still a problem)
	- test tags
	- automatic start/stop/configure bind10 - dhcp

* 2. [func] rafal

	Refactoring: generic code with dynamically loaded modules for
	specific server or protocol

* 1. [func] rafal, wlodek, tomek

	Initial code merged in. This is a result of a common development
	on separate private repos.

LEGEND
[bug] 	general bug fix.  This is generally a backward compatible change,
	unless it's deemed to be impossible or very hard to keep
	compatibility to fix the bug.
[build] compilation and installation infrastructure change.
[doc] 	update to documentation. This shouldn't change run time behavior.
[func] 	new feature.  In some cases this may be a backward incompatible
	change, which would require a bump of major version.
[sec] 	security hole fix. This is no different than a general bug
	fix except that it will be handled as confidential and will cause
	security patch releases.

*: Backward incompatible or operational change.
