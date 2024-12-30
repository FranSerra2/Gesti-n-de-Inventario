#Menus Buscar Movimientos
from tkinter import Tk, Canvas, Entry, Button, ttk
from tkcalendar import DateEntry
from funciones import mostrar_tree_movimientos

class BuscarMovimientoPT1:
    def __init__(self, master, cambiar_a_buscarMov_2, cambiar_a_menuInv, conn):
        self.master = master
        self.conn = conn

        self.canvas = Canvas(self.master, bg = "#6B5E5E", height = 768, width = 1366, bd = 0, highlightthickness = 0, relief = "ridge")
        self.canvas.place(x = 0, y = 0)


        boton_cancelar = Button(self.master, text="Cancelar",  bg="#FFA500",  fg="black",  bd=2,  font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_menuInv, relief="flat")
        boton_cancelar.place(x=735.11181640625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        boton_seleccionar = Button(self.master, text="Seleccionar",  bg="#FFA500",  fg="black",  bd=2,  font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.mostrar_buscar_2(cambiar_a_buscarMov_2), relief="flat")
        boton_seleccionar.place(x=391.47509765625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        self.canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        self.canvas.create_rectangle(37.0, 276.0, 1327.0, 638.0, fill="#FFFFFF", outline="")

        self.entry_fecha_desde = DateEntry(self.master, date_pattern='yyyy-MM-dd', width=12, background="#2B2626", foreground="white", borderwidth=2)
        self.entry_fecha_desde.pack(padx=40, pady=40)
        self.entry_fecha_desde.place(x=866.0, y=198.0, width=225.0, height=57.0)

        self.entry_fecha_hasta = DateEntry(self.master, date_pattern='yyyy-MM-dd', width=12, background="#2B2626", foreground="white", borderwidth=2)
        self.entry_fecha_hasta.pack(padx=40, pady=40)
        self.entry_fecha_hasta.place(x=1107.0, y=198.0, width=220.0, height=57.0)

        self.canvas.create_text(866.0, 150.0, anchor="nw", text="Fecha Desde", fill="#000000", font=("Inter Medium", 24 * -1))

        self.canvas.create_text(1107.0, 150.0, anchor="nw", text="Fecha Hasta", fill="#000000", font=("Inter Medium", 24 * -1))

        self.entry_inventariado = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.entry_inventariado.place(x=472.0, y=198.0, width=376.0, height=57.0)

        self.canvas.create_text(472.0, 150.0, anchor="nw", text="Número de inventariado", fill="#000000", font=("Inter Medium", 24 * -1))

        self.canvas.create_text(37.0, 150.0, anchor="nw", text="Nombre del producto", fill="#000000", font=("Inter Medium", 24 * -1))

        self.entry_nombre = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.entry_nombre.place(x=37.0, y=198.0, width=421.0, height=57.03461837768555)

        self.canvas.create_text(500.0, 47.0, anchor="nw", text="BUSCAR MOVIMIENTO", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))

        self.tree = mostrar_tree_movimientos(self.canvas, self.entry_nombre, self.entry_inventariado, self.entry_fecha_desde, self.entry_fecha_hasta, self.conn)

        self.canvas.pack()

    def mostrar_buscar_2(self, cambiar_a_buscarMov_2):
        selected_item = self.tree.selection()
        if selected_item:
            self.id_movimiento = self.tree.item(selected_item, 'values')[0]  # Suponiendo que el nombre del producto es la segunda columna
            cambiar_a_buscarMov_2(self.id_movimiento)

class BuscarMovimientoPT2:
    def __init__(self, master, cambiar_a_devolucion, cambiar_a_modificarMov, cambiar_a_cancelarMov, cambiar_a_menuInv, id_movimiento, conn):
        self.master = master

        canvas = Canvas(self.master, bg = "#6B5E5E", height = 768, width = 1366, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)

        boton_salir = Button(self.master, text="Salir", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_menuInv, relief="flat")
        boton_salir.place(x=742.0, y=626.0, width=585.3491821289062, height=79.96798706054688
        )

        boton_cancelar_mov = Button(self.master, text="Cancelar movimiento", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda:cambiar_a_cancelarMov(id_movimiento), relief="flat")
        boton_cancelar_mov.place(x=38.0, y=626.0, width=585.3491821289062, height=79.96798706054688)

        boton_modificar_mov = Button(self.master, text="Modificar movimiento", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda:cambiar_a_modificarMov(id_movimiento),relief="flat")
        boton_modificar_mov.place(x=743.0, y=485.0, width=585.3491821289062, height=79.96798706054688)

        boton_registrar_devolucion = Button(self.master, text="Registrar devolución", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda:cambiar_a_devolucion(id_movimiento), relief="flat")
        boton_registrar_devolucion.place(x=38.0, y=484.0, width=585.3491821289062, height=80.80975341796875)

        canvas.create_rectangle(38.0, 190.0, 1328.0, 424.0, fill="#FFFFFF", outline="")

        canvas.create_text(38.0, 148.0, anchor="nw", text="Movimiento", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        canvas.create_text(500.0, 47.0, anchor="nw", text="BUSCAR MOVIMIENTO", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))

        self.tree = ttk.Treeview(canvas, columns=("id_movimiento", "fecha_egreso", "tipo_egreso", "Lugar_origen", 
                                                "Lugar_destino", "Responsable_retiro", "cantidad_egresada", 
                                                "fecha_devolucion", "cantidad_devuelta", "Responsable_devolucion", 
                                                "Responsable_recepcion", "Motivo", "Comentario", 
                                                "Inventariado", "Producto", "Nro_inventariado", "definitivo"), 
                                show='headings')
        
        # Definir las columnas
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)  # Establecer encabezados
            self.tree.column(col, anchor="center")  # Alinear columnas al centro
        
        self.scrollbar_v = ttk.Scrollbar(canvas, orient="vertical", command=self.tree.yview)
        self.scrollbar_h = ttk.Scrollbar(canvas, orient="horizontal", command=self.tree.xview)
     
        self.tree.configure(yscrollcommand=self.scrollbar_v.set, xscrollcommand=self.scrollbar_h.set)
        
        # Colocar el Treeview en el canvas
        self.tree.place(x=50.0, y=210.0, width=1250.0, height=200.0)
        self.scrollbar_v.place(x=1310.0, y=210, height=200.0)  # Coloca la scrollbar vertical al lado derecho
        self.scrollbar_h.place(x=38.0, y=410, width=1290.0)  # Coloca la scrollbar horizontal en la parte inferior
        
        # Conexión a la base de datos
        cursor = conn.cursor()

        # Consultar y mostrar detalles del producto seleccionado
        cursor.execute("SELECT * FROM Movimientos WHERE id_movimiento = ?", (id_movimiento,))
        product_details = cursor.fetchone()

        if product_details:
            self.tree.insert("", "end", values=product_details)

        canvas.pack()