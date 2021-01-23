import sys
import rpyc
import socket
from constRPYC import *
from rpyc.utils.server import ThreadedServer
from datetime import datetime

class ApplicationServer(rpyc.Service):
  value = []

  def exposed_current_time(self):
    return datetime.now()

  def exposed_current_time_formatted(self):
    now = datetime.now()
    hour = str(now.hour).rjust(2, '0')
    minute = str(now.minute).rjust(2, '0')
    second = str(now.second).rjust(2, '0')
    day = str(now.day).rjust(2, '0') 
    month = str(now.month).rjust(2, '0')
    year = str(now.year)
    return f'{hour}:{minute}:{second} - {day}/{month}/{year}'

if __name__ == "__main__":
  args = sys.argv[1:]
  if (len(args) == 3):
    [SERVER_NAME, SERVER_PORT, DIR_NAME] = args
    SERVER_PORT = int(SERVER_PORT)

    server = ThreadedServer(ApplicationServer, port = SERVER_PORT)

    conn = rpyc.connect(ROOT_ADDR, ROOT_PORT)
    response = conn.root.exposed_lookup(DIR_NAME)
    print(response['message'])

    if (response['success']):
      (addr, port) = response['data']

      SERVER_ADDR = socket.gethostbyname(socket.gethostname())
      my_address = (SERVER_ADDR, SERVER_PORT)

      conn = rpyc.connect(addr, port)
      response = conn.root.exposed_register(SERVER_NAME, my_address)
      print(response['message'])

      if (response['success']):
        print('Starting server...')
        server.start()
    else:
      print(response['message'])

  else:
    print('Arguments invalid...')
