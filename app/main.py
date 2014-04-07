"""A basic FTP server which uses a DummyAuthorizer for managing 'virtual
users', setting a limit for incoming connections.
"""

import os
import yaml

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

this_dir = os.path.dirname(os.path.abspath(__file__))

def read_conf(config_file=os.path.join(this_dir, '../conf/ftp.conf')):
    conf_file = open(config_file, 'r')
    conf = yaml.safe_load(conf_file)
    return conf

def get_server(conf=None):

    print(conf)
    # Create users
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()
    for user in conf.get('users'):
        authorizer.add_user(user.get('name'), user.get('password'), user.get('dir'), perm=user.get('permission'))

    # TODO: implement anon user
    # authorizer.add_anonymous(os.getcwd())

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "simpleftp ready!"

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    server = conf.get('server', {})

    handler.masquerade_address = server.get('masquerade_address', None)
    range_start = min(server.get('passive_ports', {}).get('start', 60000), 65535)
    range_end = server.get('passive_ports', {}).get('end', max((range_start + 5000), 65535))
    # import pdb; pdb.set_trace()
    handler.passive_ports = range(range_start, range_end)

    handler.use_sendfile = server.get('use_sendfile', 'False')

    address = (server.get('address', ''), server.get('port', '2121'))
    server = FTPServer(address, handler)

    # set a limit for connections
    # server.max_cons = 256
    # server.max_cons_per_ip = 5

    # start ftp server
    # server.serve_forever()
    return server

if __name__ == '__main__':
    server = get_server(read_conf())
    server.serve_forever()