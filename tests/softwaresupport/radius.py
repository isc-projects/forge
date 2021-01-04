import os

from .multi_server_functions import fabric_sudo_command, fabric_send_file
from forge_cfg import world

# Open file, write content and at the end of the context delete the file.
class TemporaryFile(object):
    def __init__(self, file_name, content):
        self.file_name = file_name
        self.content = content

    def __enter__(self):
        with open(self.file_name, 'w') as f:
            f.write(self.content)

    def __exit__(self, exception_type, exception_value, traceback):
        os.unlink(self.file_name)

def _init_radius():
    # authorize config file
    authorize_content = '''11:08:00:27:b0:c1:41    Cleartext-password := "08:00:27:b0:c1:41"
    \tFramed-IP-Address = "192.168.51.51",
    \tFramed-Pool = "blues"


11:08:00:27:b0:c1:42    Cleartext-password := "08:00:27:b0:c1:42"
    \tFramed-IP-Address = "192.168.52.52",
    \tFramed-Pool = "gold"


11:08:00:27:b0:c5:01    Cleartext-password := "08:00:27:b0:c5:01"
    \tFramed-Pool = "gold"

11:08:00:27:b0:c5:02    Cleartext-password := "08:00:27:b0:c5:02"
    \tFramed-Pool = "gold"

11:08:00:27:b0:c5:03    Cleartext-password := "08:00:27:b0:c5:03"
    \tFramed-Pool = "gold"

11:08:00:27:b0:c5:10    Cleartext-password := "08:00:27:b0:c5:10"
    \tFramed-IP-Address = "192.168.50.5",
    \tFramed-Pool = "gold"

11:08:00:27:b0:c6:01    Cleartext-password := "08:00:27:b0:c6:01"
    \tFramed-Pool = "silver"

11:08:00:27:b0:c6:02    Cleartext-password := "08:00:27:b0:c6:02"
    \tFramed-Pool = "silver"

11:08:00:27:b0:c6:03    Cleartext-password := "08:00:27:b0:c6:03"
    \tFramed-Pool = "silver"

11:08:00:27:b0:c7:01    Cleartext-password := "08:00:27:b0:c7:01"
    \tFramed-Pool = "bronze"

11:08:00:27:b0:c7:02    Cleartext-password := "08:00:27:b0:c7:02"
    \tFramed-Pool = "bronze"

11:08:00:27:b0:c7:03    Cleartext-password := "08:00:27:b0:c7:03"
    \tFramed-Pool = "bronze"

11:08:00:27:b0:c8:01    Cleartext-password := "08:00:27:b0:c8:01"
    \tFramed-Pool = "platinum"
    '''
    authorize_file = 'authorize.txt'
    with TemporaryFile(authorize_file, authorize_content):
        if world.server_system == 'redhat':
            # freeradius 3.x
            fabric_send_file(authorize_file, "/etc/raddb/mods-config/files/authorize")
        else:
            # freeradius 3.x
            fabric_send_file(authorize_file,
                            "/etc/freeradius/3.0/mods-config/files/authorize")
            # freeradius 2.x
            fabric_send_file(authorize_file, "/etc/freeradius/users")

    # clients.conf file
    clients_conf_content = '''
client {mgmt_address} {{
   ipaddr = {mgmt_address}
   require_message_authenticator = no
   secret = testing123
   proto = *
   nas_type = other
   limit {{
      max_connections = 16
      lifetime = 0
      idle_timeout = 30
   }}
}}'''
    clients_conf_content = clients_conf_content.format(mgmt_address=world.f_cfg.mgmt_address)
    clients_conf_file = 'clients.conf'
    with TemporaryFile(clients_conf_file, clients_conf_content):
        if world.server_system == 'redhat':
            # freeradius 3.x
            fabric_send_file(clients_conf_file, "/etc/raddb/clients.conf")
        else:
            # freeradius 3.x
            fabric_send_file(clients_conf_file, "/etc/freeradius/3.0/clients.conf")
            # freeradius 2.x
            fabric_send_file(clients_conf_file, "/etc/freeradius/clients.conf")


def _start_radius():
    if world.server_system == 'redhat':
        cmd = 'sudo systemctl restart radiusd'
    else:
        cmd = 'sudo systemctl restart freeradius'
    fabric_sudo_command(cmd)


def init_and_start_radius():
    _init_radius()
    _start_radius()
