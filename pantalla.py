from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk as kt
from BD import *
import os
import sys

def ruta_recurso(relative_path):
    """Devuelve la ruta correcta para archivos dentro o fuera del exe."""
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


color = "#EB6C10"
fondo = "#292929"


class Registro:
      def __init__(self):
            
            #Creacion de ventana

            self.ventana = Tk()
            self.ventana.title("Registro")
            self.ventana.config(bg = fondo)

#  Creacion de frames

            self.frame1 = Frame(self.ventana, bg = "#424242")
            self.frame1.pack(fill='both', expand=True)
            self.frame2 = Frame(self.ventana, bg = fondo)
            self.frame2.pack(fill='both', expand=True)

#LOGO

            self.Titulo = Label(self.frame1, text = "Registro", font = ("Times New Roman", 36), bg = "#424242", fg = color,)
            self.Titulo.pack(padx = 5, pady=35)
            
            # Creacion de labels,listas y entradas

            self.Label_IDProducto = Label(self.frame2, text = " ID: ", font = ("Times New Roman", 18),bg = fondo, fg = color)
            self.Label_Marca = Label(self.frame2, text = "Marca: " ,font = ("Times New Roman", 18), bg = fondo, fg = color)
            self.Label_Sexo = Label(self.frame2, text = "Sexo: " ,font = ("Times New Roman", 18), bg = fondo, fg = color)
            self.Label_Talla = Label(self.frame2, text = "Talla: " ,font = ("Times New Roman", 18), bg = fondo, fg = color)
            self.Label_Color = Label(self.frame2, text = "Color: " ,font = ("Times New Roman", 18), bg = fondo, fg = color)
            self.Label_Material = Label(self.frame2, text = "Material: " ,font = ("Times New Roman", 18), bg = fondo, fg = color)
            self.Label_Tipo = Label(self.frame2, text = "Tipo: " ,font = ("Times New Roman", 18), bg = fondo, fg = color)
            self.Label_Precio = Label(self.frame2, text = "Precio: " ,font = ("Times New Roman", 18), bg = fondo, fg = color)
            self.Label_Stock = Label(self.frame2, text = "Stock: " ,font = ("Times New Roman", 18), bg = fondo, fg = color)

            self.ListaMarca = ["Nike", "Adidas", "Converse", "Puma", "Skechers","VANS"]
            self.ListaSexo = ["Masculino", "Femenino"]
            self.ListaMaterial = ["Sintetico", "Cuero", "Plastico"]
            self.ListaTipo = ["Tenis", "Zapato", "Sandalia", "Bota", "Zapatilla"]

            self.MarcaV = StringVar()
            self.SexoV  = StringVar()
            self.TallaV = IntVar()
            self.MaterialV = StringVar()
            self.TipoV = StringVar()
            
            
            self.Entrada_IDproducto = Entry(self.frame2, cursor = "ibeam" ,width = 20)
            self.Entrada_Marca = OptionMenu(self.frame2, self.MarcaV, *self.ListaMarca)
            self.MarcaV.set("Nike")
            self.Entrada_Sexo = OptionMenu(self.frame2, self.SexoV, *self.ListaSexo)
            self.SexoV.set("Seleccione el sexo")
            self.Entrada_Talla = Spinbox(self.frame2, textvariable  = self.TallaV, from_=0, to = 10, increment = 1, font = ("Times New Roman",8))
            self.Entrada_Color = Entry(self.frame2,cursor = "ibeam", width = 20)
            self.Entrada_Material = OptionMenu(self.frame2,self.MaterialV, *self.ListaMaterial)
            self.MaterialV.set("Eliga el material")
            self.Entrada_Tipo = OptionMenu(self.frame2,self.TipoV, *self.ListaTipo)
            self.TipoV.set("Eliga el Tipo")
            self.Entrada_Precio = Entry(self.frame2, cursor = "ibeam", width = 20 )
            self.Entrada_Stock = Entry(self.frame2, cursor = "ibeam", width = 20)

            self.Botonregistro = Button(self.frame2, text = "Registrar", font = ("Times New Roman", 20),bg = "green", command = lambda: self.Agregar(self.MarcaV.get(),self.Entrada_IDproducto.get(),self.SexoV.get(),self.TallaV.get(),self.Entrada_Color.get(),self.MaterialV.get(),self.TipoV.get(),self.Entrada_Precio.get(),self.Entrada_Stock.get()))
            self.BotonActualizar =Button(self.frame2, text = "Actualizar", font = ("Times New Roman", 20),bg = "yellow", command = lambda: self.Modificar(self.MarcaV.get(),self.Entrada_IDproducto.get(),self.Entrada_Precio.get()))
            self.BotonEliminar =Button(self.frame2, text = "Eliminar", font = ("Times New Roman", 20),bg = "red", command = lambda: self.Eliminar(self.MarcaV.get(),self.Entrada_IDproducto.get()) )

            #Posicionamiento

            self.Label_IDProducto.grid(row = 1, column = 1, pady = 8,padx = 10, sticky = E)
            self.Label_Marca.grid(row = 2, column = 1, pady = 8,padx = 10, sticky = E)
            self.Label_Sexo.grid(row = 3, column = 1, pady = 8,padx = 10, sticky = E)
            self.Label_Talla.grid(row = 4, column = 1, pady = 8,padx = 10, sticky = E)
            self.Label_Color.grid(row = 5, column = 1, pady = 8,padx = 10, sticky = E)
            self.Label_Material.grid(row = 1, column = 3, pady = 8,padx = 10, sticky = E)
            self.Label_Tipo.grid(row = 2, column = 3, pady = 8,padx = 10, sticky = E)
            self.Label_Precio.grid(row = 3, column = 3, pady = 8,padx = 10, sticky = E)
            self.Label_Stock.grid(row = 4, column = 3, pady = 8,padx = 10, sticky = E)


            self.Entrada_IDproducto.grid(row = 1, column = 2, pady=8, padx = 10)
            self.Entrada_Marca.grid(row = 2, column = 2, pady=8, padx = 10)
            self.Entrada_Sexo.grid(row = 3, column = 2, pady=8, padx = 10)
            self.Entrada_Talla.grid(row = 4, column = 2, pady=8, padx = 10)
            self.Entrada_Color.grid(row = 5, column = 2, pady=8, padx = 10)
            self.Entrada_Material.grid(row = 1, column = 4, pady=8, padx = 10)
            self.Entrada_Tipo.grid(row = 2, column = 4, pady=8, padx = 10)
            self.Entrada_Precio.grid(row = 3, column = 4, pady=8, padx = 10)
            self.Entrada_Stock.grid(row = 4, column = 4, pady=8, padx = 10)
            self.Botonregistro.grid(row  = 10, column = 1, columnspan = 1, sticky = W, pady=5, padx = 5)
            self.BotonActualizar.grid(row  = 10, column = 2, columnspan = 2, pady=5, padx = 2)
            self.BotonEliminar.grid(row  = 10, column = 4, columnspan = 1, sticky = E, pady=5, padx = 5)

      def Agregar(self,tabla,id,sexo,talla,color,material,tipo,precio,stock):
            msg = agregar_nuevo_zapato(tabla,id,sexo,talla,color,material,tipo,precio,stock)
            messagebox.showinfo("Informacion",msg)
            

      def Eliminar(self,tabla,id):
            msg = Eliminar_Zapato(tabla,id)
            messagebox.showinfo("Informacion",msg)
            mainloop ()

      def Modificar(self, tabla, id, precio):

        emergente = Toplevel(self.ventana, bg = fondo)
        emergente.title("Modificar Producto")
        emergente.geometry("300x200")
        emergente.grab_set()  

        Label(emergente, text="ID del producto:", fg = color, bg = fondo).pack(pady=5)
        entrada_Id = Entry(emergente)
        entrada_Id.insert(0, id)  
        entrada_Id.pack(pady=5)

        Label(emergente, text="Nuevo precio:", bg = fondo, fg = color).pack(pady=5)
        entrada_precio = Entry(emergente)
        precio_actual = buscar_precio(tabla,entrada_Id.get())
        entrada_precio.insert(0,precio_actual)
        entrada_precio.pack(pady=5)

        def modificar():
            nuevo_id = entrada_Id.get()
            nuevo_precio = entrada_precio.get()

            msg = Modificar_Precio(tabla, nuevo_id, nuevo_precio)
            messagebox.showinfo("Información", msg)

            emergente.destroy()  # Cierra la ventana emergente

        Button(emergente, text="Actualizar", command=modificar).pack(pady=10)
      
Registro()

mainloop()