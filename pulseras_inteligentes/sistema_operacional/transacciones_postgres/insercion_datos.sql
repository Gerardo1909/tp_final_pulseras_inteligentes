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
('Martín Torres', 'martin.torres@gmail.com', '1990-01-01', 1, '2025-01-02'),
('Lucía Fernández', 'lucia.fernandez@yahoo.com', '1989-02-02', 2, '2025-01-10'),
('Carlos Méndez', 'carlos.mendez@hotmail.com', '1991-03-03', 1, '2025-01-15'),
('Paula Sosa', 'paula.sosa@gmail.com', '1988-04-04', 2, '2025-02-01'),
('Alex Moreno', 'alex.moreno@outlook.com', '1992-05-05', 3, '2025-02-12'),
('Javier Paredes', 'javier.paredes@gmail.com', '1993-06-06', 1, '2025-03-01'),
('Sofía Aguirre', 'sofia.aguirre@hotmail.com', '1994-07-07', 2, '2025-03-10'),
('Fernando Salas', 'fernando.salas@yahoo.com', '1995-08-08', 1, '2025-04-05'),
('Camila Ríos', 'camila.rios@gmail.com', '1996-09-09', 2, '2025-04-20'),
('Valentina Suárez', 'valentina.suarez@outlook.com', '1997-10-10', 3, '2025-05-01'),
('Tomás Giménez', 'tomas.gimenez@gmail.com', '1998-11-11', 1, '2025-05-15'),
('Marina Álvarez', 'marina.alvarez@yahoo.com', '1999-12-12', 2, '2025-06-01'),
('Nicolás Herrera', 'nicolas.herrera@gmail.com', '2000-01-13', 1, '2025-06-10'),
('Florencia Vidal', 'florencia.vidal@hotmail.com', '1987-02-14', 2, '2025-06-20'),
('Dana Castro', 'dana.castro@gmail.com', '1986-03-15', 3, '2025-07-01'),
('Agustín Vera', 'agustin.vera@gmail.com', '1985-04-16', 1, '2025-07-10'),
('Julieta Navarro', 'julieta.navarro@outlook.com', '1984-05-17', 2, '2025-07-20'),
('Ramiro Díaz', 'ramiro.diaz@gmail.com', '1983-06-18', 1, '2025-08-01'),
('Milagros Domínguez', 'milagros.dominguez@gmail.com', '1982-07-19', 2, '2025-08-15'),
('Tobías Molina', 'tobias.molina@hotmail.com', '1981-08-20', 3, '2025-09-01');

-- Pagos
INSERT INTO pagos (id_metodo_pago, monto, fecha_transaccion, id_estado_pago, id_usuario) VALUES
-- Aprobados
(1, 9.99, '2025-01-03', 1, 1), (2, 24.99, '2025-01-12', 1, 2), (3, 49.99, '2025-01-20', 1, 3),
(1, 24.99, '2025-02-02', 1, 4), (2, 9.99, '2025-02-15', 1, 5), (3, 49.99, '2025-03-03', 1, 6),
(1, 24.99, '2025-03-11', 1, 7), (2, 9.99, '2025-04-06', 1, 8), (3, 49.99, '2025-04-21', 1, 9),
(1, 9.99, '2025-05-03', 1, 10), (2, 24.99, '2025-05-16', 1, 11), (3, 49.99, '2025-06-02', 1, 12),
(1, 9.99, '2025-06-11', 1, 13), (2, 24.99, '2025-06-21', 1, 14), (3, 49.99, '2025-07-02', 1, 15),
(1, 24.99, '2025-07-11', 1, 16), (2, 9.99, '2025-07-21', 1, 17), (3, 49.99, '2025-08-02', 1, 18),
(1, 9.99, '2025-08-16', 1, 19), (2, 24.99, '2025-09-02', 1, 20),

-- Pendientes
(1, 9.99, '2025-01-10', 2, 1), (2, 24.99, '2025-02-05', 2, 4), (3, 49.99, '2025-03-01', 2, 7),
(1, 9.99, '2025-04-01', 2, 9), (2, 24.99, '2025-05-01', 2, 11), (3, 49.99, '2025-06-01', 2, 13),

-- Rechazados
(1, 9.99, '2025-01-05', 3, 2), (2, 24.99, '2025-02-10', 3, 5), (3, 49.99, '2025-03-15', 3, 8),
(1, 9.99, '2025-04-10', 3, 10), (2, 24.99, '2025-05-20', 3, 12), (3, 49.99, '2025-06-10', 3, 14),

-- Repeticiones / más pagos de usuarios activos
(1, 24.99, '2025-08-10', 1, 1), (1, 24.99, '2025-1-10', 1, 1),
(2, 9.99, '2025-08-20', 1, 2), (3, 49.99, '2025-08-25', 1, 3),
(2, 9.99, '2025-09-01', 1, 4), (3, 49.99, '2025-09-05', 1, 5),
(1, 9.99, '2025-09-10', 1, 6), (2, 24.99, '2025-09-12', 1, 7),
(3, 49.99, '2025-09-15', 1, 8), (1, 9.99, '2025-09-18', 1, 9);

-- Suscripciones
INSERT INTO suscripcion (id_usuario, id_plan, fecha_inicio, fecha_fin, id_estado, id_pago) VALUES
(1, 1, '2025-01-03', '2025-02-02', 1, 1),
(2, 2, '2025-01-12', '2025-04-12', 1, 2),
(3, 3, '2025-01-20', '2026-01-20', 1, 3),
(4, 2, '2025-02-02', '2025-05-02', 2, 4),
(5, 1, '2025-02-15', '2025-03-17', 1, 5),
(6, 3, '2025-03-03', '2026-03-03', 1, 6),
(7, 2, '2025-03-11', '2025-06-11', 1, 7),
(8, 1, '2025-04-06', '2025-05-06', 2, 8),
(9, 3, '2025-04-21', '2026-04-21', 1, 9),
(10, 1, '2025-05-03', '2025-06-03', 2, 10),
(11, 2, '2025-05-16', '2025-08-16', 1, 11),
(12, 3, '2025-06-02', '2026-06-02', 1, 12),
(13, 1, '2025-06-11', '2025-07-11', 1, 13),
(14, 2, '2025-06-21', '2025-09-21', 2, 14),
(15, 3, '2025-07-02', '2026-07-02', 1, 15),
(16, 2, '2025-07-11', '2025-10-11', 1, 16),
(17, 1, '2025-07-21', '2025-08-21', 1, 17),
(18, 3, '2025-08-02', '2026-08-02', 2, 18),
(19, 2, '2025-08-16', '2025-11-16', 1, 19),
(20, 1, '2025-09-02', '2025-10-02', 1, 20),

-- Renovaciones o pagos adicionales
(1, 2, '2025-08-10', '2025-11-10', 1, 33),
(1, 2, '2025-11-10', '2025-12-10', 1, 34),
(2, 1, '2025-08-20', '2025-09-20', 2, 35),
(3, 3, '2025-08-25', '2026-08-25', 1, 36),
(4, 1, '2025-09-01', '2025-10-01', 1, 37),
(5, 3, '2025-09-05', '2026-09-05', 2, 38),
(6, 1, '2025-09-10', '2025-10-10', 1, 39),
(7, 2, '2025-09-12', '2025-12-12', 1, 40),
(8, 3, '2025-09-15', '2026-09-15', 1, 41),
(9, 1, '2025-09-18', '2025-10-18', 2, 42);