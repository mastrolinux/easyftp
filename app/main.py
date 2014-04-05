"""A basic FTP server which uses a DummyAuthorizer for managing 'virtual
users', setting a limit for incoming connections.
"""

import os

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

import yaml

def main():
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions and a read-only
    # anonymous user
    conf_file = file('../conf/dirs.conf', 'r')
    # yaml.load(conf_file)
    conf = yaml.load(conf_file)
    print(conf)
    # print(conf.get(user))
    for user in conf.get('users'):
        authorizer.add_user(user.get('name'), user.get('password'), user.get('dir'), perm=user.get('permission'))

    # exit()

    authorizer.add_user('user', '12345', os.getcwd(), perm='elradfmwM')
    # authorizer.add_anonymous(os.getcwd())

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "pyftpdlib based ftpd ready."

    # Specify a masquerade address and the range of ports to use for
    # passive connections.  Decomment in case you're behind a NAT.

    # handler.masquerade_address = '127.0.0.1'
    handler.passive_ports = range(60000, 65535)

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    server = conf.get('server', {})


    handler.masquerade_address = server.get('masquerade_address', None)
    range_start = min(server.get('passive_ports', {}).get('start', 60000), 65535)
    range_end = server.get('passive_ports', {}).get('end', max((range_start + 5000), 65535))
    # import pdb; pdb.set_trace()
    handler.passive_ports = range(range_start, range_end)
    address = (server.get('address', ''), server.get('port', '2121'))
    server = FTPServer(address, handler)

    # set a limit for connections
    # server.max_cons = 256
    # server.max_cons_per_ip = 5

    # start ftp server
    server.serve_forever()

if __name__ == '__main__':
    main()