
INSERT INTO categorias (nombre, tipo, icono) VALUES

('Comida y Almuerzos', 'gasto', 'utensils'),
('Transporte y Pasajes', 'gasto', 'bus'),
('Fotocopias y Libros', 'gasto', 'book-open'),
('Ocio y Salidas', 'gasto', 'coffee'),
('Servicios e Internet', 'gasto', 'wifi'),
('Otros Gastos', 'gasto', 'more-horizontal'),

('Beca Universitaria', 'ingreso', 'award'),
('Apoyo Familiar', 'ingreso', 'heart'),
('Trabajo / Pasantía', 'ingreso', 'briefcase'),
('Otros Ingresos', 'ingreso', 'dollar-sign');


INSERT INTO usuarios (nombre, email, password_hash) VALUES
(
    'Demo',
    'estudiante@demo.com',
    'scrypt:32768:8:1$pGzHbi6DOU2ULTKG$0cdc943613a5b934c321a2c34e39e2aef02d4e8f1014535eae8162898e5da84e81025fcfbf7b96a2836e5c242a8ddf23bd02141c4a467eb64531ed5002bc7ff9'
);


INSERT INTO movimientos (usuario_id, categoria_id, monto, tipo, descripcion, fecha) VALUES
(1, 7, 500.00, 'ingreso', 'Depósito de Beca Estudiantil', CURRENT_DATE - INTERVAL '5 days'),
(1, 8, 200.00, 'ingreso', 'Ayuda familiar para el mes', CURRENT_DATE - INTERVAL '4 days'),
(1, 1, 35.50, 'gasto', 'Almuerzo en cafetería universitaria', CURRENT_DATE - INTERVAL '3 days'),
(1, 2, 12.00, 'gasto', 'Recarga tarjeta de transporte', CURRENT_DATE - INTERVAL '2 days'),
(1, 3, 25.00, 'gasto', 'Fotocopias de guía de estudio IHC', CURRENT_DATE - INTERVAL '1 day'),
(1, 4, 18.00, 'gasto', 'Café con compañeros de grupo', CURRENT_DATE);
