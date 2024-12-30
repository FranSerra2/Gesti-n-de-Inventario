from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, Label
import sqlite3

class IniciarSesion:
    def __init__(self, master, switch_to_menuprincipal, conn):
        self.master = master     
        self.switch_to_menuprincipal = switch_to_menuprincipal

        canvas = Canvas(self.master, bg="#6B5E5E", height=768, width=1366, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        boton_iniciar_sesion = Button(self.master, text="Iniciar Sesión", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.validate_and_login(conn), relief="flat") 
        boton_iniciar_sesion.place(x=550.0, y=566.0, width=264.0133361816406, height=61.48335266113281)
       
        #boton_salir = Button(self.master, text="Salir", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_programa(), relief="flat") 
        #boton_salir.place(x=381.0, y=566.0, width=264.0133361816406, height=61.48335266113281)

        self.contrasenia = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, show="*")
        self.contrasenia.place(x=379.0, y=436.0, width=607.6497192382812, height=52.0)

        canvas.create_text(379.0, 402.0, anchor="nw", text="Contraseña", fill="#000000", font=("Inter Medium", 24 * -1))

        self.usuario = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.usuario.place(x=381.0, y=321.0, width=607.0, height=52.0)

        canvas.create_text(383.0, 288.0, anchor="nw", text="Usuario", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_rectangle(0.0, 0.0, 1366.0, 210.0, fill="#2B2626", outline="")
        canvas.create_text(467.0, 70.0, anchor="nw", text="INICIAR SESIÓN", fill="#FFFFFF", font=("PalanquinDark Regular", 60 * -1))

        canvas.pack()

        #Crea Label para mostrar msj de error.
        self.mensaje_error = Label(self.master, text="", fg="white", font=("Inter Medium", 24 * -1), bg="#6B5E5E")
        self.mensaje_error.place(x=379.0, y=500.0, width=607.0, height=40.0)

    def validate_and_login(self, conn):
        usuario = self.usuario.get()
        contrasenia = self.contrasenia.get()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Usuarios WHERE Nombre=? AND Password=?', (usuario, contrasenia))
        result = cursor.fetchone()

        if result is not None:
            self.switch_to_menuprincipal()
        else:
            self.mensaje_error.config(text="Usuario o contraseña incorrectos.")

    def cerrar_programa(self):
        self.master.destroy()


