import tkinter as tk
from tkinter import Tk, Canvas, Entry, Button, StringVar, OptionMenu, messagebox, ttk
from funciones import *

def es_entero(dato):
    return dato.isdigit()

class DisminuirPT1:
    def __init__(self, master, cambiar_a_disminuir_2, cambiar_a_menuInv, conn):
        self.master = master

        canvas = Canvas(self.master, bg = "#6B5E5E", height = 768, width = 1366, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)

        boton_cancelar = Button(self.master, text="Cancelar",  bg="#FFA500",  fg="black",  bd=2,  font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_menuInv, relief="flat")
        boton_cancelar.place(x=735.11181640625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        boton_seleccionar = Button(self.master,text="Seleccionar", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda:self.cambiar_pantalla(cambiar_a_disminuir_2), relief="flat")
        boton_seleccionar.place(x=391.47509765625, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        canvas.create_rectangle(38.0, 276.0, 1328.0, 638.0, fill="#FFFFFF", outline="")

        entry_nombre = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        entry_nombre.place(x=720.0, y=198.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(720.0, 150.0, anchor="nw", text="Nombre del producto", fill="#000000", font=("Inter Medium", 24 * -1))

        desplegable_variable = StringVar(self.master)
        desplegable_variable.set("Herramienta") #Valor por defecto

        desplegable = OptionMenu(self.master, desplegable_variable, "Herramienta", "Maquinaria", "Insumo", "Limpieza")
        desplegable.place(x=38.0, y=198.0, width=607.6497192382812, height=59.03461837768555)

        canvas.create_text(38.0, 150.0, anchor="nw", text="Seleccione tipo de producto", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        canvas.create_text(533.0, 47.0, anchor="nw", text="DISMINUIR STOCK", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))

        self.tree = mostrar_tree(canvas, entry_nombre, desplegable_variable, conn)
        
        canvas.pack()
    
    def cambiar_pantalla(self, cambiar_a_disminuir_2):
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_product = self.tree.item(selected_item, "values")[1]  # Guardar el producto seleccionado
            cambiar_a_disminuir_2(self.selected_product)

class DisminuirPT2:
    def __init__(self, master, cambiar_a_disminuir_3, cambiar_a_disminuir_1,  primary_key, conn):
        self.master = master

        canvas = Canvas(self.master, bg = "#6B5E5E", height = 768, width = 1366, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)

        boton_cancelar = Button(self.master, text="Cancelar",  bg="#FFA500",  fg="black",  bd=2,  font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=cambiar_a_disminuir_1, relief="flat")
        boton_cancelar.place(x=735.11181640625, y=665.5166015625, width=264.0133361816406, height=61.48335266113281)

        boton_confirmar = Button(self.master, text="Confirmar",  bg="#FFA500",  fg="black",  bd=2,  font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.registar_stock(cambiar_a_disminuir_3, conn, primary_key), relief="flat")
        boton_confirmar.place(x=391.47509765625, y=665.5166015625, width=264.0133361816406, height=61.48335266113281)

        self.desplegable_variable = StringVar(self.master)
        self.desplegable_variable.set("Consumo") #Valor por defecto

        self.desplegable = OptionMenu(self.master, self.desplegable_variable, "Consumo", "Desgaste", "Ruptura", "Pérdida")
        self.desplegable.place(x=720.0, y=497.0, width=607.6497192382812, height=59.03461837768555)

        canvas.create_text(720.0, 459.0, anchor="nw", text="Motivo", fill="#000000", font=("Inter Medium", 24 * -1))

        self.entry_cantidad = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.entry_cantidad.place(x=38.0, y=497.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(38.0, 459.0, anchor="nw", text="Cantidad a disminuir", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_rectangle(38.0, 197.0, 1328.0, 431.0, fill="#FFFFFF", outline="")

        canvas.create_text(38.0, 155.0, anchor="nw", text="Producto", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        canvas.create_text(533.0, 47.0, anchor="nw", text="DISMINUIR STOCK", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))

        self.tree = ttk.Treeview(canvas, columns=("Tipo producto", "Producto", "Cantidad existente", "Área", "Lugar guarda", "Cantidad migrada", "Observaciones", "Inventariado"), show='headings')
        
        # Definir las columnas
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)  # Establecer encabezados
            self.tree.column(col, anchor="center")  # Alinear columnas al centro
        
        self.scrollbar_v = ttk.Scrollbar(canvas, orient="vertical", command=self.tree.yview)
        self.scrollbar_h = ttk.Scrollbar(canvas, orient="horizontal", command=self.tree.xview)
     
        self.tree.configure(yscrollcommand=self.scrollbar_v.set, xscrollcommand=self.scrollbar_h.set)
        
        # Colocar el Treeview en el canvas
        self.tree.place(x=50.0, y=210.0, width=1250.0, height=200.0)
        self.scrollbar_v.place(x=1310.0, y=210.0, height=200.0)  # Coloca la scrollbar vertical al lado derecho
        self.scrollbar_h.place(x=39.0, y=410.0, width=1290.0)
        
        cursor = conn.cursor()

        # Consultar y mostrar detalles del producto seleccionado
        cursor.execute("SELECT * FROM stock WHERE Producto = ?", (primary_key,))
        product_details = cursor.fetchone()

        if product_details:
            self.tree.insert("", "end", values=product_details)

        canvas.pack()

    def registar_stock(self, funcion, conn, primary_key):
        cantidad = self.entry_cantidad.get().strip()
        motivo = self.desplegable_variable.get().strip()
        fecha = get_date()
        
        if not es_entero(cantidad):
            messagebox.showerror("Error.", "Ingrese un valor numérico valido en cantidad.")
            return
    
        try:
            cursor = conn.cursor()
            cursor.execute("""SELECT cantidad_existente FROM stock WHERE Producto = ?""", (primary_key,))
            existente = cursor.fetchone()
            if existente:
                existente = existente[0]
        except Exception as e:
            print(f"Error al actualizar el stock: {e}")
        finally:
            cursor.close()

        if (int(existente) - int(cantidad)) < 0:
            messagebox.showerror("Error", "El stock no puede ser menor a 0.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""UPDATE stock
                            SET cantidad_existente = cantidad_existente - ?
                            WHERE Producto = ?;
                            """, (cantidad, primary_key))

        except Exception as e:
            messagebox.showerror("Error.", f"Error al actualizar el stock: {e}")

        finally:
            conn.commit()
            cursor.close()
        
        try:
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO Movimientos (fecha_egreso, tipo_egreso, Lugar_origen, Lugar_destino, responsable_retiro, cantidad_egresada, fecha_devolucion, cantidad_devuelta, Responsable_devolucion, Responsable_recepcion, Motivo, Comentario, Inventariado, Producto, Nro_inventariado, definitivo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""", (fecha, "Disminución de stock", "N/A", "N/A", "N/A", cantidad, fecha, "N/A", "N/A", "N/A", motivo, "N/A", "N/A", primary_key, "N/A", "N/A"))
        except Exception as e:
            messagebox.showerror("Error.", f"Error al actualizar el stock: {e}")

        finally:
            conn.commit()
            cursor.close()

        funcion()

class DisminuirPT3:
    def __init__(self, root, cambiar_a_disminuir_4, cambiar_a_disminuir_1):
        self.popup = tk.Toplevel(root)
        self.popup.geometry("773x245")
        self.popup.config(bg="#6B5E5E")
        self.popup.grab_set()
        self.popup.resizable(False, False)

        canvas = Canvas(self.popup, bg = "#6B5E5E", height = 245, width = 773, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)

        boton_cancelar = Button(self.popup, text="Cancelar", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_disminuir_1), relief="flat")
        boton_cancelar.place(x=426.63671875, y=131.0, width=264.0133361816406, height=61.48335266113281)


        boton_confirmar = Button(self.popup, text="Confirmar",  bg="#FFA500",  fg="black",  bd=2,  font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_disminuir_4), relief="flat")
        boton_confirmar.place(x=83.0, y=131.0, width=264.0133361816406, height=61.48335266113281)

        canvas.create_rectangle(0.0, 0.0, 773.0, 92.0, fill="#2B2626", outline="")

        canvas.create_text(190.0, 31.0, anchor="nw", text="¿Desea mantener la modificación?", fill="#FFFFFF", font=("Inter Medium", 24 * -1))

        canvas.pack()


    def cerrar_y_ejecutar(self, funcion):
        self.popup.destroy()  # Cierra la ventana emergente
        funcion() #Ejecuta la funcion dada

class DisminuirPT4:
    def __init__(self, root, cambiar_a_disminuir_1, cambiar_a_menuInv):
        self.popup = tk.Toplevel(root)
        self.popup.geometry("773x245")
        self.popup.config(bg="#6B5E5E")
        self.popup.grab_set()
        self.popup.resizable(False, False)

        canvas = Canvas(self.popup, bg = "#6B5E5E", height = 245, width = 773, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)


        boton_cancelar = Button(self.popup,  text="No",  bg="#FFA500",  fg="black",  bd=2,  font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_menuInv), relief="flat")
        boton_cancelar.place(x=426.63671875, y=131.0, width=264.0133361816406, height=61.48335266113281)


        boton_confirmar = Button(self.popup, text="Sí", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_disminuir_1), relief="flat")
        boton_confirmar.place(x=83.0, y=131.0, width=264.0133361816406, height=61.48335266113281)

        canvas.create_rectangle(0.0, 0.0, 773.0, 92.0, fill="#2B2626", outline="")

        canvas.create_text(190.0, 31.0, anchor="nw", text="¿Desea disminuir stock de otro producto?", fill="#FFFFFF", font=("Inter Medium", 24 * -1))

        canvas.pack()


    def cerrar_y_ejecutar(self, funcion):
        self.popup.destroy()  # Cierra la ventana emergente
        funcion() #Ejecuta la funcion dada