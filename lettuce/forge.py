#!/usr/bin/python

# Copyright (C) 2013-2017 Internet Systems Consortium.
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND INTERNET SYSTEMS CONSORTIUM
# DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# INTERNET SYSTEMS CONSORTIUM BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
# FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
# WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#
# author: Wlodzimierz Wencel

import importlib
import optparse
import os
import sys


def option_parser():
    desc = '''
    Forge - Testing environment. For more information please run help.py to generate UserHelp.txt
    '''
    parser = optparse.OptionParser(description=desc, usage="%prog or type %prog -h (--help) for help")
    parser.add_option("-4", "--version4",
                      dest="version4",
                      action="store_true",
                      default=False,
                      help='Declare IP version 4 tests')

    parser.add_option("-6", "--version6",
                      dest="version6",
                      action="store_true",
                      default=False,
                      help="Declare IP version 6 tests")

    parser.add_option("-v", "--verbosity",
                      dest="verbosity",
                      type="int",
                      action="store",
                      default=4,
                      help="Level of the lettuce verbosity")

    parser.add_option("-l", "--list",
                      dest="list",
                      action="store_true",
                      default=False,
                      help='List all features (test sets) please choose also IP version')

    parser.add_option("-s", "--test_set",
                      dest="test_set",
                      action="store",
                      default=None,
                      help="Specific tests sets")

    parser.add_option("-n", "--name",
                      dest="name",
                      default=None,
                      help="Single scenario name, don't use that option with -s or -t")

    parser.add_option("-t", "--tags",
                      dest="tag",
                      action="append",
                      default=None,
                      help="Specific tests tags, multiple tags after ',' e.g. -t v6,basic." +
                      "If you wont specify any tags, Forge will perform all test for chosen IP version." +
                      "Also if you want to skip some tests use minus sing before that test tag (e.g. -kea).")

    parser.add_option("-x", "--with-xunit",
                      dest="enable_xunit",
                      action="store_true",
                      default=False,
                      help="Generate results file in xUnit format")

    parser.add_option("-p", "--explicit-path",
                      dest="explicit_path",
                      default=None,
                      help="Search path, relative to <forge>/lettuce/features for tests regardless of SUT or protocol")

    parser.add_option("-T", "--test-configuration",
                      dest="test_config",
                      action="store_true",
                      default=False,
                      help="Run basic tests on current configuration and exit.")

    (opts, args) = parser.parse_args()

    if opts.test_config:
        from features.init_all import ForgeConfiguration
        f_config = ForgeConfiguration()
        print f_config.__dict__
        f_config.test_addresses()
        f_config.test_remote_location()
        f_config.test_priviledges()
        f_config.test_database()
        sys.exit(-1)

    tag = ""
    if opts.tag is not None:
        tag = opts.tag[0].split(',')

    if not opts.version6 and not opts.version4:
        parser.print_help()
        parser.error("You must choose between -4 or -6.\n")

    if opts.version6 and opts.version4:
        parser.print_help()
        parser.error("options -4 and -6 are exclusive.\n")

    number = '6' if opts.version6 else '4'
    #Generate list of set tests and exit
    if opts.list:
        from help import UserHelp
        hlp = UserHelp()
        hlp.test(number, 0)
        sys.exit(-1)

    return number, opts.test_set, opts.name, opts.verbosity, tag, opts.enable_xunit, opts.explicit_path


def test_path_select(number, test_set, name, explicit_path):
    #path for tests, all for specified IP version or only one set
    scenario = None
    from features.init_all import SOFTWARE_UNDER_TEST
    testType = ""
    for each in SOFTWARE_UNDER_TEST:
        if "client" in each:
            testType = "client"
        elif "server" in each:
            testType = "server"
        else:
            print "Are you sure that variable SOFTWARE_UNDER_TEST is correct?"
            sys.exit(-1)

    if explicit_path is not None:
        # Test search path will be <forge>/letttuce/features/<explicit_path/
        # without regard to SUT or protocol.  Can be used with -n to run
        # specific scenarios.
        base_path = os.getcwd() + "/features/" + explicit_path + "/"
        if name is not None:
            from help import find_scenario_in_path
            base_path, scenario = find_scenario_in_path(name, base_path)
            if base_path is None:
                print "Scenario named %s has been not found" % name
                sys.exit(-1)
    elif test_set is not None:
        path = "/features/dhcpv" + number + "/" + testType + "/" + test_set + "/"
        base_path = os.getcwd() + path
    elif name is not None:
        from help import find_scenario
        base_path, scenario = find_scenario(name, number)
        if base_path is None:
            print "Scenario named %s has been not found" % name
            sys.exit(-1)
    else:
        scenario = None
        path = "/features/dhcpv" + number + "/" + testType + "/"
        base_path = os.getcwd() + path

    return base_path, scenario


def check_config_file():
    try:
        importlib.import_module("features.init_all")
    except ImportError:
        print "\n Error: You need to create 'init_all.py' file with configuration! (example file: init_all.py_example)\n"
        #option_parser().print_help()
        sys.exit(-1)

def start_all(base_path, verbosity, scenario, tag, enable_xunit):

    from features.init_all import HISTORY
    if HISTORY:
        from help import TestHistory
        history = TestHistory()
        history.start()

    #lettuce starter, adding options
    try:
        from lettuce import Runner, world
    except ImportError:
        print "You have not Lettuce installed (or in path)."
        sys.exit(-1)

    runner = Runner(base_path,
                    verbosity = verbosity,
                    scenarios = scenario,
                    failfast = False,
                    tags = tag,
                    enable_xunit = enable_xunit)

    result = runner.run()  # start lettuce

    if HISTORY:
        history.information(result.scenarios_passed, result.scenarios_ran, tag, base_path)
        history.build_report()

    return result.scenarios_ran - result.scenarios_passed

if __name__ == '__main__':
    number, test_set, name, verbosity, tag, enable_xunit, explicit_path = option_parser()
    check_config_file()
    base_path, scenario = test_path_select(number, test_set, name, explicit_path)

    failed = start_all(base_path, verbosity, scenario, tag, enable_xunit)
    if failed > 0:
        print "SCENARIOS FAILED: %d" % failed
        sys.exit(1)
    sys.exit(0)
