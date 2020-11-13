import socket as my_socket

client_socket = my_socket.socket(my_socket.AF_INET, my_socket.SOCK_STREAM)
client_socket.connect(('localhost', 1489))
print('Connected to localhost,', 1489)

counter = 0
while counter < 3:
    request = input()
    client_socket.send(request.encode())
    response = client_socket.recv(64)
    if response:
        print(response.decode())
    counter += 1
client_socket.close()
