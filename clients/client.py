import sys
import rpyc
from constRPYC import *

class Client:
  servers = []

  args = sys.argv[1:]
  for i in range(len(args)):
      server_name = args[i]
      servers.append(server_name)

  for server in servers:
    conn = rpyc.connect(ROOT_ADDR, ROOT_PORT)
    response = conn.root.exposed_lookup(server)
    print(response['message'])

    if response['success']:
      (addr, port) = response['data']
      conn = rpyc.connect(addr, port)

      if (server == 'TimeWeather:Time'):
        print('Current time: ', conn.root.exposed_current_time())
        print('Current time formatted: ', conn.root.exposed_current_time_formatted())
      elif (server == 'TimeWeather:Weather'):
        print('Current temperature: ', conn.root.exposed_current_temperature())
      elif (server == 'Calculator:Sum'):
        print(conn.root.exposed_sum(14, 9))