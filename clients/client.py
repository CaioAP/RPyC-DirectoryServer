import rpyc
from constRPYC import *

class Client:
  servers_list = ['CounterTerrorist', 'Terrorist', 'Iluminados', 'Temidos', 'Neutros']

  conn_directory = rpyc.connect(DIR_SERVER_ROOT_ADDR, DIR_SERVER_ROOT_PORT)

  for server in servers_list:
    (address, error) = conn_directory.root.exposed_lookup(server)

    if error:
      print(address)
    else:
      (addr, port) = address
      print (f'Address: {addr} - Port: {port}')

      # if addr and port:
      #   conn = rpyc.connect(addr, port)
      #   conn.root.exposed_append(2)
      #   conn.root.exposed_append(4)
      #   print (conn.root.exposed_value())
