import socket
from shutil import copyfile
from os import remove

while True:
  sock = socket.socket()
  try:
    sock.connect(('46.101.114.237', 9090))
  except socket.error:
    #print 'SOCKET ERROOOOR'
    continue
    
  print 'Conntected to socket 9090'
  sock.send('10.36.5.157')
  while True:
    try:
      data = sock.recv(10)
      if data != '':
        print data
    except socket.error:
      print 'Socket error: Receiving failed!'
      break
    finally:
      if data != '':
        f = open('temp.json', 'a')
        f.write(data)
        f.close()
        data = None
      else:
        sock.close()
  try:
    copyfile('temp.json', 'config_backup.json')
    remove('temp.json')
    f = open('mode', 'w')
    f.write('1')
    f.close()
    print 'Configuration file updated'
  except IOError:
    print 'Error copying configuration file'
  