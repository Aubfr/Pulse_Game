
from tkinter import Tk, Button, Label
from tkinter import *
import tkinter.font as font
import socket

# On définit une classe qui dérive de la classe Tk (la classe de fenêtre).
class MyWindow(Tk):

    def __init__(self):
        # On appelle le constructeur parent
        super().__init__()

        f_35 = font.Font(family="Iosevka", size = 35)
        f_15 = font.Font(family="Iosevka", size = 15)
        self.configure(bg='black')
        
        def demarrage():
            first_label.place_forget()
            second_label.place_forget()
            button.place_forget()

            host, port = ("localhost", 5566)
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                client_socket.connect((host, port))
                print("Client connecte!")

                data = "Test"
                data = data.encode("utf8")
                client_socket.sendall(data)

            except ConnectionRefusedError:
                print("Connexion échouée !")

            finally:
                client_socket.close()



        # On positionne un premier label en (10, 10)
        first_label = Label(self, text="PulseGame")
        first_label["font"] = f_35
        first_label.place(x=400, y=1)


        second_label = Label(self, text ="Bienvenue !")
        second_label["font"] = f_15
        second_label.place(x = 450, y = 200)
        # expression = StringVar()
        # expression.set("6*7")     # texte par défaut affiché dans l'entrée
        # entree = Entry(self, textvariable = expression, width = 30)
        # entree.place(x = 500, y = 200)


        # Enfin on positionne un bouton en (90, 90)
        button = Button(self, text="Se connecter au jeu", fg="black", bg ="aqua", command=demarrage)
        button.place(x=450, y=260)

        # On dimensionne la fenêtre (300 pixels de large par 200 de haut).
        self.geometry("1000x700")

        # On ajoute un titre à la fenêtre
        self.title("PulseGame")


# On crée notre fenêtre et on l'affiche
window = MyWindow()
window.mainloop()












import socket
