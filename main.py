import tkinter as tk
from tkinter import *
import sqlite3
from funciones import *
from MenuIniciarSesion import *
from MenusAgregarStock import *
from MenusBajaDM import *
from MenusBuscarMovimientos import *
from MenusCompras import *
from MenusDisminuir import *
from MenusModificarDM import *
from MenusModificarMovimientos import *
from MenusMovimientos import *
from MenusPrincipales import *
from MenusRegistrarDM import *
from MenusVizualizar import *
from MenusInventariado import *
from MenusRegistrarDM import *
from MenuReportes import *

class App: 
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1366x768")
        self.root.title("Stock e Inventariado")
        self.root.configure(bg="#6B5E5E")
        self.root.resizable(False, False)
        self.frame_actual = None

        #Inicia la conexion con la base de datos.
        self.conn = connect_to_db()
        cursor = self.conn.cursor()
        cursor.execute("PRAGMA journal_mode = DELETE")
        
        #Protocolo cuando se cierre la ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.mostrar_iniciar_sesion()

    def on_close(self):
        if self.conn:
            self.conn.close()
        self.root.destroy()
    
    def mostrar_iniciar_sesion(self):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        IniciarSesion(self.frame_actual, self.mostrar_menu_principal, self.conn)

    def mostrar_menu_principal(self):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        MenuPrincipal(self.frame_actual, self.menu_compras, self.menu_dm, self.menu_inventario, self.menu_reportes, self.mostrar_iniciar_sesion)

    def menu_dm(self):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        MenuDM(self.frame_actual, self.registrar_dm_1, self.baja_dm_1, self.modificar_dm_1, self.visualizar_dm_1, self.mostrar_menu_principal, self.agregar_inventariado_0, self.modificar_inventariado_0)
    
    def menu_compras(self):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        MenuCompras(self.frame_actual, self.compra_cabecera, self.modificar_compra1, self.mostrar_menu_principal)

    def compra_cabecera(self):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        RegistrarCompraCabecera(self.frame_actual, self.compra_posicion, self.menu_compras, self.conn)

    def compra_posicion(self):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        RegistrarCompraPosicion(self.frame_actual, self.mostrar_menu_principal, self.registrar_otro_producto, self.conn)

    def registrar_otro_producto(self):
        RegistrarOtroProducto(self.root, self.confirmacion_compra, self.compra_posicion, self.conn)

    def confirmacion_compra(self):
        Confirmacion(self.root, self.otra_compra)

    def otra_compra(self):
        RegistrarOtraCompra(self.root, self.compra_cabecera, self.mostrar_menu_principal)
    
    def modificar_compra1(self):
        if self.frame_actual:
            self.frame_actual.destroy()
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        ModificarCompra1(self.frame_actual, self.modificar_compra2, self.menu_compras, self.conn)

    def modificar_compra2(self, selected_product):
        if self.frame_actual:
            self.frame_actual.destroy()
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        ModificarCompra2(self.frame_actual, self.confirmacion_compra, self.menu_compras, self.conn, selected_product)

    def registrar_dm_1(self):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        RegistrarDM1(self.frame_actual, self.confirmacion_registro_dm, self.menu_dm, self.conn)

    def confirmacion_registro_dm(self):
        Confirmacion(self.root, self.registrar_dm_2)

    def registrar_dm_2(self):
        RegistrarDM2(self.root, self.registrar_dm_1, self.menu_dm)

    def baja_dm_1(self):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        BajaDM1(self.frame_actual, self.menu_dm, self.baja_dm_2, self.conn)

    def baja_dm_2(self, producto_seleccionado):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        BajaDM2(self.frame_actual, self.baja_dm_3, self.visualizar_dm_1, producto_seleccionado, self.conn)

    def baja_dm_3(self, producto_seleccionado):
        BajaDM3(self.root, self.confirmacion_baja_dm, self.visualizar_dm_1, producto_seleccionado, self.conn)

    def confirmacion_baja_dm(self):
        Confirmacion(self.root, self.baja_dm_4)

    def baja_dm_4(self):
        BajaDM4(self.root, self.visualizar_dm_1, self.menu_dm)

    def visualizar_dm_1(self):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        VisualizarDM(self.frame_actual, self.visualizar_dm_2, self.menu_dm, self.conn)

    def visualizar_dm_2(self, selected_product):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        VisualizarDMP2(self.frame_actual, self.baja_dm_2, self.modificar_dm_2, self.visualizar_dm_1, selected_product, self.conn)

    def modificar_dm_1(self):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        ModificarDM1(self.frame_actual, self.modificar_dm_2, self.menu_dm, self.conn)

    def modificar_dm_2(self, producto_seleccionado):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        ModificarDM2(self.frame_actual, self.modificar_dm_4, self.visualizar_dm_1, producto_seleccionado, self.conn)

    """def modificar_dm_3(self):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        ModificarDM3(self.frame_actual, self.modificar_dm_4, self.conn)"""

    def modificar_dm_4(self, cambios_realizados, producto_seleccionado):
        ModificarDM4(self.root, self.confirmacion_modificacion_dm, self.visualizar_dm_1, self.conn, cambios_realizados, producto_seleccionado)

    def confirmacion_modificacion_dm(self):
        Confirmacion(self.root, self.modificar_dm_5)

    def modificar_dm_5(self):
        ModificarDM5(self.root, self.visualizar_dm_1, self.menu_dm)

    def menu_inventario(self):
        self.root.geometry("1366x768")
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        MenuInventario(self.frame_actual, self.menu_prestamo, self.buscar_mov_1, self.agregar_1, self.disminuir_1, self.traspaso_0, self.mostrar_menu_principal)

    def menu_prestamo(self):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.root.geometry("1366x768")
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=916, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        MenuPrestamo(self.frame_actual, self.prestamo_0, self.prestamo_inventariado_1, self.menu_inventario)

    def prestamo_0(self):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.root.geometry("1366x768")
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=916, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        RegistrarPrestamo0(self.frame_actual, self.prestamo_1, self.menu_prestamo, self.conn)

    def prestamo_1(self, selected_product):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.root.geometry("1366x916")
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=916, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        RegistrarPrestamo(self.frame_actual, self.confirmacion_prestamo, self.prestamo_0, self.conn, selected_product)

    def confirmacion_prestamo(self):
        Confirmacion(self.root, self.menu_prestamo)

    def prestamo_2(self):
        RegistrarPrestamoPT2(self.root, self.prestamo_1, self.menu_inventario)

    def prestamo_inventariado_1(self):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.root.geometry("1366x768")
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=916, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        PrestamoIventariado_1(self.frame_actual, self.prestamo_inventariado_2, self.menu_prestamo, self.conn)

    def prestamo_inventariado_2(self, producto_seleccionado, nro_invent):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.root.geometry("1366x916")
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=916, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        PrestamoInventariado2(self.frame_actual, self.confirmacion_prestamo, self.menu_prestamo, self.conn, producto_seleccionado, nro_invent)

    def modificar_mov_1(self, id_movimiento):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.root.geometry("1366x916")
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=916, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        ModificarMovimiento(self.frame_actual, self.confirmacion_modif_movimiento, self.buscar_mov_1, id_movimiento, self.conn)

    def confirmacion_modif_movimiento(self):
        Confirmacion(self.root, self.modificar_mov_4)

    def modificar_mov_4(self):
        ModificarMovimientoPT4(self.root, self.buscar_mov_1, self.menu_inventario)

    def devolucion_1(self, id_movimiento):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        RegistrarDevolucion(self.frame_actual, self.confirmacion_devolucion, self.menu_inventario, id_movimiento, self.conn)

    def confirmacion_devolucion(self):
        Confirmacion(self.root, self.devolucion_2)

    def devolucion_2(self):
        RegistrarDevolucionPT2(self.root, self.buscar_mov_1, self.menu_inventario)

    def agregar_1(self):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        AgregarStock(self.frame_actual, self.agregar_2, self.menu_inventario, self.conn)

    def agregar_2(self, pk):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        AgregarStockPT2(self.frame_actual, self.confirmacion_agregar, self.agregar_1, pk, self.conn)

    def confirmacion_agregar(self):
        Confirmacion(self.root, self.agregar_4)

    """def agregar_3(self):
        AgregarStockPT3(self.root, self.agregar_4, self.agregar_1)"""

    def agregar_4(self):
        AgregarStockPT4(self.root, self.agregar_1, self.menu_inventario)

    def disminuir_1(self):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        DisminuirPT1(self.frame_actual, self.disminuir_2, self.menu_inventario, self.conn)

    def disminuir_2(self, pk):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        DisminuirPT2(self.frame_actual, self.confirmacion_disminuir, self.disminuir_1, pk, self.conn)

    def confirmacion_disminuir(self):
        Confirmacion(self.root, self.disminuir_4)

    """def disminuir_3(self):
        DisminuirPT3(self.root, self.disminuir_4, self.disminuir_1)"""

    def disminuir_4(self):
        DisminuirPT4(self.root, self.disminuir_1, self.menu_inventario)

    def buscar_mov_1(self):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        BuscarMovimientoPT1(self.frame_actual, self.buscar_mov_2, self.menu_inventario, self.conn)

    def buscar_mov_2(self, id_movimiento):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        BuscarMovimientoPT2(self.frame_actual, self.devolucion_1, self.modificar_mov_1, self.cancelar_mov_1, self.menu_inventario, id_movimiento, self.conn)

    def traspaso_0(self):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        TraspasoDefinitivo_0(self.frame_actual, self.traspaso_1, self.menu_inventario, self.conn)

    def traspaso_1(self, primary_key, nro_ivent):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        TraspasoDefinitivo_1(self.frame_actual, self.confirmacion_traspaso, self.menu_inventario, primary_key, nro_ivent, self.conn)

    def confirmacion_traspaso(self):
        Confirmacion(self.root, self.traspaso_0)

    def traspaso_2(self):
        TraspasoDefinitivoPT2(self.root, self.traspaso_1, self.menu_inventario)

    def cancelar_mov_1(self, id_movimiento):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        CancelarMovimiento1(self.frame_actual, self.cancelar_mov_2, self.buscar_mov_1, id_movimiento, self.conn)

    def cancelar_mov_2(self, id_movimiento):
        CancelarMovimiento2(self.root, self.confirmacion_cancelar, self.menu_inventario, id_movimiento, self.conn)

    def confirmacion_cancelar(self):
        Confirmacion(self.root, self.menu_inventario)
    
    def menu_reportes(self): #PLACEHOLDER
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        MenuReportes(self.frame_actual, self.mostrar_porcentaje, self.mostrar_promedios, self.mostrar_menu_principal,self.confirmacion_reportes, self.conn) #PLACEHOLDER
    
    def mostrar_porcentaje(self):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        #Porcentaje(self.frame_actual, self.confirmacion_reportes, self.menu_reportes, self.conn)
    
    def mostrar_promedios(self):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        Promedio(self.frame_actual, self.confirmacion_reportes, self.menu_reportes, self.conn)
        
    def confirmacion_reportes(self):
        Confirmacion(self.root, self.menu_reportes)

    def agregar_inventariado_0(self):
        if self.frame_actual:
            self.frame_actual.destroy()
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        VisualizarInvent(self.frame_actual, self.agregar_inventariado, self.menu_dm, self.conn)        

    def agregar_inventariado(self, producto_seleccionado):
        if self.frame_actual:
            self.frame_actual.destroy()
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        RegistrarInventariado(self.frame_actual, self.menu_dm, self.confirmacion_inventariado, producto_seleccionado, self.conn)

    def confirmacion_inventariado(self):
        Confirmacion(self.root, self.agregar_inventariado_2)

    def agregar_inventariado_2(self):
        RegistrarInventariadoPT2(self.root, self.agregar_inventariado_0, self.menu_dm)

    def modificar_inventariado_0(self):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        ModificarInventariadoPT0(self.frame_actual, self.modificar_inventariado, self.menu_dm, self.conn)

    def modificar_inventariado(self, producto_seleccionado):
        if self.frame_actual:
            self.frame_actual.destroy() # Destruye la ventana de MenuDM si está abierta
        self.frame_actual = tk.Canvas(self.root, bg="#6B5E5E", height=768, width=1366)
        self.frame_actual.pack(fill="both", expand=True)
        ModificarInventariadoPT1(self.frame_actual, self.modificar_inventariado_0, self.confirmacion_modif_inventariado, producto_seleccionado, self.conn)
    
    def confirmacion_modif_inventariado(self):
        Confirmacion(self.root, self.modificar_inventariado_0)


if __name__ == "__main__":
    app = App()
    app.root.mainloop()


