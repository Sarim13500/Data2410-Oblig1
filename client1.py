import sys
import socket

# Tar inn argumentene som er gitt
if len(sys.argv) < 4:
    print('Skriv inn: python3 client.py server_host server_port filnavn')
    sys.exit(1)

server_host = sys.argv[1]
server_port = int(sys.argv[2])
filename = sys.argv[3]

#Åpner en TCP connection til serveren
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))

#Sender en HTTP GET request til serveren
request = f'GET /{filename} HTTP/1.1\r\nHost: {server_host}\r\n\r\n'
client_socket.send(request.encode())

#Mottar og skriver ut server responsen
response = client_socket.recv(4096)
print(response.decode())

# Lukker socketem
client_socket.close()
