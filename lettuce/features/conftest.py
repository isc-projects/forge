import pytest

def pytest_runtest_setup(item):
    from features import terrain
    print("~~~~~~~~~~~~~~~~~~~~~ terrain.initialize(%s) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" % item)
    terrain.initialize(item)


def pytest_runtest_teardown(item, nextitem):
    from features import terrain
    print("~~~~~~~~~~~~~~~~~~~~~ terrain.cleanup(%s) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" % item)
    item.failed = None
    terrain.cleanup(item)


@pytest.fixture(scope='session')
def step():
    from features import lettuce_compat
    return lettuce_compat.Step()


def pytest_configure(config):
    from features import terrain
    print("~~~~~~~~~~~~~~~~~~~~~ terrain.test_start() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    terrain.test_start()


class Total(object):
    def __init__(self):
        self.scenarios_passed = 0
        self.scenarios_ran = 0

def pytest_unconfigure(config):
    from features import terrain
    print("~~~~~~~~~~~~~~~~~~~~~ terrain.say_goodbye() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    terrain.say_goodbye(Total())



def pytest_addoption(parser):
    parser.addoption("--iters-factor", action="store", default=1,
        help="iterations factor, initial iterations in tests are multiplied by this value, default 1")


@pytest.fixture
def iters_factor(request):
    return int(request.config.getoption("--iters-factor"))
