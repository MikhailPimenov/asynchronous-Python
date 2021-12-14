import socket as my_socket
import selectors as my_selectors

selector = my_selectors.DefaultSelector()


def prepare_server_socket(port):
    #  setting parameters for server socket:
    #  AF_INET - using IPv4, SOCK_STREAM - using TCP
    server_socket = my_socket.socket(my_socket.AF_INET, my_socket.SOCK_STREAM)

    #  SOL_SOCKET - layer of the option, SO_REUSEADDR - actual option - to reuse addresses,
    #  True - means turn it on
    server_socket.setsockopt(my_socket.SOL_SOCKET, my_socket.SO_REUSEADDR, True)

    #  giving server address:
    server_socket.bind(('localhost', port))

    #  activating server:
    server_socket.listen()

    print(f'Server is listening localhost at port {port}', flush=True)

    #  registering server_socket: now selector is going to watch changes in server_socket,
    #  exactly when it is going to be ready to be read.
    #  EVENT_READ means what kind of events are considered (ready to be read)
    #  data - actual payload, which is going to be used by us after
    selector.register(fileobj=server_socket, events=my_selectors.EVENT_READ, data=accept_connection)


def accept_connection(server_socket):
    #  accepting connection from the client with client_socket and address
    client_socket, address = server_socket.accept()
    print(f'Connection from {address}...', flush=True)

    #  registering client_socket: now selector is going to watch changes also in client_socket
    selector.register(fileobj=client_socket, events=my_selectors.EVENT_READ, data=send_message)


def send_message(client_socket):
    #  receiving something from client:
    request = client_socket.recv(64)

    if request:
        print(f'From client: {request.decode()}', flush=True)

        response = f'From server: {request.decode()}'

        #  sending back answer:
        client_socket.send(response.encode())
        return

    #  excluding client_socket from list with fileobjects (sockets) to watch
    #  (telling selector that we are no longer interested in client_socket, because it is closed)
    selector.unregister(client_socket)

    #  closing connection
    client_socket.close()
    print('Connection is closed...', flush=True)


def event_loop():
    while True:
        #  getting everything what is ready:
        keys_and_events = selector.select()

        #  handling every socket
        for key, _ in keys_and_events:
            callback = key.data    # payload
            callback(key.fileobj)  # executing


if __name__ == '__main__':
    prepare_server_socket(8004)
    event_loop()
