import socket as my_socket
from select import select

from collections import deque

generators_as_tasks = deque()
to_read = {}
to_write = {}


def server(port: int):
    #  creating server socket: AF_INET - using adresses of IPv4-family, SOCK_STREAM - using TCP:
    server_socket = my_socket.socket(my_socket.AF_INET, my_socket.SOCK_STREAM)

    #  setting options: SOL_SOCKET - option is on socket layer,
    #  SO_REUSEADDR - option to reuse addresses:
    server_socket.setsockopt(my_socket.SOL_SOCKET, my_socket.SO_REUSEADDR, True)

    #  setting address to server:
    server_socket.bind(('localhost', port))

    #  activating server:
    server_socket.listen()

    print(f'Server is now listening localhost on port {port}...', flush=True)

    #  adding the very first task to task queue:
    generators_as_tasks.append(accept_connection(server_socket))


def accept_connection(server_socket: my_socket.socket):
    while True:
        #  before blocking function is called control of the flow is given back:
        yield ('read', server_socket)

        #  blocking function:  it is executed only when server_socket is ready to accept,
        #  so no waiting is here. The decision whether server_socket is ready to accept is
        #  made not here but in event loop using function 'select':
        client_socket, address = server_socket.accept()

        print(f'Connection from {address} is accepted:', flush=True)

        #  on this moment connection is established and client_socket is active,
        #  so it is added to task queue for function 'select' (in event loop)
        #  to watch if client_socket is ready to do something:
        generators_as_tasks.append(send_message(client_socket))


def send_message(client_socket: my_socket.socket):
    while True:
        #  before blocking function is called control of the flow is given back:
        yield ('read', client_socket)

        #  blocking function:  it is executed only when client_socket is ready to receive
        #  (read from buffer), so no waiting is here. The decision whether client_socket
        #  is ready to receive is made not here but in event loop using function 'select':
        request = client_socket.recv(64)

        if not request:
            client_socket.close()
            print('One of connections is closed.', flush=True)
            return

        print(f'Message: {request.decode()}', flush=True)

        response = f'From server: {request.decode()}'

        #  before blocking function is called control of the flow is given back:
        yield ('write', client_socket)

        #  blocking function:  it is executed only when client_socket is ready to send
        #  (write in buffer), so no waiting is here. The decision whether client_socket
        #  is ready to sent is made not here but in event loop using function 'select':
        client_socket.send(response.encode())

        print(f'Sent to user: {response}', flush=True)


def event_loop():
    while any([generators_as_tasks, to_read, to_write]):

        #  while there are no tasks in queue - adding them from lists of ready sockets:
        while not generators_as_tasks:

            #  getting lists with sockets ready for actions. to_read, to_write are dictionaries
            #  with sockets as keys, so 'select' will take from them only lists of keys
            #  so they are exactly the sockets what 'select' is waiting for:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            for socket in ready_to_read:
                #  task is represented as generator object, but socket in list of ready sockets
                #  is not a generator object. In dictionary to_read keys are sockets, but values
                #  are generator objects. When socket is ready to read it is no longer needed in
                #  list for 'select', so it is removed from there. And as value in dictionary is
                #  generator object it suits for task queue and it is added there. pop() removes
                #  key from dictionary (that means that the socket (key) is removed from list for
                #  'select') and returns the value which is generator object (that means that it is
                #  added to the task queue):
                generators_as_tasks.append(to_read.pop(socket))

            for socket in ready_to_write:
                #  same with sockets for writing:
                generators_as_tasks.append(to_write.pop(socket))

        #  getting the next task from the task queue:
        generator_as_task = generators_as_tasks.popleft()

        try:
            #  all generators are yielding label and socket. Label represents what is that
            #  socket ready for: read or write.
            #  Executing code in generator, reading or writing occurs here in 'next':
            reason, socket = next(generator_as_task)

            #  generator is executed and yielded pair of label and socket before the next
            #  blocking function call with that socket in generator, so this socket is needed
            #  to be added to dictionary for function 'select' to decide when this socket will be
            #  ready to read or write:
            if reason == 'read':
                to_read[socket] = generator_as_task
            if reason == 'write':
                to_write[socket] = generator_as_task
        except StopIteration:
            print('Done!')


if __name__ == '__main__':
    server(8004)
    event_loop()
