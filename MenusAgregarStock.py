#Menus Agregar Stock
import tkinter as tk
from tkinter import Tk, Canvas, Entry, Button, StringVar, OptionMenu, messagebox
from funciones import *

def es_entero(dato):
    return dato.isdigit()

class AgregarStock:
    def __init__(self, master, cambiar_a_agregar_2, cambiar_a_menuInv, conn):
        self.master = master


        canvas = Canvas(self.master, bg = "#6B5E5E", height = 768, width = 1366, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)

        boton_cancelar = Button(self.master, text="Cancelar", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0,highlightthickness=0, command=cambiar_a_menuInv, relief="flat")
        boton_cancelar.place(x=735.11181640625, y=669.5166625976562, width=264.0133361816406, height=61.48335266113281)

        boton_seleccionar = Button(self.master,  text="Seleccionar",  bg="#FFA500",  fg="black",  bd=2,  font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda:self.cambiar_pantalla(cambiar_a_agregar_2), relief="flat")
        boton_seleccionar.place(x=391.47509765625, y=669.5166625976562, width=264.0133361816406, height=61.48335266113281)

        canvas.create_rectangle(38.0, 280.0, 1328.0, 642.0, fill="#FFFFFF", outline="")

        entry_nombre = Entry(self.master,  bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        entry_nombre.place(x=720.0, y=202.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(720.0, 154.0, anchor="nw", text="Nombre del producto", fill="#000000", font=("Inter Medium", 24 * -1))

        self.tipo_var = StringVar(self.master)
        self.tipo_var.set("Herramienta")
        tipo = OptionMenu(self.master, self.tipo_var, "Herramienta", "Maquinaria", "Insumo", "Limpieza")
        tipo.place(x=38.0, y=202.0, width=607.6497192382812, height=59.03461837768555)

        canvas.create_text(38.0, 154.0, anchor="nw", text="Seleccione tipo de producto", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        canvas.create_text(517.0, 47.0, anchor="nw", text="AGREGAR AL STOCK", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))
    
        self.tree = mostrar_tree(canvas, entry_nombre, self.tipo_var, conn)

        canvas.pack()
    
    def cambiar_pantalla(self, cambiar_a_agregar_2):
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_product = self.tree.item(selected_item, "values")[1]  # Guardar el producto seleccionado
            cambiar_a_agregar_2(self.selected_product)

class AgregarStockPT2:
    def __init__(self, master, cambiar_a_agregar_3, cambiar_a_agregar_1, primary_key, conn):
        self.master = master

        canvas = Canvas(self.master, bg = "#6B5E5E", height = 768, width = 1366, bd = 0, highlightthickness = 0, relief = "ridge")

        boton_cancelar = Button(self.master, text="Cancelar", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command= cambiar_a_agregar_1, relief="flat")
        boton_cancelar.place(x=735.11181640625, y=665.5166015625, width=264.0133361816406, height=61.48335266113281)

        boton_confirmar = Button(self.master, text="Confirmar", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.registar_stock(cambiar_a_agregar_3, conn, primary_key), relief="flat")
        boton_confirmar.place(x=391.47509765625, y=665.5166015625, width=264.0133361816406, height=61.48335266113281)

        self.cantidad = Entry(self.master, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Inter Medium", 20 * -1))
        self.cantidad.place(x=38.0, y=497.0, width=607.6497192382812, height=57.03461837768555)

        canvas.create_text(38.0, 459.0, anchor="nw", text="Cantidad a agregar", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_rectangle(38.0, 197.0, 1328.0, 431.0, fill="#FFFFFF", outline="")

        canvas.create_text(38.0, 155.0, anchor="nw", text="Producto", fill="#000000", font=("Inter Medium", 24 * -1))

        canvas.create_rectangle(0.0, 0.0, 1366.0, 130.0, fill="#2B2626", outline="")

        canvas.create_text(543.0, 47.0, anchor="nw", text="AGREGAR STOCK", fill="#FFFFFF", font=("PalanquinDark Regular", 36 * -1))

        self.tree = ttk.Treeview(canvas, columns=("tipo_producto", "Producto", "Cantidad_existente", "Area", "Lugar_guarda", "Cantidad_migrada", "Observaciones", "Inventariado"), show='headings')
        
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
        cantidad_agregar = self.cantidad.get().strip()
        fecha = get_date()
        
        if not es_entero(cantidad_agregar):
            messagebox.showerror("Error.", "Ingrese un valor numérico valido en.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""UPDATE stock
                            SET cantidad_existente = cantidad_existente + ?
                            WHERE Producto = ?;
                            """, (cantidad_agregar, primary_key))

        except Exception as e:
            messagebox.showerror("Error.", f"Error al actualizar el stock: {e}")

        finally:
            conn.commit()
            cursor.close()

        try:
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO Movimientos 
                          (fecha_egreso, tipo_egreso, Lugar_origen, Lugar_destino, 
                           responsable_retiro, cantidad_egresada, fecha_devolucion, 
                           cantidad_devuelta, Responsable_devolucion, Responsable_recepcion, 
                           Motivo, Comentario, Inventariado, Producto, Nro_inventariado, definitivo)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""", 
                       (fecha, "Incremento de stock", "N/A", "N/A", "N/A", 
                        cantidad_agregar, fecha, "N/A", "N/A", "N/A", 
                        "Incremento de stock", "N/A", "N/A", primary_key, "N/A", "N/A"))
        except Exception as e:
            messagebox.showerror("Error.", f"Error al actualizar el stock: {e}")

        finally:
            conn.commit()
            cursor.close()
        
        funcion()

        
class AgregarStockPT3:
    def __init__(self, root, cambiar_a_agregar_4, cambiar_a_agregar_1):
        self.popup = tk.Toplevel(root)
        self.popup.geometry("773x245")
        self.popup.config(bg="#6B5E5E")
        self.popup.grab_set()
        self.popup.resizable(False, False)

        canvas = Canvas(self.popup, bg = "#6B5E5E", height = 245, width = 773, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)

        boton_cancelar = Button(self.popup, text="Cancelar",  bg="#FFA500",  fg="black",  bd=2,  font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_agregar_1), relief="flat")
        boton_cancelar.place(x=426.63671875, y=131.0, width=264.0133361816406, height=61.48335266113281)

        boton_confirmar = Button(self.popup, text="Confirmar",  bg="#FFA500",  fg="black",  bd=2,  font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_agregar_4), relief="flat")
        boton_confirmar.place(x=83.0, y=131.0, width=264.0133361816406, height=61.4833526611328)

        canvas.create_rectangle(0.0, 0.0, 773.0, 92.0, fill="#2B2626", outline="")

        canvas.create_text(190.0, 31.0, anchor="nw", text="¿Desea mantener la modificación?", fill="#FFFFFF", font=("Inter Medium", 24 * -1))

        canvas.pack()

    def cerrar_y_ejecutar(self, funcion):
        self.popup.destroy()  # Cierra la ventana emergente
        funcion() #Ejecuta la funcion dada

class AgregarStockPT4:
    def __init__(self, root, cambiar_a_agregar_1, cambiar_a_menuInv):
        self.popup = tk.Toplevel(root)
        self.popup.geometry("773x245")
        self.popup.config(bg="#6B5E5E")
        self.popup.grab_set()
        self.popup.resizable(False, False)

        canvas = Canvas(self.popup, bg = "#6B5E5E", height = 245, width = 773, bd = 0, highlightthickness = 0, relief = "ridge")
        canvas.place(x = 0, y = 0)


        boton_cancelar = Button(self.popup, text="No", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_menuInv), relief="flat")
        boton_cancelar.place(x=426.63671875, y=131.0, width=264.0133361816406, height=61.48335266113281)

        boton_confirmar = Button(self.popup,  text="Sí",  bg="#FFA500",  fg="black",  bd=2,  font=("Inter Medium", 24 * -1), borderwidth=0, highlightthickness=0, command=lambda: self.cerrar_y_ejecutar(cambiar_a_agregar_1), relief="flat")
        boton_confirmar.place(x=83.0, y=131.0, width=264.0133361816406, height=61.48335266113281)

        canvas.create_rectangle(0.0, 0.0, 773.0, 92.0, fill="#2B2626", outline="")

        canvas.create_text(190.0, 31.0, anchor="nw", text="¿Desea agregar stock a otro producto?", fill="#FFFFFF", font=("Inter Medium", 24 * -1))

        canvas.pack()

    def cerrar_y_ejecutar(self, funcion):
        self.popup.destroy()  # Cierra la ventana emergente
        funcion() #Ejecuta la funcion dada