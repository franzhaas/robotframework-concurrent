import socket
import select


def _socket_alive(s):
    return bool(s.recv(1, socket.MSG_PEEK))

def connect_http_bare(address, port: int):
    s = socket.socket()
    s.connect((address, port,))
    return s

def send_request_bare(s, request):
    s.send(request.encode())

def get_readables(*args):
    # recvable holds all sockets of args which would not block
    # when the recv method is called on them (also far side
    # closed ones)
    (recvable, _, __,)= select.select(args, [], [], 5)
    # get rid of far side closed sockets
    return [item for item in recvable if _socket_alive(item)]

def get_data(s):
    return s.recv(4096)
