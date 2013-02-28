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


import os
import sys
import optparse

from lettuce import Runner

VERBOSITY = 4

def option_parser():
    desc='''
    Let us decide witch version
    '''
    parser = optparse.OptionParser(description=desc)
    
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
    
    parser.add_option("-s", "--scenarios",
                      dest="scenario",
                      action="append",
                      default=None,
                      help="specific tests scenarios")
    
    (opts, args) = parser.parse_args()

    if not opts.version6 and not opts.version4:
        parser.print_help()
        parser.error("You must choose between -4 or -6")

    if opts.version6 and opts.version4:
        parser.print_help()
        parser.error("options -4 and -6 are exclusive")
        
    base_path = os.getcwd()

    if opts.version6:
        tag="v6"
    if opts.version4:
        tag="v4"

    runner = Runner(base_path,
                    verbosity=VERBOSITY,
                    tags=tag)
    '''
    Aby tagowanie dzialalo (?) trzeba tagowac przez @ mniej wiecej tak:

        @v6
        Feature: DHCPv6 custom options
            This is a simple DHCPv6 options validation. Its purpose is to check if
            requested options are assigned properly.
        
            Scenario: v6.options.preference
                # Checks that server is able to serve sntp-servers option to clients.
        
                Test Setup:
                Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
                Server is configured with custom option foo/100 with type uint8 and value 123.
                Server is started.
        
            Test Procedure:
            Client requests option 100.
            Client sends SOLICIT message and expect ADVERTISE response.
        
            Pass Criteria:
            Server MUST respond with advertise message.
            Response MUST include option 100.
            Response option 100 MUST contain uint8 123.
        
            References: v6.user-options, v6.oro, RFC3315 section 22.8
        
            Tags: v6 options preference automated
    '''
    result = runner.run()
    
def main():
    option_parser()

if __name__ == '__main__':
    main()