# ui_spotify_style.py
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import io
import os
import sys

# Importa tus funciones de BD (debe existir BD.py con las funciones usadas).
from BD import (
    agregar_nuevo_zapato,
    Eliminar_Zapato,
    Modificar_Precio,
    buscar_precio,
    guardar_imagen_blob,
    obtener_productos,
    obtener_todo,
    Sin_Stock,
    Imagen
)

# -------------------------
# Utilidades
# -------------------------
def ruta_recurso(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


# -------------------------
# Estilo "Spotify-like"
# -------------------------
PALETA = {
    "fondo": "#121212",
    "panel": "#1E1E1E",
    "texto": "#FFFFFF",
    "subtexto": "#B3B3B3",
    "acento": "#1DB954",
    "secundario": "#404040",
}

CARD_WIDTH = 260  # ancho aproximado de cada card (px)
CARD_HEIGHT = 150

# -------------------------
# App (ventana principal)
# -------------------------
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Panel Principal")
        self.root.configure(bg=PALETA["fondo"])
        self.root.geometry("900x540")
        self._setup_style()
        self._build_main()

    def _setup_style(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")  # base neutral
        style.configure("TFrame", background=PALETA["fondo"])
        style.configure("Panel.TFrame", background=PALETA["panel"])
        style.configure("TLabel", background=PALETA["fondo"], foreground=PALETA["texto"])
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"), foreground=PALETA["texto"], background=PALETA["panel"])
        style.configure("Accent.TButton", background=PALETA["acento"], foreground="#ffffff", font=("Segoe UI", 10, "bold"))
        style.map("Accent.TButton", background=[("active", PALETA["acento"])])
        style.configure("Sec.TButton", background=PALETA["secundario"], foreground=PALETA["texto"])
        style.configure("Card.TFrame", background=PALETA["panel"], relief="flat")
        style.configure("CardTitle.TLabel", font=("Segoe UI", 11, "bold"), foreground=PALETA["texto"], background=PALETA["panel"])
        style.configure("CardText.TLabel", font=("Segoe UI", 9), foreground=PALETA["subtexto"], background=PALETA["panel"])

    def _build_main(self):
        container = ttk.Frame(self.root, style="TFrame")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        header = ttk.Frame(container, style="Panel.TFrame")
        header.pack(fill="x", pady=(0, 12))

        title = ttk.Label(header, text="Inventario", style="Title.TLabel")
        title.pack(side="left", padx=12, pady=12)

        btn_frame = ttk.Frame(header, style="Panel.TFrame")
        btn_frame.pack(side="right", padx=8)

        ttk.Button(btn_frame, text="Registro", style="Accent.TButton", command=self.open_registro).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Consulta", style="Sec.TButton", command=self.open_consulta).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Agregar Imagen", style="Sec.TButton", command=self.open_imagen).pack(side="left", padx=6)

        # Pie / info
        footer = ttk.Label(container, text="Diseño: estilo Spotify · Oscuro y elegante", foreground=PALETA["subtexto"])
        footer.pack(side="bottom", pady=(12,0))

    def open_registro(self):
        RegistroWindow(self.root)

    def open_consulta(self):
        ConsultaWindow(self.root)

    def open_imagen(self):
        ImagenWindow(self.root)


# -------------------------
# Registro (ventana para CRUD)
# -------------------------
class RegistroWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Registro")
        self.configure(bg=PALETA["fondo"])
        self.geometry("720x480")
        self.transient(master)
        self.grab_set()

        # Variables y listas
        self.lista_marca = ["Nike", "Adidas", "Converse", "Puma", "Skechers", "VANS"]
        self.lista_sexo = ["Masculino", "Femenino"]
        self.lista_material = ["Sintetico", "Cuero", "Plastico"]
        self.lista_tipo = ["Tenis", "Zapato", "Sandalia", "Bota", "Zapatilla"]

        self.marca_v = tk.StringVar(value=self.lista_marca[0])
        self.sexo_v = tk.StringVar(value=self.lista_sexo[0])
        self.material_v = tk.StringVar(value=self.lista_material[0])
        self.tipo_v = tk.StringVar(value=self.lista_tipo[0])
        self.talla_v = tk.IntVar(value=1)

        self._build_ui()

    def _build_ui(self):
        main = ttk.Frame(self, style="TFrame", padding=12)
        main.pack(fill="both", expand=True)

        encabezado = ttk.Frame(main, style="Panel.TFrame", padding=10)
        encabezado.pack(fill="x", pady=(0, 12))
        ttk.Label(encabezado, text="Registro de Producto", style="Title.TLabel").pack(side="left")

        form = ttk.Frame(main, style="TFrame")
        form.pack(fill="both", expand=True)

        # Left column
        left = ttk.Frame(form, style="TFrame")
        left.grid(row=0, column=0, sticky="nw", padx=(0,20))

        ttk.Label(left, text="ID:", foreground=PALETA["subtexto"]).grid(row=0, column=0, sticky="w", pady=6)
        self.e_id = ttk.Entry(left, width=24)
        self.e_id.grid(row=0, column=1, pady=6)

        ttk.Label(left, text="Marca:", foreground=PALETA["subtexto"]).grid(row=1, column=0, sticky="w", pady=6)
        self.cmb_marca = ttk.Combobox(left, values=self.lista_marca, textvariable=self.marca_v, state="readonly", width=22)
        self.cmb_marca.grid(row=1, column=1, pady=6)

        ttk.Label(left, text="Sexo:", foreground=PALETA["subtexto"]).grid(row=2, column=0, sticky="w", pady=6)
        self.cmb_sexo = ttk.Combobox(left, values=self.lista_sexo, textvariable=self.sexo_v, state="readonly", width=22)
        self.cmb_sexo.grid(row=2, column=1, pady=6)

        ttk.Label(left, text="Talla:", foreground=PALETA["subtexto"]).grid(row=3, column=0, sticky="w", pady=6)
        self.spin_talla = ttk.Spinbox(left, from_=0, to=50, textvariable=self.talla_v, width=20)
        self.spin_talla.grid(row=3, column=1, pady=6)

        ttk.Label(left, text="Color:", foreground=PALETA["subtexto"]).grid(row=4, column=0, sticky="w", pady=6)
        self.e_color = ttk.Entry(left, width=24)
        self.e_color.grid(row=4, column=1, pady=6)

        # Right column
        right = ttk.Frame(form, style="TFrame")
        right.grid(row=0, column=1, sticky="ne")

        ttk.Label(right, text="Material:", foreground=PALETA["subtexto"]).grid(row=0, column=0, sticky="w", pady=6)
        self.cmb_material = ttk.Combobox(right, values=self.lista_material, textvariable=self.material_v, state="readonly", width=22)
        self.cmb_material.grid(row=0, column=1, pady=6)

        ttk.Label(right, text="Tipo:", foreground=PALETA["subtexto"]).grid(row=1, column=0, sticky="w", pady=6)
        self.cmb_tipo = ttk.Combobox(right, values=self.lista_tipo, textvariable=self.tipo_v, state="readonly", width=22)
        self.cmb_tipo.grid(row=1, column=1, pady=6)

        ttk.Label(right, text="Precio:", foreground=PALETA["subtexto"]).grid(row=2, column=0, sticky="w", pady=6)
        self.e_precio = ttk.Entry(right, width=24)
        self.e_precio.grid(row=2, column=1, pady=6)

        ttk.Label(right, text="Stock:", foreground=PALETA["subtexto"]).grid(row=3, column=0, sticky="w", pady=6)
        self.e_stock = ttk.Entry(right, width=24)
        self.e_stock.grid(row=3, column=1, pady=6)

        ttk.Label(right, text = "Insertar Imagen:", foreground = PALETA["subtexto"]).grid(row = 4, column = 0, sticky = "w", pady = 6)
        self.btn_imagen = ttk.Button(right, text="Insertar imagen", style="Sec.TButton", command= self._seleccionar).grid(row=4, column=1, pady=8)

        # Botones
        botones = ttk.Frame(main, style="TFrame")
        botones.pack(fill="x", pady=(12,0))

        ttk.Button(botones, text="Registrar", style="Accent.TButton",
                   command=self._agregar).pack(side="left", padx=6)
        ttk.Button(botones, text="Actualizar", style="Sec.TButton",
                   command=self._abrir_modificar).pack(side="left", padx=6)
        ttk.Button(botones, text="Eliminar", style="Sec.TButton",
                   command=self._eliminar).pack(side="left", padx=6)
        
    def _seleccionar(self):
        ruta = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[("Imágenes", "*.jpg *.png *.jpeg *.gif *.bmp")]
        )
        self.datos = Imagen(ruta)


    def _agregar(self):
        msg = agregar_nuevo_zapato(
            self.marca_v.get(),
            self.e_id.get(),
            self.sexo_v.get(),
            self.talla_v.get(),
            self.e_color.get(),
            self.material_v.get(),
            self.tipo_v.get(),
            self.e_precio.get(),
            self.e_stock.get(),
            self.datos
        )
        messagebox.showinfo("Información", msg)

    def _eliminar(self):
        msg = Eliminar_Zapato(self.marca_v.get(), self.e_id.get())
        messagebox.showinfo("Información", msg)

    def _abrir_modificar(self):
        ModificarWindow(self, self.marca_v.get(), self.e_id.get())


# -------------------------
# Ventana Modificar (Toplevel)
# -------------------------
class ModificarWindow(tk.Toplevel):
    def __init__(self, master, tabla, id_val):
        super().__init__(master)
        self.title("Modificar Producto")
        self.configure(bg=PALETA["fondo"])
        self.geometry("360x200")
        self.transient(master)
        self.grab_set()

        ttk.Label(self, text="ID del producto:", foreground=PALETA["subtexto"]).pack(pady=6)
        self.e_id = ttk.Entry(self)
        self.e_id.pack(pady=6)
        self.e_id.insert(0, id_val)

        ttk.Label(self, text="Nuevo precio:", foreground=PALETA["subtexto"]).pack(pady=6)
        self.e_precio = ttk.Entry(self)
        precio_actual = buscar_precio(tabla, id_val)
        if precio_actual is None:
            precio_actual = ""
        self.e_precio.insert(0, precio_actual)
        self.e_precio.pack(pady=6)

        def confirmar():
            nuevo_id = self.e_id.get()
            nuevo_precio = self.e_precio.get()
            msg = Modificar_Precio(tabla, nuevo_id, nuevo_precio)
            messagebox.showinfo("Información", msg)
            self.destroy()

        ttk.Button(self, text="Actualizar", style="Accent.TButton", command=confirmar).pack(pady=10)


# -------------------------
# Imagen (guardar imagen en DB)
# -------------------------
class ImagenWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Guardar Imagen")
        self.configure(bg=PALETA["fondo"])
        self.geometry("420x140")
        self.transient(master)
        self.grab_set()

        marcas = ["Nike", "Adidas", "Converse", "Puma", "Skechers", "VANS"]
        self.marca_v = tk.StringVar(value=marcas[0])

        frm = ttk.Frame(self, padding=10, style="TFrame")
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Id:", foreground=PALETA["subtexto"]).grid(row=0, column=0, sticky="w", pady=6)
        self.e_id = ttk.Entry(frm, width=12)
        self.e_id.grid(row=0, column=1, pady=6, padx=6)

        ttk.Label(frm, text="Marca:", foreground=PALETA["subtexto"]).grid(row=0, column=2, sticky="w")
        self.cmb = ttk.Combobox(frm, values=marcas, textvariable=self.marca_v, state="readonly", width=12)
        self.cmb.grid(row=0, column=3, pady=6, padx=6)

        ttk.Button(frm, text="Insertar imagen", style="Sec.TButton", command=self._seleccionar).grid(row=1, column=1, pady=8)
        ttk.Button(frm, text="Regresar", style="Sec.TButton", command=self.destroy).grid(row=1, column=2, pady=8)

    def _seleccionar(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.jpg *.png *.jpeg *.gif *.bmp")]
        )
        if ruta:
            msg = guardar_imagen_blob(self.marca_v.get(), self.e_id.get(), ruta)
            messagebox.showinfo("Información", msg)


# -------------------------
# Consulta Window (grid responsive con scroll)
# -------------------------
class ConsultaWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Lista de Productos")
        self.configure(bg=PALETA["fondo"])
        self.geometry("1000x600")
        self.transient(master)
        self.grab_set()

        self.imagenes_cache = []  # mantener referencias a PhotoImage
        self.lista_marca = ["Nike", "Adidas", "Converse", "Puma", "Skechers", "VANS"]
        self.marca_v = tk.StringVar(value="Todas")

        self._build_ui()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def _build_ui(self):
        # Contenedor principal
        cont = ttk.Frame(self, style="TFrame", padding=12)
        cont.pack(fill="both", expand=True)

        # Panel derecho: controles
        control_panel = ttk.Frame(cont, width=260, style="Panel.TFrame", padding=10)
        control_panel.pack(side="right", fill="y", padx=(8,0))

        ttk.Label(control_panel, text="Filtros", foreground=PALETA["subtexto"], font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0,8))
        marcas = ["Todas"] + self.lista_marca
        self.cmb_marca = ttk.Combobox(control_panel, values=marcas, textvariable=self.marca_v, state="readonly")
        self.cmb_marca.pack(fill="x", pady=6)

        ttk.Button(control_panel, text="Consultar", style="Accent.TButton", command=self.consultar_marca).pack(fill="x", pady=8)
        ttk.Button(control_panel, text="Consultar todos", style="Sec.TButton", command=self.consultar_todos).pack(fill="x", pady=4)
        ttk.Button(control_panel, text="Sin Stock", style="Sec.TButton", command=self.consultar_sin_stock).pack(fill="x", pady=4)
        ttk.Button(control_panel, text="Regresar", style="Sec.TButton", command=self.destroy).pack(side="bottom", fill="x", pady=8)

        # Panel izquierdo: canvas con scroll (donde estarán las cards)
        left_panel = ttk.Frame(cont, style="TFrame")
        left_panel.pack(side="left", fill="both", expand=True)

        # Canvas
        self.canvas = tk.Canvas(left_panel, bg=PALETA["fondo"], highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar vertical
        self.v_scroll = ttk.Scrollbar(left_panel, orient="vertical", command=self.canvas.yview)
        self.v_scroll.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.v_scroll.set)

        # Marco interior donde colocaremos las cards en grid
        self.inner_frame = ttk.Frame(self.canvas, style="TFrame")
        self.window_id = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Bindings: ajustar scrollregion y reorganizar al cambiar tamaño
        self.inner_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # Scroll con rueda del mouse (Windows / Mac / Linux)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel_windows)   # Windows
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux)      # Linux scroll up
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux)      # Linux scroll down

        # Estado inicial: mostrar todos
        self.productos_actuales = []
        self.consultar_todos()

    # ---------- eventos / util ----------
    def _on_frame_configure(self, event=None):
        # Ajusta el scrollregion al contenido
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        # Recalcula layout responsive cuando cambia la anchura
        self._recalcular_grid(event.width)

    def _on_mousewheel_windows(self, event):
        # delta negativo -> scroll down
        # Multiplicador para velocidad natural
        if self.canvas.winfo_height() < self.canvas.bbox("all")[3]:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _on_mousewheel_linux(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")

    # ---------- consultas ----------
    def consultar_marca(self):
        marca = self.marca_v.get()
        if marca == "Todas":
            prods = obtener_todo()
        else:
            prods = obtener_productos(marca)
        self._mostrar_productos(prods)

    def consultar_todos(self):
        prods = obtener_todo()
        self._mostrar_productos(prods)

    def consultar_sin_stock(self):
        prods = Sin_Stock()
        self._mostrar_productos(prods)

    # ---------- renderizado de cards ----------
    def _mostrar_productos(self, productos):
        # productos: iterable de filas (marca, id, sexo, talla, material, precio, stock, imagen_blob)
        # Guardamos y dibujamos
        self.productos_actuales = list(productos)
        # Limpiar
        for child in self.inner_frame.winfo_children():
            child.destroy()
        self.imagenes_cache.clear()

        # Crear cards
        for idx, fila in enumerate(self.productos_actuales):
            marca, idp, sexo, talla, material, precio, stock, imagen = fila
            card = ttk.Frame(self.inner_frame, style="Card.TFrame", width=300, height=CARD_HEIGHT)
            card.grid_propagate(False)  # forzar tamaño
            # Estilo visual del card: padding y borde sutil
            card.grid(row=0, column=idx, padx=10, pady=10)  # temporal; serán reorganizados por _recalcular_grid

            # Imagen (izq)
            left = ttk.Frame(card, style="Card.TFrame")
            left.grid(row=0, column=0, sticky="nsw", padx=(8,6), pady=8)
            if imagen:
                try:
                    img = Image.open(io.BytesIO(imagen))
                    img.thumbnail((100, 100))
                    img_tk = ImageTk.PhotoImage(img)
                    lbl_img = ttk.Label(left, image=img_tk, background=PALETA["panel"])
                    lbl_img.image = img_tk
                    lbl_img.pack()
                    self.imagenes_cache.append(img_tk)
                except Exception:
                    ttk.Label(left, text="(imagen)", style="CardText.TLabel").pack()
            else:
                ttk.Label(left, text="(sin imagen)", style="CardText.TLabel").pack()

            # Info (derecha)
            right = ttk.Frame(card, style="Card.TFrame")
            right.grid(row=0, column=1, sticky="nsew", padx=(4,8))
            card.columnconfigure(1, weight=1)
            ttk.Label(right, text=f"{marca}  ·  ID: {idp}", style="CardTitle.TLabel").pack(anchor="w")
            info_text = f"Sexo: {sexo}   Talla: {talla}\nMaterial: {material}   Stock: {stock}\nPrecio: {precio}"
            ttk.Label(right, text=info_text, style="CardText.TLabel", justify="left").pack(anchor="w", pady=(6,0))

        # Forzar reorganización y focus al inicio
        self._recalcular_grid(self.canvas.winfo_width())
        self.after(50, lambda: self.canvas.yview_moveto(0.0))  # volver al inicio

    def _recalcular_grid(self, width_px):
        # Calcula cuántas columnas caben según CARD_WIDTH + padding
        if width_px <= 0:
            return
        # El espacio util disponible es canvas width menos margen derecho para el panel lateral
        usable = width_px
        col_space = CARD_WIDTH + 20  # margen aprox por card
        cols = max(1, usable // col_space)
        # Reposicionar children en grid de filas/columnas
        children = self.inner_frame.winfo_children()
        for i, child in enumerate(children):
            r = i // cols
            c = i % cols
            child.grid_configure(row=r, column=c, padx=10, pady=10, sticky="n")
        # Actualizar scrollregion
        self.inner_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

# -------------------------
# Lanzador
# -------------------------
def main():
    root = tk.Tk()
    root.withdraw()  # ocultamos por ahora el root si queremos que app abra su propio UI
    app = App(root)
    root.deiconify()
    root.mainloop()


if __name__ == "__main__":
    main()
