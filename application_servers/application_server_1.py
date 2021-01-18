import rpyc
import socket
from constRPYC import *
from rpyc.utils.server import ForkingServer

class ApplicationServer1(rpyc.Service):
  value = []

  def exposed_append(self, data):
    self.value = self.value + [data]
    print ('Appended value: ', data)
    return self.value

  def exposed_value(self):
    return self.value

if __name__ == "__main__":
  server = ForkingServer(ApplicationServer1, port = APP_SERVER_1_PORT)
  conn = rpyc.connect(DIR_SERVER_ROOT_ADDR, DIR_SERVER_ROOT_PORT)
  my_addr = socket.gethostbyname(socket.gethostname())
  (fully_qualified_name, error) = conn.root.exposed_register('Application_1', my_addr, APP_SERVER_1_PORT)
  print(fully_qualified_name)

  if not error:
    server.start()
