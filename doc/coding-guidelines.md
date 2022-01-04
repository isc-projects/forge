Coding Guidelines
=================

The lines should not exceed 100 characters.

Test comments
-------------

Each new test must have a short (1-3 sentences) description of the goal of the test. It should
be added as a standard triple quote comment after the test function signature. Try to convey the
purpose of the test (why you felt it was important enough to dedicate time to write it) rather than
simply state what it does. Many tests don't have a description. We can address this problem
incrementally. If you edit an existing test that is missing a description, you should add it.

pylint
------

The long term goal is use pylint everywhere. However, we have a huge legacy code that didn't adhere
to pylint. When adding new code, make sure there are no new pylint warnings reported and the overall
score is not lower. Do not clutter your MRs that have substantial code changes with pylint fixes.
If you want to, open dedicated MRs for that, but please do that in moderation. This is a rabbit hole
that can easily suck a lot of time.

To check the code with pylint, use `check-style.sh` script.

Changelog
---------

We do have a changelog. Please document changes that may be useful for others, such as adding new
tests, fixing problems in existing ones, refactoring functions that will be used by others etc.
Smaller changes (e.g. "I did fifth round of minor tweaks to something") should be skipped.

Writing new tests
-----------------

Since forge moved from lettuce to pytest, writing new tests is just python programming.
Functions available in `tests/srv_control.py` are used to operate remote DHCP/DNS servers.
Functions available in `tests/srv_msg.py` are used to generate and parse traffic. Don't forget
to write test description for new tests.

Additional info
---------------

- [Pytest homepage](https://docs.pytest.org/en/latest/)
- [Scapy homepage](http://www.secdev.org/projects/scapy/)
