from tkinter import Tk, Canvas, Entry, Button, StringVar, OptionMenu, ttk
from funciones import mostrar_tree, mostrar_treemod

class VisualizarDM:
    def __init__(self, master, cambiar_a_visualizarDM_2, cambiar_a_menuDM, conn):
        self.master = master
        
        canvas = Canvas(self.master, bg="#6B5E5E", height=768, width=1366, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        boton_cancelar = Button(self.master, text="Cancelar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_menuDM, relief="flat") 
        boton_cancelar.place(x=735.11181640625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        boton_seleccionar = Button(self.master, text="Seleccionar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.mostrar_vizualizarDMP2(cambiar_a_visualizarDM_2), relief="flat") 
        boton_seleccionar.place(x=391.47509765625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        canvas.create_rectangle(38.0, 279.0, 1328.0, 641.0, fill="#FFFFFF", outline="")

        # Variable para el menú desplegable
        selected_product_type = StringVar(master)
        selected_product_type.set("Herramienta")  # Valor inicial

        # Menú desplegable
        product_type_menu = OptionMenu(master, selected_product_type, "Herramienta", "Maquinaria", "Insumo", "Limpieza")
        product_type_menu.place(x=38.0, y=201.0, width=607.6497192382812, height=59.03461837768555)

        canvas.create_text(40.0, 150.0, anchor="nw", text="Tipo de producto", fill="#000000", font=("Inter Medium", 24 * -1))

        nombre_del_producto = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1 ))
        nombre_del_producto.place(x=720.0, y=198.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(720.0, 150.0, anchor="nw", text="Nombre del producto", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        canvas.create_text(483.0, 47.0, anchor="nw", text="VISUALIZAR PRODUCTO", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))

        self.tree = mostrar_tree(canvas, nombre_del_producto, selected_product_type, conn)

        canvas.pack()

    def mostrar_vizualizarDMP2(self, cambiar_a_visualizarDM_2):
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_product = self.tree.item(selected_item, 'values')[1]  # Suponiendo que el nombre del producto es la segunda columna
            cambiar_a_visualizarDM_2(self.selected_product)

class VisualizarDMP2:
    def __init__(self, master, cambiar_a_bajaDM_2, cambiar_a_modifDM_2, cambiar_a_visualizarDM_1, selected_product, conn):
        self.master = master
        self.producto_seleccionado = selected_product
        canvas = Canvas(self.master, bg="#6B5E5E", height=768, width=1366, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        boton_volver = Button(self.master, text="Volver", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_visualizarDM_1, relief="flat") 
        boton_volver.place(x=1064.0, y=676.0, width=264.0133361816406, height=61.48335266113281)

        boton_modificar = Button(self.master, text="Modificar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: cambiar_a_modifDM_2(selected_product), relief="flat") 
        boton_modificar.place(x=483.0, y=676.0, width=400.0, height=61.48335266113281)

        boton_eliminar = Button(self.master, text="Eliminar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: cambiar_a_bajaDM_2(selected_product), relief="flat") 
        boton_eliminar.place(x=38.0, y=676.0, width=400.0, height=61.48335266113281)
    
        canvas.create_rectangle(38.0, 197.0, 1328.0, 641.0, fill="#FFFFFF", outline="")

        canvas.create_text(38.0, 155.0, anchor="nw", text="Producto seleccionado", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        canvas.create_text(483.0, 47.0, anchor="nw", text="VISUALIZAR PRODUCTO", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))

        self.tree = ttk.Treeview(canvas, columns=("tipo_producto", "Producto", "Cantidad_existente", "Area", "Lugar_guarda", "Cantidad_migrada", "Observaciones", "Inventariado"), show='headings')
        
        # Definir las columnas
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)  # Establecer encabezados
            self.tree.column(col, anchor="center")  # Alinear columnas al centro
        
        self.scrollbar_v = ttk.Scrollbar(canvas, orient="vertical", command=self.tree.yview)
        self.scrollbar_h = ttk.Scrollbar(canvas, orient="horizontal", command=self.tree.xview)
     
        self.tree.configure(yscrollcommand=self.scrollbar_v.set, xscrollcommand=self.scrollbar_h.set)
        
        # Colocar el Treeview en el canvas
        self.tree.place(x=38.0, y=197.0, width=1290.0, height=444.0)
        self.scrollbar_v.place(x=1328.0, y=197.0, height=444.0)  # Coloca la scrollbar vertical al lado derecho
        self.scrollbar_h.place(x=38.0, y=641.0, width=1290.0)  # Coloca la scrollbar horizontal en la parte inferior
        
        # Conexión a la base de datos
        cursor = conn.cursor()

        # Consultar y mostrar detalles del producto seleccionado
        cursor.execute("SELECT * FROM stock WHERE Producto = ?", (selected_product,))
        product_details = cursor.fetchone()

        if product_details:
            self.tree.insert("", "end", values=product_details)
            
        canvas.pack()
        
class VisualizarInvent:
    def __init__(self, master, cambiar_a_visualizarDM_2, cambiar_a_menuDM, conn):
        self.master = master
        
        canvas = Canvas(self.master, bg="#6B5E5E", height=768, width=1366, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        boton_cancelar = Button(self.master, text="Cancelar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_menuDM, relief="flat") 
        boton_cancelar.place(x=735.11181640625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        boton_seleccionar = Button(self.master, text="Seleccionar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.mostrar_vizualizarDMP2(cambiar_a_visualizarDM_2), relief="flat") 
        boton_seleccionar.place(x=391.47509765625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        canvas.create_rectangle(38.0, 279.0, 1328.0, 641.0, fill="#FFFFFF", outline="")

        # Variable para el menú desplegable
        selected_product_type = StringVar(master)
        selected_product_type.set("Herramienta")  # Valor inicial

        # Menú desplegable
        product_type_menu = OptionMenu(master, selected_product_type, "Herramienta", "Maquinaria", "Insumo", "Limpieza")
        product_type_menu.place(x=38.0, y=201.0, width=607.6497192382812, height=59.03461837768555)

        canvas.create_text(40.0, 150.0, anchor="nw", text="Tipo de producto", fill="#000000", font=("Inter Medium", 24 * -1))

        nombre_del_producto = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1 ))
        nombre_del_producto.place(x=720.0, y=198.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(720.0, 150.0, anchor="nw", text="Nombre del producto", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        canvas.create_text(483.0, 47.0, anchor="nw", text="INVENTARIAR PRODUCTO", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))

        self.tree = mostrar_treemod(canvas, nombre_del_producto, selected_product_type, conn)

        canvas.pack()

    def mostrar_vizualizarDMP2(self, cambiar_a_visualizarDM_2):
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_product = self.tree.item(selected_item, 'values')[1]  # Suponiendo que el nombre del producto es la segunda columna
            cambiar_a_visualizarDM_2(self.selected_product)