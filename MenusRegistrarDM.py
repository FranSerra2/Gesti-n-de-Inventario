import sqlite3
from pathlib import Path
import tkinter as tk
from tkinter import Tk, Entry, Button, StringVar, OptionMenu, Canvas, Text, messagebox

class RegistrarDM1:
    def __init__(self, master, cambiar_a_registrarDM_2, cambiar_a_menuDm, conn):
        self.master = master

        canvas = Canvas(self.master, bg="#6B5E5E", height=768, width=1366, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        boton_cancelar = Button(self.master, text="Cancelar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_menuDm, relief="flat")
        boton_cancelar.place(x=735.11181640625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        boton_registrar = Button(self.master, text="Registrar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.registrar_producto(cambiar_a_registrarDM_2, conn), relief="flat")
        boton_registrar.place(x=391.47509765625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        self.observaciones = Text(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.observaciones.place(x=708.1552734375, y=440.0, width=607.0, height=118.0)
        canvas.create_text(712.1552734375, 405.0, anchor="nw", text="Observaciones", fill="#000000", font=("Inter Medium", 24 * -1))

        self.comentario = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.comentario.place(x=712.155273437, y=320.0, width=607.0, height=58.0)
        canvas.create_text(712.155273437, 280.0, anchor="nw", text="Comentario (Rellenar SOLO si lugar de guarda OTRO)", fill="#000000", font=("Inter Medium", 24 * -1))

        # Menú desplegable 2
        self.lugar_de_guarda_var = StringVar(self.master)
        self.lugar_de_guarda_var.set("ESCUELA DE FORMACION TECNICA LABORAL")
        lugar_de_guarda = OptionMenu(self.master, self.lugar_de_guarda_var, "ESCUELA DE FORMACION TECNICA LABORAL", "ESCUELA AGRARIA", "OTRO")
        lugar_de_guarda.place(x=707.0, y=200, width=607.6497192382812, height=59.03461837768555)
        canvas.create_text(712.1552734375, 165.0, anchor="nw", text="Lugar de guarda", fill="#000000", font=("Inter Medium", 24 * -1))

        # Menú desplegable 1
        self.area_var = StringVar(self.master)
        self.area_var.set("Mantenimiento - ESCUELA DE FORMACION TECNICA LABORAL")
        area = OptionMenu(self.master, self.area_var, "Mantenimiento - ESCUELA DE FORMACION TECNICA LABORAL", "Mantenimiento - ESCUELA AGRARIA", "Capacitacion - ESCUELA DE FORMACION TECNICA LABORAL", "Capacitacion - ESCUELA AGRARIA")
        area.place(x=35.0, y=560.0, width=607.6497192382812, height=59.03461837768555)
        canvas.create_text(38.0, 525.0, anchor="nw", text="Área", fill="#000000", font=("Inter Medium", 24 * -1))

        self.inventariado_var = StringVar(self.master)
        self.inventariado_var.set("NO")
        inventariado = OptionMenu(self.master, self.inventariado_var, "SI", "NO")
        inventariado.place(x=35.0, y=440.0, width=607.0, height=57.0)
        canvas.create_text(38.0, 405.0, anchor="nw", text="¿Articulo inventariado?", fill="#000000", font=("Inter Medium", 24 * -1))

        # Menú desplegable 3
        self.tipo_var = StringVar(self.master)
        self.tipo_var.set("Herramienta")
        tipo = OptionMenu(self.master, self.tipo_var, "Herramienta", "Maquinaria", "Insumo", "Limpieza")
        tipo.place(x=35.0, y=320, width=607.6497192382812, height=59.03461837768555)
        canvas.create_text(35.0, 285.0, anchor="nw", text="Tipo", fill="#000000", font=("Inter Medium", 24 * -1))

        self.producto = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.producto.place(x=35.0, y=200.0, width=607.0, height=58.0)
        canvas.create_text(38.0, 165.0, anchor="nw", text="Producto", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")
        canvas.create_text(423.0, 47.0, anchor="nw", text="REGISTRAR NUEVO PRODUCTO", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))

        canvas.pack()

            
    def registrar_producto(self, funcion, conn):
        # Recopilando los datos desde los widgets
        tipo_producto = self.tipo_var.get()
        producto = self.producto.get().strip().capitalize()
        cantidad_existente = 0
        area = self.area_var.get()
        lugar_guarda = self.lugar_de_guarda_var.get()
        cantidad_migrada = 0
        observaciones = self.observaciones.get("1.0", tk.END).strip().capitalize()
        inventariado = self.inventariado_var.get()

        if lugar_guarda == "OTRO":
            lugar_guarda = self.comentario.get().strip().capitalize()

        try:
            cursor = conn.cursor()  # Crear el cursor aquí
            # Inserción en la base de datos
            cursor.execute("""
                INSERT INTO stock (tipo_producto, Producto, Cantidad_existente, Area, Lugar_guarda, Cantidad_migrada, Observaciones, Inventariado)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (tipo_producto, producto, cantidad_existente, area, lugar_guarda, cantidad_migrada, observaciones, inventariado))
                
            print("Producto registrado exitosamente.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error.", "El producto ya existe, ingrese otro nombre.")
            self.producto.focus_set() #Enfoca el campo de producto
            return #No avanza hasta que se ingresa un valor valido
        except sqlite3.Error as e:
            messagebox.showerror(f"Error.", "Error al registrar producto: {e}")  # Manejo de otros errores
        finally:
            conn.commit()
            cursor.close()  # Cerrar el cursor después de usarlo
        funcion()


class RegistrarDM2:
    def __init__(self, root, cambiar_a_registrarDM, cambiar_a_menuDM):
        self.popup = tk.Toplevel(root)
        self.popup.geometry("773x245")
        self.popup.config(bg="#6B5E5E")
        self.popup.grab_set()
        self.popup.resizable(False, False)

        canvas = Canvas(self.popup, bg = "#6B5E5E", height = 245, width = 773, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x=0, y=0)

        boton_si = Button(self.popup, text="Sí", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_registrarDM), relief="flat") 
        boton_si.place(x=83.0, y=131.0, width=264.0133361816406, height=61.48335266113281)

        boton_no = Button(self.popup, text="No", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_menuDM), relief="flat") 
        boton_no.place(x=426.63671875, y=131.0, width=264.0133361816406, height=61.48335266113281)


        canvas.create_rectangle(0.0, 0.0, 773.0, 92.0, fill="#2B2626", outline="")

        canvas.create_text(216.0, 31.0, anchor="nw",
            text="¿Desea cargar otro producto?", fill="#FFFFFF",
            font=("Inter Medium", 24 * -1))
        
        canvas.pack()

    def cerrar_y_ejecutar(self, funcion):
        self.popup.destroy()  # Cierra la ventana emergente
        funcion() #Ejecuta la funcion dada

