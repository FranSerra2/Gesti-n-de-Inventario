import tkinter as tk
from tkinter import Button, Canvas, messagebox
from tkcalendar import DateEntry
import sqlite3
import pandas as pd
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from funciones import mostrar_tree_porcentaje

class MenuReportes:
    def __init__(self, master, cambiar_a_porcentaje, cambiar_a_promedio, cambiar_a_menuDM, cambiar_a_listo, conn):
        self.master = master

        canvas = Canvas(self.master, bg="#6B5E5E", height=768, width=1366, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        boton_volver = Button(self.master, text="Volver", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1),
                              borderwidth=0, highlightthickness=0, command=cambiar_a_menuDM, relief="flat")
        boton_volver.place(x=272.0, y=550.0, width=821.0, height=72.1)

        boton_promedio = Button(self.master, text="Reporte de compras realizadas según fecha", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1),
                                borderwidth=0, highlightthickness=0, command=cambiar_a_promedio, relief="flat")
        boton_promedio.place(x=272.0, y=400.0, width=821.0, height=72.1)

        boton_porcentaje = Button(self.master, text="Porcentaje de productos migrados", bg="#FFA500", fg="black", bd=2, font=("Inter Medium", 24 * -1),
                                  borderwidth=0, highlightthickness=0, command=lambda:self.query_porcentaje(cambiar_a_listo, conn), relief="flat")
        boton_porcentaje.place(x=272.0, y=300.0, width=821.0, height=72.1)

        canvas.create_rectangle(0.0, 0.0, 1366.0, 210.0, fill="#2B2626", outline="")
        canvas.create_text(530.0, 70.0, anchor="nw", text="REPORTES", fill="#FFFFFF", font=("PalanquinDark Regular", 60 * -1))

        canvas.pack()

    def query_porcentaje(self, funcion, conn):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    Producto, 
                    Cantidad_existente, 
                    Cantidad_migrada, 
                    CASE 
                        WHEN Cantidad_migrada = 0 THEN 0
                        ELSE (CAST(Cantidad_migrada AS FLOAT) / Cantidad_existente) * 100
                    END AS Porcentaje_migracion
                FROM 
                    stock
                WHERE 
                    Cantidad_existente > 0;
            """)
            resultados = cursor.fetchall()
            df = pd.DataFrame(resultados, columns=["Producto", "Cantidad_existente", "Cantidad_migrada", "Porcentaje_migracion"])
            # Exportar a Excel
            df.to_excel("resultados_porcentaje.xlsx", index=False)
        except sqlite3.Error as e:
            messagebox.showerror(f"Error al exportar el : {e}")
        finally:
            cursor.close()  # Cerrar el cursor después de usarlo
        
        funcion()

class Promedio:
    def __init__(self, master, cambiar_a_listo, cambiar_a_menurepor, conn):
        self.master = master
        self.conn = conn

        canvas = Canvas(self.master, bg="#6B5E5E", height=768, width=1366, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        boton_cancelar = Button(self.master, text="Cancelar", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1),
                                 borderwidth=0, highlightthickness=0, command=cambiar_a_menurepor, relief="flat")
        boton_cancelar.place(x=800, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        boton_sumaygasto = Button(self.master, text="Cantidad y Gastos", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1),
                                borderwidth=0, highlightthickness=0, command=lambda: self.query_promedio(cambiar_a_listo), relief="flat")
        boton_sumaygasto.place(x=500, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        boton_facturas = Button(self.master, text="Reporte Compras", bg="#FFA500", bd=2, font=("Inter Medium", 24 * -1),
                                borderwidth=0, highlightthickness=0, command=lambda: self.compra_detalle(cambiar_a_listo), relief="flat")
        boton_facturas.place(x=200, y=665.5166625976562, width=264.0133361816406, height=61.48335266113281)

        canvas.create_rectangle(38.0, 281.0, 1328.0, 643.0, fill="#FFFFFF", outline="")

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

    def exportar_a_pdf1(self, df, fecha_desde, fecha_hasta):
        c = canvas.Canvas("Cantidad_y_Gastos.pdf", pagesize=letter)
        width, height = letter
        
        # Título principal y fechas
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, height - 50, "Resultados de Cantidad y Gastos")
        c.setFont("Helvetica", 10)
        c.drawString(100, height - 70, f"Desde: {fecha_desde}  Hasta: {fecha_hasta}")
        
        # Encabezados de columna
        y = height - 120
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y, "Producto")
        c.drawString(250, y, "Cantidad Total Comprada")
        c.drawString(450, y, "Total Gastado")
        
        # Línea separadora debajo de los encabezados
        y -= 10
        c.setLineWidth(0.5)
        c.line(80, y, 530, y)
        y -= 20
        
        # Contenido de las filas
        c.setFont("Helvetica", 10)
        for index, row in df.iterrows():
            # Ajuste de las posiciones x para columnas separadas
            c.drawString(100, y, str(row['Producto']))
            c.drawString(250, y, str(row['Cantidad_Total_Comprada']))
            c.drawString(450, y, str(row['Total_Gastado']))
            y -= 20
            
            # Salto de página si el contenido excede el tamaño de la página
            if y < 50:
                c.showPage()
                y = height - 50

        # Guardar el PDF
        c.save()

    def exportar_a_pdf2(self, df):
        # Configuración de la página en orientación vertical
        c = canvas.Canvas("Reporte Compras.pdf", pagesize=letter)
        width, height = letter

        # Agrupar productos por número de factura
        facturas = df.groupby('Nro_factura')

        for nro_factura, grupo in facturas:
            # Encabezado de la factura en una nueva página
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 50, "Factura de Compra")
            
            # Detalles del encabezado
            c.setFont("Helvetica", 10)
            c.drawString(50, height - 80, f"Número de Factura: {nro_factura}")
            c.drawString(250, height - 80, f"Fecha de Factura: {grupo.iloc[0]['Fecha_factura']}")
            c.drawString(50, height - 100, f"Fecha OC: {grupo.iloc[0]['Fecha_OC']}")
            c.drawString(250, height - 100, f"Número de OC: {grupo.iloc[0]['Nro_OC']}")
            c.drawString(50, height - 120, f"Proveedor: {grupo.iloc[0]['Proveedor']}")

            # Línea de separación
            c.setLineWidth(1)
            c.line(50, height - 140, width - 50, height - 140)

            # Encabezados de la tabla de productos
            y = height - 160
            c.setFont("Helvetica-Bold", 8)
            c.drawString(50, y, "id_cabecera")
            c.drawString(150, y, "id_posicion")
            c.drawString(250, y, "Producto")
            c.drawString(400, y, "Cantidad")
            c.drawString(480, y, "Unitario")

            # Imprimir los detalles de todos los productos de la misma factura
            for index, row in grupo.iterrows():
                y -= 20
                c.setFont("Helvetica", 8)
                c.drawString(50, y, str(row['id_cabecera']).strip())
                c.drawString(150, y, str(row['id_posicion']).strip())
                c.drawString(250, y, str(row['Producto']).strip())
                c.drawString(400, y, str(row['Cantidad']).strip())
                c.drawString(480, y, str(row['Precio_unitario']).strip())

                # Si se necesita un salto de página dentro de la misma factura
                if y < 100:  # Cambiar a nueva página si el espacio es limitado
                    c.showPage()
                    y = height - 160  # Reiniciar la posición y en la nueva página
                    c.setFont("Helvetica-Bold", 8)
                    c.drawString(50, y, "id_cabecera")
                    c.drawString(150, y, "id_posicion")
                    c.drawString(250, y, "Producto")
                    c.drawString(400, y, "Cantidad")
                    c.drawString(480, y, "Unitario")
                    y -= 20

            # Tomar el monto total desde el primer registro del grupo y colocarlo en el pie de página
            total_factura = grupo.iloc[0]['Monto_total']
            c.setFont("Helvetica-Bold", 10)
            c.drawString(400, 50, f"Total de la Factura: {total_factura}")

            # Añadir una nueva página para la siguiente factura
            c.showPage()

        # Guardar el archivo PDF
        c.save()

    def query_promedio(self, funcion):
        desde = self.fecha_desde.get_date()
        hasta = self.fecha_hasta.get_date()

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                    SELECT 
                    cp.Producto,
                    SUM(cp.Cantidad) AS Cantidad_Total_Comprada,
                    SUM(cp.Cantidad * cp.Precio_Unitario) AS Total_Gastado
                    FROM 
                        compra_posicion cp
                    JOIN 
                        compra_cabecera cc ON cp.id_cabecera = cc.id_cabecera
                    WHERE 
                        cc.Fecha_OC >= ?
                    AND cc.Fecha_OC <= ?
                    GROUP BY 
                    cp.Producto;
            """, (desde, hasta))
            
            resultados = cursor.fetchall()
            df = pd.DataFrame(resultados, columns=["Producto", "Cantidad_Total_Comprada", "Total_Gastado"])
            # Exportar a Excel
            df.to_excel("Cantidad y Gastos.xlsx", index=False)
            # Exportar a PDF
            self.exportar_a_pdf1(df, desde, hasta)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al exportar: {e}")
        finally:
            cursor.close()  # Cerrar el cursor después de usarlo

        funcion()
    def compra_detalle(self, funcion):
        desde = self.fecha_desde.get_date()
        hasta = self.fecha_hasta.get_date()

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT *
                FROM Compra_cabecera AS cc
                JOIN Compra_posicion AS cp ON cc.id_cabecera = cp.id_cabecera
                WHERE cc.Fecha_OC >= ? AND cc.Fecha_OC <= ?;
            """, (desde, hasta))

            resultados = cursor.fetchall()
            df = pd.DataFrame(resultados, columns=[desc[0] for desc in cursor.description])
            df = df.loc[:, ~df.columns.duplicated()].copy()
            print(df.columns)
            # Exportar a Excel
            df.to_excel("Reporte Compras.xlsx", index=False)

            # Exportar a PDF
            self.exportar_a_pdf2(df)
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al exportar: {e}")
        finally:
            cursor.close()

        funcion()       