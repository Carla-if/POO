-- ===============================================
-- CREACIÓN DE BASE DE DATOS Y TABLAS
-- ===============================================

CREATE DATABASE IF NOT EXISTS ferreteria;
USE ferreteria;

-- ===============================================
-- TABLA: empleados
-- ===============================================
CREATE TABLE IF NOT EXISTS empleados (
    id_empleado INTEGER PRIMARY KEY AUTO_INCREMENT,
    num_empleado TEXT NOT NULL UNIQUE,
    nombre TEXT NOT NULL,
    correo TEXT,
    fecha_nacimiento TEXT,
    puesto TEXT,
    usuario TEXT NOT NULL UNIQUE,
    contraseña TEXT NOT NULL
);

-- Insertar usuario administrador inicial
INSERT INTO empleados (num_empleado, nombre, correo, fecha_nacimiento, puesto, usuario, contraseña)
VALUES ('0001', 'Administrador General', 'admin@ferreteria.com', '1980-01-01', 'Administrador', 'admin', '1234');

-- ===============================================
-- TABLA: clientes
-- ===============================================
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INTEGER PRIMARY KEY AUTO_INCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT,
    correo TEXT,
    direccion TEXT,
    fecha_registro TEXT
);

-- ===============================================
-- TABLA: productos
-- ===============================================
CREATE TABLE IF NOT EXISTS productos (
    id_producto INTEGER PRIMARY KEY AUTO_INCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    categoria TEXT,
    precio REAL NOT NULL,
    cantidad INTEGER DEFAULT 0
);

-- ===============================================
-- TABLA: ventas
-- ===============================================
CREATE TABLE IF NOT EXISTS ventas (
    folio INTEGER PRIMARY KEY AUTO_INCREMENT,
    id_cliente INTEGER,
    id_empleado INTEGER,
    fecha TEXT,
    total REAL,
    detalles TEXT    -- Aquí se puede guardar un JSON con los productos vendidos
);

-- ===============================================
-- TABLA: actividad_empleados
-- (similar a actividad_trabajadores del ejemplo)
-- ===============================================
CREATE TABLE IF NOT EXISTS actividad_empleados (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    id_empleado INTEGER,
    fecha TEXT,
    accion TEXT
);