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
# This file contains a number of common steps that are general and may be used
# By a lot of feature files.
#

from lettuce import *
import msg6
import msg4

@step('Client requests option (\d+).')
def client_requests_option(step, opt_type):
    if (world.proto == "v4"):
        msg4.client_requests_option(step, opt_type)
    elif (world.proto == "v6"):
        msg6.client_requests_option(step, opt_type)
    else:
        assert False, "Invalid protocol family specified:" + world.proto

@step('Server MUST respond with (\w+) message')
def send_wait_for_message(step, message):
    if (world.proto == "v4"):
        msg4.send_wait_for_message(step, message)
    elif (world.proto == "v6"):
        msg6.send_wait_for_message(step, message)
    else:
        assert False, "Invalid protocol family specified:" + world.proto

@step('Response MUST (NOT )?include option (\d+).')
def response_check_include_option(step, yes_or_no, opt_code):
    if (world.proto == "v4"):
        msg4.response_check_include_option(step, yes_or_no, opt_code)
    elif (world.proto == "v6"):
        msg6.response_check_include_option(step, yes_or_no, opt_code)
    else:
        assert False, "Invalid protocol family specified:" + world.proto


@step('Response option (\d+) MUST (NOT )?contain (\S+) (\S+).')
def response_check_option_content(step, opt_code, expect, data_type, expected):
    if (world.proto == "v4"):
        msg4.response_check_option_content(step, opt_code, expect, data_type, expected)
    elif (world.proto == "v6"):
        msg6response_check_option_content(step, opt_code, expect, data_type, expected)
    else:
        assert False, "Invalid protocol family specified:" + world.proto


@step('Client sends (\w+) message( with (\w+) option)?')
def client_send_msg(step, msgname, opt_type, unknown):
    if (world.proto == "v4"):
        msg4.client_send_msg(step, msgname, opt_type, unknown)
    elif (world.proto == "v6"):
        msg4.client_send_msg(step, msgname, opt_type, unknown)
    else:
        assert False, "Invalid protocol family specified:" + world.proto
