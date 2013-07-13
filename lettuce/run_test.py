# Copyright (C) 2013 Internet Systems Consortium.
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


from lettuce import Runner

import importlib
import optparse
import os
import sys


def option_parser():
    desc='''
    Forge version .... ? :)
    '''
    parser = optparse.OptionParser(description=desc, usage="%prog or type %prog -h (--help) for help")
    parser.add_option("-4","--version4",
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
    parser.add_option("-l","--list",
                      dest="list",
                      action="store_true",
                      default=False,
                      help='List all features (test sets) please choose also IP version')
    parser.add_option("-s", "--test_set",
                      dest="test_set",
                      action="store",
                      default=None,
                      help="Specific tests sets")
#     parser.add_option("-n", "--name",
#                       dest="name",
#                       default=None,
#                       help='Comma separated list of scenarios/test names to run')
    parser.add_option("-t", "--tags",
                      dest="tag",
                      action="append",
                      default=None,
                      help="Specific tests tags, multiple tags after ',' e.g. -t v6,basic. If you wont specify any tags, Forge will perform all test for chosen IP version.")
    parser.add_option("-x", "--with-xunit",
                      dest="enable_xunit",
                      action="store_true",
                      default=False,
                      help="Generate results file in xUnit format")

    (opts, args) = parser.parse_args()
    
    if not opts.version6 and not opts.version4:
        parser.print_help()
        parser.error("You must choose between -4 or -6.\n")
        
    if opts.version6 and opts.version4:
        parser.print_help()
        parser.error("options -4 and -6 are exclusive.\n")
        
    number = '6' if opts.version6 else '4'
    
    #Generate list of set tests.
    if opts.list:
        from features.help import UserHelp
        hlp = UserHelp()
        hlp.test(number, 0)
        sys.exit()
        
    tag = None
    #adding tags for lettuce
    if opts.tag is not None:
        tag = opts.tag[0].split(',')
    else:
        tag = 'v6' if opts.version6 else 'v4'
    
    #path for tests, all for specified IP version or only one set
    if opts.test_set is not None:
        base_path = os.getcwd() + "/features/tests_v" + number + "/" + opts.test_set + "/"
    else:
        base_path = os.getcwd() + "/features/tests_v" + number + "/"
    
    #lettuce starter, adding options
    runner = Runner(
                    base_path,
                    verbosity = opts.verbosity,
                    scenarios = opts.name,
                    failfast = False,
                    tags = tag,
                    enable_xunit = opts.enable_xunit)\
                     
    runner.run() #start lettuce
    print "used tags:", tag, "\npath:", base_path
    
def main():
    try :
        config = importlib.import_module("features.init_all")
    except ImportError:
        print "You need to create 'init_all.py' file with configuration! (example file: init_all.py_default)"
        sys.exit()
    if config.SERVER_TYPE == "":
        print "Please make sure your configuration is valid\nProject Forge shutting down."
        sys.exit()       
    option_parser()

if __name__ == '__main__':
    main()
