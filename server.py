import socket
import threading
import json


def handle_client(client_socket, address):
    print(f"Connexion de {address}")
    while True:
        try:
            message = client_socket.recv(1024)
            if message.decode("utf8").startswith("givename"):
                print(message.decode("utf8"))
                with open("names.json", "r+") as f:
                    message = message.removeprefix(b"givename")
                    json_data = json.load(f)
                    json_data.append(message.decode("utf8"))
                    f.seek(0)
                    json.dump(json_data, f, indent=4)
                    f.truncate()  # supprime l'éventuel résidu si le nouveau contenu est plus court
                client_socket.send("Message du serveur : Nom reçu !".encode("utf8"))
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