
DROP TABLE IF EXISTS movimientos CASCADE;
DROP TABLE IF EXISTS categorias CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;


CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    token_recuperacion VARCHAR(255) DEFAULT NULL,    
    codigo_expira TIMESTAMP DEFAULT NULL,           
    codigo_intentos INTEGER DEFAULT 0,             
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('ingreso', 'gasto')),
    icono VARCHAR(50) DEFAULT 'tag'
);


CREATE TABLE movimientos (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    categoria_id INTEGER REFERENCES categorias(id) ON DELETE SET NULL,
    monto NUMERIC(10, 2) NOT NULL CHECK (monto > 0),
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('ingreso', 'gasto')),
    descripcion VARCHAR(255) NOT NULL,
    fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    estado VARCHAR(20) NOT NULL DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'pagado')),
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX idx_movimientos_usuario ON movimientos(usuario_id);
CREATE INDEX idx_movimientos_fecha ON movimientos(fecha);
