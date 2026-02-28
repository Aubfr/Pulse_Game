from tkinter import Tk, Button, Label
from tkinter import *
import tkinter.font as font
import socket

connexion_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # permet connexion : IPV4 et TCP
connexion_serveur.connect(('192.168.1.236', 5566)) # TODO à remplacer par l'adresse IPV4 du PC hôte
data = "Demande de connexion d'un client ! -- MESSAGE INITIAL"
data = data.encode("utf8")
connexion_serveur.send(data)

class PulseGame_wait(Toplevel):
    def __init__(self, master):
        super().__init__(master)

        f_15 = font.Font(family="Iosevka", size=15)

        self.configure(bg='black')
        self.geometry("1000x700")
        self.title("PulseGame_client_name")

        self.label = Label(self, bg="red", font=f_15)
        self.label.place(x=400, y=300)

        self.dots = 0
        self.animate()
    def animate(self):
        self.dots = (self.dots % 3) + 1
        self.label.config(text="En attente de l'hôte " + "." * self.dots)
        self.after(300, self.animate)
        self.label_confirm = Label(self, bg ="red")
        self.label_confirm.place(x = 200, y = 200)



class PulseGame_input_name(Tk):
    def __init__(self):
        super().__init__()

        f_35 = font.Font(family="Iosevka", size = 35)
        f_15 = font.Font(family="Iosevka", size = 15) # polices pour pouvoir mieux éditer la fenêtre
        self.configure(bg='black')
        
        def stock_name():

            try:
                print("DEBUG : Vous êtes sur le point de donner son nom !")
                entry_name = entry.get()
                prefix_for_server = "givename"
                data = (prefix_for_server + entry_name).encode("utf8")
                connexion_serveur.sendall(data)

            except ConnectionRefusedError:
                print("Connexion échouée ! Voir si le serveur est démarré ou non ...")

            finally:
                try:
                    get_verif = connexion_serveur.recv(1024)
                    print(get_verif.decode("utf8"))
                except:
                    print("L'envoie du nom a échoué")
                if get_verif.decode("utf8").startswith("Nom"):
                    # TODO Ici lancement de la fenêtre de jeu
                    print("DEBUG : Votre nom a bien été stocké par le serveur !")
                else:
                    print("La vérification demandée au serveur a échouée !")
                PulseGame_wait(self)
                self.withdraw()

        self.pulse_game_logo = PhotoImage(file="pulse_game_logo.png")
        label_logo = Label(self, image=self.pulse_game_logo)
        label_logo.place(x = 100, y = 300)

        label_name = Label(self, text="Veuillez entrer votre nom pour commencer !", bg = "aqua")
        label_name["font"] = f_15
        label_name.place(x = 300, y = 100)

        entry = Entry(self,font=f_35, fg = "black")
        entry.place(x = 270, y = 150)

        button_name = Button(self, text="Valider", command= stock_name)
        button_name["font"] = f_15
        button_name.place(x= 460, y = 240)

        label_credits = Label(self, text="Dévéloppé par Aubin avec les conseils d'Oery et la contribution de Chamseddine", bg="black", fg="white")
        label_credits["font"] = f_15
        label_credits.place(x = 110, y = 665)

        self.geometry("1000x700")

        self.title("PulseGame_client_name")


get_game_state = connexion_serveur.recv(1024)
message = get_game_state.decode("utf8")
print(f"Message exact reçu: {message}")
if message == "CONNEXIONOK":
    print("Lancement de l'interface pour donner son nom ...")
    window = PulseGame_input_name()
    window.mainloop()
else:
    print("ERROR : Le serveur n'a pas pu communiquer l'état du jeu actuel !")

