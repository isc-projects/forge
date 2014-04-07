from init_all import PROTO
from lettuce import world, step
import importlib


clntMsg = importlib.import_module("protosupport.%s.clnt_msg"  % (PROTO))

@step("Server receives (\S+) message from client.")
def client_msg_capture(step, msgType):
    clntMsg.client_msg_capture(step, msgType)

@step("Server answers with (\S+) message.")
def send_msg_to_client(step, msgType):
    clntMsg.send_msg_to_client(step, msgType)