import socket as my_socket
from select import select

server_socket = my_socket.socket(my_socket.AF_INET, my_socket.SOCK_STREAM)
server_socket.setsockopt(my_socket.SOL_SOCKET, my_socket.SO_REUSEADDR, True)
port = 8004
server_socket.bind(('localhost', port))
server_socket.listen()
print(f'Server is listeting localhost on port {port}...', flush=True)
to_monitor_read = [server_socket]
client_socket_and_address = {}


def accept_connection(server_socket):
    client_socket, address = server_socket.accept()
    print(f'Received connection from {address}...', flush=True)
    client_socket_and_address[client_socket] = address
    to_monitor_read.append(client_socket)


def send_message(client_socket):
    request = client_socket.recv(64)

    if request:
        print(f'From client: {request.decode()}', flush=True)
        client_socket.send(f'From server: {request.decode()}'.encode())
        return

    client_socket.close()
    to_monitor_read.remove(client_socket)
    print(f'Closed connection from {client_socket_and_address[client_socket]}...', flush=True)


def event_loop():
    while True:
        to_read, _, _ = select(to_monitor_read, [], [])

        for socket in to_read:
            if socket is server_socket:
                accept_connection(socket)
            else:
                send_message(socket)


if __name__ == '__main__':
    event_loop()
