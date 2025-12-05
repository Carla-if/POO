from abc import ABC, abstractmethod
from datetime import datetime
import mysql.connector

BD = dict(host="localhost", user="root", password="", database="ferreteria")

def conn():
    return mysql.connector.connect(**BD)

# -------- CLASES ----------
class Persona(ABC):
    def __init__(self, nombre, correo):
        self.nombre = nombre
        self.correo = correo

    @abstractmethod
    def mostrar(self):
        pass

class Empleado(Persona):
    def __init__(self, num, nombre, correo, usuario, contrasena):
        super()._init_(nombre, correo)
        self.num = num
        self.usuario = usuario
        self.contrasena = contrasena

    def mostrar(self):
        print(f"[Empleado] {self.nombre} ({self.usuario})")

class Cliente(Persona):
    def __init__(self, nombre, correo, tel):
        super()._init_(nombre, correo)
        self.tel = tel

    def mostrar(self):
        print(f"[Cliente] {self.nombre}, Tel: {self.tel}")

class Producto:
    def __init__(self, codigo, nombre, precio, cantidad):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    def mostrar(self):
        print(f"[{self.codigo}] {self.nombre} ${self.precio} | Cant: {self.cantidad}")


# -------- FUNCIONES ----------
def alta_producto():
    print("\n--- Alta producto ---")
    codigo = input("Código: ")
    nombre = input("Nombre: ")
    precio = float(input("Precio: "))
    cant = int(input("Cantidad: "))
    c = conn(); cur = c.cursor()
    cur.execute("INSERT INTO productos (codigo,nombre,precio,cantidad) VALUES (%s,%s,%s,%s)",
                (codigo,nombre,precio,cant))
    c.commit(); c.close()
    print("Producto registrado.")

def alta_cliente():
    print("\n--- Alta cliente ---")
    nombre = input("Nombre: ")
    correo = input("Correo: ")
    tel = input("Teléfono: ")
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c = conn(); cur = c.cursor()
    cur.execute("INSERT INTO clientes (nombre,correo,telefono,fecha_registro) VALUES (%s,%s,%s,%s)",
                (nombre,correo,tel,fecha))
    c.commit(); c.close()
    print("Cliente registrado.")

def mostrar_productos():
    c = conn(); cur = c.cursor(dictionary=True)
    cur.execute("SELECT * FROM productos")
    for p in cur.fetchall():
        print(f"[{p['codigo']}] {p['nombre']} ${p['precio']} | Cant: {p['cantidad']}")
    c.close()

def mostrar_clientes():
    c = conn(); cur = c.cursor(dictionary=True)
    cur.execute("SELECT * FROM clientes")
    for x in cur.fetchall():
        print(f"[{x['id_cliente']}] {x['nombre']} - {x['telefono']}")
    c.close()

def vender(empleado):
    print("\n--- Vender producto ---")
    mostrar_productos()
    cod = input("Código del producto: ")
    cant = int(input("Cantidad: "))
    c = conn(); cur = c.cursor(dictionary=True)

    cur.execute("SELECT * FROM productos WHERE codigo=%s", (cod,))
    p = cur.fetchone()
    if not p:
        print("No existe."); c.close(); return
    if p["cantidad"] < cant:
        print("Inventario insuficiente."); c.close(); return

    total = p["precio"] * cant
    nueva = p["cantidad"] - cant

    cur.execute("UPDATE productos SET cantidad=%s WHERE codigo=%s", (nueva, cod))
    cur.execute("INSERT INTO ventas (id_empleado,fecha,total,detalles) VALUES (%s,%s,%s,%s)",
                (empleado, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), total, f"{cod} x{cant}"))
    c.commit(); c.close()
    print("Venta registrada. Total:", total)

def mostrar_ventas():
    c = conn(); cur = c.cursor(dictionary=True)
    cur.execute("SELECT * FROM ventas ORDER BY folio DESC")
    for v in cur.fetchall():
        print(f"[{v['folio']}] {v['fecha']} | Total: {v['total']} | {v['detalles']}")
    c.close()


def iniciar_sesion():
    print("\n== Iniciar Sesión ==")
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")

    c = conn(); cur = c.cursor(dictionary=True)
    cur.execute("SELECT * FROM empleados WHERE usuario=%s AND contraseña=%s", (usuario,contraseña))
    r = cur.fetchone()
    c.close()
    if r:
        print("Bienvenido,", r["nombre"])
        return r["id_empleado"]
    else:
        print("Credenciales incorrectas.")
        return None


def menu():
    emp = None
    while not emp:
        emp = iniciar_sesion()

    while True:
        print("\n--- MENÚ ---")
        print("1. Alta producto")
        print("2. Alta cliente")
        print("3. Mostrar productos")
        print("4. Mostrar clientes")
        print("5. Registrar venta")
        print("6. Mostrar ventas")
        print("7. Cerrar sesión")
        op = input("Opción: ")

        if op=="1": alta_producto()
        elif op=="2": alta_cliente()
        elif op=="3": mostrar_productos()
        elif op=="4": mostrar_clientes()
        elif op=="5": vender(emp)
        elif op=="6": mostrar_ventas()
        elif op=="7":
            print("Cerrando sesión...\n")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()