import socket as my_socket
from collections import deque as my_deque
from select import select as my_select


def initialize_server(port):
    socket = my_socket.socket(my_socket.AF_INET, my_socket.SOCK_STREAM)
    socket.setsockopt(my_socket.SOL_SOCKET, my_socket.SO_REUSEADDR, True)
    socket.bind(('localhost', port))
    socket.listen(5)

    print('Server is running')
    return socket


def waiting_for_connections(server_socket, active_connections):
    while True:
        print('Before accept():')

        yield ('read', server_socket)

        client_socket, address = server_socket.accept()                             # read
        print('Connection from', address)
        tasks.append(execute_server_logic(client_socket, active_connections))
        active_connections[client_socket] = address

        execute_server_logic(client_socket, active_connections)


def execute_server_logic(client_socket, active_connections):
    while True:

        yield ('read', client_socket)

        request = client_socket.recv(64)                                            # read

        if request:
            print('Client', active_connections[client_socket], end=': ')
            print(request.decode())
            response = 'Server: ' + request.decode()

            yield('write', client_socket)

            client_socket.send(response.encode())                                   # write
        else:
            client_socket.close()
            break


def run_event_loop():
    while any([tasks, to_read, to_write]):

        while not tasks:
            ready_to_read, ready_to_write, _ = my_select(to_read, to_write, [])

            for socket in ready_to_read:
                tasks.append(to_read.pop(socket))
            for socket in ready_to_write:
                tasks.append(to_write.pop(socket))

        try:
            task = tasks.popleft()
            reason, socket = next(task)

            if reason == 'read':
                to_read[socket] = task
            if reason == 'write':
                to_write[socket] = task
        except StopIteration:
            pass


if __name__ == '__main__':
    to_read = dict()
    to_write = dict()
    tasks = my_deque()

    server_port = 8888
    all_active_connections = dict()

    this_server_socket = initialize_server(server_port)

    tasks.append(waiting_for_connections(this_server_socket, all_active_connections))

    run_event_loop()
