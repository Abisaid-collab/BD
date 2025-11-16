import sqlite3
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import io

# -------------------------------------
# Leer productos desde la base de datos
# -------------------------------------
def obtener_productos():
    conn = sqlite3.connect("productos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, precio, descripcion, imagen FROM productos")
    datos = cursor.fetchall()
    conn.close()
    return datos

# -------------------------------------
# Activar scroll con la rueda del mouse
# -------------------------------------
def hacer_scroll_con_rueda(canvas, evento):
    if evento.num == 5 or evento.delta < 0:     # Scroll hacia abajo
        canvas.yview_scroll(1, "units")
    elif evento.num == 4 or evento.delta > 0:   # Scroll hacia arriba
        canvas.yview_scroll(-1, "units")

def crear_interfaz():
    root = tk.Tk()
    root.title("Lista de Productos")
    root.geometry("600x500")

    # ----- Contenedor principal -----
    contenedor = tk.Frame(root)
    contenedor.pack(fill="both", expand=True)

    # Canvas donde va el contenido scrolleable
    canvas = tk.Canvas(contenedor)
    canvas.pack(side="left", fill="both", expand=True)

    # Barra lateral
    scrollbar = ttk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    # Ajustar la región scrolleable cuando cambie el tamaño
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # ----- Frame interno -----
    marco = tk.Frame(canvas)
    canvas.create_window((0, 0), window=marco, anchor="nw")

    # --------------------------
    # Conectar scroll del mouse
    # --------------------------
    # Windows y Linux
    canvas.bind_all("<MouseWheel>", lambda e: hacer_scroll_con_rueda(canvas, e))
    # Linux (algunas distros)
    canvas.bind_all("<Button-4>", lambda e: hacer_scroll_con_rueda(canvas, e))
    canvas.bind_all("<Button-5>", lambda e: hacer_scroll_con_rueda(canvas, e))

    # -------------------------------------
    # Mostrar productos desde la base de datos
    # -------------------------------------
    productos = obtener_productos()
    imagenes_cache = []  # Previene GC

    for nombre, precio, descripcion, imagen_blob in productos:
        frame_producto = tk.Frame(marco, pady=10, padx=10, borderwidth=2, relief="ridge")
        frame_producto.pack(fill="x", padx=5, pady=5)

        # Imagen
        if imagen_blob:
            img = Image.open(io.BytesIO(imagen_blob))
            img = img.resize((120, 120))
            img_tk = ImageTk.PhotoImage(img)
            imagenes_cache.append(img_tk)

            tk.Label(frame_producto, image=img_tk).pack(side="left", padx=10)
        else:
            tk.Label(frame_producto, text="(Sin imagen)").pack(side="left", padx=10)

        # Texto
        info = f"Nombre: {nombre}\nPrecio: ${precio}\nDescripción: {descripcion}"
        tk.Label(frame_producto, text=info, justify="left").pack(side="left")

    root.mainloop()

def insertar_productos_ejemplo():
    conn = sqlite3.connect("productos.db")
    cursor = conn.cursor()

    # Verificar si ya hay datos
    cursor.execute("SELECT COUNT(*) FROM productos")
    if cursor.fetchone()[0] > 0:
        print("La base ya tiene datos, no se insertará de nuevo.")
        conn.close()
        return

    # Rutas iniciales de imágenes SOLO para cargar a la BD una vez
    productos = [
        ("Coca Cola", 18.5, "Refresco sabor cola 600ml", "coca.jpeg"),
        ("Galletas Oreo", 22.0, "Galletas de chocolate con crema 117g", "oreo.jpeg"),
        ("Sabritas", 17.0, "Papas fritas originales 45g", "sabritas.jpeg")
    ]

    for nombre, precio, descripcion, ruta_img in productos:
        # Convertir archivo en BLOB solo esta vez
        with open(ruta_img, "rb") as img_file:
            blob = img_file.read()

        cursor.execute("""
            INSERT INTO productos (nombre, precio, descripcion, imagen)
            VALUES (?, ?, ?, ?)
        """, (nombre, precio, descripcion, blob))

    conn.commit()
    conn.close()
    print("Productos insertados y guardados en SQLite como BLOB.")

crear_interfaz()
