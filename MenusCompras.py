#Menus Compras
#MODIFICAR QUERY Y LAS TREES DE REPORTES CUANDO SE ACTUALICE LA BASE
import sqlite3
from pathlib import Path
import tkinter as tk
from tkinter import Tk, Entry, Button, Canvas, StringVar, OptionMenu, messagebox, ttk
from tkcalendar import DateEntry
from funciones import mostrar_tree_porcentaje, obtener_datos4


def mostrar_tree(canvas, entry_nombre_producto, conn):
    # Crear el Treeview
    tree = ttk.Treeview(canvas, columns=("tipo_producto", "Producto", "Cantidad_existente", "Area", "Lugar_guarda", "Cantidad_migrada", "Observaciones", "Inventariado"), show='headings')

    # Definir las columnas con títulos y alineación
    headers = ["Tipo Producto", "Producto", "Cantidad Existente", "Área", "Lugar Guarda", "Cantidad Migrada", "Observaciones", "Inventariado"]
    for col, header in zip(tree["columns"], headers):
        tree.heading(col, text=header)  # Encabezados
        tree.column(col, anchor="center")  # Centramos cada columna

    # Crear Scrollbars
    scrollbar_v = ttk.Scrollbar(canvas, orient="vertical", command=tree.yview)
    scrollbar_h = ttk.Scrollbar(canvas, orient="horizontal", command=tree.xview)

    # Configurar el Treeview para usar los Scrollbars
    tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

    # Colocar el Treeview y Scrollbars en el canvas
    tree.place(x=38, y=283, width=1270, height=362)
    scrollbar_v.place(x=1310, y=283, height=344)  # Barra vertical a la derecha
    scrollbar_h.place(x=39, y=628, width=1289)    # Barra horizontal abajo

    # Conexión a la base de datos
    def update_tree():
        # Limpiar Treeview
        for row in tree.get_children():
            tree.delete(row)

        # Obtener filtro del Entry
        filter_text = entry_nombre_producto.get().strip().lower()

        # Buscar en la base de datos
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stock WHERE LOWER(Producto) LIKE ?", (f'%{filter_text}%',))
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)  # Insertar filas filtradas
        cursor.close()
    # Inicializar el Treeview
    update_tree()

    # Evento de selección en Treeview
    def on_select(event):
        selected_item = tree.selection()
        if selected_item:
            # Columna "Producto" para el Entry
            product = tree.item(selected_item, "values")[1]
            entry_nombre_producto.delete(0, tk.END)  
            entry_nombre_producto.insert(0, product)  # Mostrar producto seleccionado

    tree.bind("<<TreeviewSelect>>", on_select)  # Vínculo de selección

    # Vínculo para actualizar el Treeview
    entry_nombre_producto.bind("<KeyRelease>", lambda event: update_tree())
    
    return tree  # Devolver Treeview

def es_entero(dato):
    return dato.isdigit()

class RegistrarCompraCabecera:
    def __init__(self, master, cambiar_a_compra_posicion, cambiar_a_main_menu, conn):
        self.master = master

        canvas = Canvas(self.master, bg = "#6B5E5E", height = 768, width = 1366, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x=0, y=0)

        boton_cancelar = Button(self.master, text="Cancelar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_main_menu, relief="flat") 
        boton_cancelar.place(x=708.0, y=672.0, width=264.0133361816406, height=61.48335266113281)

        boton_registrar = Button(self.master, text="Registrar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.registrar_compra_cabecera(cambiar_a_compra_posicion, conn), relief="flat") 
        boton_registrar.place(x=382.0, y=672.0, width=264.0133361816406, height=61.48335266113281)

        # Crear un Entry
        self.objetivo_compra = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))  # Ajusta el tamaño de la fuente según sea necesario)
        self.objetivo_compra.place(x=708.0, y=500.0, width=607.6497192382812, height=89.0)  # El height se ignorará en Entry, puedes ajustarlo según sea necesario
        
        # Crear el texto en el canvas
        canvas.create_text(709.0, 470.0,  anchor="nw", text="Objetivo Compra\n", fill="#000000", font=("Inter Medium", 24 * -1))

        # Entry 2
        self.fecha_ingreso = DateEntry(self.master, date_pattern='yyyy-MM-dd', width=12, background="#2B2626", foreground="white", borderwidth=2)
        self.fecha_ingreso.pack(padx=40, pady=40)
        self.fecha_ingreso.place(x=708.0, y=420.0, width=607.6497192382812, height=40)

        # Texto para el Entry 2
        canvas.create_text(709.0, 390.0, anchor="nw", text="Fecha ingreso", fill="#000000", font=("Inter", 24 * -1))

        self.comentario = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.comentario.place(x=708.0, y=340.0, width=607.6497192382812, height=40)
        canvas.create_text(709.0, 310.0, anchor="nw", text="Comentario (completar SOLO si lugar recepcion es OTRO)", fill="#000000", font=("Inter", 24 * -1))

        # Entry 3
        self.lugar_recepcion_var = StringVar(master)
        self.lugar_recepcion_var.set("ESCUELA DE FORMACION TECNICA LABORAL")  # Valor predeterminado
        
        self.lugar_recepcion = OptionMenu(master, self.lugar_recepcion_var, "ESCUELA DE FORMACION TECNICA LABORAL", "ESCUELA AGRARIA", "OTRO")
        
        self.lugar_recepcion.place(x=709.0, y=260.0, width=607.0, height=40)

        # Texto para el Entry 3
        canvas.create_text(708.0, 230.0, anchor="nw", text="Lugar recepción", fill="#000000", font=("Inter", 24 * -1))

        # Entry 4
        self.recepcionado = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))  # Ajusta el tamaño de la fuente según sea necesario)
        self.recepcionado.place(x=708.0, y=180.0, width=607.6497192382812, height=40)

        # Texto para el Entry 4
        canvas.create_text(708.0, 150.0, anchor="nw", text="Recepcionado", fill="#000000", font=("Inter Medium", 24 * -1))

        # Entry 5
        self.origenfondo_var = StringVar(master)
        self.origenfondo_var.set("ORDINARIO")  # Valor predeterminado
        
        self.origen_fondo = OptionMenu(master, self.origenfondo_var, "ORDINARIO", "EDUCATIVO", "CAJA CHICA")
        self.origen_fondo.place(x=39.0, y=500.0, width=607.6497192382812, height=40)

        # Texto para el Entry 5
        canvas.create_text(39.0, 470.0, anchor="nw", text="Origen fondo", fill="#000000", font=("Inter Medium", 24 * -1))

        self.proveedor = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))  # Ajusta el tamaño de la fuente según sea necesario
        self.proveedor.place(x=39.0, y=580.0, width=607.0, height=40)
        canvas.create_text(41.0, 550.0, anchor="nw", text="Proveedor", fill="#000000", font=("Inter Medium", 24 * -1))
        
        self.fecha_factura = DateEntry(self.master, date_pattern='yyyy-MM-dd', width=12, background="#2B2626", foreground="white", borderwidth=2)
        self.fecha_factura.pack(padx=40, pady=40)
        self.fecha_factura.place(x=38.0, y=420.0, width=607.6497192382812, height=40)

        canvas.create_text(38.0, 390.0, anchor="nw", text="Fecha factura", fill="#000000", font=("Inter Medium", 24 * -1))

        # Entry 8
        self.nro_factura = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter", 20 * -1)) # Ajusta el tamaño de la fuente según sea necesario
        self.nro_factura.place(x=39.0, y=340.0, width=607.0, height=40)

        canvas.create_text(38.0, 310.0, anchor="nw", text="Nro factura", fill="#000000", font=("Inter Medium", 24 * -1))

        self.fecha_OC = DateEntry(self.master, date_pattern='yyyy-MM-dd', width=12, background="#2B2626", foreground="white", borderwidth=2)
        self.fecha_OC.pack(padx=40, pady=40)
        self.fecha_OC.place(x=38.0, y=260.0, width=607.6497192382812, height=40)

        canvas.create_text(38.0, 230.0, anchor="nw", text="Fecha OC", fill="#000000", font=("Inter Medium", 24 * -1))

        # Entry 8
        self.nro_OC = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter", 20 * -1)) # Ajusta el tamaño de la fuente según sea necesario
        self.nro_OC.place(x=39.0, y=180.0, width=607.0, height=40)

        # Texto para el Entry 8
        canvas.create_text(39.0, 150.0, anchor="nw", text="Nro OC", fill="#000000", font=("Inter", 24 * -1))

        # Crear el rectángulo en el canvas
        canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        # Título en el canvas
        canvas.create_text(415.0, 47.0, anchor="nw", text="REGISTRAR COMPRA CABECERA", fill="#FFFFFF",  font=("PalanquinDark Regular", 36 * -1))

        canvas.pack()

    def registrar_compra_cabecera(self, funcion, conn):
        objetivo_compra = self.objetivo_compra.get().strip().capitalize()
        fecha_ingreso = self.fecha_ingreso.get_date()
        lugar_recepcion = self.lugar_recepcion_var.get()
        recepcionado = self.recepcionado.get().strip().title()
        origen_fondo = self.origenfondo_var.get()
        fecha_oc = self.fecha_OC.get_date()
        nro_oc =  self.nro_OC.get().strip()
        fecha_factura = self.fecha_factura.get_date()
        nro_factura = self.nro_factura.get().strip()
        comentario = self.comentario.get().strip().capitalize()
        proveedor = self.proveedor.get().strip().capitalize()

        if lugar_recepcion == "OTRO":
            lugar_recepcion = comentario

        #if not es_entero(monto_total):
         #   messagebox.showerror("Error.", "Ingrese un valor numérico valido en monto.")
          #  return

        if not es_entero(nro_oc):
            messagebox.showerror("Error.", "Ingrese un valor numérico valido en nro. OC.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Compra_cabecera (Nro_OC, Fecha_OC, Monto_total, Origen_fondo, Recepcionado, Lugar_recepcion, Fecha_ingreso, Objetivo_compra, Nro_factura, Fecha_factura, Proveedor)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (nro_oc, fecha_oc, 0, origen_fondo, recepcionado, lugar_recepcion, fecha_ingreso, objetivo_compra, nro_factura, fecha_factura, proveedor)) 

            print("La compra se ha registrado exitosamente.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error.", "El producto ya existe o hay un problema de integridad.")
        except sqlite3.Error as e:
            messagebox.showerror("Error.", f"Error al actualizar el stock: {e}")
        finally:
            conn.commit()
            cursor.close()  # Cerrar el cursor después de usarlo
        
        funcion()


class RegistrarCompraPosicion:

    def __init__(self, master, cambiar_a_main_menu, cambiar_a_otra_compra, conn):
        self.master = master
        self.conn = conn
        self.cont = 1

        canvas = Canvas(self.master, bg="#6B5E5E", height=768, width=1366, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
    
        boton_registrar = Button(self.master, text="Registrar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), command=lambda:self.registrar_compra_posicion(cambiar_a_otra_compra, conn))
        boton_registrar.place(x=391.475, y=665.516, width=264.013, height=61.483)

        boton_cancelar = Button(self.master, text="Cancelar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), command=lambda:self.eliminar_compra(cambiar_a_main_menu, conn))
        boton_cancelar.place(x=735.111, y=665.516, width=264.013, height=61.483)

        canvas.create_rectangle(38.0, 281.0, 1328.0, 643.0, fill="#FFFFFF", outline="")

        self.precio_unitario = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.precio_unitario.place(x=885.0, y=197.0, width=443.0, height=57.0)

        canvas.create_text(885.0, 164.0, anchor="nw", text="Precio unitario", fill="#000000", font=("Inter Medium", 24 * -1))

        self.Cantidad = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.Cantidad.place(x=573.0, y=197.0, width=288.0, height=57.0)
        
        canvas.create_text(573.0, 164.0, anchor="nw", text="Cantidad", fill="#000000", font=("Inter Medium", 24 * -1))

        self.producto = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.producto.place(x=38.0, y=197.0, width=507.0, height=57.0)

        canvas.create_text(38.0, 164.0, anchor="nw", text="Producto", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        canvas.create_text(524.0, 47.0, anchor="nw", text="COMPRA POSICION", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))

        self.tree = mostrar_tree(canvas, self.producto, conn)

        canvas.pack()

    def obtener_id(self):
        cursor = self.conn.cursor()
        try:
            # Fetch the last id_cabecera
            cursor.execute("SELECT id_cabecera FROM Compra_cabecera ORDER BY id_cabecera DESC LIMIT 1;")
            resultado = cursor.fetchone()
            id_cabecera = resultado[0] if resultado else None
        except sqlite3.Error as e:
            messagebox.showerror("Error.", f"Error al actualizar el stock: {e}")
            id_cabecera = None
        finally:
            cursor.close()
        
        return id_cabecera

    def obtener_nuevo_id_posicion(self, id_cabecera):
        cursor = self.conn.cursor()
        try:
            # Get the max id_posicion for the given id_cabecera
            cursor.execute("SELECT MAX(id_posicion) FROM Compra_posicion WHERE id_cabecera = ?", (id_cabecera,))
            resultado = cursor.fetchone()
            nuevo_id_posicion = (resultado[0] or 0) + 1  # Start from 1 if no previous id_posicion exists
        except sqlite3.Error as e:
            messagebox.showerror("Error.", f"Error al actualizar el stock: {e}")
            nuevo_id_posicion = None
        finally:
            cursor.close()
        
        return nuevo_id_posicion

    def registrar_compra_posicion(self, funcion, conn):
        selected_item = self.tree.selection()
        if selected_item:
            selected_product = self.tree.item(selected_item, "values")[1]  # Product selected from Treeview

        precio_unitario = self.precio_unitario.get().strip()
        cantidad = self.Cantidad.get().strip()

        if not es_entero(cantidad):
            messagebox.showerror("Error.", "Ingrese un valor numérico válido en cantidad.")
            return
        if not es_entero(precio_unitario):
            messagebox.showerror("Error.", "Ingrese un valor numérico válido en precio.")
            return


        id_cabecera = self.obtener_id()
        id_posicion = self.obtener_nuevo_id_posicion(id_cabecera)

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO Compra_posicion (id_posicion, id_cabecera, Producto, Cantidad, Precio_unitario, Inventariado)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (id_posicion, id_cabecera, selected_product, cantidad, precio_unitario, None)
            )
            cursor.execute(
                """
                UPDATE stock
                SET Cantidad_existente = Cantidad_existente + ?
                WHERE Producto = ?
                """, (cantidad, selected_product)
            )

            print("La compra se ha registrado exitosamente.")
        except sqlite3.Error as e:
            messagebox.showerror("Error.", f"Error al actualizar el stock: {e}")
        finally:
            conn.commit()
            cursor.close()

        self.cont += 1
        funcion()
    
    def eliminar_compra(self, funcion, conn):
        resultado = self.obtener_id()
        cursor = conn.cursor()
        try:
            cursor.execute("""DELETE FROM Compra_cabecera
                           Where id_cabecera = ?""", (resultado,))
        finally:
            conn.commit()
            cursor.close()
        funcion()    
        
class RegistrarOtroProducto:
    def __init__(self, root, cambiar_a_otra_compra, cambiar_a_compra_posicion, registrar_compra_posicion_instance):
        self.popup = tk.Toplevel(root)
        self.popup.geometry("773x245")
        self.popup.config(bg="#6B5E5E")
        self.popup.grab_set()
        self.popup.resizable(False, False)
        self.registrar_compra_posicion_instance = registrar_compra_posicion_instance
    

        canvas = Canvas(self.popup, bg = "#6B5E5E", height = 245, width = 773, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)

        boton_no = Button(self.popup, text="No", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.agregar_monto_total(cambiar_a_otra_compra, registrar_compra_posicion_instance), relief="flat") 
        boton_no.place(x=426.63671875,y=131.0, width=264.0133361816406, height=61.48335266113281)

        boton_si = Button(self.popup, text="Sí", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.agregar_otro_producto(cambiar_a_compra_posicion), relief="flat") 
        boton_si.place(x=83.0, y=131.0, width=264.0133361816406, height=61.48335266113281)
        
        canvas.create_rectangle(0.0, 0.0, 773.0, 92.0, fill="#2B2626", outline="")

        canvas.create_text(216.0, 31.0, anchor="nw", text="¿Desea agregar otro producto?", fill="#FFFFFF", font=("Inter Medium", 24 * -1))
        
        canvas.pack()

    def agregar_otro_producto(self, funcion):
        #self.registrar_compra_posicion_instance.cont += 1
        self.cerrar_y_ejecutar(funcion)

    def agregar_monto_total(self, funcion, conn):
        
        id_cabecera = self.obtener_id(conn)

        try:
            cursor = conn.cursor()
            cursor.execute("""UPDATE Compra_cabecera
                           SET Monto_total = (SELECT SUM (Cantidad * precio_unitario)
                           FROM compra_posicion 
                           WHERE compra_posicion.id_cabecera = Compra_cabecera.id_cabecera)
                           WHERE id_cabecera = ?
            """, (id_cabecera,))
            
            print(id_cabecera)
        except sqlite3.Error as e:
            messagebox.showerror("Error.", f"Error al actualizar el stock: {e}")

        finally:
            conn.commit()
            cursor.close()
        
        self.cerrar_y_ejecutar(funcion)

    def obtener_id(self, conn):
        cursor = conn.cursor()
        try:
            # Fetch the last id_cabecera
            cursor.execute("SELECT id_cabecera FROM Compra_cabecera ORDER BY id_cabecera DESC LIMIT 1;")
            resultado = cursor.fetchone()
            id_cabecera = resultado[0] if resultado else None
        except sqlite3.Error as e:
            messagebox.showerror("Error.", f"Error al actualizar el stock: {e}")
            id_cabecera = None
        finally:
            cursor.close()
        
        return id_cabecera

    def cerrar_y_ejecutar(self, funcion):
        self.popup.destroy()
        funcion()


class RegistrarOtraCompra:
    def __init__(self, root, cambiar_a_compra_cabecera, cambiar_a_main_menu):
        self.popup = tk.Toplevel(root)
        self.popup.geometry("773x245")
        self.popup.config(bg="#6B5E5E")
        self.popup.grab_set()
        self.popup.resizable(False, False)

        canvas = Canvas(self.popup, bg = "#6B5E5E", height = 245, width = 773, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)

        boton_no = Button(self.popup, text="No", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_main_menu), relief="flat") 
        boton_no.place(x=426.63671875,y=131.0, width=264.0133361816406, height=61.48335266113281)

        boton_si = Button(self.popup, text="Sí", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_compra_cabecera), relief="flat") 
        boton_si.place(x=83.0, y=131.0, width=264.0133361816406, height=61.48335266113281)
        
        canvas.create_rectangle(0.0, 0.0, 773.0, 92.0, fill="#2B2626", outline="")

        canvas.create_text(216.0, 31.0, anchor="nw", text="¿Desea registrar otra compra?", fill="#FFFFFF", font=("Inter Medium", 24 * -1))
        
        canvas.pack()

    def cerrar_y_ejecutar(self, funcion):
        self.popup.destroy()  # Cierra la ventana emergente
        funcion() #Ejecuta la funcion dada


class ModificarCompra1:
    def __init__(self, master, cambiar_a_modif_compra_2, cambiar_a_compras, conn):
        self.master = master
        self.conn = conn

        canvas = Canvas(self.master, bg="#6B5E5E", height=768, width=1366, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        boton_cancelar = Button(self.master, text="Cancelar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_compras, relief="flat")
        boton_cancelar.place(x=800, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        boton_modificar = Button(self.master, text="Modificar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.mostrar_modificar_compra_2(cambiar_a_modif_compra_2), relief="flat")
        boton_modificar.place(x=500, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        self.fecha_hasta = DateEntry(self.master, date_pattern='yyyy-MM-dd', width=12, background="#2B2626", foreground="white", borderwidth=2)
        self.fecha_hasta.pack(padx=40, pady=40)
        self.fecha_hasta.place(x=720.0, y=197.0,  width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(720.0, 149.0, anchor="nw", text="Fecha hasta:", fill="#000000", font=("Inter Medium", 24 * -1))

        self.fecha_desde = DateEntry(self.master, date_pattern='yyyy-MM-dd', width=12, background="#2B2626", foreground="white", borderwidth=2)
        self.fecha_desde.pack(padx=40, pady=40)
        self.fecha_desde.place(x=38.0, y=203.0, width=607.6497192382812, height=59.03461837768555)

        canvas.create_text(38.0, 155.0, anchor="nw", text="Fecha desde:", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")
        canvas.create_text(545.0, 47.0, anchor="nw", text="FACTURAS", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))
      
        self.tree = mostrar_tree_porcentaje(canvas, self.fecha_desde, self.fecha_hasta, conn)
        
        canvas.pack()

    def mostrar_modificar_compra_2(self, cambiar_a_modif_compra_2):
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_product = self.tree.item(selected_item, 'values')[0]  # Suponiendo que el nombre del producto es la segunda columna
            cambiar_a_modif_compra_2(self.selected_product)

class ModificarCompra2:
    def __init__(self, master, cambiar_a_listo, cambiar_a_compras, conn, selected_product):
        self.master = master
        lista = obtener_datos4(selected_product, conn)
        canvas = Canvas(self.master, bg = "#6B5E5E", height = 768, width = 1366, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x=0, y=0)

        boton_cancelar = Button(self.master, text="Cancelar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_compras, relief="flat") 
        boton_cancelar.place(x=708.0, y=672.0, width=264.0133361816406, height=61.48335266113281)

        boton_modificar = Button(self.master, text="Modificar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.registrar_compra_cabecera(cambiar_a_listo, conn, selected_product), relief="flat") 
        boton_modificar.place(x=382.0, y=672.0, width=264.0133361816406, height=61.48335266113281)

        # Crear un Entry
        self.objetivo_compra = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.objetivo_compra.insert(0, lista[8])
        self.objetivo_compra.place(x=708.0, y=500.0, width=607.6497192382812, height=89.0)
        
        # Crear el texto en el canvas
        canvas.create_text(709.0, 470.0,  anchor="nw", text="Objetivo Compra\n", fill="#000000", font=("Inter Medium", 24 * -1))

        # Entry 2
        self.fecha_ingreso = DateEntry(self.master, date_pattern='yyyy-MM-dd', width=12, background="#2B2626", foreground="white", borderwidth=2)
        self.fecha_ingreso.set_date(lista[7])
        self.fecha_ingreso.pack(padx=40, pady=40)
        self.fecha_ingreso.place(x=708.0, y=420.0, width=607.6497192382812, height=40)

        # Texto para el Entry 2
        canvas.create_text(709.0, 390.0, anchor="nw", text="Fecha ingreso", fill="#000000", font=("Inter", 24 * -1))

        self.comentario = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.comentario.place(x=708.0, y=340.0, width=607.6497192382812, height=40)
        canvas.create_text(709.0, 310.0, anchor="nw", text="Comentario (completar SOLO si lugar recepcion es OTRO)", fill="#000000", font=("Inter", 24 * -1))

        # Entry 3
        self.lugar_recepcion_var = StringVar(master)
        self.lugar_recepcion_var.set(lista[6])  # Valor predeterminado
        
        self.lugar_recepcion = OptionMenu(master, self.lugar_recepcion_var, "ESCUELA DE FORMACION TECNICA LABORAL", "ESCUELA AGRARIA", "OTRO")
        
        self.lugar_recepcion.place(x=709.0, y=260.0, width=607.0, height=40)

        # Texto para el Entry 3
        canvas.create_text(708.0, 230.0, anchor="nw", text="Lugar recepción", fill="#000000", font=("Inter", 24 * -1))

        # Entry 4
        self.recepcionado = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.recepcionado.insert(0, lista[5])
        self.recepcionado.place(x=708.0, y=180.0, width=607.6497192382812, height=40)

        # Texto para el Entry 4
        canvas.create_text(708.0, 150.0, anchor="nw", text="Recepcionado", fill="#000000", font=("Inter Medium", 24 * -1))

        # Entry 5
        self.origenfondo_var = StringVar(master)
        self.origenfondo_var.set(lista[4])  # Valor predeterminado
        
        self.origen_fondo = OptionMenu(master, self.origenfondo_var, "ORDINARIO", "EDUCATIVO", "CAJA CHICA")
        self.origen_fondo.place(x=39.0, y=500.0, width=607.6497192382812, height=40)

        # Texto para el Entry 5
        canvas.create_text(39.0, 470.0, anchor="nw", text="Origen fondo", fill="#000000", font=("Inter Medium", 24 * -1))

        self.proveedor = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.proveedor.insert(0, lista[11])
        self.proveedor.place(x=39.0, y=580.0, width=607.0, height=40)
        canvas.create_text(41.0, 550.0, anchor="nw", text="Proveedor", fill="#000000", font=("Inter Medium", 24 * -1))
        
        self.fecha_factura = DateEntry(self.master, date_pattern='yyyy-MM-dd', width=12, background="#2B2626", foreground="white", borderwidth=2)
        self.fecha_factura.set_date(lista[10])
        self.fecha_factura.pack(padx=40, pady=40)
        self.fecha_factura.place(x=38.0, y=420.0, width=607.6497192382812, height=40)

        canvas.create_text(38.0, 390.0, anchor="nw", text="Fecha factura", fill="#000000", font=("Inter Medium", 24 * -1))

        # Entry 8
        self.nro_factura = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter", 20 * -1)) # Ajusta el tamaño de la fuente según sea necesario
        self.nro_factura.place(x=39.0, y=340.0, width=607.0, height=40)
        self.nro_factura.insert(0, lista[9])

        canvas.create_text(38.0, 310.0, anchor="nw", text="Nro factura", fill="#000000", font=("Inter Medium", 24 * -1))

        self.fecha_OC = DateEntry(self.master, date_pattern='yyyy-MM-dd', width=12, background="#2B2626", foreground="white", borderwidth=2)
        self.fecha_OC.pack(padx=40, pady=40)
        self.fecha_OC.set_date(lista[2])
        self.fecha_OC.place(x=38.0, y=260.0, width=607.6497192382812, height=40)

        canvas.create_text(38.0, 230.0, anchor="nw", text="Fecha OC", fill="#000000", font=("Inter Medium", 24 * -1))

        # Entry 8
        self.nro_OC = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter", 20 * -1))
        self.nro_OC.insert(0, lista[1])
        self.nro_OC.place(x=39.0, y=180.0, width=607.0, height=40)

        # Texto para el Entry 8
        canvas.create_text(39.0, 150.0, anchor="nw", text="Nro OC", fill="#000000", font=("Inter", 24 * -1))

        # Crear el rectángulo en el canvas
        canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        # Título en el canvas
        canvas.create_text(415.0, 47.0, anchor="nw", text="REGISTRAR COMPRA CABECERA", fill="#FFFFFF",  font=("PalanquinDark Regular", 36 * -1))

        canvas.pack()

    def registrar_compra_cabecera(self, funcion, conn, id_cabecera):
        objetivo_compra = self.objetivo_compra.get().strip().capitalize()
        fecha_ingreso = self.fecha_ingreso.get_date()
        lugar_recepcion = self.lugar_recepcion_var.get()
        recepcionado = self.recepcionado.get().strip().title()
        origen_fondo = self.origenfondo_var.get()
        fecha_oc = self.fecha_OC.get_date()
        nro_oc =  self.nro_OC.get().strip()
        fecha_factura = self.fecha_factura.get_date()
        nro_factura = self.nro_factura.get().strip()
        comentario = self.comentario.get().strip().capitalize()
        proveedor = self.proveedor.get().strip().capitalize()

        if lugar_recepcion == "OTRO":
            lugar_recepcion = comentario

        #if not es_entero(monto_total):
         #   messagebox.showerror("Error.", "Ingrese un valor numérico valido en monto.")
          #  return

        if not es_entero(nro_oc):
            messagebox.showerror("Error.", "Ingrese un valor numérico valido en nro. OC.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Compra_cabecera 
                SET Nro_OC = ?,
                Fecha_OC = ?,
                Origen_fondo = ?,
                Recepcionado = ?,
                Lugar_recepcion = ?,
                Fecha_ingreso = ?,
                Objetivo_compra = ?,
                Nro_factura = ?,
                Fecha_factura = ?,
                Proveedor = ?
                WHERE id_cabecera = ?
            """, (nro_oc, fecha_oc, origen_fondo, recepcionado, lugar_recepcion, fecha_ingreso, objetivo_compra, nro_factura, fecha_factura, proveedor, id_cabecera)) 

            print("La compra se ha registrado exitosamente.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error.", "El producto ya existe o hay un problema de integridad.")
        except sqlite3.Error as e:
            messagebox.showerror("Error.", f"Error al actualizar el stock: {e}")
        finally:
            conn.commit()
            cursor.close()  # Cerrar el cursor después de usarlo
        
        funcion()