import tkinter as tk
from tkinter import Canvas, Button, Entry, StringVar, OptionMenu, ttk, Text, messagebox
import sqlite3
from funciones import mostrar_tree_inventario_modificacion, obtener_datos

class RegistrarInventariado:
    def __init__(self, master, cambiar_a_menuDM, cambiar_a_confirmacion, primary_key, conn):
        self.master = master
        canvas = Canvas(self.master, bg = "#6B5E5E", height = 768, width = 1366, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x=0, y=0)
        self.selected_product = primary_key

        boton_registrar = Button(self.master, text="Registrar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.registrar_datos(cambiar_a_confirmacion, conn, self.selected_product), relief="flat") 
        boton_registrar.place(x=391.47509765625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        boton_cancelar = Button(self.master, text="Cancelar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_menuDM, relief="flat") 
        boton_cancelar.place(x=707.0, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        self.observaciones = Text(bd=0, bg="#FFFFFF",  fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.observaciones.place(x=707.0, y=440.0, width=607.0, height=110.0)

        canvas.create_text(712.1552734375, 400.0,  anchor="nw", text="Observaciones", fill="#000000", font=("Inter Medium", 24 * -1))

        self.lugar_var = StringVar(master)
        self.lugar_var.set("ESCUELA DE FORMACION TECNICA LABORAL")  # Valor predeterminado

        lugar_menu = OptionMenu(master, self.lugar_var, "ESCUELA DE FORMACION TECNICA LABORAL", "ESCUELA AGRARIA", "OTRO")
        lugar_menu.place(x=707.0, y=200.0, width=607.6497192382812, height=59.03461837768555)

        canvas.create_text(712.1552734375, 160.0, anchor="nw", text="Lugar de guarda", fill="#000000",  font=("Inter Medium", 24 * -1))

        self.comentario = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.comentario.place(x=707.0, y=320.0, width=607.6497192382812, height=59.03461837768555)
        
        canvas.create_text(712.1552734375, 280.0, anchor="nw", text="Comentario (completar SOLO si lugar de guarda es OTRO)", fill="#000000",  font=("Inter Medium", 24 * -1))

        self.area_var = StringVar(master)
        self.area_var.set("Mantenimiento - ESCUELA DE FORMACION TECNICA LABORAL")  # Valor predeterminado
        area_menu = OptionMenu(master, self.area_var, "Mantenimiento - ESCUELA DE FORMACION TECNICA LABORAL", "Mantenimiento - ESCUELA AGRARIA", "Capacitacion - ESCUELA DE FORMACION TECNICA LABORAL", "Capacitacion - ESCUELA AGRARIA")
        area_menu.place(x=35.0, y=560.0, width=607.6497192382812, height=59.03461837768555)

        canvas.create_text(38.0, 520.0, anchor="nw", text="Área",  fill="#000000", font=("Inter Medium", 24 * -1))

        self.detalle = Entry(bd=0,  bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.detalle.place(x=35.0, y=320.0, width=607.0, height=57.0)

        canvas.create_text(38.0, 280.0, anchor="nw", text="Detalle", fill="#000000", font=("Inter Medium", 24 * -1))

        self.numero_inventariado = Entry(bd=0,  bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.numero_inventariado.place(x=35.0, y=440.0, width=607.0, height=57.0)

        canvas.create_text(38.0, 400.0, anchor="nw", text="Número de inventariado", fill="#000000", font=("Inter Medium", 24 * -1))
        
        #canvas.create_text(35.0, 280.0, anchor="nw", text="Tipo", fill="#000000", font=("Inter Medium", 24 * -1))
        
        self.estado_var = StringVar(master)
        self.estado_var.set("ACTIVO")  # Valor predeterminado
        
        tipo_menu = OptionMenu(master, self.estado_var, "ACTIVO", "BAJA")
        tipo_menu.place(x=35.0, y=200.0, width=607.6497192382812, height=59.03461837768555)

        canvas.create_text(38.0, 160.0, anchor="nw", text="Estado", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        canvas.create_text(480.0, 47.0, anchor="nw", text="REGISTRAR INVENTARIADO", fill="#FFFFFF",  font=("PalanquinDark Regular", 36 * -1))

        canvas.pack()

    

    def registrar_datos(self, funcion, conn, primary_key):
        observaciones = self.observaciones.get("1.0", tk.END).strip().capitalize()
        lugar = self.lugar_var.get()
        area = self.area_var.get()
        detalle = self.detalle.get().strip().capitalize()
        nro_invent = self.numero_inventariado.get().strip().upper()
        estado = self.estado_var.get()
        comentario = self.comentario.get().strip().capitalize()

        if lugar == "OTRO":
            lugar = comentario

        try:
            cursor = conn.cursor()
            cursor.execute("""UPDATE stock
                           SET Inventariado = 'SI'
                           WHERE Producto = ?""", (primary_key,))
            cursor.execute("""SELECT tipo_producto FROM stock WHERE Producto = ?""", (primary_key,))
            temporal = cursor.fetchone()
            if temporal is None:
                print("No se encontró el producto especificado.")
                return
            tipo = temporal[0]
            cursor.execute("""
                        INSERT INTO Inventariados (tipo_producto, Producto, detalle, Area, lugar_guarda, observaciones, Nro_inventario, estado)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",(tipo, primary_key, detalle, area, lugar, observaciones, nro_invent, estado))
        except sqlite3.IntegrityError:
            messagebox.showerror("Error.", "El nro de inventariado o el producto ya se encuentra registrado")
            self.producto.focus_set() #Enfoca el campo de producto
            return #No avanza hasta que se ingresa un valor valido
        except sqlite3.Error as e:
            messagebox.showerror("Error.", f"Error al registrar producto: {e}")  # Manejo de otros errores
        finally:
                conn.commit()
                cursor.close()  # Cerrar el cursor después de usarlo
        funcion()



class RegistrarInventariadoPT2:
    def __init__(self, root, cambiar_a_inventariado_1, cambiar_a_menuDM):
        self.popup = tk.Toplevel(root)
        self.popup.geometry("773x245")
        self.popup.config(bg="#6B5E5E")
        self.popup.grab_set()
        self.popup.resizable(False, False)

        canvas = Canvas(self.popup, bg = "#6B5E5E", height = 245, width = 773, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)

        boton_cancelar = Button(self.popup, text="No", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_menuDM), relief="flat")
        boton_cancelar.place(x=426.63671875, y=131.0, width=264.0133361816406, height=61.48335266113281)

        boton_confirmar = Button(self.popup, text="Sí", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_inventariado_1), relief="flat")
        boton_confirmar.place(x=83.0, y=131.0, width=264.0133361816406, height=61.48335266113281)

        canvas.create_rectangle(0.0, 0.0, 773.0, 92.0, fill="#2B2626", outline="")

        canvas.create_text(190.0, 31.0, anchor="nw", text="¿Desea registrar otro producto inventariado?", fill="#FFFFFF", font=("Inter Medium", 24 * -1))

        canvas.pack()

    def cerrar_y_ejecutar(self, funcion):
        self.popup.destroy()  # Cierra la ventana emergente
        funcion() #Ejecuta la funcion dada

class ModificarInventariadoPT0:
    def __init__(self, master, cambiar_a_visualizarDM_2, cambiar_a_menuDM, conn):
        self.master = master
        
        canvas = Canvas(self.master, bg="#6B5E5E", height=768, width=1366, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        boton_cancelar = Button(self.master, text="Cancelar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_menuDM, relief="flat") 
        boton_cancelar.place(x=735.11181640625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        boton_seleccionar = Button(self.master, text="Seleccionar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cambiar_pantalla(cambiar_a_visualizarDM_2), relief="flat") 
        boton_seleccionar.place(x=391.47509765625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        canvas.create_rectangle(38.0, 279.0, 1328.0, 641.0, fill="#FFFFFF", outline="")

        # Entradas para Nro inventariado y Producto
        self.nro_inventariado_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.nro_inventariado_entry.place(x=885.0, y=197.0, width=443.0, height=57.0)
        canvas.create_text(885.0, 164.0, anchor="nw", text="Nro inventariado", fill="#000000", font=("Inter Medium", 24 * -1))

        self.producto_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.producto_entry.place(x=560.0, y=197.0, width=288.0, height=57.0)
        canvas.create_text(560.0, 164.0, anchor="nw", text="Producto", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_text(38.0, 164.0, anchor="nw", text="Tipo Producto", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")
        canvas.create_text(354.0, 47.0, anchor="nw", text="MODIFICAR PRODUCTO INVENTARIADO", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))

        # Menú desplegable para "Tipo Producto"
        self.tipo_producto = StringVar(self.master)
        self.tipo_producto.set("Tipo de producto")  # Valor por defecto
        dropdown_tipo = OptionMenu(self.master, self.tipo_producto, "Herramienta", "Maquinaria")
        dropdown_tipo.place(x=40.0, y=197.0, width=483.0, height=59.03461837768555)

        canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        canvas.create_text(483.0, 47.0, anchor="nw", text="PRODUCTOS INVENTARIADOS", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))

        # Crear el Treeview
        self.tree = mostrar_tree_inventario_modificacion(
            canvas,
            self.nro_inventariado_entry,
            self.producto_entry,
            self.tipo_producto,
            conn
        )

        canvas.pack()
    
    def cambiar_pantalla(self, cambiar_a_modif_invent_2):
        selected_item = self.tree.selection()
        if selected_item:
            self.nro_inventariado = self.tree.item(selected_item, "values")[6]
            cambiar_a_modif_invent_2(self.nro_inventariado)


class ModificarInventariadoPT1:
    def __init__(self, master, cambiar_a_menuDM, cambiar_a_confirmacion, producto_seleccionado, conn):
        self.master = master
        self.producto_seleccionado = producto_seleccionado
        lista = obtener_datos(self.producto_seleccionado, conn)
               
        canvas = Canvas(self.master, bg = "#6B5E5E", height = 768, width = 1366, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x=0, y=0)

        boton_registrar = Button(self.master, text="Modificar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.modificar_datos(cambiar_a_confirmacion, conn, self.producto_seleccionado), relief="flat") 
        boton_registrar.place(x=391.47509765625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        boton_cancelar = Button(self.master, text="Cancelar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_menuDM, relief="flat") 
        boton_cancelar.place(x=707.0, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        self.observaciones = Text(bd=0, bg="#FFFFFF",  fg="#000716", highlightthickness=0)
        self.observaciones.place(x=707.0, y=440.0, width=607.0, height=110.0)
        self.observaciones.insert("1.0", lista[5])

        canvas.create_text(712.1552734375, 400.0,  anchor="nw", text="Observaciones", fill="#000000", font=("Inter Medium", 24 * -1))

        self.lugar_var = StringVar(master)
        self.lugar_var.set(lista[4])

        lugar_menu = OptionMenu(master, self.lugar_var, "ESCUELA DE FORMACION TECNICA LABORAL", "ESCUELA AGRARIA", "OTRO")
        lugar_menu.place(x=707.0, y=320.0, width=607.6497192382812, height=59.03461837768555)
        
        canvas.create_text(712.1552734375, 280.0, anchor="nw", text="Lugar de guarda", fill="#000000",  font=("Inter Medium", 24 * -1))

        self.area_var = StringVar(master)
        self.area_var.set(lista[3])  # Valor predeterminado

        area_menu = OptionMenu(master, self.area_var, "Mantenimiento - ESCUELA DE FORMACION TECNICA LABORAL", "Mantenimiento - ESCUELA AGRARIA", "Capacitacion - ESCUELA DE FORMACION TECNICA LABORAL", "Capacitacion - ESCUELA AGRARIA")
        area_menu.place(x=707.0, y=200.0, width=607.6497192382812, height=59.03461837768555)

        canvas.create_text(708.1552734375, 160.0, anchor="nw", text="Área",  fill="#000000", font=("Inter Medium", 24 * -1))

        self.detalle = Entry(bd=0,  bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.detalle.place(x=35.0, y=320.0, width=607.0, height=57.0)
        self.detalle.insert(0, lista[2])
        canvas.create_text(38.0, 280.0, anchor="nw", text="Detalle", fill="#000000", font=("Inter Medium", 24 * -1))

        self.numero_inventariado = Entry(bd=0,  bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.numero_inventariado.place(x=35.0, y=440.0, width=607.0, height=57.0)
        self.numero_inventariado.insert(0, producto_seleccionado)

        canvas.create_text(38.0, 400.0, anchor="nw", text="Número de inventariado", fill="#000000", font=("Inter Medium", 24 * -1))
        
        self.estado_var = StringVar(master)
        self.estado_var.set(lista[7])
        
        tipo_menu = OptionMenu(master, self.estado_var, "ACTIVO", "BAJA")
        tipo_menu.place(x=35.0, y=200.0, width=607.6497192382812, height=59.03461837768555)

        canvas.create_text(38.0, 160.0, anchor="nw", text="Estado", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        canvas.create_text(480.0, 47.0, anchor="nw", text="MODIFICAR INVENTARIADO", fill="#FFFFFF",  font=("PalanquinDark Regular", 36 * -1))

        canvas.pack()

    def modificar_datos(self, funcion, conn, nro_inventariado):
        observaciones = self.observaciones.get("1.0", tk.END).strip().capitalize()
        lugar = self.lugar_var.get()
        area = self.area_var.get()
        detalle = self.detalle.get().strip().capitalize()
        nro_invent = self.numero_inventariado.get().strip().upper()
        estado = self.estado_var.get()
        

        try:
            cursor = conn.cursor()

            cursor.execute("""SELECT Producto FROM Inventariados WHERE Nro_inventario = ? """, (nro_inventariado,))
            producto = cursor.fetchone()
            if producto:
                producto = producto[0]  
                print(producto)
            cursor.execute("""
                        UPDATE Inventariados
                        SET detalle = ?,
                           Area = ?,
                           lugar_guarda = ?,
                           observaciones = ?,
                           Nro_inventario = ?,
                           estado = ?
                        WHERE Producto = ? AND Nro_inventario = ?""", (detalle, area, lugar, observaciones, nro_invent, estado, producto, nro_inventariado))
        except sqlite3.IntegrityError:
            self.producto.focus_set() #Enfoca el campo de producto
            return #No avanza hasta que se ingresa un valor valido
        except sqlite3.Error as e:
            messagebox.showerror("Error.", f"Error al registrar producto: {e}")  # Manejo de otros errores
        finally:
            conn.commit()
            cursor.close()  # Cerrar el cursor después de usarlo
        
        funcion()