import socket as my_socket
from select import select as my_select


def initialize_server(port):
    socket = my_socket.socket(my_socket.AF_INET, my_socket.SOCK_STREAM)
    socket.setsockopt(my_socket.SOL_SOCKET, my_socket.SO_REUSEADDR, True)
    socket.bind(('localhost', port))
    socket.listen(5)

    return socket


def accept_connection(socket, active_connections: dict):
    client_socket, address = socket.accept()
    print('Connection from', address)

    to_monitor.append(client_socket)
    active_connections[client_socket] = address


def execute_server_logic(socket, active_connections):
    request = socket.recv(32)

    if request:
        print('Client', active_connections[socket], end=': ')
        print(request.decode())
        response = 'Server: ' + request.decode()
        socket.send(response.encode())
    else:
        socket.close()
        active_connections.pop(socket)


def run_event_loop(server_socket, active_connections):
    while True:
        ready_to_read, _, _ = my_select(to_monitor, [], [])

        for socket in ready_to_read:
            if socket is server_socket:
                accept_connection(socket, active_connections)
            else:
                execute_server_logic(socket, active_connections)


if __name__ == "__main__":
    server_port = 6666
    to_monitor = []
    all_active_connections = dict()

    this_server_socket = initialize_server(server_port)
    to_monitor.append(this_server_socket)

    print('Server is running')
    run_event_loop(this_server_socket, all_active_connections)
