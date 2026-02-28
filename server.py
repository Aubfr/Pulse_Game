import socket
import threading
import json



socket_client_data = {}

def handle_client(client_socket, address):
    print(f"Connexion de {address}")
    while True:
        try:
            message = client_socket.recv(1024)
            if message.decode("utf8").startswith("givename"):
                name = message.decode("utf8").removeprefix("givename").strip()

                socket_client_data[name] = client_socket

                client_socket.send("Nom reçu !".encode("utf8")) # TODO nettoyuer le client socket stocké.
                print(socket_client_data)
            elif not message:
                break
            else:
                print(f"Message reçu : {message.decode('utf8')}")
                client_socket.send("CONNEXIONOK".encode("utf8"))
        finally:
            print("Retour cycle")


socket_ecoute = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPV4 and TCP
socket_ecoute.bind(('', 5566)) # TODO localhost and port 5566
# Ici, le serveur est accessible depuis n'importe interface réseau

print("Serveur en attente...")

socket_ecoute.listen(5)
while True:
    client_socket, address = socket_ecoute.accept()

    thread = threading.Thread(
        target=handle_client,
        args=(client_socket, address)
    )
    thread.start()