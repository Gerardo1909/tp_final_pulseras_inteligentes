-- POBLADO DE TABLAS DE DIMENSIONES DW

INSERT INTO "dim_plan" ("nombre_plan", "descripcion", "duracion_dias") VALUES
('Básico', 'Acceso limitado a funcionalidades básicas.', 30),
('Estándar', 'Acceso completo durante 3 meses.', 90),
('Premium', 'Acceso completo con beneficios exclusivos por 1 año.', 365);

INSERT INTO "dim_metodo_pago" ("descripcion") VALUES
('Tarjeta de crédito'),
('PayPal'),
('Transferencia bancaria');

INSERT INTO "dim_estado_pago" ("descripcion") VALUES
('Aprobado'),
('Pendiente'),
('Rechazado');

INSERT INTO "dim_actividad" ("descripcion") VALUES
('tiempo_pantalla'),
('click_boton'),
('envio_formulario'),
('uso_funcionalidad'),
('caminar'),
('correr'),
('ciclismo'),
('entrenamiento_fuerza'),
('yoga'),
('reposo'),
('sueño');