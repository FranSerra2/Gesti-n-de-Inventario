#Menu Iniciar Sesion

from tkinter import Tk, Canvas, Button

class MenuDM:
    def __init__(self, master, cambiar_a_registrarDM, cambiar_a_bajaDM, cambiar_a_modificarDM, cambiar_a_visualizarDM, cambiar_a_mainMenu, cambiar_a_agregar_invent, cambiar_a_modif_invent):
        self.master = master
        
        canvas = Canvas(self.master, bg = "#6B5E5E", height = 768, width = 1366, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)

        boton_volver = Button(self.master, text="Volver", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_mainMenu, relief="flat")
        boton_volver.place(x=272, y=650, width=821, height=66)

        boton_visualizar = Button(self.master, text="Visualizar/Modificar Producto", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_visualizarDM, relief="flat")
        boton_visualizar.place(x=272, y=350, width=821, height=66)

        boton_agregar_inventariado = Button(self.master, text="Inventariar Producto", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_agregar_invent, relief="flat")
        boton_agregar_inventariado.place(x=272, y=450, width=821, height=66)

        boton_modificar_inventariado = Button(self.master, text="Visualizar/Modificar Inventariado", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_modif_invent, relief="flat")
        boton_modificar_inventariado.place(x=272.0, y=550, width=821, height=72)

        boton_nuevo_prod = Button(self.master, text="Registrar Producto", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_registrarDM, relief="flat")
        boton_nuevo_prod.place(x=272.0, y=255, width=821, height=66)

        canvas.create_rectangle(0.0, 3.0, 1366.0, 213.0, fill="#2B2626", outline="")

        canvas.create_text(507.0, 70.0, anchor="nw", text="PRODUCTOS", fill="#FFFFFF", font=("PalanquinDark Regular", 60 * -1))

        canvas.pack()

class MenuInventario:
    def __init__(self, master, cambiar_a_prestamo, cambiar_a_buscar_movi, cambiar_a_agregar, cambiar_a_disminuir, cambiar_a_traspaso, cambiar_a_mainMenu):
        self.master = master

        canvas = Canvas(self.master, bg = "#6B5E5E", height = 768, width = 1366, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x=0, y=0)

        boton_volver = Button(self.master, text="Volver", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_mainMenu, relief="flat") 
        boton_volver.place(x=272.0, y=650.0, width=821.0536499023438, height=65)

        boton_Traspaso_definitivo = Button(self.master, text="Traspaso Definitivo", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_traspaso, relief="flat")
        boton_Traspaso_definitivo.place(x=272.0, y=570.0, width=821.0, height=65)

        boton_Disminuir_invrntario = Button(self.master, text="Disminuir Stock", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_disminuir, relief="flat")
        boton_Disminuir_invrntario.place(x=272.0, y=490.0, width=821.0, height=65)

        boton_Agregar_stock = Button(self.master, text="Agregar Stock", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_agregar, relief="flat")
        boton_Agregar_stock.place(x=272.0, y=410.0, width=821.0, height=65)

        """boton_cancelar_movimiento = Button(self.master, text="Cancelar Movimiento", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_buscar_movi, relief="flat")
        boton_cancelar_movimiento.place(x=745.74365234375, y=177.0, width=460.74365234375, height=63.60746765136719)"""

        boton_buscar_movimiento = Button(self.master, text="Buscar Movimiento", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_buscar_movi, relief="flat")
        boton_buscar_movimiento.place(x=272.0, y=330.0, width=821.0, height=65)

        """boton_modificar_movimiento = Button(self.master, text="Modificar Movimiento", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_buscar_movi, relief="flat")
        boton_modificar_movimiento.place(x=160.0, y=411.0, width=460.74365234375, height=63.60746765136719)

        boton_registrar_devolucion = Button(self.master, text="Registrar Devolución", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_buscar_movi, relief="flat")
        boton_registrar_devolucion.place(x=160.0, y=294.0, width=460.74365234375, height=63.60746765136719)"""

        boton_registrar_prestamo = Button(self.master, text="Registrar Prestamo", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_prestamo, relief="flat")
        boton_registrar_prestamo.place(x=272.0, y=250.0, width=821.0, height=65)

        canvas.create_rectangle(0.0, 3.0, 1366.0, 210.0, fill="#2B2626", outline="")

        canvas.create_text(506.0, 70.0, anchor="nw", text="MOVIMIENTOS", fill="#FFFFFF", font=("PalanquinDark Regular", 60 * -1))


        canvas.pack()

class MenuPrincipal:
    def __init__(self, master, cambiar_a_compra_cabecera, cambiar_a_menuDM, cambiar_a_menuInventario, cambiar_a_reportes, cambiar_a_incioSesion):
        
        self.master = master

        canvas = Canvas(self.master, bg = "#6B5E5E", height = 768, width = 1366, bd = 0, highlightthickness = 0, relief = "ridge")   
        canvas.place(x=0, y=0)

        boton_volver = Button(self.master, text="Volver", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_incioSesion, relief="flat")
        boton_volver.place(x=272.0, y=650.0, width=821.0536499023438, height=66.169677734375)

        boton_reportes = Button(self.master, text="Reportes", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_reportes, relief="flat")
        boton_reportes.place(x=272.0, y=550.0, width=821.0, height=72.1036376953125)

        boton_inventario = Button(self.master, text="Movimientos", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_menuInventario, relief="flat")
        boton_inventario.place(x=272.0, y=450.0, width=821.0, height=72.1036376953125)
        
        boton_productos = Button(self.master, text="ABM productos", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_menuDM, relief="flat")
        boton_productos.place(x=272.0, y=350.0, width=821.0, height=72.1)

        boton_compra = Button(self.master, text="Compras", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_compra_cabecera, relief="flat")
        boton_compra.place(x=272.0, y=255.0, width=821.0536499023438, height=66.169677734375)

        canvas.create_rectangle(0.0, 0.0, 1366.0, 210.0, fill="#2B2626", outline="")

        canvas.create_text(440.0, 70.0, anchor="nw", text="MENÚ PRINCIPAL", fill="#FFFFFF", font=("PalanquinDark Regular", 60 * -1))

        canvas.pack()

class MenuCompras:
    def __init__(self, master, cambiar_a_registrar, cambiar_a_modificar, cambiar_a_menuDM):
        self.master = master

        canvas = Canvas(self.master, bg="#6B5E5E", height=768, width=1366, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        boton_volver = Button(self.master, text="Volver", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1),
                              borderwidth=0, highlightthickness=0, command=cambiar_a_menuDM, relief="flat")
        boton_volver.place(x=272.0, y=550.0, width=821.0, height=72.1)

        boton_registrar_compra = Button(self.master, text="Modificar Compra", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1),
                                borderwidth=0, highlightthickness=0, command=cambiar_a_modificar, relief="flat")
        boton_registrar_compra.place(x=272.0, y=400.0, width=821.0, height=72.1)

        boton_modificar_compra = Button(self.master, text="Registrar Compra", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1),
                                  borderwidth=0, highlightthickness=0, command=cambiar_a_registrar, relief="flat")
        boton_modificar_compra.place(x=272.0, y=300.0, width=821.0, height=72.1)

        canvas.create_rectangle(0.0, 0.0, 1366.0, 210.0, fill="#2B2626", outline="")
        canvas.create_text(530.0, 70.0, anchor="nw", text="COMPRAS", fill="#FFFFFF", font=("PalanquinDark Regular", 60 * -1))

        canvas.pack()

class MenuPrestamo:
    def __init__(self, master, cambiar_a_prestamo, cambiar_a_inventariado, cambiar_a_menuInv):
        self.master = master

        canvas = Canvas(self.master, bg="#6B5E5E", height=768, width=1366, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        boton_volver = Button(self.master, text="Volver", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1),
                              borderwidth=0, highlightthickness=0, command=cambiar_a_menuInv, relief="flat")
        boton_volver.place(x=272.0, y=550.0, width=821.0, height=72.1)

        boton_prestamo = Button(self.master, text="Producto no inventariado", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1),
                                borderwidth=0, highlightthickness=0, command=cambiar_a_prestamo, relief="flat")
        boton_prestamo.place(x=272.0, y=400.0, width=821.0, height=72.1)

        boton_inventariado = Button(self.master, text="Producto Inventariado", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1),
                                  borderwidth=0, highlightthickness=0, command=cambiar_a_inventariado, relief="flat")
        boton_inventariado.place(x=272.0, y=300.0, width=821.0, height=72.1)

        canvas.create_rectangle(0.0, 0.0, 1366.0, 210.0, fill="#2B2626", outline="")
        canvas.create_text(530.0, 70.0, anchor="nw", text="PRESTAMOS", fill="#FFFFFF", font=("PalanquinDark Regular", 60 * -1))

        canvas.pack()