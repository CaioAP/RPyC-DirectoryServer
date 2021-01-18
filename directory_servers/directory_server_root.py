import rpyc
from constRPYC import *
from rpyc.utils.server import ThreadedServer

class DirectoryServerRoot(rpyc.Service):
  servers = {}

  def exposed_register(self, server_name, address):
    if (server_name not in self.servers):
      self.servers[server_name] = address
      return dict(
        success = True, 
        message = f'Directory server {server_name} registered successfully'
      )
    
    return dict(
      success = False, 
      message = f'Directory server {server_name} already exists'
    )


  def exposed_lookup(self, server_name):
    if (server_name.find(':') > 0):
      return self.get_local_address(server_name)
    
    dir_name = server_name.split(':')[0]
    server_name = server_name.split(':')[1]
    return self.get_global_address(dir_name, server_name)
      

  def exposed_unregister(self, server_name):
    if (server_name not in self.servers):
      return dict(
        success = False,
        message = f'Directory server {server_name} is not registered'
      )
    
    del self.servers[server_name]
    if (server_name not in self.servers):
      return dict(
        success = True,
        message = f'Directory server {server_name} unregistered successfully'
      )
    else:
      return dict(
        success = False,
        message = f'Error trying to unregister directory server {server_name}'
      )


  def exposed_re_register(self, server_name, address):
    if (server_name not in self.servers):
      return self.exposed_register(server_name, address)
    
    self.servers[server_name] = address
    return dict(
      success = True,
      message = f'Directory server {server_name} re-registered successfully'
    )


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
  server = ThreadedServer(DirectoryServerRoot, port = ROOT_PORT)
  server.start()
