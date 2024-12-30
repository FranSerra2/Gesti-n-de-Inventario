#Menus Baja DM
import tkinter as tk
from tkinter import Tk, Canvas, StringVar, OptionMenu, Entry, Button, ttk, messagebox
import sqlite3
from funciones import mostrar_tree

class BajaDM1:
    def __init__(self, master, cambiar_a_menuDM, cambiar_a_bajaDM_2, conn):
        self.master = master
        self.selected_product_type = None

        self.canvas = Canvas(self.master, bg = "#6B5E5E", height = 768, width = 1366, bd = 0, highlightthickness = 0, relief = "ridge")
        self.canvas.place(x=0, y=0)

        boton_cancelar = Button(self.master, text="Cancelar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_menuDM, relief="flat") 
        boton_cancelar.place(x=735.11181640625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        boton_seleccionar = Button(self.master, text="Seleccionar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.mostrar_bajaDM2(cambiar_a_bajaDM_2), relief="flat") 
        boton_seleccionar.place(x=391.47509765625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        self.canvas.create_rectangle(38.0, 283.0, 1328.0, 645.0, fill="#FFFFFF", outline="")

        self.nombre_producto = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.nombre_producto.place(x=720.0, y=203.0, width=607.6497192382812, height=57.03461837768555)

        self.canvas.create_text(720.0, 155.0, anchor="nw", text="Nombre del producto", fill="#000000", font=("Inter Medium", 24 * -1))
               
        # Variable para el menú desplegable
        self.selected_product_type = StringVar(master)
        self.selected_product_type.set("Herramienta")  # Valor por defecto

        # Crear el menú desplegable
        self.product_type_menu = OptionMenu(master, self.selected_product_type, "Herramienta", "Maquinaria", "Insumo", "Limpieza")
        self.product_type_menu.place(x=38.0, y=205.0, width=607.6497192382812, height=59.03461837768555)
        
        self.canvas.create_text(38.0, 155.0, anchor="nw", text="Tipo de producto", fill="#000000", font=("Inter Medium", 24 * -1))

        self.canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        self.canvas.create_text(541.0, 47.0, anchor="nw", text="BAJA PRODUCTO", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))

        self.tree = mostrar_tree(self.canvas, self.nombre_producto, self.selected_product_type, conn)

        self.canvas.pack()

    def mostrar_bajaDM2(self, cambiar_a_bajaDM_2):
        # Llamar a la clase BajaDM2 y pasarle el producto seleccionado
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_product = self.tree.item(selected_item, "values")[1]  # Guardar el producto seleccionado
            cambiar_a_bajaDM_2(self.selected_product)  # Pasar el producto a BajaDM2

class BajaDM2:
    def __init__(self, master, cambiar_a_bajaDM_3, cambiar_a_bajaDM_1, selected_product, conn):
        self.master = master
        
        self.canvas = Canvas(self.master, bg = "#6B5E5E", height = 768, width = 1366, bd = 0, highlightthickness = 0, relief = "ridge")
        self.canvas.place(x = 0, y = 0)

        boton_cancelar = Button(self.master, text="Cancelar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_bajaDM_1, relief="flat") 
        boton_cancelar.place(x=735.11181640625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        boton_eliminar = Button(self.master, text="Eliminar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.mostrar_bajaDM3(cambiar_a_bajaDM_3, cambiar_a_bajaDM_1, selected_product), relief="flat") 
        boton_eliminar.place(x=391.47509765625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        self.canvas.create_rectangle(38.0, 197.0, 1328.0, 641.0, fill="#FFFFFF", outline="")

        self.canvas.create_text(38.0, 155.0, anchor="nw", text="Producto seleccionado", fill="#000000", font=("Inter Medium", 24 * -1))

        self.canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        self.canvas.create_text(541.0, 47.0, anchor="nw", text="BAJA PRODUCTO", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))

        self.tree = ttk.Treeview(self.canvas, columns=("tipo_producto", "Producto", "Cantidad_existente", "Area", "Lugar_guarda", "Cantidad_migrada", "Observaciones", "Inventariado"), show='headings')
        
        # Definir las columnas
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)  # Establecer encabezados
            self.tree.column(col, anchor="center")  # Alinear columnas al centro
        
        self.scrollbar_v = ttk.Scrollbar(self.canvas, orient="vertical", command=self.tree.yview)
        self.scrollbar_h = ttk.Scrollbar(self.canvas, orient="horizontal", command=self.tree.xview)
     
        self.tree.configure(yscrollcommand=self.scrollbar_v.set, xscrollcommand=self.scrollbar_h.set)
        
        # Colocar el Treeview en el canvas
        self.tree.place(x=38.0, y=197.0, width=1290.0, height=444.0)
        self.scrollbar_v.place(x=1310.0, y=283.0, height=344.0)  # Coloca la scrollbar vertical al lado derecho
        self.scrollbar_h.place(x=39.0, y=628.0, width=1289.0)
        
        cursor = conn.cursor()

        # Consultar y mostrar detalles del producto seleccionado
        cursor.execute("SELECT * FROM stock WHERE Producto = ?", (selected_product,))
        product_details = cursor.fetchone()

        if product_details:
            self.tree.insert("", "end", values=product_details)
        
        self.canvas.pack()

    def mostrar_bajaDM3(self, cambiar_a_bajaDM_3, cambiar_a_bajaDM_1, selected_product):
        cambiar_a_bajaDM_3(selected_product)

class BajaDM3:
    def __init__(self, root, cambiar_a_bajaDM_4, cambiar_a_bajaDM_1, producto_seleccionado, conn):
        self.popup = tk.Toplevel(root)
        self.popup.geometry("773x245")
        self.popup.config(bg="#6B5E5E")
        self.popup.grab_set()
        self.popup.resizable(False, False)
        
        self.producto_seleccionado = producto_seleccionado
        self.conn = conn
        self.cambiar_a_bajaDM_4 = cambiar_a_bajaDM_4

        canvas = Canvas(self.popup, bg = "#6B5E5E", height = 768, width = 1366, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)

        boton_cancelar = Button(self.popup, text="Cancelar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_bajaDM_1), relief="flat") 
        boton_cancelar.place(x=426.63671875,y=131.0, width=264.0133361816406, height=61.48335266113281)

        boton_confirmar = Button(self.popup, text="Confirmar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.dar_de_baja(conn), relief="flat") 
        boton_confirmar.place(x=83.0, y=131.0, width=264.0133361816406, height=61.48335266113281)

        canvas.create_rectangle(0.0, 0.0, 773.0, 92.0, fill="#2B2626", outline="")

        canvas.create_text(94.0, 31.0, anchor="nw", text="¿Está seguro de que desea eliminar este producto?", fill="#FFFFFF", font=("Inter Medium", 24 * -1))
        
        canvas.pack()

    def dar_de_baja(self, conn):
        # Conexión a la base de datos
        cursor = conn.cursor()

        # Eliminar el producto de la base de datos
        query = "DELETE FROM stock WHERE Producto = ?"
        cursor.execute(query, (self.producto_seleccionado,))

        conn.commit()  # Guardar cambios

        self.cerrar_y_ejecutar(self.cambiar_a_bajaDM_4)  # Volver a la pantalla de confirmación

    def cerrar_y_ejecutar(self, funcion):
        self.popup.destroy()  # Cierra la ventana emergente
        funcion()  # Ejecuta la función dada

class BajaDM4:
    def __init__(self, root, cambiar_a_bajaFM_1, cambiar_a_menuDM):
        self.popup = tk.Toplevel(root)
        self.popup.geometry("773x245")
        self.popup.config(bg="#6B5E5E")
        self.popup.grab_set()
        self.popup.resizable(False, False)

        canvas = Canvas(self.popup, bg = "#6B5E5E", height = 768, width = 1366, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)

        boton_no = Button(self.popup, text="No", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_menuDM), relief="flat") 
        boton_no.place(x=426.63671875,y=131.0, width=264.0133361816406, height=61.48335266113281)

        boton_si = Button(self.popup, text="Sí", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_bajaFM_1), relief="flat") 
        boton_si.place(x=83.0, y=131.0, width=264.0133361816406, height=61.48335266113281)


        canvas.create_rectangle(0.0, 0.0, 773.0, 92.0, fill="#2B2626", outline="")

        canvas.create_text(216.0, 31.0, anchor="nw", text="¿Desea eliminar otro producto?", fill="#FFFFFF", font=("Inter Medium", 24 * -1))
        
        canvas.pack()

    def cerrar_y_ejecutar(self, funcion):
        self.popup.destroy()  # Cierra la ventana emergente
        funcion() #Ejecuta la funcion dada