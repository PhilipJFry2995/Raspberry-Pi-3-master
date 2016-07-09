import socket

def is_connected(REMOTE_SERVER, port):
  try:
    host = socket.gethostbyname(REMOTE_SERVER)
    s = socket.create_connection((host, port), 2)
    return True
  except:
    pass
  return False