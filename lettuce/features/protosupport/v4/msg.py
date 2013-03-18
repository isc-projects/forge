from lettuce import world

def client_requests_option(step, opt_type):
    if not hasattr(world, 'prl'):
        world.prl = "" # don't request anything by default
    world.prl += chr(int(opt_type)) # put a single byte there
