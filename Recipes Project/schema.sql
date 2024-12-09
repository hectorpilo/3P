CREATE TABLE producto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    calorias FLOAT,
    unidad_medida VARCHAR(20)
);

CREATE TABLE consumo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha DATETIME NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad FLOAT NOT NULL,
    FOREIGN KEY (producto_id) REFERENCES producto (id)
);

-- Datos de ejemplo
INSERT INTO producto (nombre, calorias, unidad_medida) VALUES
    ('Manzana', 52, 'unidad'),
    ('Arroz', 130, 'gramos'),
    ('Leche', 42, 'ml'),
    ('Pan', 265, 'unidad'),
    ('Pollo', 165, 'gramos'); 