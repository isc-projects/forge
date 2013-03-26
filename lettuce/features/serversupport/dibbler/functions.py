def prepare_cfg_dibbler(step, config_file):
    world.cfg["conf"] = "iface " + world.cfg["iface"] + "\n" + \
    "    class {\n" + \
    "        pool 2001:db8:1::/64\n" + \
    "    }\n" + \
    "}\n"

def start_srv_dibbler(step):
    args = [ 'dibbler-server', 'run' ]
    world.processes.add_process(step, "dhcpv6-server", args)
    # check output to know when startup has been completed
    (message, line) = world.processes.wait_for_stdout_str("dhcpv6-server",
                                                     ["Accepting connections.",
                                                      "Critical"])
    assert message == "Accepting connections.", "Got: " + str(line)

