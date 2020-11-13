import socket as my_socket

port = 6666
client_socket = my_socket.socket(my_socket.AF_INET, my_socket.SOCK_STREAM)
client_socket.connect(('localhost', port))
print('Connected to localhost,', port)

counter = 0
while counter < 3:
    request = input()
    client_socket.send(request.encode())
    response = client_socket.recv(64)
    if response:
        print(response.decode())
    counter += 1
client_socket.close()
