import tkinter as tk
import sqlite3
from pathlib import Path
from tkinter import Tk, Canvas, Button, Entry, StringVar, OptionMenu, Text, messagebox
from funciones import mostrar_tree, obtener_datos2


class ModificarDM1:
    def __init__(self, master, cambiar_a_modifDM_2, cambiar_a_menuDM, conn):
        self.master = master
        
        self.canvas = Canvas(self.master, bg = "#6B5E5E", height = 768, width = 1366, bd = 0, highlightthickness = 0, relief = "ridge")
        self.canvas.place(x=0, y=0)

        self.boton_cancelar = Button(self.master, text="Cancelar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_menuDM, relief="flat") 
        self.boton_cancelar.place(x=735.11181640625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        self.boton_seleccionar = Button(self.master, text="Seleccionar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cambiar_a_modifDM_2(cambiar_a_modifDM_2), relief="flat") 
        self.boton_seleccionar.place(x=391.47509765625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)


        self.canvas.create_rectangle(38.0, 281.0, 1328.0, 643.0, fill="#FFFFFF", outline="")

        self.nombre_del_producto = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.nombre_del_producto.place(x=720.0, y=197.0,  width=607.6497192382812, height=57.03461837768555)

        self.canvas.create_text(720.0, 149.0, anchor="nw", text="Nombre del producto", fill="#000000", font=("Inter Medium", 24 * -1))

        # Crear una variable para la opción seleccionada
        self.selected_product_type = StringVar(master)
        self.selected_product_type.set("Herramienta")
        # Crear el menú desplegable
        self.product_type_menu = OptionMenu(master, self.selected_product_type, "Herramienta", "Maquinaria", "Insumo", "Limpieza")

        self.product_type_menu.place(x=38.0, y=203.0, width=607.6497192382812, height=59.03461837768555)

        self.canvas.create_text(38.0, 155.0, anchor="nw", text="Seleccione el tipo de producto", fill="#000000", font=("Inter Medium", 24 * -1))

        self.canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        self.canvas.create_text(489.0, 47.0, anchor="nw", text="MODIFICAR PRODUCTO", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))

        self.tree = mostrar_tree(self.canvas, self.nombre_del_producto, self.selected_product_type, conn)

        self.canvas.pack()

    # Función para cambiar a la clase ModificarDM2 pasando el producto seleccionado
    def cambiar_a_modifDM_2(self, cambiar_a_modifDM_2):
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_product = self.tree.item(selected_item, "values")[1]  # Guardar el producto seleccionado
            cambiar_a_modifDM_2(self.selected_product)

class ModificarDM2:
    def __init__(self, master, cambiar_a_modifDM_3, cambiar_a_modifDM_1, producto_seleccionado, conn):
        self.master = master
        self.producto_seleccionado = producto_seleccionado
        lista = obtener_datos2(producto_seleccionado, conn)
        
        canvas = Canvas(self.master, bg="#6B5E5E", height=768, width=1366, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        boton_cancelar = Button(self.master, text="Cancelar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_modifDM_1, relief="flat") 
        boton_cancelar.place(x=735.11181640625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        boton_modificar = Button(self.master, text="Modificar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.registrar_modificacion(cambiar_a_modifDM_3, producto_seleccionado), relief="flat") 
        boton_modificar.place(x=391.47509765625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        self.observaciones = Text(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.observaciones.insert("1.0", lista[6])
        self.observaciones.place(x=708.1552734375, y=477.0, width=607.0, height=118.0)

        canvas.create_text(712.1552734375, 426.0, anchor="nw", text="Observaciones", fill="#000000", font=("Inter Medium", 24 * -1))

        # Menú desplegable para "Lugar de guarda"
        self.lugar_var = StringVar(self.master)
        self.lugar_var.set(lista[4])  # Valor por defecto
        lugar_menu = OptionMenu(self.master, self.lugar_var, "ESCUELA DE FORMACION TECNICA LABORAL", "ESCUELA AGRARIA", "OTRO")
        lugar_menu.place(x=707.0, y=339.0325927734375, width=607.6497192382812, height=59.03461837768555)

        canvas.create_text(712.1552734375, 294.0, anchor="nw", text="Lugar de guarda", fill="#000000", font=("Inter Medium", 24 * -1))

        # Menú desplegable para "Área"
        self.area_var = StringVar(self.master)
        self.area_var.set(lista[3])  # Valor por defecto
        area_menu = OptionMenu(self.master, self.area_var, "Mantenimiento - ESCUELA DE FORMACION TECNICA LABORAL", "Mantenimiento - ESCUELA AGRARIA", "Capacitacion - ESCUELA DE FORMACION TECNICA LABORAL", "Capacitacion - ESCUELA AGRARIA")
        area_menu.place(x=707.0, y=210.784912109375, width=607.6497192382812, height=59.03461837768555)

        canvas.create_text(708.1552734375, 166.0, anchor="nw", text="Área", fill="#000000", font=("Inter Medium", 24 * -1))

        self.inventariado_var = StringVar(self.master)
        self.inventariado_var.set(lista[7])
        inventariado = OptionMenu(self.master, self.inventariado_var, "SI", "NO")
        inventariado.place(x=35.0, y=501.0, width=607.0, height=57.0)

        canvas.create_text(38.0, 426.0, anchor="nw", text="Producto inventariado", fill="#000000", font=("Inter Medium", 24 * -1))

        # Menú desplegable para "Tipo"
        self.tipo_var = StringVar(self.master)
        self.tipo_var.set(lista[0])  # Valor por defecto
        tipo_menu = OptionMenu(self.master, self.tipo_var, "Herramienta", "Maquinaria", "Insumo", "Limpieza")
        tipo_menu.place(x=35.0, y=341.068115234375, width=607.6497192382812, height=59.03461837768555)

        canvas.create_text(35.0, 291.0, anchor="nw", text="Tipo", fill="#000000", font=("Inter Medium", 24 * -1))

        self.producto = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.producto.place(x=35.0, y=210.0, width=607.0, height=58.0)

        self.producto.insert(1, self.producto_seleccionado)

        canvas.create_text(38.0, 166.0, anchor="nw", text="Producto", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        canvas.create_text(462.0, 47.0, anchor="nw", text="MODIFICAR PRODUCTO", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))

        canvas.pack()

    def registrar_modificacion(self, cambiar_a_modifDM4, producto_seleccionado):
        cambios_realizados = {
            "tipo_producto": self.tipo_var.get(),
            "Producto": self.producto.get().strip(),
            "Area": self.area_var.get(),
            "Lugar_guarda": self.lugar_var.get(),
            "Observaciones": self.observaciones.get("1.0", tk.END).strip().capitalize(),
            "Inventariado": self.inventariado_var.get()
        }
        cambiar_a_modifDM4(cambios_realizados, producto_seleccionado)

class ModificarDM3:
    def __init__(self, master, cambiar_a_modifDM_4, conn):
        self.master = master     

        canvas = Canvas(self.master, bg="#6B5E5E", height=768, width=1366, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        boton_confirmar = Button(self.master, text="Confirmar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_modifDM_4(conn), relief="flat") 
        boton_confirmar.place(x=1063.0, y=681.0,  width=264.0133361816406, height=61.48335266113281)

        canvas.create_rectangle(38.0, 455.0, 1328.0, 642.0, fill="#FFFFFF", outline="")

        canvas.create_text(38.0, 411.0, anchor="nw",  text="Producto modificado", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_rectangle(37.0, 199.0, 1327.0, 386.0, fill="#FFFFFF", outline="")

        canvas.create_text(38.0, 155.0, anchor="nw", text="Producto anterior",  fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        canvas.create_text(451.0, 47.0, anchor="nw", text="MODIFICAR PRODUCTO", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))

        canvas.pack()

class ModificarDM4:
    def __init__(self, root, cambiar_a_modifDM_5, cambiar_a_modifDM_1, conn, cambios_realizados, producto_seleccionado):
        print("EN VENTANA MODIF4: ", cambios_realizados)
        
        self.popup = tk.Toplevel(root)
        self.popup.geometry("773x245")
        self.popup.config(bg="#6B5E5E")
        self.popup.grab_set()
        self.popup.resizable(False, False)  

        canvas = Canvas(self.popup, bg="#6B5E5E", height=245, width=773, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        boton_cancelar = Button(self.popup, text="Cancelar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_modifDM_1), relief="flat") 
        boton_cancelar.place(x=426.63671875, y=131.0, width=264.0133361816406, height=61.48335266113281)
       
        boton_confirmar = Button(self.popup, text="Confirmar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.actualizar_producto(conn, cambios_realizados, producto_seleccionado, cambiar_a_modifDM_5), relief="flat") 
        boton_confirmar.place(x=83.0, y=131.0, width=264.0133361816406, height=61.48335266113281)

 
        canvas.create_rectangle(0.0, 0.0, 773.0, 92.0, fill="#2B2626", outline="")

        canvas.create_text(216.0, 31.0, anchor="nw", text="¿Desea mantener la modificación?", fill="#FFFFFF", font=("Inter Medium", 24 * -1))

        canvas.pack()

    def actualizar_producto(self, conn, cambios_realizados, id_producto, funcion):
        # Construimos la parte de SET para la consulta
        columnas = ", ".join(f"{col} = ?" for col in cambios_realizados.keys())
        
        # Creamos los valores de la consulta
        valores = list(cambios_realizados.values())
        
        # Añadimos el ID al final para el WHERE
        valores.append(id_producto)
        
        # Consulta SQL
        query = f"""
            UPDATE stock
            SET {columnas}
            WHERE Producto = ?
        """
        
        try:
            # Ejecutamos la consulta
            cursor = conn.cursor()
            cursor.execute(query, valores)
            
            print("Producto actualizado correctamente.")
        except sqlite3.Error as e:
            messagebox.showerror("Error.", f"Error al registrar producto: {e}")
        finally:
            conn.commit()
            cursor.close()
            
            self.popup.destroy()  # Cierra la ventana emergente
            funcion() #Ejecuta la funcion dada
    
    def cerrar_y_ejecutar(self, funcion):
        self.popup.destroy()  # Cierra la ventana emergente
        funcion() #Ejecuta la funcion dada

class ModificarDM5:
    def __init__(self, root, cambiar_a_modifDM_1, cambiar_a_menuDM):
        self.popup = tk.Toplevel(root)
        self.popup.geometry("773x245")
        self.popup.config(bg="#6B5E5E")
        self.popup.grab_set()
        self.popup.resizable(False, False)

        canvas = Canvas(self.popup, bg = "#6B5E5E", height = 245, width = 773, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)

        boton_no = Button(self.popup, text="No", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_menuDM), relief="flat") 
        boton_no.place(x=426.63671875,y=131.0, width=264.0133361816406, height=61.48335266113281)

        boton_si = Button(self.popup, text="Sí", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_modifDM_1), relief="flat") 
        boton_si.place(x=83.0, y=131.0, width=264.0133361816406, height=61.48335266113281)
        
        canvas.create_rectangle(0.0, 0.0, 773.0, 92.0, fill="#2B2626", outline="")

        canvas.create_text(216.0, 31.0, anchor="nw", text="¿Desea modificar otro producto?", fill="#FFFFFF", font=("Inter Medium", 24 * -1))

        canvas.pack()

    def cerrar_y_ejecutar(self, funcion):
        self.popup.destroy()  # Cierra la ventana emergente
        funcion() #Ejecuta la funcion dada