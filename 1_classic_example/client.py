import socket as my_socket

if __name__ == '__main__':
    client_socket = my_socket.socket(my_socket.AF_INET, my_socket.SOCK_STREAM)
    port = 8004
    client_socket.connect(('localhost', port))
    print(f'Connected to server localhost on port {port}:')

    message_counter = 0
    while message_counter < 5:
        request = input()

        client_socket.send(request.encode())

        response = client_socket.recv(64)

        if response:
            print(f'Received from the server: {response.decode()}')

        message_counter += 1

    client_socket.close()
    print('Connection is closed.')
