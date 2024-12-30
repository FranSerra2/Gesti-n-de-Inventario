import tkinter as tk
from tkinter import Tk, Canvas, Entry, Text, Button, StringVar, OptionMenu, messagebox
import sqlite3
from tkcalendar import DateEntry
from funciones import obtener_datos3

def es_entero(dato):
    return dato.isdigit()

class ModificarMovimiento:
    def __init__(self, master, cambiar_a_modificar_mov_2, cambiar_a_buscar_mov_1, id_movimiento, conn):
        self.master = master
        lista = obtener_datos3(id_movimiento, conn)
        canvas = Canvas(self.master, bg = "#6B5E5E", height = 916, width = 1366, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)


        boton_cancelar = Button(self.master, text="Cancelar",  bg="#FFA500",  fg="black",  bd=2,  font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_buscar_mov_1, relief="flat")
        boton_cancelar.place(x=746.63671875, y=822.0, width=264.0133361816406, height=61.48335266113281)

        boton_modificar = Button(self.master, text="Confirmar", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.registrar_modificacion(cambiar_a_modificar_mov_2, conn, id_movimiento), relief="flat")
        boton_modificar.place(x=403.0, y=822.0, width=264.0133361816406, height=61.48335266113281)


        self.entry_comentario = Text(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.entry_comentario.insert("1.0", lista[12])
        self.entry_comentario.place(x=714.0, y=716.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(714.0, 678.0, anchor="nw", text="Comentario", fill="#000000", font=("Inter Medium", 24 * -1))


        self.entry_responsable_devolucion = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.entry_responsable_devolucion.insert(0, lista[9])
        self.entry_responsable_devolucion.place(x=714.0, y=611.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(714.0, 572.0, anchor="nw", text="Responsable de devolución", fill="#000000", font=("Inter Medium", 24 * -1))


        self.lugar_var = StringVar(self.master)
        self.lugar_var.set(lista[3])  # Valor por defecto
        self.lugar_origen = OptionMenu(self.master, self.lugar_var, "ESCUELA DE FORMACION TECNICA LABORAL", "ESCUELA AGRARIA", "OTRO")
        self.lugar_origen.place(x=714.0, y=504.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(714.0, 466.0, anchor="nw", text="Lugar de origen", fill="#000000", font=("Inter Medium", 24 * -1))

        self.entry_motivo = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.entry_motivo.insert(0, lista[11])
        self.entry_motivo.place(x=714.0, y=396.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(714.0, 358.0, anchor="nw", text="Motivo", fill="#000000", font=("Inter Medium", 24 * -1))

        self.entry_fecha_devolucion = DateEntry(self.master, date_pattern='yyyy-MM-dd', width=12, background="#2B2626", foreground="white", borderwidth=2)
        self.entry_fecha_devolucion.set_date(lista[7])
        self.entry_fecha_devolucion.pack(padx=40, pady=40)
        self.entry_fecha_devolucion.place(x=714.0, y=290.0, width=607.6497192382812, height=57.0346183776855)

        canvas.create_text(735.0, 305.0, anchor="nw", text="DD/MM/AAAA", fill="#000000", font=("Inter", 24 * -1))

        canvas.create_text(714.0, 252.0, anchor="nw", text="Fecha devolución", fill="#000000", font=("Inter Medium", 24 * -1))

        self.entry_cantidad_egresada = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.entry_cantidad_egresada.insert(0, lista[6])
        self.entry_cantidad_egresada.place(x=714.0, y=184.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(714.0, 146.0, anchor="nw", text="Cantidad egresada", fill="#000000", font=("Inter Medium", 24 * -1))

        self.responsable_recepcion = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.responsable_recepcion.insert(0, lista[10])
        self.responsable_recepcion.place(x=45.0, y=717.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(45.0, 679.0, anchor="nw", text="Responsable recepción", fill="#000000", font=("Inter Medium", 24 * -1))

        self.entry_responsable_retiro = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.entry_responsable_retiro.insert(0, lista[5])
        self.entry_responsable_retiro.place(x=45.0, y=611.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(45.0, 573.0, anchor="nw", text="Responsable del retiro", fill="#000000", font=("Inter Medium", 24 * -1))

        self.lugar_var2 = StringVar(self.master)
        self.lugar_var2.set(lista[4])  # Valor por defecto
        self.lugar_destino = OptionMenu(self.master, self.lugar_var2, "ESCUELA DE FORMACION TECNICA LABORAL", "ESCUELA AGRARIA", "OTRO")
        self.lugar_destino.place(x=45.0, y=504.0, width=607.0, height=58.0)

        canvas.create_text(45.0, 466.0, anchor="nw", text="Lugar de destino", fill="#000000", font=("Inter Medium", 24 * -1))

        
        self.desplegable_variable = StringVar(self.master)
        self.desplegable_variable.set(lista[2]) #Valor por defecto

        desplegable = OptionMenu(self.master, self.desplegable_variable, "Préstamo", "Traspaso")
        desplegable.place(x=45.0, y=397.0, width=607.6497192382812, height=59.03461837768555)

        canvas.create_text(45.0,359.0,anchor="nw",text="Tipo de egreso",fill="#000000",font=("Inter Medium", 24 * -1))

        self.entry_fecha_egreso = DateEntry(self.master, date_pattern='yyyy-MM-dd', width=12, background="#2B2626", foreground="white", borderwidth=2)
        self.entry_fecha_egreso.set_date(lista[1])
        self.entry_fecha_egreso.pack(padx=40, pady=40)
        self.entry_fecha_egreso.place(x=45.0,y=291.0,width=607.6497192382812,height=57.03461837768555)

        canvas.create_text(65.95361328125, 305.24969482421875, anchor="nw", text="DD/MM/AAAA", fill="#000000", font=("Inter", 24 * -1))

        canvas.create_text(45.0, 253.0, anchor="nw", text="Fecha de egreso", fill="#000000", font=("Inter Medium", 24 * -1))

        self.entry_producto = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.entry_producto.place(x=45.0, y=184.0, width=607.0, height=58.0)

        selected_product = self.obtener_producto(conn, id_movimiento)
        self.entry_producto.insert(0, selected_product)

        canvas.create_text(45.0, 146.0, anchor="nw", text="Producto", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        canvas.create_text(475.0, 47.0, anchor="nw", text="MODIFICAR MOVIMIENTO ", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))


        canvas.pack()

    def obtener_producto(self, conn, primary_key):
        try:
            cursor = conn.cursor()
            cursor.execute("""SELECT Producto FROM Movimientos WHERE id_movimiento = ?""", (primary_key,))
            selected_product = cursor.fetchone() 
        finally:
            cursor.close()

        if selected_product:
            return selected_product[0]
        else:
            return None

    def registrar_modificacion(self, funcion, conn, primary_key):
        comentario = self.entry_comentario.get("1.0", tk.END).strip().capitalize()
        responsable_dev = self.entry_responsable_devolucion.get().strip().title()
        lugar_origen = self.lugar_var.get()
        motivo = self.entry_motivo.get().strip().capitalize()
        fecha_dev = self.entry_fecha_devolucion.get_date()
        cant_egresada = self.entry_cantidad_egresada.get().strip()
        responsable_recep = self.responsable_recepcion.get().strip().title()
        responsable_retiro = self.entry_responsable_retiro.get().strip().title()
        lugar_destino = self.lugar_var2.get()
        tipo_egreso = self.desplegable_variable.get()
        fecha_egreso = self.entry_fecha_egreso.get_date()
        producto = self.entry_producto.get().strip()

        if not es_entero(cant_egresada):
            messagebox.showerror("Error.", "Ingrese un valor numérico valido en cantidad.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""SELECT Nro_inventariado FROM Movimientos WHERE id_movimiento = ?""",(primary_key,))
            nro_invent = cursor.fetchone()
        finally:
            cursor.close()

        if nro_invent:
            nro_invent = nro_invent[0]
            inventariado = "SI"
        else:
            nro_invent = None
            inventariado = "NO"

        try:
            cursor = conn.cursor()  # Crear el cursor aquí
            # Inserción en la base de datos
            cursor.execute("""
                UPDATE   Movimientos 
                SET fecha_egreso = ?, 
                    tipo_egreso = ?, 
                    Lugar_origen = ?,
                    Lugar_destino = ?, 
                    responsable_retiro = ?, 
                    cantidad_egresada = ?, 
                    fecha_devolucion = ?, 
                    cantidad_devuelta = ?, 
                    Responsable_devolucion = ?, 
                    Responsable_recepcion = ?, 
                    Motivo = ?, 
                    Comentario = ?, 
                    Inventariado = ?, 
                    Producto = ?, 
                    Nro_inventariado = ?
                WHERE id_movimiento = ?
            """, (fecha_egreso, tipo_egreso, lugar_origen, lugar_destino, responsable_retiro, cant_egresada, fecha_dev, "0", responsable_dev, responsable_recep, motivo, comentario, inventariado, producto, nro_invent, primary_key))
            
            conn.commit()
            
            print("Producto registrado exitosamente.") #agregar mensajes en Label
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El producto ya existe o hay un problema de integridad.")
        except sqlite3.Error as e:
            messagebox.showerror("Error.", f"Error al registrar producto: {e}")  # Manejo de otros errores
        finally:
            conn.commit()
            cursor.close()  # Cerrar el cursor después de usarlo
        
        funcion()

class ModificarMovimientoPT4:
    def __init__(self, root, cambiar_a_buscar_mov_1, cambiar_a_menuInv):
        self.popup = tk.Toplevel(root)
        self.popup.geometry("773x245")
        self.popup.config(bg="#6B5E5E")
        self.popup.grab_set()
        self.popup.resizable(False, False)

        canvas = Canvas(self.popup, bg = "#6B5E5E", height = 245, width = 773, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)


        boton_cancelar = Button(self.popup, text="No", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_menuInv), relief="flat")
        boton_cancelar.place(x=426.63671875, y=131.0, width=264.0133361816406, height=61.48335266113281)


        boton_confirmar = Button(self.popup,  text="Sí",  bg="#FFA500",  fg="black",  bd=2,  font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_buscar_mov_1), relief="flat")
        boton_confirmar.place(x=83.0, y=131.0, width=264.0133361816406, height=61.48335266113281)

        canvas.create_rectangle(0.0, 0.0, 773.0, 92.0, fill="#2B2626", outline="")

        canvas.create_text(190.0, 31.0, anchor="nw", text="¿Desea buscar otro movimiento?", fill="#FFFFFF", font=("Inter Medium", 24 * -1))

        canvas.pack()

    def cerrar_y_ejecutar(self, funcion):
        self.popup.destroy()  # Cierra la ventana emergente
        funcion() #Ejecuta la funcion dada