# Copyright (C) 2019-2024 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Pytest additional configuration."""

import pytest
from src.forge_cfg import world

# pylint: disable=import-outside-toplevel
# pylint: disable=unused-argument


@pytest.fixture(autouse=True, scope='session')
def get_number_of_tests(request):
    """Get the total number of tests.

    Function is called automatically, but after the first test
    so test_count will be != 0 from the second test onward.

    :param request: pytest request to run a test
    :type request: pytest.SubRequest
    """
    world.test_count = len(request.node.items)


def pytest_runtest_setup(item):
    """Call for each test before execution.

    :param item: pytest item to run a test
    :type item: pytest.Item
    """
    pass  # pylint: disable=unnecessary-pass


@pytest.fixture(autouse=True)
def initialize_terrain(request):
    """Reset test configuration before each test.

    :param request: pytest request to run a test
    :type request: pytest.SubRequest
    """
    from src import terrain
    terrain.initialize(request)
    world.f_cfg.control_agent = request.config.getoption("--with-ca")


def pytest_runtest_teardown(item, nextitem):
    """Call for each test after execution.

    :param item: pytest item to run a test
    :type item: pytest.Item
    :param nextitem: pytest item to run next
    :type nextitem: pytest.Item
    """
    from src import terrain
    item.failed = None
    terrain.cleanup(item)


def pytest_runtest_logstart(nodeid, location):
    """Print start line before each test, with test counter.

    :param nodeid: pytest node id
    :type nodeid: str
    :param location: pytest location
    :type location: str
    """
    banner = f' START {world.get_test_progress()}: {nodeid} '
    stars = 140 - len(banner)
    half_stars = int(stars / 2)
    banner = '\n\n\u001b[36m' + ('*' * half_stars) + banner + ('*' * (stars - half_stars)) + '\u001b[0m\n'
    print(banner)


def pytest_runtest_logfinish(nodeid, location):
    """Print finish line after each test, with test counter.

    :param nodeid: pytest node id
    :type nodeid: str
    :param location: pytest location
    :type location: str
    """
    banner = f' END {world.get_test_progress()}: {nodeid} '
    stars = 140 - len(banner)
    half_stars = int(stars / 2)
    banner = '\n\u001b[36;1m' + ('*' * half_stars) + banner + ('*' * (stars - half_stars)) + '\u001b[0m'
    world.current_test_index += 1
    print(banner)


def pytest_runtest_logreport(report):
    """Print result line after each test, with test counter.

    :param report: pytest report
    :type report: pytest.Report
    """
    if report.when == 'call':
        outcome = report.outcome.upper()
        node_id = report.nodeid
        banner = f' RESULT {outcome} {world.get_test_progress()}: {node_id} '
        stars = 140 - len(banner)
        half_stars = int(stars / 2)
        banner = ('*' * half_stars) + banner + ('*' * (stars - half_stars))
        if report.outcome == 'passed':
            banner = '\u001b[32;1m' + banner + '\u001b[0m'
        else:
            banner = '\u001b[31;1m' + banner + '\u001b[0m'
        print(banner)


def pytest_generate_tests(metafunc):
    """Generate two tests if there is dhcp_version as a fixture.

    If a test function has dhcp_version as fixtures ie. it has such argument
    then generate 3 versions of this test, for v4, v4_bootp, v6 ie. automagically
    parametrize.

    :param metafunc: pytest metafunction
    :type metafunc: pytest.Metafunc
    """
    if 'dhcp_version' not in metafunc.fixturenames:
        return

    # Get the list of markers attributed to the function.
    list_of_versions = ['v4', 'v4_bootp', 'v6']
    list_of_attributed_versions = [m for m in list_of_versions if metafunc.definition.get_closest_marker(m)]

    # If the -m parameter was provided...
    mark_expression = metafunc.config.getoption("-m")
    if mark_expression:
        # Then start with an empty list and fill it in the loop below.
        dhcp_versions = []

        # For all versions attributed to the function...
        explicit_dhcp_version = False
        for v in list_of_attributed_versions:
            # If conflicting expressions were provided...
            if v in mark_expression and f'not {v}' in mark_expression:
                # Then complain to the user.
                raise Exception(f'conflicting markers: "{v}" and "not {v}')
            # If this version was provided...
            if v in mark_expression:
                explicit_dhcp_version = True
                # And if "not version" was omitted...
                if 'not {v}' not in mark_expression:
                    # Then add it to the list of parametrized versions.
                    dhcp_versions.append(v)

        # If no dhcp_version mentioned in marker, enable all versions
        # attributed to the function.
        if not explicit_dhcp_version:
            dhcp_versions = list_of_attributed_versions
    else:
        # Otherwise, meaning if -m was not provided, enable all versions
        # attributed to the function.
        dhcp_versions = list_of_attributed_versions

    # Parametrize.
    if dhcp_versions:
        metafunc.parametrize('dhcp_version', dhcp_versions)


def pytest_configure(config):
    """Configure before each test.

    :param config: pytest config
    :type config: pytest.Config
    """
    from src import terrain
    terrain.test_start()


def pytest_unconfigure(config):
    """Clean up after each test.

    :param config: pytest config
    :type config: pytest.Config
    """
    from src import terrain
    terrain.say_goodbye()


def pytest_addoption(parser):
    """Add options to pytest.

    :param parser: pytest parser
    :type parser: pytest.Parser
    """
    parser.addoption("--iters-factor", action="store", default=1,
                     help="iterations factor, initial iterations in tests are multiplied by this value, default 1")
    parser.addoption("--with-ca", action="store_true", default=False,
                     help="Enable CA settings in the test suite")


@pytest.fixture
def iters_factor(request):
    """
    Get the iterations factor (how many times the test should be repeated).

    :param request: pytest request to run a test
    :type request: pytest.SubRequest
    :return: iterations factor
    :rtype: int
    """
    return int(request.config.getoption("--iters-factor"))


# enable pytest assert introspection in the helper modules
pytest.register_assert_rewrite('protosupport.v4.srv_msg')
pytest.register_assert_rewrite('protosupport.multi_protocol_functions')
pytest.register_assert_rewrite('cb_model')
pytest.register_assert_rewrite('dhcp4_scen')
pytest.register_assert_rewrite('softwaresupport.kea6_server.mysql_reservation')
pytest.register_assert_rewrite('softwaresupport.kea')
