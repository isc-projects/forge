# Copyright (C) 2014 Internet Systems Consortium.
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

# Author: Maciek Fijalkowski


from init_all import PROTO, SOFTWARE_UNDER_TEST
from lettuce import world, step
import importlib

# TODO: write some comments what particular functions do; file's getting messy.

if PROTO == "v6":
    clntMsg = importlib.import_module("protosupport.%s.clnt_msg"  % (PROTO))
    borrowedSteps = importlib.import_module("protosupport.%s.srv_msg"  % (PROTO))

##############   getting client message   ##############

    @step("Sniffing client (\S+) message from network( with timeout)?.")
    def client_msg_capture(step, msgType, tout):
        tout_ = not (tout == " with timeout")
        clntMsg.client_msg_capture(step, msgType, tout_)

##############   validating received message   ##############

    @step("Client MUST (NOT )?respond with (\S+) message.")
    def client_send_receive(step, yes_no, msgType):
        contain = not (yes_no == "NOT ")
        clntMsg.client_send_receive(step, contain, msgType)

    @step("Client message MUST (NOT )?contain option (\d+).")
    def client_msg_contains_opt(step, yes_or_no, opt):
        contain = not (yes_or_no == "NOT ")
        clntMsg.client_msg_contains_opt(step, contain, opt)

    @step("Client message MUST (NOT )?contain (\d+) options with opt-code (\d+).")
    def client_msg_count_opt(step, yes_no, count, optcode):
        contain = not (yes_no == "NOT ")
        clntMsg.client_msg_count_opt(step, contain, count, optcode)

    @step("Client message MUST (NOT )?contain (\d+) sub-options with opt-code (\d+) within option (\d+).")
    def client_msg_count_subopt(step, yes_no, count, subopt_code, opt_code):
        contain = not (yes_no == "NOT ")
        clntMsg.client_msg_count_subopt(step, contain, count, subopt_code, opt_code)

    @step("Client message MUST (NOT )?contain (\S+) field in option (\d+).")
    def client_check_field_presence(step, yes_no, field, optcode):
        contain = not (yes_no == "NOT ")
        clntMsg.client_check_field_presence(step, contain, field, optcode)

    @step("Client message option (\d+) MUST (NOT )?include sub-option (\d+).")
    def client_msg_contains_subopt(step, opt_code, yes_or_no, subopt_code):
        contain = not (yes_or_no == "NOT ")
        clntMsg.client_msg_contains_subopt(step, opt_code, contain, subopt_code)

    @step("Retransmission time has required value.")
    def client_time_interval(step):
        clntMsg.client_time_interval(step)

    @step("Message was sent after maximum (\S+) second(s)?.")
    def client_rt_delay(step, timeval, plural):
        preciseTimeVal = float(timeval)
        dont_care = (plural == "s")
        clntMsg.client_rt_delay(step, preciseTimeVal, dont_care)

    @step("Message was retransmitted after maximum (\S+) second(s)?.")
    def client_rt_delay(step, timeval, plural):
        preciseTimeVal = float(timeval)
        dont_care = (plural == "s")
        clntMsg.client_rt_delay(step, preciseTimeVal, dont_care)

    @step("(\S+) value in client message is the same as saved one.")
    def client_cmp_values(step, value):
        clntMsg.client_cmp_values(step, value)

    @step("Client message sub-option (\d+) from option (\d+) MUST (NOT )?contain (\S+) (\S+).")
    def client_subopt_check_value(step, subopt_code, opt_code, yes_or_no, value_name, value):
        expect = not (yes_or_no == "NOT ")
        clntMsg.client_subopt_check_value(step, subopt_code, opt_code, expect, value_name, value)

    @step("Client message option (\d+) MUST (NOT )?contain (\S+) (\S+).")
    def client_opt_check_value(step, opt_code, yes_or_no, value_name, value):
        expect = not (yes_or_no == "NOT ")
        clntMsg.client_opt_check_value(step, opt_code, expect, value_name, value)

##############   building server message   #############

    @step("Server builds new message.")
    def srv_msg_clean(step):
        clntMsg.srv_msg_clean(step)

    @step("Save (\S+) value.")
    def save_value(step, value):
        clntMsg.save_value(step, value)

    @step("Server sets wrong (\S+) value.")
    def server_set_wrong_val(step, value):
        clntMsg.server_set_wrong_val(step, value)

    @step("(\S+) value is set to (\S+).")
    def server_sets_value(step, value_name, new_value):
        clntMsg.msg_set_value(step, value_name, new_value)

    @step("Server adds (\S+) (\d+ )?option to message.")
    def add_option(step, opt, optcode):
        clntMsg.add_option(step, opt, optcode)

    @step("Server does NOT add (\S+) option to message.")
    def server_not_add(step, opt):
        clntMsg.server_not_add(step, opt)

    @step("Server sends (back )?(\S+) message.")
    def server_build_msg(step, back, msgType):
        response = not (back == "back ")
        clntMsg.server_build_msg(step, response, msgType)

else:
    pass
