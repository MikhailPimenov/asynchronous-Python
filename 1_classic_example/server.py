import socket as my_socket

if __name__ == '__main__':
    server_socket = my_socket.socket(my_socket.AF_INET, my_socket.SOCK_STREAM)
    server_socket.setsockopt(my_socket.SOL_SOCKET, my_socket.SO_REUSEADDR, True)
    port = 8004
    server_socket.bind(('localhost', port))
    server_socket.listen()
    print(f'Server is listening localhost on port {port}', flush=True)

    connection_counter = 0
    while connection_counter < 5:
        print('Before accept():', flush=True)
        client_socket, address = server_socket.accept()
        print(f'Connection from {address} accepted:', flush=True)

        message_counter = 0
        while message_counter < 5:
            request = client_socket.recv(64)
            print(f'Received from {address}: {request.decode()}', flush=True)

            if not request:
                break

            response = f'From server: {request.decode()}'
            client_socket.send(response.encode())
            print(f'Sent back: {response}', flush=True)

            message_counter += 1

        client_socket.close()
        print(f'Connection {address} is closed.')

        connection_counter += 1

    server_socket.close()
    print('Server is shut down.')
