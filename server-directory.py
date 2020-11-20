import rpyc
from constRPYC import * #-
from rpyc.utils.server import ThreadedServer

class Directory(rpyc.Service):
  registry = {}

  def exposed_register(self, server_name, ip_address, port_number):
    message = 'Registration OK'

    if server_name not in self.registry:
      self.registry[server_name] = (ip_address, port_number)
    elif self.registry[server_name][0] == ip_address:
      self.registry[server_name] = (ip_address, port_number)
    else:
      message = 'Server name already exists!'

    print (self.registry)
    return message

  def exposed_unregister(self, server_name):
    if server_name in self.registry:
      del self.registry[server_name]
      return f'Server {server_name} unregistered!'
    else:
      return f'Server name does not exist!'

  def exposed_lookup(self, server_name):
    if server_name in self.registry:
      print (self.registry)
      return self.registry[server_name]
    else:
      print ('Server name does not exist!')
      return ('', 0)

if __name__ == "__main__":
  server = ThreadedServer(Directory, port = DIR_PORT)
  server.start()
