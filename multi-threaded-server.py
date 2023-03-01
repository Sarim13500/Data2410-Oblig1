from socket import *
import sys
import _thread as thread


sock = socket(AF_INET, SOCK_STREAM)

#Binder serveren
serverPort = 12000
sock.bind(('127.0.0.1', serverPort))
sock.listen(1)

#Lager funksjonen handleclient som sjekker om filen klienten spør etter er tilgjengelig
def handleclient (connectionSocket, addr):


    try:
        # Leser melding fra klient
        message = connectionSocket.recv(1024).decode()


        # Henter filnavn fra meldingen
        filename = message.split()[1]
        print(filename)

        # Fjerner / fra filnavnet
        filename = filename[1:]

        # Åpner filen og leser innholdet
        fopen = open(filename)
        print("Prøver å åpne filen")
        outputdata = fopen.read()
        fopen.close()

        # HTTP responsheader
        header = 'HTTP/1.1 200 OK\r\n'
        header += 'Content-Type: text/html\r\n\r\n'
        header += outputdata
        connectionSocket.sendall(header.encode())

        # connectionSocket.sendall("\r\n".encode())

        # Lukker forbindelsen
        connectionSocket.close()

    except IOError:
        # Hvis filen ikke kan åpnes, sender en error 404 Not Found melding og lukker forbindelsen
        print("Filen eksisterer ikke")
        connectionSocket.send("HTTP/2.2 404 Not found\r\n\r\n".encode())
        connectionSocket.close()



#mens serveren er åpen
while True:
    # Klart til å betjene klient
    print("[Server] Klar til å koble seg til ")


    connectionSocket, addr = sock.accept()

    #Kaller på metoden handleclient som returnerer fil eller feilmelding
    thread.start_new_thread(handleclient, (connectionSocket, addr))



print("Avslutter")
sock.close()
sys.exit()