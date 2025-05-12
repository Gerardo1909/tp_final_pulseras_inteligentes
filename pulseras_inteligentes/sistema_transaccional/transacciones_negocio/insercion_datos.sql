-- POBLADO DE TABLAS

-- Géneros
INSERT INTO genero (genero) VALUES
('Masculino'),
('Femenino'),
('Prefiero no decirlo');

-- Planes
INSERT INTO planes (nombre_plan, descripcion, duracion_dias) VALUES
('Básico', 'Acceso limitado a funcionalidades básicas.', 30),
('Estándar', 'Acceso completo durante 3 meses.', 90),
('Premium', 'Acceso completo con beneficios exclusivos por 1 año.', 365);

-- Métodos de pago
INSERT INTO metodo_pago (descripcion) VALUES
('Tarjeta de crédito'),
('PayPal'),
('Transferencia bancaria');

-- Estados de pago
INSERT INTO estado_pago (descripcion) VALUES
('Aprobado'),
('Pendiente'),
('Rechazado');

-- Estados de suscripción
INSERT INTO estado_suscripcion (descripcion) VALUES
('Activa'),
('Cancelada');

-- Usuarios
INSERT INTO usuarios (nombre, email, fecha_nacimiento, id_genero, fecha_registro) VALUES
('Ana Gómez', 'ana.gomez@example.com', '1995-03-12', 2, NOW()),
('Luis Martínez', 'luis.martinez@example.com', '1990-07-08', 1, NOW()),
('Sofía Pérez', 'sofia.perez@example.com', '2000-11-20', 2, NOW()),
('Diego Torres', 'diego.torres@example.com', '1988-02-25', 1, NOW()),
('Alex Rivera', 'alex.rivera@example.com', '1998-06-14', 3, NOW());

-- Pagos
INSERT INTO pagos (id_metodo_pago, monto, fecha_transaccion, id_estado_pago, id_usuario) VALUES
(1, 9.99, NOW(), 1, 1),
(2, 24.99, NOW(), 1, 2),
(3, 49.99, NOW(), 1, 3),
(1, 49.99, NOW(), 1, 4),
(2, 9.99, NOW(), 1, 5);

-- Suscripciones
INSERT INTO suscripcion (id_usuario, id_plan, fecha_inicio, fecha_fin, id_estado, id_pago) VALUES
(1, 1, NOW(), NOW() + INTERVAL '30 days', 1, 1),
(2, 2, NOW(), NOW() + INTERVAL '90 days', 1, 2),
(3, 3, NOW(), NOW() + INTERVAL '365 days', 1, 3),
(4, 3, NOW(), NOW() + INTERVAL '365 days', 1, 4),
(5, 1, NOW(), NOW() + INTERVAL '30 days', 1, 5);