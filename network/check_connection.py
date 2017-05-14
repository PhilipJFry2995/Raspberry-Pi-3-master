import socket


def is_connected(remote_server, port):
    try:
        host = socket.gethostbyname(remote_server)
        socket.create_connection((host, port), 2)
        return True
    except:
        pass
    return False
