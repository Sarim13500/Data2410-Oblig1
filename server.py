from socket import *
import sys


sock = socket(AF_INET, SOCK_STREAM)

serverPort = 12000

#Binder serveren og starter den
sock.bind(('127.0.0.1', serverPort))

#venter på at klienter skal joine serveren
sock.listen(1)

while True:
    # Klart til å betjene klient
    print("[Server] Klar til å koble seg til ")

    try:
        # Venter på innkommende TCP-forbindelse fra klient
        print("Ser etter tilkobling")
        connectionSocket, addr = sock.accept()

        # Leser melding fra klient
        message = connectionSocket.recv(1024).decode()

        # Henter filnavn fra meldingen
        filename = message.split()[1]
        print(filename)

        # Fjerner / fra filnavnet
        filename = filename[1:]

        # Åpner filen og leser innholdet
        f = open(filename)
        print("Prøver å åpne filen")
        outputdata = f.read()
        f.close()

        # HTTP respons. Sender innholdet til klienten
        header = 'HTTP/1.1 200 OK\r\n'
        header += 'Content-Type: text/html\r\n\r\n'
        header += outputdata
        connectionSocket.sendall(header.encode())


        # Lukker forbindelsen
        connectionSocket.close()

    except IOError:
        # Hvis filen ikke kan åpnes, sender en error 404 Not Found melding og lukker forbindelsen
        print("Filen eksisterer ikke")
        connectionSocket.send("HTTP/2.2 404 Not found\r\n\r\n".encode())
        connectionSocket.close()
        continue

#lukker serveren
print("Avslutter")
sock.close()
sys.exit()