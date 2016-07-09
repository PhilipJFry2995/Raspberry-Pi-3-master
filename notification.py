import socket
import time

def send_notification(message, ip, port, timeout):
  error = False
  sock = socket.socket()
  try:
    sock.connect((ip, port))
    sock.send(message)
    print 'Sent ' + str(message)
  except socket.error:
    error = True
    print 'Socket error'
  if (error and timeout < 10):
    sock.close()
    timeout = timeout + 1
    return send_notification(message, ip, port, timeout)
  else:
    sock.close()
    return 0