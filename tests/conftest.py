import pytest


def pytest_runtest_setup(item):
    import terrain
    terrain.initialize(item)


def pytest_runtest_teardown(item, nextitem):
    import terrain
    item.failed = None
    terrain.cleanup(item)


def pytest_runtest_logstart(nodeid, location):
    banner = '\n\n************ START   %s ' % nodeid
    banner += '*' * (140 - len(banner))
    banner += '\n'
    banner = '\u001b[36m' + banner + '\u001b[0m'
    print(banner)


def pytest_runtest_logfinish(nodeid, location):
    banner = '\n************ END   %s ' % nodeid
    banner += '*' * (140 - len(banner))
    banner = '\u001b[36;1m' + banner + '\u001b[0m'
    print(banner)


def pytest_runtest_logreport(report):
    if report.when == 'call':
        banner = '\n************ RESULT %s   %s ' % (report.outcome.upper(), report.nodeid)
        banner += '*' * (140 - len(banner))
        if report.outcome == 'passed':
            banner = '\u001b[32;1m' + banner + '\u001b[0m'
        else:
            banner = '\u001b[31;1m' + banner + '\u001b[0m'
        print(banner)


def pytest_generate_tests(metafunc):
    # If a test function has dhcp_version as fixtures ie. it has such argument
    # then generate 2 version of this test, for v4 and v6 ie. do automagically
    # parametrize.
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
        explicit_dhcp_version=False
        for v in list_of_attributed_versions:
            # If conflicting expressions were provided...
            if v in mark_expression and f'not {v}' in mark_expression:
                # Then complain to the user.
                raise Error(f'conflicting markers: "{v}" and "not {v}')
            # If this version was provided...
            if v in mark_expression:
                explicit_dhcp_version=True
                # And if "not version" was omitted...
                if 'not {v}' not in mark_expression:
                    # Then add it to the list of parametrized versions.
                    dhcp_versions.append(v)

        # If no dhcp_version mentioned in marker, enable all versions
        # atrributed to the function.
        if not explicit_dhcp_version:
            dhcp_versions = list_of_attributed_versions
    else:
        # Otherwise, meaning if -m was not provided, enable all versions
        # atrributed to the function.
        dhcp_versions = list_of_attributed_versions

    # Parameterize.

    if dhcp_versions:
        metafunc.parametrize('dhcp_version', dhcp_versions)


def pytest_configure(config):
    import terrain
    terrain.test_start()


def pytest_unconfigure(config):
    import terrain
    terrain.say_goodbye()



def pytest_addoption(parser):
    parser.addoption("--iters-factor", action="store", default=1,
        help="iterations factor, initial iterations in tests are multiplied by this value, default 1")


@pytest.fixture
def iters_factor(request):
    return int(request.config.getoption("--iters-factor"))


# enable pytest assert introspection in the helper modules
pytest.register_assert_rewrite('protosupport.v4.srv_msg')
pytest.register_assert_rewrite('protosupport.multi_protocol_functions')
pytest.register_assert_rewrite('cb_model')
pytest.register_assert_rewrite('dhcp4_scen')
pytest.register_assert_rewrite('softwaresupport.kea6_server.mysql_reservation')
pytest.register_assert_rewrite('softwaresupport.kea')
