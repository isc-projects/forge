from init_all import PROTO, SOFTWARE_UNDER_TEST
from lettuce import world, step
import importlib

if PROTO == "v6":
    clntMsg = importlib.import_module("protosupport.%s.clnt_msg"  % (PROTO))

    @step("Client sent (\S+) message.")
    def client_msg_capture(step, msgType):
        clntMsg.client_msg_capture(step, msgType)

    @step("Server sends back (\S+) message.")
    def send_msg_to_client(step, msgType):
        clntMsg.send_msg_to_client(step, msgType)

    @step("Client message MUST (NOT )?contain option (\d+).")
    def client_msg_contains_opt(step, yes_or_no, opt):
        contain = not (yes_or_no == "NOT ")
        clntMsg.client_msg_contains_opt(step, contain, opt)
else:
    pass