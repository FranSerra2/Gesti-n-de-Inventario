#ACOMODAR LA INTERFAZ
import tkinter as tk
from tkinter import Tk, Canvas, Entry, Button, messagebox, StringVar, OptionMenu, Text, ttk
import sqlite3
from tkcalendar import DateEntry
from funciones import mostrar_tree_inventario, mostrar_tree_modificado

def es_entero(dato):
    return dato.isdigit()

class RegistrarDevolucion:
    def __init__(self, master, cambiar_a_devolucion_2, cambiar_a_buscar_mov_1, primary_key, conn):
        self.master = master

        canvas = Canvas(self.master,bg = "#6B5E5E",height = 768,width = 1366,bd = 0,highlightthickness = 0,relief = "ridge")
        canvas.place(x = 0, y = 0)

        boton_cancelar = Button(self.master, text="Cancelar", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_buscar_mov_1,relief="flat")
        boton_cancelar.place(x=735.11181640625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        self.boton_registrar = Button(self.master, text="Registrar", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.registrar_devolucion(cambiar_a_devolucion_2, conn, primary_key), relief="flat")
        self.boton_registrar.place(x=391.47509765625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        canvas.create_text(472.0, 47.0, anchor="nw", text="REGISTRAR DEVOLUCIÓN", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))


        self.entry_responsable_devolucion = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.entry_responsable_devolucion.place(x=714.0, y=370.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(714.0, 341.0, anchor="nw", text="Responsable de devolución", fill="#000000", font=("Inter Medium", 24 * -1))
        
        self.entry_cant_devuelta = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.entry_cant_devuelta.place(x=714.0, y=238.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(714.0, 209.0, anchor="nw", text="Cantidad devuelta", fill="#000000", font=("Inter Medium", 24 * -1))


        self.entry_fecha_devolucion = DateEntry(self.master, date_pattern='yyyy-MM-dd', width=12, background="#2B2626", foreground="white", borderwidth=2)
        self.entry_fecha_devolucion.pack(padx=40, pady=40)
        self.entry_fecha_devolucion.place(x=45.0, y=370.0, width=607.0, height=58.0)
        
        canvas.create_text(45.0, 330.0, anchor="nw", text="Fecha de devolución", fill="#000000", font=("Inter Medium", 24 * -1))


        self.entry_producto = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.entry_producto.place(x=45.0, y=238.0, width=607.0, height=58.0)
        
        selected_product = self.obtener_producto(conn, primary_key)
        self.entry_producto.insert(0, selected_product)

        canvas.create_text(46.0, 209.0, anchor="nw", text="Producto", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.pack()

    def obtener_producto(self, conn, primary_key):
        try:
            cursor = conn.cursor()
            cursor.execute("""SELECT Producto FROM Movimientos WHERE id_movimiento = ?""", (primary_key,))
            selected_product = cursor.fetchone() 
        finally:
            cursor.close()

        # Si hay un resultado, devolvemos el primer valor (la columna Producto)
        if selected_product:
            return selected_product[0]
        else:
            return None

    def verificar_cantidad(self, conn, primary_key):
        try:
            cursor = conn.cursor()
            cursor.execute("""SELECT cantidad_egresada FROM Movimientos WHERE id_movimiento = ?""", (primary_key,))
            cantidad_prestada = cursor.fetchone()
        finally:
            cursor.close()
        
        if cantidad_prestada:
            return cantidad_prestada[0]


    def registrar_devolucion(self, funcion, conn, primary_key):
        responsable_dev = self.entry_responsable_devolucion.get().strip().title()
        cantidad_dev = self.entry_cant_devuelta.get().strip()
        fecha_dev = self.entry_fecha_devolucion.get_date()
        producto = self.entry_producto.get().strip().capitalize()

        cantidad_prestada = self.verificar_cantidad(conn, primary_key)
        if int(cantidad_dev) > int(cantidad_prestada):
            messagebox.showerror("Error.", "Cantidad devuelta no puede ser mayor a la cantidad prestada.")
            return

        if not es_entero(cantidad_dev):
            messagebox.showerror("Error.", "Ingrese un valor numérico valido en cantidad devuelta.")
            return

        try:
            cursor = conn.cursor()  # Crear el cursor aquí
            # Inserción en la base de datos
            cursor.execute("""SELECT Producto FROM Movimientos WHERE id_movimiento = ?""", (primary_key,))

            cursor.execute("""
                UPDATE Movimientos
                SET Producto = ?,
                    fecha_devolucion = ?,
                    Responsable_devolucion = ?,
                    cantidad_devuelta = ?
                WHERE id_movimiento = ?
            """, (producto, fecha_dev, responsable_dev, cantidad_dev, primary_key)) #ID se obtiene de lo seleccionado en el tree

            cursor.execute("""UPDATE stock 
                                SET Cantidad_migrada = Cantidad_migrada - ?, 
                                Cantidad_existente = Cantidad_existente + ? 
                            WHERE Producto = ?""", (cantidad_dev, cantidad_dev, producto))

            
            print("Producto registrado exitosamente.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error.", "El producto ya existe o hay un problema de integridad.")
        except sqlite3.Error as e:
            messagebox.showerror("Error.", f"Error al registrar producto: {e}")  # Manejo de otros errores
        finally:

            conn.commit()
            cursor.close()  # Cerrar el cursor después de usarlo
        
        funcion()

class RegistrarDevolucionPT2:
    def __init__(self, root, cambiar_a_buscar_mov_1, cambiar_a_menuInv):
        self.popup = tk.Toplevel(root)
        self.popup.geometry("773x245")
        self.popup.config(bg="#6B5E5E")
        self.popup.grab_set()

        canvas = Canvas(self.popup, bg = "#6B5E5E", height = 245, width = 773, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)

        boton_cancelar = Button(self.popup,  text="No",  bg="#FFA500",  fg="black",  bd=2,  font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_menuInv), relief="flat")
        boton_cancelar.place(x=426.63671875, y=131.0, width=264.0133361816406, height=61.48335266113281)


        boton_confirmar = Button(self.popup,  text="Sí",  bg="#FFA500",  fg="black",  bd=2,  font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_buscar_mov_1), relief="flat")
        boton_confirmar.place(x=83.0, y=131.0, width=264.0133361816406, height=61.48335266113281)

        canvas.create_rectangle(0.0, 0.0, 773.0, 92.0, fill="#2B2626", outline="")

        canvas.create_text(190.0, 31.0, anchor="nw", text="¿Desea registrar otra devolución?", fill="#FFFFFF", font=("Inter Medium", 24 * -1))

        canvas.pack()

    def cerrar_y_ejecutar(self, funcion):
        self.popup.destroy()  # Cierra la ventana emergente
        funcion() #Ejecuta la funcion dada
        

class RegistrarPrestamo0:
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
        selected_product_type.set("Herramienta")
        # Menú desplegable
        product_type_menu = OptionMenu(master, selected_product_type, "Herramienta", "Maquinaria", "Insumo", "Limpieza")
        product_type_menu.place(x=38.0, y=201.0, width=607.6497192382812, height=59.03461837768555)
        canvas.create_text(40.0, 150.0, anchor="nw", text="Tipo de producto", fill="#000000", font=("Inter Medium", 24 * -1))
        
        nombre_del_producto = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1 ))
        nombre_del_producto.place(x=720.0, y=198.0, width=607.6497192382812, height=57.03461837768555)
        canvas.create_text(720.0, 150.0, anchor="nw", text="Nombre del producto", fill="#000000", font=("Inter Medium", 24 * -1))

        inventariado = "NO"
        
        canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        canvas.create_text(500.0, 47.0, anchor="nw", text="PRESTAMO", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))
        
        # Crear ambas vistas de Treeview
        self.tree = mostrar_tree_modificado(canvas, nombre_del_producto, selected_product_type, inventariado,conn)
    
        canvas.pack()

    def mostrar_vizualizarDMP2(self, cambiar_a_visualizarDM_2):
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_product = self.tree.item(selected_item, 'values')[1]  # Suponiendo que el nombre del producto es la segunda columna
            cambiar_a_visualizarDM_2(self.selected_product)


class RegistrarPrestamo:
    def __init__(self, master, cambiar_a_prestamo_2, cambiar_a_menuInv, conn, selected_product):
        self.master = master

        canvas = Canvas(self.master, bg = "#6B5E5E", height = 916, width = 1366, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)

        boton_cancelar = Button(self.master, text="Cancelar", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command= cambiar_a_menuInv, relief="flat")
        boton_cancelar.place(x=746.6368408203125, y=822.0, width=264.0133361816406, height=61.48335266113281)

        boton_registrar = Button(self.master, text="Registrar", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.registrar_prestamo(cambiar_a_prestamo_2, conn), relief="flat")
        boton_registrar.place(x=403.0, y=822.0, width=264.0133361816406, height=61.48335266113281)

        self.comentario = Text(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.comentario.place(x=714.0, y=611.0, width=607.6497192382812, height=57.03461837768555)
        canvas.create_text(714.0, 572.0, anchor="nw", text="Comentario", fill="#000000", font=("Inter Medium", 24 * -1))

        self.resp_devolucion = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.resp_devolucion.place(x=714.0, y=504.0, width=607.6497192382812, height=57.03461837768555)
        canvas.create_text(714.0, 466.0, anchor="nw", text="Responsable de devolución", fill="#000000", font=("Inter Medium", 24 * -1))

        self.lugar_var = StringVar(self.master)
        self.lugar_var.set("ESCUELA DE FORMACION TECNICA LABORAL")  # Valor por defecto
        self.lugar_origen = OptionMenu(self.master, self.lugar_var, "ESCUELA DE FORMACION TECNICA LABORAL", "ESCUELA AGRARIA", "OTRO")
        self.lugar_origen.place(x=714.0, y=396.0, width=607.6497192382812, height=57.03461837768555)
        canvas.create_text(714.0, 358.0, anchor="nw", text="Lugar de origen", fill="#000000", font=("Inter Medium", 24 * -1 ))

        self.motivo = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.motivo.place(x=714.0, y=290.0, width=607.6497192382812, height=57.03461837768555)
        canvas.create_text(714.0, 252.0, anchor="nw", text="Motivo", fill="#000000", font=("Inter Medium", 24 * -1))

        #self.entry_5 = DateEntry(self.master, date_pattern='yyyy-MM-dd', width=12, background="#2B2626", foreground="white", borderwidth=2)
        #self.entry_5.pack(padx=40, pady=40)
        #self.entry_5.place(x=714.0, y=290.0, width=607.6497192382812, height=57.03461837768555)
        #self.entry_5.delete(0, tk.END) #Permite dejar el espacio en blanco
        #canvas.create_text(714.0, 252.0, anchor="nw", text="Fecha devolución", fill="#000000", font=("Inter Medium", 24 * -1))

        self.cantidad_egresada = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.cantidad_egresada.place(x=714.0, y=184.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(714.0, 146.0, anchor="nw", text="Cantidad egresada", fill="#000000", font=("Inter Medium", 24 * -1))

        self.responsable_recepcion = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.responsable_recepcion.place(x=45.0, y=717.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(45.0, 679.0, anchor="nw", text="Responsable recepción", fill="#000000", font=("Inter Medium", 24 * -1))

        self.entry_8 = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.entry_8.place(x=45.0, y=611.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(45.0, 573.0, anchor="nw", text="Responsable del retiro", fill="#000000", font=("Inter Medium", 24 * -1))

        self.lugar_var2 = StringVar(self.master)
        self.lugar_var2.set("ESCUELA DE FORMACION TECNICA LABORAL")  # Valor por defecto
        self.lugar_destino = OptionMenu(self.master, self.lugar_var2, "ESCUELA DE FORMACION TECNICA LABORAL", "ESCUELA AGRARIA", "OTRO")
        self.lugar_destino.place(x=45.0,y=504.0,width=607.0,height=58.0)

        canvas.create_text(45.0,466.0,anchor="nw",text="Lugar de destino",fill="#000000",font=("Inter Medium", 24 * -1))

        self.desplegable_variable = StringVar(self.master)
        self.desplegable_variable.set("Préstamo") #Valor por defecto

        desplegable = OptionMenu(self.master, self.desplegable_variable, "Préstamo", "Traspaso")
        desplegable.place( x=45.0, y=397.0, width=607.6497192382812, height=59.03461837768555)

        canvas.create_text( 45.0, 359.0, anchor="nw", text="Tipo de egreso", fill="#000000", font=("Inter Medium", 24 * -1))

        self.entry_10 = DateEntry(self.master, date_pattern='yyyy-MM-dd', width=12, background="#2B2626", foreground="white", borderwidth=2)
        self.entry_10.pack(padx=40, pady=40)
        self.entry_10.place( x=45.0, y=291.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text( 45.0, 253.0, anchor="nw", text="Fecha de egreso", fill="#000000", font=("Inter Medium", 24 * -1))

        self.entry_11 = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.entry_11.insert(0, selected_product)
        self.entry_11.place( x=45.0, y=184.0, width=607.0, height=58.0)

        canvas.create_text( 45.0, 146.0, anchor="nw", text="Producto", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_rectangle( 0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        canvas.create_text( 493.0, 47.0, anchor="nw", text="REGISTRAR PRÉSTAMO ", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))

        canvas.pack()

    def registrar_prestamo(self, funcion, conn):
        comentario = self.comentario.get("1.0", tk.END).strip()
        responsable_dev = self.resp_devolucion.get().strip().title()
        lugar_origen = self.lugar_var.get()
        motivo = self.motivo.get().strip()
        #fecha_dev = self.entry_5.get_date()
        cant_egresada = self.cantidad_egresada.get().strip()
        responsable_recep = self.responsable_recepcion.get().strip().title()
        responsable_retiro = self.entry_8.get().strip().title()
        lugar_destino = self.lugar_var2.get()
        tipo_egreso = self.desplegable_variable.get()
        fecha_egreso = self.entry_10.get_date()
        producto = self.entry_11.get().strip().capitalize()

        if not es_entero(cant_egresada):
            messagebox.showerror("Error.", "Ingrese un valor numérico valido en cantidad egresada.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""SELECT Cantidad_existente FROM stock WHERE Producto = ?""", (producto, ))
        except sqlite3.Error as e:
            messagebox.showerror("Error.", f"Error al registrar producto: {e}")  # Manejo de otros errores
        finally:
            cantidad_existente = cursor.fetchone()
            if cantidad_existente:
                cantidad_existente = cantidad_existente[0]
        
        if int(cant_egresada) > int(cantidad_existente):
            messagebox.showerror("Error.", f"La cantidad prestada no puede ser mayor a la cantidad existente.")
            return
        
        if cantidad_existente == 0:
            messagebox.showerror("Error.", f"No posee existencias disponibles.")
            return

        try:
            cursor = conn.cursor()  # Crear el cursor aquí
            # Inserción en la base de datos
            cursor.execute("""
                INSERT INTO Movimientos (fecha_egreso, tipo_egreso, Lugar_origen, Lugar_destino, responsable_retiro, cantidad_egresada, fecha_devolucion, cantidad_devuelta, Responsable_devolucion, Responsable_recepcion, Motivo, Comentario, Inventariado, Producto, Nro_inventariado, definitivo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (fecha_egreso, tipo_egreso, lugar_origen, lugar_destino, responsable_retiro, cant_egresada, "N/A", "0", responsable_dev, responsable_recep, motivo, comentario, "NO", producto, "N/A", "N/A"))

            if tipo_egreso != "Traspaso":
                cursor.execute("""UPDATE stock 
                            SET Cantidad_migrada = Cantidad_migrada + ?,
                            Cantidad_existente = Cantidad_existente - ?
                            WHERE Producto = ?""", (cant_egresada, cant_egresada, producto))
            else:
                cursor.execute("""UPDATE stock
                               SET Cantidad_existente = Cantidad_existente - ?
                               WHERE Producto = ?""", (cant_egresada, producto))

            print("Producto registrado exitosamente.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error.", "El producto ya existe o hay un problema de integridad.")
        except sqlite3.Error as e:
            messagebox.showerror("Error.", f"Error al registrar producto: {e}")  # Manejo de otros errores
        finally:

            conn.commit()
            cursor.close()  # Cerrar el cursor después de usarlo
        
        funcion()


class RegistrarPrestamoPT2:
    def __init__(self, root, cambiar_a_prestamo_1, cambiar_a_menuInv):
        self.popup = tk.Toplevel(root)
        self.popup.geometry("773x245")
        self.popup.config(bg="#6B5E5E")
        self.popup.grab_set()

        canvas = Canvas(self.popup, bg = "#6B5E5E", height = 245, width = 773, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)


        boton_cancelar = Button(self.popup,  text="No",  bg="#FFA500",  fg="black",  bd=2,  font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_menuInv), relief="flat")
        boton_cancelar.place(x=426.63671875, y=131.0, width=264.0133361816406, height=61.48335266113281)


        boton_confirmar = Button(self.popup, text="Sí", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_prestamo_1), relief="flat")
        boton_confirmar.place(x=83.0, y=131.0, width=264.0133361816406, height=61.48335266113281)

        canvas.create_rectangle(0.0, 0.0, 773.0, 92.0, fill="#2B2626", outline="")

        canvas.create_text(190.0, 31.0, anchor="nw", text="¿Desea registrar otro préstamo?", fill="#FFFFFF", font=("Inter Medium", 24 * -1))

        canvas.pack()
    
    def cerrar_y_ejecutar(self, funcion):
        self.popup.destroy()  # Cierra la ventana emergente
        funcion() #Ejecuta la funcion dada

class TraspasoDefinitivo_0:
    def __init__(self, master, cambiar_a_traspaso_1, cambiar_a_menuInv, conn):
        self.master = master
        canvas = Canvas(self.master, bg="#6B5E5E", height=768, width=1366, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        boton_cancelar = Button(self.master, text="Cancelar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_menuInv, relief="flat") 
        boton_cancelar.place(x=735.11181640625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        boton_seleccionar = Button(self.master, text="Seleccionar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda:self.mostrar_traspaso(cambiar_a_traspaso_1), relief="flat") 
        boton_seleccionar.place(x=391.47509765625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        canvas.create_rectangle(38.0, 279.0, 1328.0, 641.0, fill="#FFFFFF", outline="")

        # Variable para el menú desplegable
        selected_product_type = StringVar(master)
        selected_product_type.set("Herramienta")  # Valor inicial

        # Menú desplegable
        product_type_menu = OptionMenu(master, selected_product_type, "Herramienta", "Maquinaria", "Insumo", "Limpieza")
        product_type_menu.place(x=38.0, y=201.0, width=607.6497192382812, height=59.03461837768555)

        nombre_del_producto = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1 ))
        nombre_del_producto.place(x=720.0, y=198.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(720.0, 150.0, anchor="nw", text="Nombre del producto", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        canvas.create_text(483.0, 47.0, anchor="nw", text="VISUALIZAR PRODUCTO", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))

        self.tree = mostrar_tree_inventario(canvas, nombre_del_producto, selected_product_type, conn)

        canvas.pack()

    def mostrar_traspaso(self, cambiar_a_traspaso_1):
        # Llamar a la clase BajaDM2 y pasarle el producto seleccionado
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_product = self.tree.item(selected_item, "values")[1]  # Guardar el producto seleccionado
            self.nro_inventariado = self.tree.item(selected_item, "values")[6]
            cambiar_a_traspaso_1(self.selected_product, self.nro_inventariado)  # Pasar el producto a BajaDM2

class TraspasoDefinitivo_1:
    def __init__(self, master, cambiar_a_traspaso_2, cambiar_a_menuInv, primary_key, nro_ivent, conn):
        self.master = master

        canvas = Canvas(self.master, bg = "#6B5E5E", height = 768, width = 1366, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)

        boton_cancelar = Button(self.master, text="Cancelar",  bg="#FFA500",  fg="black",  bd=2,  font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_menuInv, relief="flat")
        boton_cancelar.place(x=735.1123046875, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)


        boton_registrar = Button(self.master, text="Registrar", bg="#FFA500", fg="black", bd=2,  font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda:self.registrar_traspaso(cambiar_a_traspaso_2, primary_key, conn), relief="flat")
        boton_registrar.place(x=391.474609375, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        self.entry_comentario = Text(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.entry_comentario.place(x=707.0, y=551.0, width=607.6497192382812, height=57.0)

        canvas.create_text(707.0, 513.0, anchor="nw", text="Comentario (Completar SOLO si lugar destino es OTRO)", fill="#000000", font=("Inter Medium", 24 * -1))

        self.nro_inventariado = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.nro_inventariado.place(x=39.0, y=551.0, width=607.6497192382812, height=57.03461837768555)
        self.nro_inventariado.insert(0, nro_ivent)
        canvas.create_text(38.0, 513.0, anchor="nw", text="Nro. Inventariado", fill="#000000", font=("Inter Medium", 24 * -1))

        self.entry_responsable_retiro = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.entry_responsable_retiro.place(x=707.0, y=438.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(707.0, 400.0, anchor="nw", text="Responsable de retiro", fill="#000000", font=("Inter Medium", 24 * -1))

        self.entry_responsable_reception = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.entry_responsable_reception.place(x=707.0, y=323.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(707.0, 285.0, anchor="nw", text="Responsable de recepcion", fill="#000000", font=("Inter Medium", 24 * -1))

        self.lugar_var = StringVar(master)
        self.lugar_var.set("ESCUELA DE FORMACION TECNICA LABORAL")  # Valor predeterminado

        self.entry_destino = OptionMenu(master, self.lugar_var, "ESCUELA DE FORMACION TECNICA LABORAL", "ESCUELA AGRARIA", "OTRO")
        self.entry_destino.place(x=707.0, y=210.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(707.0, 166.0, anchor="nw", text="Lugar de destino", fill="#000000", font=("Inter Medium", 24 * -1))

        self.entry_cantidad = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.entry_cantidad.place(x=39.0, y=438.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(39.0, 399.0, anchor="nw", text="Cantidad traspasada", fill="#000000", font=("Inter Medium", 24 * -1))

        self.entry_fecha_traspaso = DateEntry(self.master, date_pattern='yyyy-MM-dd', width=12, background="#2B2626", foreground="white", borderwidth=2)
        self.entry_fecha_traspaso.pack(padx=40, pady=40)
        self.entry_fecha_traspaso.place(x=39.0, y=324.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(59.953125, 338.24969482421875, anchor="nw", text="DD/MM/AAAA", fill="#000000", font=("Inter", 24 * -1))

        canvas.create_text(39.0, 285.0, anchor="nw", text="Fecha de traspaso", fill="#000000", font=("Inter Medium", 24 * -1))

        self.entry_producto = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.entry_producto.place(x=39.0, y=210.0, width=607.0, height=58.0)

        self.entry_producto.insert(1, primary_key)

        canvas.create_text(39.0, 166.0, anchor="nw", text="Producto", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        canvas.create_text(493.0, 47.0, anchor="nw", text="TRASPASO DEFINITIVO", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))

        canvas.pack()

    def registrar_traspaso(self, funcion, primary_key, conn):
        comentario = self.entry_comentario.get("1.0", tk.END).strip().capitalize()
        responsable_retiro = self.entry_responsable_retiro.get().strip().title()
        responsable_recepcion = self.entry_responsable_reception.get().strip().title()
        lugar_destino = self.lugar_var.get()
        cantidad = self.entry_cantidad.get().strip()
        fecha_traspaso = self.entry_fecha_traspaso.get_date()
        producto = self.entry_producto.get().strip().capitalize()
        nro_invent = self.nro_inventariado.get().strip().upper()

        if not es_entero(cantidad):
            messagebox.showerror("Error.", "Ingrese un valor numérico valido en.")
            return
        
        try:
            cursor = conn.cursor()
            cursor.execute("""SELECT Cantidad_existente FROM stock WHERE Producto = ?""", (producto, ))
        except sqlite3.Error as e:
            messagebox.showerror("Error.", f"Error al registrar producto: {e}")  # Manejo de otros errores
        finally:
            cantidad_existente = cursor.fetchone()
            if cantidad_existente:
                cantidad_existente = cantidad_existente[0]
        
        if int(cantidad) > int(cantidad_existente):
            messagebox.showerror("Error.", f"La cantidad prestada no puede ser mayor a la cantidad existente.")
            return


        if cantidad_existente == 0:
            messagebox.showerror("Error.", f"No posee existencias disponibles.")
            return

        if lugar_destino == "OTRO":
            lugar_destino = comentario

        try:
            cursor = conn.cursor()
            cursor.execute("""SELECT Lugar_guarda FROM stock WHERE Producto = ?""",(producto,))
            lugar_origen = cursor.fetchone()
            if lugar_origen:
                lugar_origen = lugar_origen[0]
            #INVENTARIADO

            # Inserción en la base de datos
            cursor.execute("""
                            INSERT INTO Movimientos (fecha_egreso, tipo_egreso, Lugar_origen, Lugar_destino, responsable_retiro, cantidad_egresada, fecha_devolucion, cantidad_devuelta, Responsable_devolucion, Responsable_recepcion, Motivo, Comentario, Inventariado, Producto, Nro_inventariado, definitivo)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (fecha_traspaso, "Traspaso Definitivo", lugar_origen, lugar_destino, responsable_retiro, cantidad, fecha_traspaso, "N/A", "N/A",responsable_recepcion, "Traspaso Definitivo", comentario, nro_invent, producto, nro_invent, "X"))

            cursor.execute("""UPDATE stock
                           SET Cantidad_existente = Cantidad_existente - ?,
                           Cantidad_migrada = Cantidad_migrada + ?
                           WHERE Producto = ?""", (cantidad, cantidad, producto))

            cursor.execute("""DELETE FROM Inventariados WHERE Producto = ? AND Nro_inventario = ?""", (producto, nro_invent))
            

            print("Producto registrado exitosamente.")
        except sqlite3.IntegrityError:
            
            messagebox.showerror("Error.", "El producto ya existe o hay un problema de integridad.")
        except sqlite3.Error as e:
            messagebox.showerror("Error.", f"Error al registrar producto: {e}") # Manejo de otros errores
        finally:
            
            conn.commit()
            cursor.close()  # Cerrar el cursor después de usarlo
        
        funcion()

class TraspasoDefinitivoPT2:
    def __init__(self, root, cambiar_a_traspaso_1, cambiar_a_menuInv):
        self.popup = tk.Toplevel(root)
        self.popup.geometry("773x245")
        self.popup.config(bg="#6B5E5E")
        self.popup.grab_set()
        self.popup.resizable(False, False)

        canvas = Canvas(self.popup, bg = "#6B5E5E", height = 245, width = 773, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)


        boton_cancelar = Button(self.popup,  text="No",  bg="#FFA500",  fg="black",  bd=2,  font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_menuInv), relief="flat")
        boton_cancelar.place(x=426.63671875, y=131.0, width=264.0133361816406, height=61.48335266113281)


        boton_confirmar = Button(self.popup,  text="Sí",  bg="#FFA500",  fg="black",  bd=2,  font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_traspaso_1), relief="flat")
        boton_confirmar.place(x=83.0, y=131.0, width=264.0133361816406, height=61.48335266113281)

        canvas.create_rectangle(0.0, 0.0, 773.0, 92.0, fill="#2B2626", outline="")

        canvas.create_text(190.0, 31.0, anchor="nw", text="¿Desea registrar otro traspaso?", fill="#FFFFFF", font=("Inter Medium", 24 * -1))

        canvas.pack()

    def cerrar_y_ejecutar(self, funcion):
        self.popup.destroy()  # Cierra la ventana emergente
        funcion() #Ejecuta la funcion dada

class CancelarMovimiento1():
    def __init__(self, master, cambiar_a_cancelar2, cambiar_a_menuInv, primary_key, conn):
        self.master = master
        canvas = Canvas(self.master, bg = "#6B5E5E", height = 768, width = 1366, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)

        boton_cancelar = Button(self.master, text="Cancelar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_menuInv, relief="flat") 
        boton_cancelar.place(x=735.11181640625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        boton_eliminar = Button(self.master, text="Eliminar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda:self.cambiar_pantalla(cambiar_a_cancelar2, primary_key), relief="flat") 
        boton_eliminar.place(x=391.47509765625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        canvas.create_rectangle(38.0, 197.0, 1328.0, 641.0, fill="#FFFFFF", outline="")

        canvas.create_text(38.0, 155.0, anchor="nw", text="Producto seleccionado", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        canvas.create_text(541.0, 47.0, anchor="nw", text="CANCELAR MOVIMIENTO", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))
        
        self.tree = ttk.Treeview(canvas, columns=("ID movimiento", "Fecha egreso", "Tipo egreso", "Lugar origen", 
                                          "Lugar destino", "Responsable retiro", "cantidad egresada", 
                                          "Fecha devolucion", "Cantidad devuelta", "Responsable devolucion", 
                                          "Responsable recepcion", "Motivo", "Comentario", 
                                          "Inventariado", "Producto", "Nro.inventariado", "Definitivo"), show='headings')
        
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)  # Establecer encabezados
            self.tree.column(col, anchor="center")  # Alinear columnas al centro
        
        self.scrollbar_v = ttk.Scrollbar(canvas, orient="vertical", command=self.tree.yview)
        self.scrollbar_h = ttk.Scrollbar(canvas, orient="horizontal", command=self.tree.xview)
     
        self.tree.configure(yscrollcommand=self.scrollbar_v.set, xscrollcommand=self.scrollbar_h.set)
        
        # Colocar el Treeview en el canvas
        self.tree.place(x=38.0, y=197.0, width=1275.0, height=444.0)
        self.scrollbar_v.place(x=1310.0, y=197.0, height=444.0)  # Coloca la scrollbar vertical al lado derecho
        self.scrollbar_h.place(x=39.0, y=628.0, width=1289.0)
        
        cursor = conn.cursor()

        # Consultar y mostrar detalles del producto seleccionado
        cursor.execute("SELECT * FROM Movimientos WHERE Id_movimiento = ?", (primary_key,))
        product_details = cursor.fetchone()

        if product_details:
            self.tree.insert("", "end", values=product_details)
        
        canvas.pack()
    
    def cambiar_pantalla(self, cambiar_a_cancelar2, primary_key):
        cambiar_a_cancelar2(primary_key)

class CancelarMovimiento2():
    def __init__(self, root, cambiar_a_confirmacion, cambiar_a_menuInv, primary_key, conn):
        self.popup = tk.Toplevel(root)
        self.popup.geometry("773x245")
        self.popup.config(bg="#6B5E5E")
        self.popup.grab_set()
        self.popup.resizable(False, False)

        canvas = Canvas(self.popup, bg = "#6B5E5E", height = 245, width = 773, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)

        boton_cancelar = Button(self.popup,  text="No",  bg="#FFA500",  fg="black",  bd=2,  font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_menuInv, relief="flat")
        boton_cancelar.place(x=426.63671875, y=131.0, width=264.0133361816406, height=61.48335266113281)

        boton_confirmar = Button(self.popup,  text="Sí",  bg="#FFA500",  fg="black",  bd=2,  font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_confirmacion, primary_key, conn), relief="flat")
        boton_confirmar.place(x=83.0, y=131.0, width=264.0133361816406, height=61.48335266113281)

        canvas.create_rectangle(0.0, 0.0, 773.0, 92.0, fill="#2B2626", outline="")

        canvas.create_text(190.0, 31.0, anchor="nw", text="¿Desea elimiar este producto?", fill="#FFFFFF", font=("Inter Medium", 24 * -1))

        canvas.pack()

    def cerrar_y_ejecutar(self, funcion, primary_key, conn):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                            DELETE FROM Movimientos
                           WHERE id_movimiento = ?
                            """,(primary_key,))
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error.", "El producto no existe.")
        except sqlite3.Error as e:
            messagebox.showerror("Error.", f"Error al registrar producto: {e}")  # Manejo de otros errores
        finally:
                conn.commit()
                cursor.close()  # Cerrar el cursor después de usarlo       
        
        self.popup.destroy()  # Cierra la ventana emergente
        
        funcion() #Ejecuta la funcion dada


class PrestamoIventariado_1():
    def __init__(self, master, cambiar_a_prestamo_inventariado_2, cambiar_a_menuPrestamo, conn):
        self.master = master
        canvas = Canvas(self.master, bg="#6B5E5E", height=768, width=1366, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        boton_cancelar = Button(self.master, text="Cancelar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_menuPrestamo, relief="flat") 
        boton_cancelar.place(x=735.11181640625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        boton_seleccionar = Button(self.master, text="Seleccionar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda:self.mostrar_traspaso(cambiar_a_prestamo_inventariado_2), relief="flat") 
        boton_seleccionar.place(x=391.47509765625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        canvas.create_rectangle(38.0, 279.0, 1328.0, 641.0, fill="#FFFFFF", outline="")

        # Variable para el menú desplegable
        selected_product_type = StringVar(master)
        selected_product_type.set("Herramienta")  # Valor inicial

        # Menú desplegable
        product_type_menu = OptionMenu(master, selected_product_type, "Herramienta", "Maquinaria", "Insumo", "Limpieza")
        product_type_menu.place(x=38.0, y=201.0, width=607.6497192382812, height=59.03461837768555)

        nombre_del_producto = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1 ))
        nombre_del_producto.place(x=720.0, y=198.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(720.0, 150.0, anchor="nw", text="Nombre del producto", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        canvas.create_text(483.0, 47.0, anchor="nw", text="VISUALIZAR PRODUCTO", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))

        self.tree = mostrar_tree_inventario(canvas, nombre_del_producto, selected_product_type, conn)

        canvas.pack()

    def mostrar_traspaso(self, cambiar_a_prestamo_inventariado_2):
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_product = self.tree.item(selected_item, "values")[1]
            self.nro_inventariado = self.tree.item(selected_item, "values")[6]
            cambiar_a_prestamo_inventariado_2(self.selected_product, self.nro_inventariado)

class PrestamoInventariado2:
    def __init__(self, master, cambiar_a_listo, cambiar_a_menu_prestamo, conn, selected_product, nro_inventariado):
        self.master = master

        canvas = Canvas(self.master, bg = "#6B5E5E", height = 916, width = 1366, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)

        boton_cancelar = Button(self.master, text="Cancelar", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command= cambiar_a_menu_prestamo, relief="flat")
        boton_cancelar.place(x=746.6368408203125, y=822.0, width=264.0133361816406, height=61.48335266113281)

        boton_registrar = Button(self.master, text="Registrar", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.registrar_prestamo(cambiar_a_listo, conn, nro_inventariado), relief="flat")
        boton_registrar.place(x=403.0, y=822.0, width=264.0133361816406, height=61.48335266113281)

        self.comentario = Text(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.comentario.place(x=714.0, y=611.0, width=607.6497192382812, height=57.03461837768555)
        canvas.create_text(714.0, 572.0, anchor="nw", text="Comentario", fill="#000000", font=("Inter Medium", 24 * -1))

        self.resp_devolucion = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.resp_devolucion.place(x=714.0, y=504.0, width=607.6497192382812, height=57.03461837768555)
        canvas.create_text(714.0, 466.0, anchor="nw", text="Responsable de devolución", fill="#000000", font=("Inter Medium", 24 * -1))

        self.lugar_var = StringVar(self.master)
        self.lugar_var.set("ESCUELA DE FORMACION TECNICA LABORAL")  # Valor por defecto
        self.lugar_origen = OptionMenu(self.master, self.lugar_var, "ESCUELA DE FORMACION TECNICA LABORAL", "ESCUELA AGRARIA", "OTRO")
        self.lugar_origen.place(x=714.0, y=396.0, width=607.6497192382812, height=57.03461837768555)
        canvas.create_text(714.0, 358.0, anchor="nw", text="Lugar de origen", fill="#000000", font=("Inter Medium", 24 * -1 ))

        self.motivo = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.motivo.place(x=714.0, y=290.0, width=607.6497192382812, height=57.03461837768555)
        canvas.create_text(714.0, 252.0, anchor="nw", text="Motivo", fill="#000000", font=("Inter Medium", 24 * -1))

        self.cantidad_egresada = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.cantidad_egresada.place(x=714.0, y=184.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(714.0, 146.0, anchor="nw", text="Cantidad egresada", fill="#000000", font=("Inter Medium", 24 * -1))

        self.responsable_recepcion = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.responsable_recepcion.place(x=45.0, y=717.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(45.0, 679.0, anchor="nw", text="Responsable recepción", fill="#000000", font=("Inter Medium", 24 * -1))

        self.entry_8 = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.entry_8.place(x=45.0, y=611.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(45.0, 573.0, anchor="nw", text="Responsable del retiro", fill="#000000", font=("Inter Medium", 24 * -1))

        self.lugar_var2 = StringVar(self.master)
        self.lugar_var2.set("ESCUELA DE FORMACION TECNICA LABORAL")  # Valor por defecto
        self.lugar_destino = OptionMenu(self.master, self.lugar_var2, "ESCUELA DE FORMACION TECNICA LABORAL", "ESCUELA AGRARIA", "OTRO")
        self.lugar_destino.place(x=45.0,y=504.0,width=607.0,height=58.0)

        canvas.create_text(45.0,466.0,anchor="nw",text="Lugar de destino",fill="#000000",font=("Inter Medium", 24 * -1))

        self.desplegable_variable = StringVar(self.master)
        self.desplegable_variable.set("Préstamo") #Valor por defecto

        desplegable = OptionMenu(self.master, self.desplegable_variable, "Préstamo", "Traspaso")
        desplegable.place( x=45.0, y=397.0, width=607.6497192382812, height=59.03461837768555)

        canvas.create_text( 45.0, 359.0, anchor="nw", text="Tipo de egreso", fill="#000000", font=("Inter Medium", 24 * -1))

        self.entry_10 = DateEntry(self.master, date_pattern='yyyy-MM-dd', width=12, background="#2B2626", foreground="white", borderwidth=2)
        self.entry_10.pack(padx=40, pady=40)
        self.entry_10.place( x=45.0, y=291.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text( 45.0, 253.0, anchor="nw", text="Fecha de egreso", fill="#000000", font=("Inter Medium", 24 * -1))

        self.entry_11 = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.entry_11.insert(0, selected_product)
        self.entry_11.place( x=45.0, y=184.0, width=607.0, height=58.0)

        canvas.create_text( 45.0, 146.0, anchor="nw", text="Producto", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_rectangle( 0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        canvas.create_text( 493.0, 47.0, anchor="nw", text="REGISTRAR PRÉSTAMO ", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))

        canvas.pack()

    def registrar_prestamo(self, funcion, conn, nro_inventariado):
        comentario = self.comentario.get("1.0", tk.END).strip()
        responsable_dev = self.resp_devolucion.get().strip().title()
        lugar_origen = self.lugar_var.get()
        motivo = self.motivo.get().strip()
        cant_egresada = self.cantidad_egresada.get().strip()
        responsable_recep = self.responsable_recepcion.get().strip().title()
        responsable_retiro = self.entry_8.get().strip().title()
        lugar_destino = self.lugar_var2.get()
        tipo_egreso = self.desplegable_variable.get()
        fecha_egreso = self.entry_10.get_date()
        producto = self.entry_11.get().strip().capitalize()

        if not es_entero(cant_egresada):
            messagebox.showerror("Error.", "Ingrese un valor numérico valido en cantidad egresada.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""SELECT Cantidad_existente FROM stock WHERE Producto = ?""", (producto, ))
        except sqlite3.Error as e:
            messagebox.showerror("Error.", f"Error al registrar producto: {e}")  # Manejo de otros errores
        finally:
            cantidad_existente = cursor.fetchone()
            if cantidad_existente:
                cantidad_existente = cantidad_existente[0]
        
        if int(cant_egresada) > int(cantidad_existente):
            messagebox.showerror("Error.", f"La cantidad prestada no puede ser mayor a la cantidad existente.")
            return
        
        if cantidad_existente == 0:
            messagebox.showerror("Error.", f"No posee existencias disponibles.")
            return

        try:
            cursor = conn.cursor()  # Crear el cursor aquí
            # Inserción en la base de datos
            cursor.execute("""
                INSERT INTO Movimientos (fecha_egreso, tipo_egreso, Lugar_origen, Lugar_destino, responsable_retiro, cantidad_egresada, fecha_devolucion, cantidad_devuelta, Responsable_devolucion, Responsable_recepcion, Motivo, Comentario, Inventariado, Producto, Nro_inventariado, definitivo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (fecha_egreso, tipo_egreso, lugar_origen, lugar_destino, responsable_retiro, cant_egresada, "N/A", "0", responsable_dev, responsable_recep, motivo, comentario, "SI", producto, nro_inventariado, "N/A"))

            if tipo_egreso != "Traspaso":
                cursor.execute("""UPDATE stock 
                            SET Cantidad_migrada = Cantidad_migrada + ?,
                            Cantidad_existente = Cantidad_existente - ?
                            WHERE Producto = ?""", (cant_egresada, cant_egresada, producto))
            else:
                cursor.execute("""UPDATE stock
                               SET Cantidad_existente = Cantidad_existente - ?
                               WHERE Producto = ?""", (cant_egresada, producto))

            print("Producto registrado exitosamente.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error.", "El producto ya existe o hay un problema de integridad.")
        except sqlite3.Error as e:
            messagebox.showerror("Error.", f"Error al registrar producto: {e}")  # Manejo de otros errores
        finally:

            conn.commit()
            cursor.close()  # Cerrar el cursor después de usarlo
        
        funcion()