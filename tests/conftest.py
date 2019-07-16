import pytest


def pytest_runtest_setup(item):
    import terrain
    terrain.initialize(item)


def pytest_runtest_teardown(item, nextitem):
    import terrain
    item.failed = None
    terrain.cleanup(item)


def pytest_generate_tests(metafunc):
    # If a test function has dhcp_version as fixtures ie. it has such argument
    # then generate 2 version of this test, for v4 and v6 ie. do automagically
    # parametrize.
    if 'dhcp_version' not in metafunc.fixturenames:
        return
    dhcp_versions = []
    # check if v4 and v6 markers are present in function
    if metafunc.definition.get_closest_marker('v4') and metafunc.definition.get_closest_marker('v6'):
        # if tests are filtered by markers then generate test versions
        # only if given marker was selected
        markexpr = metafunc.config.getoption("-m")
        if not markexpr:
            # no filtering, then pick both versions
            dhcp_versions = ['v4', 'v6']
        elif 'not v4' not in markexpr and 'v4' in markexpr:
            # v4 is not filtered out or explicitly selected then take v4 only
            dhcp_versions = ['v4']
        elif 'not v6' not in markexpr and 'v6' in markexpr:
            # v6 is not filtered out or explicitly selected then take v6 only
            dhcp_versions = ['v6']
        else:
            # filtering present but it does not look into proto version, then pick both versions
            dhcp_versions = ['v4', 'v6']
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
