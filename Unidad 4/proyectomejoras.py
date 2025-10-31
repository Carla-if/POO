class Persona:
    def __init__(self, nombre, correo, direccion, telefono):
        self.nombre = nombre
        self.correo = correo
        self.direccion = direccion
        self.telefono = telefono

    def mostrar_info(self):
        print(f"Nombre: {self.nombre} | Correo: {self.correo} | Dirección: {self.direccion} | Teléfono: {self.telefono}")

class Cliente(Persona):
    def __init__(self, nombre, correo, direccion, telefono, rfc):
        super().__init__(nombre, correo, direccion, telefono)
        self.rfc = rfc

    def mostrar_info(self):
        super().mostrar_info()
        print(f"RFC: {self.rfc}")

class Empleado(Persona):
    def __init__(self, nombre, correo, direccion, telefono, id_empleado, departamento, usuario, contrasena):
        super().__init__(nombre, correo, direccion, telefono)
        self.id_empleado = id_empleado
        self.departamento = departamento
        self.usuario = usuario
        self.contrasena = contrasena

    def mostrar_info(self):
        super().mostrar_info()
        print(f"ID Empleado: {self.id_empleado} | Departamento: {self.departamento}")

class Producto:
    def __init__(self, codigo, nombre, categoria, precio_unitario):
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.precio_unitario = precio_unitario

    def mostrar_info(self):
        print(f"Código: {self.codigo} | Nombre: {self.nombre} | Categoría: {self.categoria} | Precio: ${self.precio_unitario:.2f}")

class InventarioProducto:
    def __init__(self, producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad
        self.vendidos = 0

    def disponibles(self):
        return self.cantidad - self.vendidos

    def vender(self, cantidad):
        if cantidad <= self.disponibles():
            self.vendidos += cantidad
            print(f"Venta registrada: {cantidad} unidades de {self.producto.nombre}")
            return True
        else:
            print("No hay suficiente inventario disponible.")
            return False

    def agregar_stock(self, cantidad):
        self.cantidad += cantidad
        print(f"Se agregaron {cantidad} unidades al inventario de {self.producto.nombre}")

    def mostrar_estado(self):
        self.producto.mostrar_info()
        print(f"Existencia total: {self.cantidad} | Vendidos: {self.vendidos} | Disponibles: {self.disponibles()}")

class Venta:
    def __init__(self, folio, id_cliente, codigo_producto, fecha, cantidad, total):
        self.folio = folio
        self.id_cliente = id_cliente
        self.codigo_producto = codigo_producto
        self.fecha = fecha
        self.cantidad = cantidad
        self.total = total

    def mostrar_info(self):
        print(f"Folio: {self.folio} | Cliente: {self.id_cliente} | Producto: {self.codigo_producto} | Fecha: {self.fecha} | Cantidad: {self.cantidad} | Total: ${self.total:.2f}")

# Datos en memoria
productos = []
inventario = []
clientes = []
empleados = []
ventas = []
folio_actual = 1
sesion_activa = None

from datetime import datetime

# Empleado administrador por defecto
empleados.append(Empleado("Admin", "admin@ferre.com", "Sucursal Central", "555-0000", "E001", "Administración", "admin", "1234"))

def buscar_producto(codigo):
    for item in inventario:
        if item.producto.codigo == codigo:
            return item
    return None

def buscar_cliente(id_cliente):
    for cliente in clientes:
        if cliente.rfc == id_cliente:
            return cliente
    return None

def login():
    global sesion_activa
    print("\n INICIO DE SESIÓN")
    usuario = input("Usuario: ")
    contrasena = input("Contraseña: ")
    for emp in empleados:
        if emp.usuario == usuario and emp.contrasena == contrasena:
            sesion_activa = emp
            print(f"Bienvenido, {emp.nombre} ({emp.departamento})")
            return True
    print("Credenciales incorrectas.")
    return False

def logout():
    global sesion_activa
    sesion_activa = None
    print("Sesión cerrada.")

def menu():
    global folio_actual
    while True:
        if not sesion_activa:
            if not login():
                continue

        print("\n MENÚ PRINCIPAL")
        print("1. Dar de alta un producto")
        print("2. Mostrar inventario de productos")
        print("3. Consultar producto por código")
        print("4. Registrar cliente")
        print("5. Consultar cliente por RFC")
        print("6. Mostrar todos los clientes")
        print("7. Registrar una venta")
        print("8. Mostrar historial de ventas")
        print("9. Cerrar sesión")
        print("10. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            codigo = input("Código del producto: ")
            nombre = input("Nombre: ")
            categoria = input("Categoría: ")
            precio = float(input("Precio unitario: "))
            cantidad = int(input("Cantidad inicial: "))
            nuevo_producto = Producto(codigo, nombre, categoria, precio)
            productos.append(nuevo_producto)
            inventario.append(InventarioProducto(nuevo_producto, cantidad))
            print("Producto registrado.")

        elif opcion == "2":
            for item in inventario:
                item.mostrar_estado()

        elif opcion == "3":
            codigo = input("Código del producto: ")
            item = buscar_producto(codigo)
            if item:
                item.mostrar_estado()
            else:
                print("Producto no encontrado.")

        elif opcion == "4":
            nombre = input("Nombre: ")
            correo = input("Correo: ")
            direccion = input("Dirección: ")
            telefono = input("Teléfono: ")
            rfc = input("RFC: ")
            clientes.append(Cliente(nombre, correo, direccion, telefono, rfc))
            print("Cliente registrado.")

        elif opcion == "5":
            rfc = input("RFC del cliente: ")
            cliente = buscar_cliente(rfc)
            if cliente:
                cliente.mostrar_info()
            else:
                print("Cliente no encontrado.")

        elif opcion == "6":
            for cliente in clientes:
                cliente.mostrar_info()

        elif opcion == "7":
            rfc = input("RFC del cliente (999999 para público general): ")
            codigo = input("Código del producto: ")
            cantidad = int(input("Cantidad a vender: "))
            item = buscar_producto(codigo)
            if item and item.vender(cantidad):
                total = item.producto.precio_unitario * cantidad
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                venta = Venta(folio_actual, rfc, codigo, fecha, cantidad, total)
                ventas.append(venta)
                folio_actual += 1
                print("Venta registrada.")
            else:
                print("No se pudo completar la venta.")

        elif opcion == "8":
            for venta in ventas:
                venta.mostrar_info()

        elif opcion == "9":
            logout()

        elif opcion == "10":
            print("Gracias por usar el sistema. ¡Hasta pronto!")
            break

        else:
            print("Opción inválida. Intente de nuevo.")

menu()

