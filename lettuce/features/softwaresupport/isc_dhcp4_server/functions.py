def prepare_cfg_isc_dhcp(step):
    # TODO: Implement me
    get_common_logger().error("TODO: Config generation for ISC DHCP is not implemented yet.")

def start_srv_isc_dhcp(step, config_file):
    args = ['dhcpd' , '-d', '-cf', config_file ]

    world.processes.add_process(step, "dibbler-server", args)
    # check output to know when startup has been completed
    # TODO: Replace accepting connections.
    (message, line) = world.processes.wait_for_stderr_str(process_name,
                                                     ["Accepting connections.",
                                                      "exiting"])
    assert message == "Accepting connections.", "Got: " + str(line)


def save_leases():
    assert False, "TODO!"


def save_logs():
    assert False, "TODO!"


def clear_all():
    assert False, "TODO!"
