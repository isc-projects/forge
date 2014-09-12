
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
    """
    Step sniffs message(s) sent by client and stores it in list. It is an 
    important step and a lot of things take place here. We can sniff a
    message with or without a timeout. If, after reaching timeout, specific
    message was not sniffed, whole test fails. 
    Sniffed message is splitted onto particular options and stored in 
    variable. Time of receiving message is also saved.
    """
    def client_msg_capture(step, msgType, tout):
        tout_ = not (tout == " with timeout")
        clntMsg.client_msg_capture(step, msgType, tout_)


##############   validating received message   ##############


    @step("Message was sent to (multicast|unicast) address.")
    """
    Step checks whether message sent by dhcp client was sent to
    multicast or unicast address. If the destination address
    begins with 'ff', then it is interpreted as a multicast
    address. Otherwise, we assume that it is an unicast address.
    """
    def client_dst_address_check(step, dst_type):
        clntMsg.client_dst_address_check(step, dst_type)


    @step("Client MUST (NOT )?respond with (\S+) message.")
    """
    Step is responsible for sending previously prepared server's
    message and checking the response of a client. Scapy's sr()
    function is used here.
    """
    def client_send_receive(step, yes_no, msgType):
        contain = not (yes_no == "NOT ")
        clntMsg.client_send_receive(step, contain, msgType)


    @step("Client message MUST (NOT )?contain option (\d+).")
    """
    Step verifies the presence of particular option in received
    message from client. Options are checked by their option code.
    """
    def client_msg_contains_opt(step, yes_or_no, opt):
        contain = not (yes_or_no == "NOT ")
        clntMsg.client_msg_contains_opt(step, contain, opt)


    @step("Client message MUST (NOT )?contain (\d+) options with opt-code (\d+).")
    """
    Step checks whether client had included a expected number of particular
    option in message.
    """
    def client_msg_count_opt(step, yes_no, count, optcode):
        contain = not (yes_no == "NOT ")
        clntMsg.client_msg_count_opt(step, contain, count, optcode)


    @step("Client message MUST (NOT )?contain (\d+) sub-options with opt-code (\d+) within option (\d+).")
    """
    Step checks whether client had included a expected number of particular
    sub-option within option in message.
    """
    def client_msg_count_subopt(step, yes_no, count, subopt_code, opt_code):
        contain = not (yes_no == "NOT ")
        clntMsg.client_msg_count_subopt(step, contain, count, subopt_code, opt_code)


    @step("Client message MUST (NOT )?contain (\S+) field in option (\d+).")
    """
    Step checks if in specified option, specific field is present - like
    T1 field in option 25 (IA_PD).
    """
    def client_check_field_presence(step, yes_no, field, optcode):
        contain = not (yes_no == "NOT ")
        clntMsg.client_check_field_presence(step, contain, field, optcode)


    @step("Client message option (\d+) MUST (NOT )?include sub-option (\d+).")
    """
    Step verifies the presence of particular sub-option within option 
    in received message from client. Sub-options and options are checked 
    by their option code.
    """
    def client_msg_contains_subopt(step, opt_code, yes_or_no, subopt_code):
        contain = not (yes_or_no == "NOT ")
        clntMsg.client_msg_contains_subopt(step, opt_code, contain, subopt_code)


    @step("Retransmission time has required value.")
    """
    Step is used for measuring message retransmission time and verifying
    it whether it fits in given time scope (which was previously computed).
    See retransmission_time_validation directory and tests in it.
    """
    def client_time_interval(step):
        clntMsg.client_time_interval(step)


    @step("Message was (sent|retransmitted) after maximum (\S+) second(s)?.")
    """
    Step for checking the time between last received message and the previous
    received message. This has nothing to do with retransmission times.
    This is used for example when we want to check that we have reached
    a maximum timeout for retransmission time.
    """
    def client_rt_delay(step, s_or_r, timeval, plural):
        # s_or_r is not needed
        preciseTimeVal = float(timeval)
        dont_care = (plural == "s")
        clntMsg.client_rt_delay(step, preciseTimeVal, dont_care)


    @step("(\S+) value in client message is the same as saved one.")
    """
    This step compares value from received client message with the value
    saved with "Save (\S+) value." step.
    """
    def client_cmp_values(step, value):
        clntMsg.client_cmp_values(step, value)


    @step("Client message sub-option (\d+) from option (\d+) MUST (NOT )?contain (\S+) (\S+).")
    """
    Step checks the value of field within a specific sub-option. It is compared
    with the value given in step. It might be used as following:
    Client message sub-option 26 from option 25 MUST contain prefix 3111::.
    """
    def client_subopt_check_value(step, subopt_code, opt_code, yes_or_no, value_name, value):
        expect = not (yes_or_no == "NOT ")
        clntMsg.client_subopt_check_value(step, subopt_code, opt_code, expect, value_name, value)


    @step("Client message option (\d+) MUST (NOT )?contain (\S+) (\S+).")
    """
    Step checks the value of field within a specific option. It is compared
    with the value given in step. It might be used as following:
    Client message option 25 MUST NOT contain T1 2000.
    """
    def client_opt_check_value(step, opt_code, yes_or_no, value_name, value):
        expect = not (yes_or_no == "NOT ")
        clntMsg.client_opt_check_value(step, opt_code, expect, value_name, value)


##############   building server message   #############

    @step("Server builds new message.")
    """
    Step prepares fresh instance of server's message. Previously saved
    values are removed and every other values are set to default.
    """
    def srv_msg_clean(step):
        clntMsg.srv_msg_clean(step)


    @step("Set timer to (\S+).")
    """
    This step sets a timer to a provided value. It can take values from
    world.clntCfg["values"] dictionary (T1, T2, preferred-lifetime,
    valid-lifetime) or be set to an implicit value, like 1234.
    """
    def set_timer(step, timer_val):
        clntMsg.set_timer(step, timer_val)


    @step("Save (\S+) value.")
    """
    Step saves value in variable for further comparison. One case of usage
    is checking the consistency of IAID value over message exchange.
    """
    def save_value(step, value):
        clntMsg.save_value(step, value)


    @step("Server sets wrong (\S+) value.")
    """
    Step sets deliberately wrong value of given server's message
    component. It can be:
    - iaid,
    - client Id,
    - server Id,
    - transaction id.
    """
    def server_set_wrong_val(step, value):
        clntMsg.server_set_wrong_val(step, value)


    @step("(\S+) value is set to (\S+).")
    """
    Server sets value of one key from world.clntCfg["values"] 
    to different than its default value. It can be for example
    T1, T2, preferred-lifetime, valid-lifetime, prefix.
    """
    def server_sets_value(step, value_name, new_value):
        clntMsg.msg_set_value(step, value_name, new_value)


    @step("Server adds (\S+) (\d+ )?option to message.")
    """
    Step adds an option to server's message. Options that can be added:
    -  IA_PD
    -  IA_Prefix
    -  Status_Code
    -  preference
    -  rapid_commit
    -  option_request
    -  elapsed_time
    -  iface_id
    -  reconfigure
    -  relay_message
    -  server_unicast
    """
    def add_option(step, opt, optcode):
        clntMsg.add_option(step, opt, optcode)


    @step("Server does NOT add (\S+) option to message.")
    """
    By default, to generic server message, options client id and server
    id are included. This step can provide not adding one of them, in
    order to check client's behaviour in that situation.
    """
    def server_not_add(step, opt):
        clntMsg.server_not_add(step, opt)


    @step("Server sends (back )?(\S+) message.")
    """
    Step is used for sending server's message to client. Mostly, it is
    used to send a REPLY message. If current message is ADVERTISE, the
    message is only build with this step and it would be sent with
    "Client MUST (NOT )?respond with (\S+) message." step.
    """
    def server_build_msg(step, back, msgType):
        response = not (back == "back ")
        clntMsg.server_build_msg(step, response, msgType)

else:
    pass
