import pytest

# import logging
# log = logging.getLogger('forge')


def pytest_runtest_setup(item):
    from features import terrain
    # log.info("~~~~~~~~~~~~~~~~~~~~~ terrain.initialize(%s) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" % item)
    terrain.initialize(item)


def pytest_runtest_teardown(item, nextitem):
    from features import terrain
    # log.info("~~~~~~~~~~~~~~~~~~~~~ terrain.cleanup(%s) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" % item)
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
    if hasattr(metafunc.function, 'v4') and hasattr(metafunc.function, 'v6'):
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
    if dhcp_versions:
        metafunc.parametrize('dhcp_version', dhcp_versions)


def pytest_configure(config):
    from features import terrain
    # log.info("~~~~~~~~~~~~~~~~~~~~~ terrain.test_start() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    terrain.test_start()


class Total(object):
    def __init__(self):
        self.scenarios_passed = 0
        self.scenarios_ran = 0

def pytest_unconfigure(config):
    from features import terrain
    # log.info("~~~~~~~~~~~~~~~~~~~~~ terrain.say_goodbye() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    terrain.say_goodbye(Total())



def pytest_addoption(parser):
    parser.addoption("--iters-factor", action="store", default=1,
        help="iterations factor, initial iterations in tests are multiplied by this value, default 1")


@pytest.fixture
def iters_factor(request):
    return int(request.config.getoption("--iters-factor"))
