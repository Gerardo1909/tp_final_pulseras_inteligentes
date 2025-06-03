-- =====================================================================================
-- FUNCIONES Y TRIGGERS PARA AUDITORÍA DEL DATA WAREHOUSE
-- =====================================================================================
-- Este archivo contiene las funciones PL/pgSQL y triggers necesarios para registrar
-- automáticamente los eventos de inserción y actualización en las tablas principales
-- del Data Warehouse en la tabla log_eventos.
-- =====================================================================================

-- =====================================================================================
-- TRIGGERS PARA TABLA DE HECHOS_PAGOS
-- =====================================================================================

-- Función para registrar inserción en la tabla hechos_pagos
CREATE OR REPLACE FUNCTION registrar_insert_hechos_pagos()
RETURNS TRIGGER AS $$
DECLARE
    clave_pk TEXT;
BEGIN
    -- Extraemos la clave primaria como texto
    clave_pk := NEW.id_hecho::TEXT;

    -- Insertamos el evento en la tabla de logs
    INSERT INTO log_eventos (
        tabla_afectada,
        operacion,
        fecha_operacion,
        clave_primaria,
        datos_anteriores,
        datos_nuevos
    )
    VALUES (
        'hechos_pagos',
        'INSERT',
        CURRENT_TIMESTAMP,
        clave_pk,
        NULL,  -- Para INSERT no hay datos anteriores
        NULL
    );

    RETURN NULL; -- AFTER triggers deben retornar NULL
END;
$$ LANGUAGE plpgsql;

-- Trigger para hechos_pagos - INSERT
CREATE TRIGGER trg_insert_hechos_pagos
AFTER INSERT ON hechos_pagos
FOR EACH ROW
EXECUTE FUNCTION registrar_insert_hechos_pagos();

-- =====================================================================================
-- TRIGGERS PARA TABLA DE HECHOS_ACTIVIDAD
-- =====================================================================================

-- Función para registrar inserción en la tabla hechos_actividad
CREATE OR REPLACE FUNCTION registrar_insert_hechos_actividad()
RETURNS TRIGGER AS $$
DECLARE
    clave_pk TEXT;
BEGIN
    -- Extraemos la clave primaria como texto
    clave_pk := NEW.id_hecho::TEXT;

    -- Insertamos el evento en la tabla de logs
    INSERT INTO log_eventos (
        tabla_afectada,
        operacion,
        fecha_operacion,
        clave_primaria,
        datos_anteriores,
        datos_nuevos
    )
    VALUES (
        'hechos_actividad',
        'INSERT',
        CURRENT_TIMESTAMP,
        clave_pk,
        NULL,  -- Para INSERT no hay datos anteriores
        NULL
    );

    RETURN NULL; -- AFTER triggers deben retornar NULL
END;
$$ LANGUAGE plpgsql;

-- Trigger para hechos_actividad - INSERT
CREATE TRIGGER trg_insert_hechos_actividad
AFTER INSERT ON hechos_actividad
FOR EACH ROW
EXECUTE FUNCTION registrar_insert_hechos_actividad();

-- =====================================================================================
-- TRIGGERS PARA TABLA DE DIM_USUARIO
-- =====================================================================================

-- Función para registrar inserción en la tabla dim_usuario
CREATE OR REPLACE FUNCTION registrar_insert_dim_usuario()
RETURNS TRIGGER AS $$
DECLARE
    clave_pk TEXT;
BEGIN
    -- Extraemos la clave primaria como texto
    clave_pk := NEW.id_usuario::TEXT;

    -- Insertamos el evento en la tabla de logs
    INSERT INTO log_eventos (
        tabla_afectada,
        operacion,
        fecha_operacion,
        clave_primaria,
        datos_anteriores,
        datos_nuevos
    )
    VALUES (
        'dim_usuario',
        'INSERT',
        CURRENT_TIMESTAMP,
        clave_pk,
        NULL,  -- Para INSERT no hay datos anteriores
        NULL
    );

    RETURN NULL; -- AFTER triggers deben retornar NULL
END;
$$ LANGUAGE plpgsql;

-- Trigger para dim_usuario - INSERT
CREATE TRIGGER trg_insert_dim_usuario
AFTER INSERT ON dim_usuario
FOR EACH ROW
EXECUTE FUNCTION registrar_insert_dim_usuario();

-- Función para registrar actualización en la tabla dim_usuario
CREATE OR REPLACE FUNCTION registrar_update_dim_usuario()
RETURNS TRIGGER AS $$
DECLARE
    clave_pk TEXT;
BEGIN
    -- Extraemos la clave primaria como texto
    clave_pk := NEW.id_usuario::TEXT;

    -- Insertamos el evento en la tabla de logs
    INSERT INTO log_eventos (
        tabla_afectada,
        operacion,
        fecha_operacion,
        clave_primaria,
        datos_anteriores,
        datos_nuevos
    )
    VALUES (
        'dim_usuario',
        'UPDATE',
        CURRENT_TIMESTAMP,
        clave_pk,
        to_jsonb(OLD),  -- Estado anterior del registro
        to_jsonb(NEW)   -- Estado actualizado del registro
    );

    RETURN NULL; -- AFTER triggers deben retornar NULL
END;
$$ LANGUAGE plpgsql;

-- Trigger para dim_usuario - UPDATE
CREATE TRIGGER trg_update_dim_usuario
AFTER UPDATE ON dim_usuario
FOR EACH ROW
EXECUTE FUNCTION registrar_update_dim_usuario();

-- =====================================================================================
-- COMENTARIOS ADICIONALES
-- =====================================================================================
-- 
-- Estos triggers proporcionan las siguientes funcionalidades:
--
-- 1. HECHOS_PAGOS (INSERT): Registra cada nuevo hecho de pago cargado en el DW
-- 2. HECHOS_ACTIVIDAD (INSERT): Registra cada nuevo hecho de actividad cargado en el DW
-- 3. DIM_USUARIO (INSERT): Registra cada nuevo usuario cargado en la dimensión
-- 4. DIM_USUARIO (UPDATE): Registra cada actualización de datos de usuario en la dimensión
--
-- Beneficios:
-- - Trazabilidad completa de cambios en el Data Warehouse
-- - Auditoría de procesos ETL
-- - Detección de inconsistencias o problemas en los procesos de carga
-- - Análisis de patrones de carga de datos
-- - Soporte para procesos de rollback si es necesario
-- 
-- Notas importantes:
-- - Todos los triggers son tipo AFTER para no interferir con las operaciones de inserción/actualización
-- - Se utiliza JSONB para almacenar los datos de forma eficiente y permitir consultas avanzadas
-- - La clave primaria se almacena como TEXT para mantener compatibilidad con diferentes tipos de datos
-- =====================================================================================