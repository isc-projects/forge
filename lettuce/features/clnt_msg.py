from init_all import PROTO, SOFTWARE_UNDER_TEST
from lettuce import world, step
import importlib

if PROTO == "v6":
    clntMsg = importlib.import_module("protosupport.%s.clnt_msg"  % (PROTO))
    borrowedSteps = importlib.import_module("protosupport.%s.srv_msg"  % (PROTO))

    @step("Client sent (\S+) message.")
    def client_msg_capture(step, msgType):
        clntMsg.client_msg_capture(step, msgType)

    @step("Client MUST NOT sent (\S+) message. Client sent (\S+) message instead.")
    def client_msg_wrong_capture(step, wrongMsgType,correctMsgType):
        clntMsg.client_msg_wrong_capture(step, wrongMsgType,correctMsgType)

    @step("Server sends (back )?(\S+) message(from another link)?.")
    def send_msg_to_client(step, back, msgType, another):
        response = not (back == "back ")
        newLink = not (another == "from another link")
        clntMsg.send_msg_to_client(step, response, msgType, newLink)

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

    @step("(\S+) field MUST (NOT )?be present in option (\d+) from client message.")
    def client_check_field_presence(step, field, yes_no, optcode):
        contain = not (yes_no == "NOT ")
        clntMsg.client_check_field_presence(step, field, contain, optcode)

    @step("Client message option (\d+) MUST (NOT )?include sub-option (\d+).")
    def client_msg_contains_subopt(step, opt_code, yes_or_no, subopt_code):
        contain = not (yes_or_no == "NOT ")
        clntMsg.client_msg_contains_subopt(step, opt_code, contain, subopt_code)

    @step("Message was sent after at least (\S+) second.")
    def client_check_time_delay(step, timeval):
        preciseTimeVal = float(timeval)
        clntMsg.client_check_time_delay(step, preciseTimeVal)

    @step("(\S+) value in client message is the same as saved one.")
    def client_cmp_values(step, value):
        clntMsg.client_cmp_values(step, value)

    @step("(\S+) value is set to (\S+).")
    def server_sets_value(step, value_name, new_value):
        clntMsg.msg_set_value(step, value_name, new_value)

    @step("Server adds (\S+) (\d+ )?option to message.")
    def add_option(step, msgType, optcode):
        clntMsg.add_option(step, msgType, optcode)

    @step("Server adds another (\S+) option to message.")
    def add_another_option(step, msgType):
        clntMsg.add_another_option(step, msgType)

    @step("Client message sub-option (\d+) from option (\d+) MUST (NOT )?contain (\S+) (\S+).")
    def client_subopt_check_value(step, subopt_code, opt_code, yes_or_no, value_name, value):
        expect = not (yes_or_no == "NOT ")
        clntMsg.client_subopt_check_value(step, subopt_code, opt_code, expect, value_name, value)

    @step("Client message option (\d+) MUST (NOT )?contain (\S+) (\S+).")
    def client_opt_check_value(step, opt_code, yes_or_no, value_name, value):
        expect = not (yes_or_no == "NOT ")
        clntMsg.client_opt_check_value(step, opt_code, expect, value_name, value)

    @step("Server builds new message.")
    def srv_msg_clean(step):
        clntMsg.srv_msg_clean(step)

else:
    pass
