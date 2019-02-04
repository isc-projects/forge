import sys
import threading

import pytest

import forge


# lettuce global object that stores all needed data: configs, etc.
world = threading.local()
world.f_cfg = forge.ForgeConfiguration()


# stub that replaces lettuce step decorator
def step(pattern):
    def wrap(func):
        return func
    return wrap


# stub that replaces lettuce decorators @after.each_step, etc
class Main(object):
    def __init__(self, callback):
        self.name = callback

    def __getattr__(self, name):
        def wrapper(func):
            return func

        return wrapper
before = Main('before')
after = Main('after')


# helper class which object is used as argument to test functions
class Step(object):
    pass
