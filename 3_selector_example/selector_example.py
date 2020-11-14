import socket as my_socket
import selectors as my_selectors


def initialise_server(port, active_connections, selectors):
    socket = my_socket.socket(my_socket.AF_INET, my_socket.SOCK_STREAM)
    socket.setsockopt(my_socket.SOL_SOCKET, my_socket.SO_REUSEADDR, True)
    socket.bind(('localhost', port))
    socket.listen(5)

    selectors.register(fileobj=socket, events=my_selectors.EVENT_READ,
                       data=(accept_connection, active_connections, selectors))

    return socket


def accept_connection(socket, active_connections, selectors):
    client_socket, address = socket.accept()
    active_connections[client_socket] = address
    print('Connection from', address)

    selectors.register(fileobj=client_socket, events=my_selectors.EVENT_READ,
                       data=(execute_server_logic, active_connections, selectors))


def execute_server_logic(socket, active_connections, selectors):
    request = socket.recv(64)

    if request:
        print('Client', active_connections[socket], end=': ')
        print(request.decode())
        response = 'Server: ' + request.decode()
        socket.send(response.encode())
    else:
        selectors.unregister(socket)
        print('Client', all_active_connections[socket], 'disconnected')
        all_active_connections.pop(socket)
        socket.close()


def run_event_loop(selectors):
    while True:
        events = selectors.select()

        for key, _ in events:
            callback = key.data[0]
            callback(key.fileobj, key.data[1], key.data[2])


if __name__ == '__main__':
    server_selectors = my_selectors.DefaultSelector()
    all_active_connections = dict()
    server_port = 7777
    this_server_socket = initialise_server(server_port, all_active_connections, server_selectors)

    print('Server is running')
    run_event_loop(server_selectors)
