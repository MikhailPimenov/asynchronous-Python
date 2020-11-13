import socket as my_socket

server_socket = my_socket.socket(my_socket.AF_INET, my_socket.SOCK_STREAM)
server_socket.setsockopt(my_socket.SOL_SOCKET, my_socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 1489))
server_socket.listen(5)

counter = 0
while counter < 5:
    print('Before accept():')
    client_socket, address = server_socket.accept()
    print('Connection from', address)

    while True:
        request = client_socket.recv(64)

        if not request:
            break
        else:
            print(request.decode())
            response = 'Server: ' + request.decode()
            client_socket.send(response.encode())
    print('Connection from', address, 'is closed')
    counter += 1

    client_socket.close()