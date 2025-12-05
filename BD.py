import sqlite3 as sql

def ruta_db(nombre_db="CalzaIsoft.db"):
    import sys, os
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, nombre_db)

def Conex():
    ruta = ruta_db()
    conexion = sql.connect(ruta)
    conexion.execute("PRAGMA foreign_keys = ON;")
    cursor = conexion.cursor()
    return conexion,cursor



def crear_Tabla():
        conexion,cursor = Conex()
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS VANS (
        Id_Producto TEXT PRIMARY KEY,
        Sexo TEXT,
        Talla INTEGER,
        Color TEXT,
        Material Text,
        Tipo TEXT,
        Precio FLOAT,
        Stock INTEGER
        )  
        """)
        conexion.commit()
        conexion.close()

def Eliminar_tabla(Tabla):
        conexion,cursor = Conex()
        cursor.execute(f"DROP TABLE {Tabla}")
        conexion.commit()
        conexion.close()

def agregar_nuevo_zapato(tabla, id, sexo, talla, color, material, tipo, precio, stock, datos):
    conexion, cursor = Conex()
    try:
        query = f"""
            INSERT INTO {tabla}
            (id_producto, sexo, talla, color, material, tipo, precio, stock, imagen)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(query, (
            id,
            sexo,
            talla,
            color,
            material,
            tipo,
            precio,
            stock,
            datos   # bytes de la imagen
        ))

        mensaje = "Producto agregado correctamente"
        conexion.commit()

    except sql.IntegrityError:
        mensaje = "Error: el ID del producto ya existe o hay conflicto de integridad."
    except sql.OperationalError as e:
        mensaje = f"Error de operación {e}"
    except Exception as e:
        mensaje = f"Ocurrió un error inesperado: {e}"
    finally:
        conexion.close()

    return mensaje
def mostrar_datos(Tabla):
        conexion,cursor = Conex()
        cursor.execute(f"Select * from {Tabla}")
        filas = cursor.fetchall()

        for filas in filas:
                print(filas)
        
        conexion.close()

def Eliminar_Zapato(Tabla,Id):
        conexion,cursor = Conex()
        try:
                cursor.execute(f"DELETE FROM {Tabla} WHERE Id_Producto = '{Id}'")
                conexion.commit()
                if cursor.rowcount == 0:
                        mensaje = ("No se encontro el producto")
                else:
                        mensaje = ("Producto eliminado")
        except sql.OperationalError as e:
                mensaje = (f"Ocurrio un error operacional {e}")
        except sql.IntegrityError as e:
                mensaje = (f"Ocurrio un error de Integridad {e}")
        except Exception as e:
                mensaje = (f"Ocurrio un error {e}")
        finally:
                conexion.close()
        return mensaje

def Modificar_Precio(tabla,id,precio):
        conexion,cursor = Conex()
        try:
                cursor.execute(f"""
                UPDATE {tabla}
                SET Precio = {precio}
                WHERE Id_Producto = '{id}'""")
                conexion.commit()
                if cursor.rowcount == 0:
                        msg = ("No se encontro el producto para actualizar")
                else:
                        msg = ("Precio Actualizado correctamente")
                        
        except Exception as e:
                msg = (f"Ocurrio un error {e}")
        except sql.OperationalError as e:
                msg = (f"Ocurrio un error operacional {e}")
        except sql.IntegrityError as e:
                msg = (f"Ocurrio un error de integridad {e}")
        finally:
                conexion.close()
        return msg

def buscar_precio(tabla,id):
        conexion,cursor = Conex()
        cursor.execute(f"SELECT precio FROM '{tabla}' WHERE Id_Producto = '{id}'")
        fila = cursor.fetchone()
        conexion.close()
        return fila[0] if fila else ""


def Agregar_Stock(Tabla,agregado,id):
        conexion,cursor = Conex()
        cursor.execute(f"""
        UPDATE {Tabla}
        SET Stock = Stock + {agregado}
        WHERE Id_Producto = '{id}'
        """)
        conexion.commit()
        conexion.close()

def Eliminar_Stock(Tabla,eliminado,id):
        conexion,cursor = Conex()
        cursor.execute(f"""
        UPDATE {Tabla}
        SET Stock = Stock - {eliminado}
        WHERE Id_Producto = '{id}'
        """)
        conexion.commit()
        conexion.close()


def Agregar_Administrador(usuario,contra,id):
        conexion,cursor = Conex()
        cursor.execute(f"SELECT Id FROM Empleados WHERE Id = '{id}'")
        fila = cursor.fetchone()
        if fila is None:
                print("El empleado no existe")
        else:
                cursor.execute(f"INSERT INTO Administradores VALUES ('{usuario}','{contra}','{id}')")
                cursor.execute(f"UPDATE Empleados SET Rol = 'Administrador' WHERE id = '{id}'")
        conexion.commit()
        conexion.close()

def Eliminar_Administrador(usuario,rol):
        conexion,cursor = Conex()
        cursor.execute(f"SELECT Id_Empleado FROM Administradores WHERE Usuario = '{usuario}'")
        fila = cursor.fetchone()
        id = fila[0]
        cursor.execute(f"UPDATE Empleados SET Rol = '{rol}' WHERE Id = '{id}'")
        cursor.execute(f"DELETE FROM Administradores WHERE Usuario = '{usuario}' ")
        conexion.commit()
        conexion.close()

def Actualizar_contra(Usuario,contra):
        conexion,cursor = Conex()
        cursor.execute(f"""
        UPDATE Administradores
        SET Contra = '{contra}'
        WHERE Usuario = '{Usuario}'""")
        conexion.commit()
        conexion.close()

def Agregar_Empleado(id,nombre,ap_paterno,ap_materno,telefono,direccion,anti,rol,contra):
        conexion,cursor = Conex()
        cursor.execute(f"INSERT INTO Empleados VALUES('{id}','{nombre}','{ap_paterno}','{ap_materno}','{telefono}','{direccion}','{anti}','{rol}','{contra}')")
        conexion.commit()
        conexion.close()

def Eliminar_Empleado(id):
        conexion,cursor = Conex()
        cursor.execute(f"SELECT Rol FROM Empleados WHERE Id = '{id}'")
        fila = cursor.fetchone()
        rol = fila[0]
        cursor.execute(f"DELETE FROM Empleados WHERE Id = '{id}'")
        conexion.commit()
        if rol == "Administrador":
                cursor.execute(f"DELETE FROM Administradores WHERE Id_Empleado = '{id}'")
                conexion.commit()
        conexion.close()

def comparar_contra(usuario,contra):
        conexion,cursor = Conex()
        cursor.execute(f"SELECT contra from Empleados WHERE Nombre = '{usuario}'")
        fila = cursor.fetchone()
        conexion.close()
        if fila is None:
                return False
        return contra == fila[0]

def comparar_Admin(usuario,contra):
        conexion,cursor = Conex()
        cursor.execute(f"SELECT contra from Administradores WHERE Usuario = '{usuario}'")
        fila = cursor.fetchone()
        conexion.close()
        if fila is None:
                return False
        return contra == fila[0]
'''
def imprimir(tabla):
        conexion,cursor = Conex()
        cursor.execute(f"SELECT * FROM {tabla}")
        filas = cursor.fetchall()
        columnas = [descripcion[0] for descripcion in cursor.description]
        print(" | ".join(columnas))
        print("-" * (len(" | ".join(columnas)) + 5))
        for fila in filas:
                 print(" | ".join(str(campo) for campo in fila))
        conexion.close()
'''
def Stock_Total(tabla):
        conexion,cursor = Conex()
        cursor.execute(f"SELECT SUM(Stock) FROM  {tabla} AS Stock_Total")
        resultado = cursor.fetchone()[0]
        columna = [descripcion[0] for descripcion in cursor.description]
        print("Stock Total")
        print(resultado)

def Sin_Stock():
    conexion, cursor = Conex()
    cursor.execute("""
        SELECT 'Adidas' AS Marca, Id_Producto, Sexo, Talla, Material, Precio, Stock, Imagen
        FROM Adidas
        WHERE Stock = 0 OR Stock IS NULL

        UNION ALL

        SELECT 'Converse', Id_Producto, Sexo, Talla, Material, Precio, Stock, Imagen
        FROM Converse
        WHERE Stock = 0 OR Stock IS NULL

        UNION ALL

        SELECT 'Nike', Id_Producto, Sexo, Talla, Material, Precio, Stock, Imagen
        FROM Nike
        WHERE Stock = 0 OR Stock IS NULL

        UNION ALL

        SELECT 'Puma', Id_Producto, Sexo, Talla, Material, Precio, Stock, Imagen
        FROM Puma
        WHERE Stock = 0 OR Stock IS NULL

        UNION ALL

        SELECT 'Skechers', Id_Producto, Sexo, Talla, Material, Precio, Stock, Imagen
        FROM Skechers
        WHERE Stock = 0 OR Stock IS NULL

        UNION ALL

        SELECT 'VANS', Id_Producto, Sexo, Talla, Material, Precio, Stock, Imagen
        FROM VANS
        WHERE Stock = 0 OR Stock IS NULL
    """)
    datos = cursor.fetchall()
    conexion.close()
    return datos

'''
    print("Marca | ID | Precio | Stock")
    print("---------------------------------")
    for fila in datos:
        print(f"{fila[0]} | {fila[1]} | {fila[2]} | {fila[3]}")
'''

def Precio_Medio():
        conexion,cursor = Conex()
        cursor.execute("""
        SELECT 'Adidas' AS Marca, AVG(Precio) AS Precio_Medio
        FROM Adidas
        UNION ALL
        SELECT 'Converse', AVG(Precio) 
        FROM Converse
        UNION ALL
        SELECT 'Nike', AVG(Precio) 
        FROM Nike
        UNION ALL
        SELECT 'Puma', AVG(Precio) 
        FROM Puma
        UNION ALL
        SELECT 'Skechers', AVG(Precio)
        FROM Skechers
        UNION ALL
        SELECT 'VANS', AVG(Precio) 
        FROM VANS
        """)
        filas = cursor.fetchall()
        columnas = [descripcion[0] for descripcion in cursor.description]
        print(" | ".join(columnas))
        print("-" * (len(" | ".join(columnas)) + 5))
        for fila in filas:
                 print(" | ".join(str(campo) for campo in fila))
        conexion.close()
'''
def Ganancias_Esperadas():
        conexion,cursor = Conex()
        cursor.execute("""
        SELECT 'Adidas' AS Marca, SUM(Precio) AS Total_Invertido, SUM(Precio) + (SUM(Precio)*.20) AS Ganancia_Esperada
        FROM Adidas
        UNION ALL
        SELECT 'Converse', SUM(Precio) AS Total_Invertido, SUM(Precio) + (SUM(Precio)*.20) AS Ganancia_Esperada
        FROM Converse
        UNION ALL
        SELECT 'Nike', SUM(Precio) AS Total_Invertido, SUM(Precio) + (SUM(Precio)*.20) AS Ganancia_Esperada
        FROM Nike
        UNION ALL
        SELECT 'Puma', SUM(Precio) AS Total_Invertido, SUM(Precio) + (SUM(Precio)*.20) AS Ganancia_Esperada
        FROM Puma
        UNION ALL
        SELECT 'Skechers', SUM(Precio) AS Total_Invertido, SUM(Precio) + (SUM(Precio)*.20) AS Ganancia_Esperada
        FROM Skechers
        UNION ALL
        SELECT 'VANS', SUM(Precio) AS Total_Invertido, SUM(Precio) + (SUM(Precio)*.20) AS Ganancia_Esperada
        FROM VANS
        """)
        filas = cursor.fetchall()
        columnas = [descripcion[0] for descripcion in cursor.description]
        print(" | ".join(columnas))
        print("-" * (len(" | ".join(columnas)) + 5))
        for fila in filas:
                 print(" | ".join(str(campo) for campo in fila))
        conexion.close()
'''


def guardar_imagen_blob(tabla, id_producto, ruta_imagen):
    conexion, cursor = Conex()

    try:
        with open(ruta_imagen, "rb") as f:
            datos = f.read()

        cursor.execute(
            f"UPDATE {tabla} SET Imagen = ? WHERE Id_Producto = ?",
            (datos, id_producto)
        )

        conexion.commit()

        if cursor.rowcount == 0:
            return "No se encontró el producto para asignar imagen."
        
        return "Imagen guardada correctamente."

    except Exception as e:
        return f"Ocurrió un error: {e}"

    finally:
        conexion.close()

def Imagen(ruta):
       try:
              with open(ruta, "rb") as f:
                     datos = f.read()
                     return datos
       except:
              print("Ocurrio un error")


def obtener_productos(tabla):
    conn,cursor = Conex()
    cursor.execute(f"SELECT '{tabla}' AS MARCA, Id_Producto, Sexo, Talla, Material, Precio, Stock, Imagen FROM {tabla}")
    datos = cursor.fetchall()
    conn.close()
    return datos

def obtener_todo():
    conexion, cursor = Conex()
    cursor.execute("""
        SELECT 'Adidas' AS Marca, Id_Producto, Sexo, Talla, Material, Precio, Stock, Imagen
        FROM Adidas

        UNION ALL

        SELECT 'Converse', Id_Producto,  Sexo, Talla, Material, Precio, Stock, Imagen
        FROM Converse

        UNION ALL

        SELECT 'Nike', Id_Producto,  Sexo, Talla, Material, Precio, Stock, Imagen
        FROM Nike


        UNION ALL

        SELECT 'Puma', Id_Producto,  Sexo, Talla, Material, Precio, Stock, Imagen
        FROM Puma

        UNION ALL

        SELECT 'Skechers', Id_Producto,  Sexo, Talla, Material, Precio, Stock, Imagen
        FROM Skechers

        UNION ALL

        SELECT 'VANS', Id_Producto, Sexo, Talla, Material, Precio, Stock, Imagen
        FROM VANS
    """)
    datos = cursor.fetchall()
    conexion.close()
    return datos



def hacer_scroll_con_rueda(canvas, evento):
    if evento.num == 5 or evento.delta < 0:    
        canvas.yview_scroll(1, "units")
    elif evento.num == 4 or evento.delta > 0:   
        canvas.yview_scroll(-1, "units")
'''
print("Datos Tabla Adidas:")
imprimir("Adidas")
print(" ")
print("Datos Tabla Nike:")
imprimir("Nike")
print(" ")
print("Datos Tabla Converse:")
imprimir("Converse")
print(" ")
print("Datos Tabla Nike:")
imprimir("Nike")
print(" ")
print("Datos Tabla Puma:")
imprimir("Puma")
print(" ")
print("Datos Tabla Skechers:")
print(" ")
imprimir("Skechers")
print(" ")
print("Datos Tabla VANS:")
imprimir("VANS")


print("Adidas")
Stock_Total("Adidas")
print("Nike")
Stock_Total("Nike")
print("Converse")
Stock_Total("Converse")
print("Puma")
Stock_Total("Puma")
print("Skechers")
Stock_Total("Skechers")
print("VANS")
Stock_Total("VANS")

print(" ")
print("Productos sin stock:")
Sin_Stock()

print(" ")
print("Precio medio de producto por tabla:")
Precio_Medio()
print(" ")
print("Ganancias esperadas por tabla:")
Ganancias_Esperadas()
'''
