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
import optparse
import os

def option_parser():
    desc='''
    Let us decide which version
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
                      default=4,
                      help="Level of the lettuce verbosity")
    parser.add_option("-s", "--scenarios",
                      dest="scenario",
                      action="append",
                      default=None,
                      help="specific tests scenarios")
    parser.add_option("-t", "--tags",
                      dest="tag",
                      action="append",
                      default=None,
                      help="specific tests tags, multiple tags after ',' e.g. -t v6,v4")   
    (opts, args) = parser.parse_args()

    if not opts.version6 and not opts.version4:
        parser.print_help()
        parser.error("You must choose between -4 or -6")

    if opts.version6 and opts.version4:
        parser.print_help()
        parser.error("options -4 and -6 are exclusive")

    tag=None
    if opts.tag:
        tag = opts.tag[0].split(',')
    #TO DO - scenarios, dodac multi.
    base_path = os.getcwd()
    runner = Runner(base_path,
                    verbosity=opts.verbosity,
                    failfast=False,
                    tags=tag)

    result = runner.run()
    
def main():
    option_parser()

if __name__ == '__main__':
    main()