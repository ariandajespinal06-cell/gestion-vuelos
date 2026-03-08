CREATE TABLE IF NOT EXISTS roles (
    id     SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS permisos (
    id     SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS rol_permiso (
    id         SERIAL PRIMARY KEY,
    rol_id     INTEGER NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    permiso_id INTEGER NOT NULL REFERENCES permisos(id) ON DELETE CASCADE,
    UNIQUE(rol_id, permiso_id)
);

CREATE TABLE IF NOT EXISTS usuarios (
    id             SERIAL PRIMARY KEY,
    nombre         VARCHAR(100) NOT NULL,
    correo         VARCHAR(150) NOT NULL UNIQUE,
    password       VARCHAR(255) NOT NULL,
    rol_id         INTEGER NOT NULL REFERENCES roles(id),
    estado         BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT NOW()
);

INSERT INTO roles (nombre) VALUES
    ('admin'),('agente'),('cliente')
ON CONFLICT (nombre) DO NOTHING;

INSERT INTO permisos (nombre) VALUES
    ('crear_usuario'),('editar_usuario'),('eliminar_usuario'),
    ('ver_usuarios'),('gestionar_vuelos'),('gestionar_reservas'),
    ('ver_vuelos'),('ver_reservas'),('realizar_reserva'),('cancelar_reserva')
ON CONFLICT (nombre) DO NOTHING;

INSERT INTO rol_permiso (rol_id, permiso_id)
SELECT r.id, p.id FROM roles r, permisos p
WHERE r.nombre = 'admin'
ON CONFLICT DO NOTHING;

INSERT INTO rol_permiso (rol_id, permiso_id)
SELECT r.id, p.id FROM roles r, permisos p
WHERE r.nombre = 'agente'
  AND p.nombre IN ('gestionar_vuelos','gestionar_reservas','ver_vuelos','ver_reservas','ver_usuarios')
ON CONFLICT DO NOTHING;

INSERT INTO rol_permiso (rol_id, permiso_id)
SELECT r.id, p.id FROM roles r, permisos p
WHERE r.nombre = 'cliente'
  AND p.nombre IN ('realizar_reserva','cancelar_reserva','ver_vuelos','ver_reservas')
ON CONFLICT DO NOTHING;