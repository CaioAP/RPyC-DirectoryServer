import sys
import rpyc
import socket
from constRPYC import *
from rpyc.utils.server import ThreadedServer

class DirectoryServer(rpyc.Service):
  servers = {}

  def exposed_register(self, server_name, address):
    if (server_name not in self.servers):
      self.servers[server_name] = address
      return dict(
        success = True, 
        message = f'Application server {server_name} registered successfully'
      )
    
    return dict(
      success = False, 
      message = f'Application server {server_name} already exists'
    )


  def exposed_lookup(self, server_name):
    if (server_name.find(':') > 0):
      return self.get_global_address(server_name)
    
    return self.get_local_address(server_name)


  def exposed_unregister(self, server_name):
    if (server_name not in self.servers):
      return dict(
        success = False,
        message = f'Application server {server_name} is not registered'
      )
    
    del self.servers[server_name]
    return dict(
      success = True,
      message = f'Application server {server_name} unregistered successfully'
    )


  def exposed_re_register(self, server_name, address):
    if (server_name not in self.servers):
      return self.exposed_register(server_name, address)
    
    self.servers[server_name] = address
    return dict(
      success = True,
      message = f'Application server {server_name} re-registered successfully'
    )


  def get_local_address(self, server_name):
    if (server_name not in self.servers):
      return dict(
        success = False,
        message = f'Application server {server_name} does not exist'
      )
    
    address = self.servers[server_name]
    return dict(
      success = True,
      message = f'Application server {server_name} found with address {address}',
      data = address
    )


  def get_global_address(self, server_name):
    conn = rpyc.connect(ROOT_ADDR, SERVER_PORT)
    response = conn.root.lookup(server_name)

    return response


if __name__ == "__main__":
  args = sys.argv[1:]
  if (len(args) == 2):
    [SERVER_NAME, SERVER_PORT] = args
    SERVER_PORT = int(SERVER_PORT)

    server = ThreadedServer(DirectoryServer, port = SERVER_PORT)

    conn = rpyc.connect(ROOT_ADDR, ROOT_PORT)
    SERVER_ADDR = socket.gethostbyname(socket.gethostname())
    my_address = (SERVER_ADDR, SERVER_PORT)

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
