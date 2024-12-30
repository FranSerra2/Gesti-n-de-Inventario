import tkinter as tk
import sqlite3
from tkinter import Tk, Canvas, Button, Entry, StringVar, OptionMenu, ttk, Text
from tkcalendar import DateEntry
from datetime import datetime
import os
import configparser
from tkinter import *
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo

#FUNCIONES DATABASE PATH
def get_db_path():
    config = configparser.ConfigParser()
    config_file = "config.ini"
    if os.path.exists(config_file):
        config.read(config_file)
        db_path = config["DEFAULT"].get("db_path")
        if db_path and os.path.exists(db_path):
            return db_path
        else:
            print("La ruta especificada no es valida")

    db_path = askstring("Ruta DB", "Ingrese la ruta completa de la base de datos: ")
    config["DEFAULT"] = {"db_path": db_path}
    with open(config_file, "w") as configfile:
        config.write(configfile)
    return db_path

def connect_to_db():
    db_path = get_db_path()
    try:
        conn = sqlite3.connect(db_path)
        print("Conexion exitosa con la base de datos.")
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

def obtener_datos(id, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Inventariados WHERE Nro_inventario = ?", (id,))
    resultado = cursor.fetchone()  
    cursor.close()
    return resultado

def obtener_datos2(id, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stock WHERE Producto = ?", (id,))
    resultado = cursor.fetchone()  
    cursor.close()
    return resultado

def obtener_datos3(id, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Movimientos WHERE id_movimiento = ?", (id,))
    resultado = cursor.fetchone()  
    cursor.close()
    return resultado

def obtener_datos4(id, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Compra_cabecera WHERE id_cabecera = ?", (id,))
    resultado = cursor.fetchone()  
    cursor.close()
    return resultado
    
#OBTENER FECHA
def get_date():
    return datetime.today().strftime('%Y-%m-%d')

#FUNCIONES TREES
def mostrar_tree_porcentaje(canvas, entry_fecha_desde, entry_fecha_hasta, conn):
    # Crear el Treeview
    tree = ttk.Treeview(canvas, columns=("Id cabecera", "Nro OC", "Fecha OC", "Monto Total", "Origen Fondo", "Recepcionado", "Lugar Recepcion", "Fecha Ingreso", "Objetivo compra", "Nro factura", "Fecha factura", "Proveedor"), show='headings')

    # Definir las columnas
    for col in tree["columns"]:
        tree.heading(col, text=col)  # Establecer encabezados
        tree.column(col, anchor="e")  # Alinear columnas a la derecha

    # Crear Scrollbars
    scrollbar_v = ttk.Scrollbar(canvas, orient="vertical", command=tree.yview)
    scrollbar_h = ttk.Scrollbar(canvas, orient="horizontal", command=tree.xview)

    # Configurar el Treeview para usar los Scrollbars
    tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

    # Colocar el Treeview en el canvas
    tree.place(x=38, y=283, width=1270, height=362)
    scrollbar_v.place(x=1310, y=283, height=344)  # Coloca la barra vertical al lado derecho del Treeview
    scrollbar_h.place(x=39, y=628, width=1289)

    # Conexión a la base de datos
    cursor = conn.cursor()

    def update_tree():
        # Limpiar el Treeview antes de volver a llenarlo
        for row in tree.get_children():
            tree.delete(row)

        # Obtener los filtros
        fecha_desde = entry_fecha_desde.get_date()
        fecha_hasta = entry_fecha_hasta.get_date()

        # Consulta para obtener los datos filtrados
        query = "SELECT * FROM Compra_cabecera WHERE 1=1"  # Siempre verdadero para facilitar la concatenación
        params = []

        if fecha_desde:
            query += " AND Fecha_OC >= ?"
            params.append(fecha_desde)

        if fecha_hasta:
            query += " AND Fecha_OC <= ?"
            params.append(fecha_hasta)

        cursor.execute(query, params)

        # Insertar los datos en el Treeview
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    # Inicializar el Treeview
    update_tree()

    entry_fecha_desde.bind("<<DateEntrySelected>>", lambda event: update_tree())  # Filtro por fecha desde
    entry_fecha_hasta.bind("<<DateEntrySelected>>", lambda event: update_tree())  # Filtro por fecha hasta

    return tree  # Devolver el Treeview

def mostrar_tree_inventario_modificacion(canvas, entry_nro_inventariado, entry_producto, selected_product_type, conn):
    # Crear el Treeview
    tree = ttk.Treeview(canvas, columns=("Tipo producto", "Producto", "Detalle", "Área", "Lugar de guarda", "Observaciones", "Nro.inventariado", "Estado"), show='headings')

    # Definir las columnas
    for col in tree["columns"]:
        tree.heading(col, text=col)  # Establecer encabezados
        tree.column(col, anchor="e")  # Alinear columnas a la derecha

    # Crear Scrollbars
    scrollbar_v = ttk.Scrollbar(canvas, orient="vertical", command=tree.yview)
    scrollbar_h = ttk.Scrollbar(canvas, orient="horizontal", command=tree.xview)

    # Configurar el Treeview para usar los Scrollbars
    tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

    # Colocar el Treeview en el canvas
    tree.place(x=38, y=283, width=1270, height=362)
    scrollbar_v.place(x=1310, y=283, height=344)  # Coloca la barra vertical al lado derecho del Treeview
    scrollbar_h.place(x=39, y=628, width=1289)    # Coloca la barra horizontal en la parte inferior del Treeview
    
    # Conexión a la base de datos
    cursor = conn.cursor()

    def update_tree():
        # Limpiar el Treeview antes de volver a llenarlo
        for row in tree.get_children():
            tree.delete(row)

        # Obtener los filtros de los Entry y del OptionMenu
        nro_inventariado_filter = entry_nro_inventariado.get().lower()
        producto_filter = entry_producto.get().lower()
        product_type = selected_product_type.get()

        # Consulta para obtener los datos filtrados
        query = "SELECT * FROM Inventariados WHERE 1=1"  # Siempre verdadero para facilitar la concatenación
        params = []

        if nro_inventariado_filter:
            query += " AND Nro_inventario LIKE ?"
            params.append(f'%{nro_inventariado_filter}%')  # Filtrar por número de inventariado

        if producto_filter:
            query += " AND Producto LIKE ?"
            params.append(f'%{producto_filter}%')  # Filtrar por nombre de producto

        if product_type != "Tipo de producto":
            query += " AND tipo_producto = ?"
            params.append(product_type)

        cursor.execute(query, params)

        # Insertar los datos en el Treeview
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    # Inicializar el Treeview
    update_tree()

    # Evento de selección en el Treeview
    def on_select(event):
        selected_item = tree.selection()
        if selected_item:
            nro_inventariado = tree.item(selected_item, "values")[6]  # Columna "Nro.inventariado"
            entry_nro_inventariado.delete(0, tk.END)  # Limpiar el Entry
            entry_nro_inventariado.insert(0, nro_inventariado)  # Mostrar el número de inventariado seleccionado en el Entry

    tree.bind("<<TreeviewSelect>>", on_select)  # Vínculo del evento

    # Vínculo de eventos para actualizar el Treeview
    entry_nro_inventariado.bind("<KeyRelease>", lambda event: update_tree())  # Filtro por Entry Nro inventariado
    entry_producto.bind("<KeyRelease>", lambda event: update_tree())  # Filtro por Entry Producto
    selected_product_type.trace("w", lambda *args: update_tree())  # Filtro por menú desplegable

    return tree  # Devolver el Treeview

def mostrar_tree_modificado(canvas, entry_nombre_producto, selected_product_type, inventariado,conn):
    # Crear el Treeview
    tree = ttk.Treeview(canvas, columns=("Tipo producto", "Producto", "Cantidad existente", "Área", "Lugar de guarda", "Cantidad migrada", "Observaciones", "Inventariado"), show='headings')

    # Definir las columnas
    for col in tree["columns"]:
        tree.heading(col, text=col)  # Establecer encabezados
        tree.column(col, anchor="e")  # Alinear columnas a la derecha

    # Crear Scrollbars
    scrollbar_v = ttk.Scrollbar(canvas, orient="vertical", command=tree.yview)
    scrollbar_h = ttk.Scrollbar(canvas, orient="horizontal", command=tree.xview)

    # Configurar el Treeview para usar los Scrollbars
    tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

    # Colocar el Treeview en el canvas
    tree.place(x=38, y=283, width=1270, height=362)
    scrollbar_v.place(x=1310, y=283, height=344)  # Coloca la barra vertical al lado derecho del Treeview
    scrollbar_h.place(x=39, y=628, width=1289)    # Coloca la barra horizontal en la parte inferior del Treeview
    
    # Conexión a la base de datos
    cursor = conn.cursor()

    def update_tree():
        # Limpiar el Treeview antes de volver a llenarlo
        for row in tree.get_children():
            tree.delete(row)

        # Obtener el filtro del Entry
        filter_text = entry_nombre_producto.get().lower()
        product_type = selected_product_type.get()
        invent = inventariado

        # Consulta para obtener los datos filtrados
        query = "SELECT * FROM stock WHERE 1=1 "  # Siempre verdadero para facilitar la concatenación
        params = []

        if filter_text:
            query += " AND Producto LIKE ?"
            params.append(f'%{filter_text}%')  # Filtrar por nombre de producto

        if product_type != "Tipo de producto":
            query += " AND tipo_producto = ?"
            params.append(product_type)
        
        if inventariado:
            query += " AND Inventariado LIKE ?"
            params.append(f'%{invent}%')

        cursor.execute(query, params)

        # Insertar los datos en el Treeview
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    # Inicializar el Treeview
    update_tree()

    # Evento de selección en el Treeview
    def on_select(event):
        selected_item = tree.selection()
        if selected_item:
            product = tree.item(selected_item, "values")[1]  # Columna "Producto"
            entry_nombre_producto.delete(0, tk.END)  # Limpiar el Entry
            entry_nombre_producto.insert(0, product)  # Mostrar el producto seleccionado en el Entry

    tree.bind("<<TreeviewSelect>>", on_select)  # Vínculo del evento

    # Vínculo de eventos para actualizar el Treeview
    entry_nombre_producto.bind("<KeyRelease>", lambda event: update_tree())  # Filtro por Entry
    selected_product_type.trace("w", lambda *args: update_tree())  # Filtro por menú desplegable

    return tree  # Devolver el Treeview

def mostrar_tree(canvas, entry_nombre_producto, selected_product_type, conn):
    # Crear el Treeview
    tree = ttk.Treeview(canvas, columns=("Tipo producto", "Producto", "Cantidad existente", "Área", "Lugar de guarda", "Cantidad migrada", "Observaciones", "Inventariado"), show='headings')

    # Definir las columnas
    for col in tree["columns"]:
        tree.heading(col, text=col)  # Establecer encabezados
        tree.column(col, anchor="e")  # Alinear columnas a la derecha

    # Crear Scrollbars
    scrollbar_v = ttk.Scrollbar(canvas, orient="vertical", command=tree.yview)
    scrollbar_h = ttk.Scrollbar(canvas, orient="horizontal", command=tree.xview)

    # Configurar el Treeview para usar los Scrollbars
    tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

    # Colocar el Treeview en el canvas
    tree.place(x=38, y=283, width=1270, height=362)
    scrollbar_v.place(x=1310, y=283, height=344)  # Coloca la barra vertical al lado derecho del Treeview
    scrollbar_h.place(x=39, y=628, width=1289)    # Coloca la barra horizontal en la parte inferior del Treeview
    
    # Conexión a la base de datos
    cursor = conn.cursor()

    def update_tree():
        # Limpiar el Treeview antes de volver a llenarlo
        for row in tree.get_children():
            tree.delete(row)

        # Obtener el filtro del Entry
        filter_text = entry_nombre_producto.get().lower()
        product_type = selected_product_type.get()

        # Consulta para obtener los datos filtrados
        query = "SELECT * FROM stock WHERE 1=1"  # Siempre verdadero para facilitar la concatenación
        params = []

        if filter_text:
            query += " AND Producto LIKE ?"
            params.append(f'%{filter_text}%')  # Filtrar por nombre de producto

        if product_type != "Tipo de producto":
            query += " AND tipo_producto = ?"
            params.append(product_type)

        cursor.execute(query, params)

        # Insertar los datos en el Treeview
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    # Inicializar el Treeview
    update_tree()

    # Evento de selección en el Treeview
    def on_select(event):
        selected_item = tree.selection()
        if selected_item:
            product = tree.item(selected_item, "values")[1]  # Columna "Producto"
            entry_nombre_producto.delete(0, tk.END)  # Limpiar el Entry
            entry_nombre_producto.insert(0, product)  # Mostrar el producto seleccionado en el Entry

    tree.bind("<<TreeviewSelect>>", on_select)  # Vínculo del evento

    # Vínculo de eventos para actualizar el Treeview
    entry_nombre_producto.bind("<KeyRelease>", lambda event: update_tree())  # Filtro por Entry
    selected_product_type.trace("w", lambda *args: update_tree())  # Filtro por menú desplegable

    return tree  # Devolver el Treeview

def mostrar_treemod(canvas, entry_nombre_producto, selected_product_type, conn):
    # Crear el Treeview
    tree = ttk.Treeview(canvas, columns=("Tipo producto", "Producto", "Cantidad existente", "Área", "Lugar de guarda", "Cantidad migrada", "Observaciones", "Inventariado"), show='headings')

    # Definir las columnas
    for col in tree["columns"]:
        tree.heading(col, text=col)  # Establecer encabezados
        tree.column(col, anchor="e")  # Alinear columnas a la derecha

    # Crear Scrollbars
    scrollbar_v = ttk.Scrollbar(canvas, orient="vertical", command=tree.yview)
    scrollbar_h = ttk.Scrollbar(canvas, orient="horizontal", command=tree.xview)

    # Configurar el Treeview para usar los Scrollbars
    tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

    # Colocar el Treeview en el canvas
    tree.place(x=38, y=283, width=1270, height=362)
    scrollbar_v.place(x=1310, y=283, height=344)  # Coloca la barra vertical al lado derecho del Treeview
    scrollbar_h.place(x=39, y=628, width=1289)    # Coloca la barra horizontal en la parte inferior del Treeview
    
    # Conexión a la base de datos
    cursor = conn.cursor()

    def update_tree():
        # Limpiar el Treeview antes de volver a llenarlo
        for row in tree.get_children():
            tree.delete(row)

        # Obtener el filtro del Entry
        filter_text = entry_nombre_producto.get().lower()
        product_type = selected_product_type.get()

        # Consulta para obtener los datos filtrados
        query = "SELECT * FROM stock WHERE 1=1"  # Siempre verdadero para facilitar la concatenación
        params = []

        if filter_text:
            query += " AND Producto LIKE ?"
            params.append(f'%{filter_text}%')  # Filtrar por nombre de producto

        if product_type != "Tipo de producto":
            query += " AND tipo_producto = ?"
            params.append(product_type)
            
        query += " AND Inventariado = 'SI'"
        
        cursor.execute(query, params)

        # Insertar los datos en el Treeview
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    # Inicializar el Treeview
    update_tree()

    # Evento de selección en el Treeview
    def on_select(event):
        selected_item = tree.selection()
        if selected_item:
            product = tree.item(selected_item, "values")[1]  # Columna "Producto"
            entry_nombre_producto.delete(0, tk.END)  # Limpiar el Entry
            entry_nombre_producto.insert(0, product)  # Mostrar el producto seleccionado en el Entry

    tree.bind("<<TreeviewSelect>>", on_select)  # Vínculo del evento

    # Vínculo de eventos para actualizar el Treeview
    entry_nombre_producto.bind("<KeyRelease>", lambda event: update_tree())  # Filtro por Entry
    selected_product_type.trace("w", lambda *args: update_tree())  # Filtro por menú desplegable

    return tree  # Devolver el Treeview

#TREE MOSTRAR INVENTARIADOS
def mostrar_tree_inventario(canvas, entry_nombre_producto, selected_product_type, conn):
    # Crear el Treeview
    tree = ttk.Treeview(canvas, columns=("Tipo producto", "Producto", "Detalle", "Área", "Lugar de guarda", "Observaciones", "Nro.inventariado", "Estado"), show='headings')

    # Definir las columnas
    for col in tree["columns"]:
        tree.heading(col, text=col)  # Establecer encabezados
        tree.column(col, anchor="e")  # Alinear columnas a la derecha

    # Crear Scrollbars
    scrollbar_v = ttk.Scrollbar(canvas, orient="vertical", command=tree.yview)
    scrollbar_h = ttk.Scrollbar(canvas, orient="horizontal", command=tree.xview)

    # Configurar el Treeview para usar los Scrollbars
    tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

    # Colocar el Treeview en el canvas
    tree.place(x=38, y=283, width=1270, height=362)
    scrollbar_v.place(x=1310, y=283, height=344)  # Coloca la barra vertical al lado derecho del Treeview
    scrollbar_h.place(x=39, y=628, width=1289)    # Coloca la barra horizontal en la parte inferior del Treeview
    
    # Conexión a la base de datos
    cursor = conn.cursor()

    def update_tree():
        # Limpiar el Treeview antes de volver a llenarlo
        for row in tree.get_children():
            tree.delete(row)

        # Obtener el filtro del Entry
        filter_text = entry_nombre_producto.get().lower()
        product_type = selected_product_type.get()

        # Consulta para obtener los datos filtrados
        query = "SELECT * FROM Inventariados WHERE 1=1"  # Siempre verdadero para facilitar la concatenación
        params = []

        if filter_text:
            query += " AND Producto LIKE ?"
            params.append(f'%{filter_text}%')  # Filtrar por nombre de producto

        if product_type != "Tipo de producto":
            query += " AND tipo_producto = ?"
            params.append(product_type)
        
        
        cursor.execute(query, params)

        # Insertar los datos en el Treeview
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    # Inicializar el Treeview
    update_tree()

    # Evento de selección en el Treeview
    def on_select(event):
        selected_item = tree.selection()
        if selected_item:
            product = tree.item(selected_item, "values")[1]  # Columna "Producto"
            entry_nombre_producto.delete(0, tk.END)  # Limpiar el Entry
            entry_nombre_producto.insert(0, product)  # Mostrar el producto seleccionado en el Entry

    tree.bind("<<TreeviewSelect>>", on_select)  # Vínculo del evento

    # Vínculo de eventos para actualizar el Treeview
    entry_nombre_producto.bind("<KeyRelease>", lambda event: update_tree())  # Filtro por Entry
    selected_product_type.trace("w", lambda *args: update_tree())  # Filtro por menú desplegable

    return tree  # Devolver el Treeview

#TREE MOVIMIENTOS
def mostrar_tree_movimientos(canvas, entry_nombre_producto, entry_inventariado, entry_fecha_desde, entry_fecha_hasta, conn):
    # Crear el Treeview
    tree = ttk.Treeview(canvas, columns=("ID movimiento", "Fecha egreso", "Tipo egreso", "Lugar origen", 
                                          "Lugar destino", "Responsable retiro", "Cantidad egresada", 
                                          "Fecha devolucion", "Cantidad devuelta", "Responsable devolucion", 
                                          "Responsable recepcion", "Motivo", "Comentario", 
                                          "Inventariado", "Producto", "Nro.inventariado", "Definitivo"), show='headings')

    # Definir las columnas
    for col in tree["columns"]:
        tree.heading(col, text=col)  # Establecer encabezados
        tree.column(col, anchor="e")  # Alinear columnas a la derecha

    # Crear Scrollbars
    scrollbar_v = ttk.Scrollbar(canvas, orient="vertical", command=tree.yview)
    scrollbar_h = ttk.Scrollbar(canvas, orient="horizontal", command=tree.xview)

    # Configurar el Treeview para usar los Scrollbars
    tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

    # Colocar el Treeview en el canvas
    tree.place(x=38, y=283, width=1270, height=362)
    scrollbar_v.place(x=1310, y=283, height=344)  # Coloca la barra vertical al lado derecho del Treeview
    scrollbar_h.place(x=39, y=628, width=1289)

    # Conexión a la base de datos
    cursor = conn.cursor()

    def update_tree():
        # Limpiar el Treeview antes de volver a llenarlo
        for row in tree.get_children():
            tree.delete(row)

        # Obtener los filtros
        filter_text = entry_nombre_producto.get().lower()
        inventariado_text = entry_inventariado.get().lower()
        fecha_desde = entry_fecha_desde.get_date()
        fecha_hasta = entry_fecha_hasta.get_date()

        # Consulta para obtener los datos filtrados
        query = """
        SELECT * FROM Movimientos 
        WHERE 1=1
        """
        params = []

        if filter_text:
            query += " AND Producto LIKE ?"
            params.append(f'%{filter_text}%')  # Filtrar por nombre de producto

        if inventariado_text:
            query += " AND Nro_inventariado LIKE ?"
            params.append(f'%{inventariado_text}%')  # Filtrar por número de inventariado

        if fecha_desde:
            query += " AND fecha_egreso >= ?"
            params.append(fecha_desde)

        if fecha_hasta:
            query += """
            AND (fecha_devolucion <= ? OR fecha_devolucion = 'N/A')
            """
            params.append(fecha_hasta)

        cursor.execute(query, params)

        # Insertar los datos en el Treeview
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    # Inicializar el Treeview
    update_tree()

    # Evento de selección en el Treeview
    def on_select(event):
        selected_item = tree.selection()
        if selected_item:
            product = tree.item(selected_item, "values")[14]  # Columna "Producto"
            entry_nombre_producto.delete(0, tk.END)  # Limpiar el Entry
            entry_nombre_producto.insert(0, product)  # Mostrar el producto seleccionado en el Entry

    tree.bind("<<TreeviewSelect>>", on_select)  # Vínculo del evento

    # Vínculo de eventos para actualizar el Treeview
    entry_nombre_producto.bind("<KeyRelease>", lambda event: update_tree())  # Filtro por Entry
    entry_inventariado.bind("<KeyRelease>", lambda event: update_tree())  # Filtro por Entry de inventariado
    entry_fecha_desde.bind("<<DateEntrySelected>>", lambda event: update_tree())  # Filtro por fecha desde
    entry_fecha_hasta.bind("<<DateEntrySelected>>", lambda event: update_tree())  # Filtro por fecha hasta

    return tree  # Devolver el Treeview

def es_entero(dato):
    if dato.isdigit():
        return True
    else:
        return False

#VENTANA GENERICA "ACCION EXITOSA"

class Confirmacion:
    def __init__(self, root, siguiente_ventana):
        self.popup = tk.Toplevel(root)
        self.popup.geometry("773x245")
        self.popup.config(bg="#6B5E5E")
        self.popup.grab_set()
        self.popup.resizable(False, False)

        canvas = Canvas(
            self.popup,
            bg = "#6B5E5E",
            height = 245,
            width = 773,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        canvas.place(x = 0, y = 0)


        boton = Button(
            self.popup, 
            text="Siguiente", 
            bg="#FFA500", 
            fg="black", 
            bd=2, 
            font=("Inter Medium", 24 * -1),
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.cerrar_y_ejecutar(siguiente_ventana),
            relief="flat"
        )
        boton.place(
            x=250,
            y=131.0,
            width=264.0133361816406,
            height=61.48335266113281
        )

        canvas.create_rectangle(
            0.0,
            0.0,
            773.0,
            92.0,
            fill="#2B2626",
            outline="")

        canvas.create_text(
            250.0,
            31.0,
            anchor="nw",
            text="Acción realizada con éxito",
            fill="#FFFFFF",
            font=("Inter Medium", 24 * -1)
        )

        canvas.pack()
    
    def cerrar_y_ejecutar(self, funcion):
        self.popup.destroy()
        funcion()