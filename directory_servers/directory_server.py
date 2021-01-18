import sys
import rpyc
import socket
from constRPYC import *
from rpyc.utils.server import ThreadedServer

class DirectoryServer1(rpyc.Service):
  servers = {}

  def exposed_register(self, server_name, ip_address, port_number):
    pass


  def exposed_lookup(self, server_name):
    if (server_name.find(':') > 0):
      return self.get_local_address(server_name)
    
    dir_name = server_name.split(':')[0]
    server_name = server_name.split(':')[1]
    return self.get_global_address(dir_name, server_name)


  def exposed_unregister(self, server_name):
    pass


  def get_local_address(self, server_name):
    if (server_name not in self.servers):
      return dict(
        success = False,
        message = f'Directory server {server_name} does not exist'
      )
    
    address = self.servers[server_name]
    return dict(
      success = True,
      message = f'Directory server {server_name} found with address {address}',
      data = address
    )


  def get_global_address(self, dir_name, server_name):
    if (dir_name not in self.servers):
      return dict(
        success = False,
        message = f'Directory server {dir_name} does not exist'
      )

    (addr, port) = self.servers[dir_name]
    conn = rpyc.connect(addr, port)
    response = conn.root.lookup(server_name)

    return response


if __name__ == "__main__":
  args = sys.argv[1:]
  if (len(args == 3)):
    [SERVER_NAME, SERVER_ADDR, SERVER_PORT] = args
    SERVER_PORT = int(SERVER_PORT)

    server = ThreadedServer(DirectoryServer1, port = SERVER_PORT)

    conn = rpyc.connect(ROOT_ADDR, ROOT_PORT)
    my_hostname = socket.gethostbyname(socket.gethostname())
    my_address = tuple(my_hostname, SERVER_PORT)

    response = conn.root.exposed_register(SERVER_NAME, my_address)
    print(response['message'])

    if (response['success']):
      print('Starting server...')
      server.start()
    else:
      response = conn.root.exposed_re_register(SERVER_NAME, my_address)
      print(response['message'])

      if (response['success']):
        server.start()
  else:
    print('Arguments invalid...')
