-- =====================================================================================
-- FUNCIONES Y TRIGGERS PARA AUDITORÍA DEL SISTEMA OPERACIONAL
-- =====================================================================================
-- Este archivo contiene las funciones PL/pgSQL y triggers necesarios para registrar
-- automáticamente los eventos de actualización en las tablas principales del sistema
-- operacional en la tabla log_eventos.
-- 
-- El sistema de auditoría permite:
-- - Rastrear cambios en datos críticos de usuarios
-- - Mantener un historial completo de modificaciones
-- - Facilitar los procesos ETL del Data Warehouse
-- - Proporcionar trazabilidad para auditorías y debugging
-- =====================================================================================

-- =====================================================================================
-- TRIGGERS PARA TABLA DE USUARIOS
-- =====================================================================================

-- Función para registrar actualización en la tabla usuarios
-- Esta función se ejecuta automáticamente después de cada UPDATE en la tabla usuarios
-- y registra tanto el estado anterior como el nuevo estado del registro modificado
CREATE OR REPLACE FUNCTION registrar_update_usuarios()
RETURNS TRIGGER AS $$
DECLARE
    clave_pk TEXT;
BEGIN
    -- Extraemos la clave primaria como texto para compatibilidad universal
    clave_pk := NEW.id_usuario::TEXT;

    -- Insertamos el evento en la tabla de logs con información completa
    INSERT INTO log_eventos (
        tabla_afectada,
        operacion,
        fecha_operacion,
        clave_primaria,
        datos_anteriores,
        datos_nuevos
    )
    VALUES (
        'usuarios',                -- Tabla que fue modificada
        'UPDATE',                  -- Tipo de operación realizada
        CURRENT_TIMESTAMP,         -- Momento exacto de la operación
        clave_pk,                  -- ID del usuario modificado
        to_jsonb(OLD),            -- Estado anterior del registro (antes del UPDATE)
        to_jsonb(NEW)             -- Estado actualizado del registro (después del UPDATE)
    );

    RETURN NULL; -- AFTER triggers deben retornar NULL para no afectar la operación
END;
$$ LANGUAGE plpgsql;

-- Trigger que se activa después de cada UPDATE en la tabla usuarios
-- Ejecuta la función registrar_update_usuarios() para cada fila modificada
CREATE TRIGGER trg_update_usuarios
AFTER UPDATE ON usuarios
FOR EACH ROW
EXECUTE FUNCTION registrar_update_usuarios();

-- =====================================================================================
-- COMENTARIOS ADICIONALES
-- =====================================================================================
-- 
-- Este trigger de auditoría proporciona las siguientes funcionalidades:
--
-- 1. USUARIOS (UPDATE): Registra cada modificación de datos de usuario en el sistema
--    - Cambios de información personal (nombre, email, etc.)
--    - Actualizaciones de configuración de usuario
--    - Modificaciones de estado o permisos
--
-- Beneficios del sistema de auditoría:
-- - Trazabilidad completa: Saber qué cambió, cuándo y cómo
-- - Soporte para ETL: Los procesos del Data Warehouse pueden identificar registros
--   modificados consultando log_eventos en lugar de hacer comparaciones costosas
-- - Debugging: Facilita la identificación de problemas y inconsistencias
-- - Compliance: Cumple con requisitos de auditoría y regulaciones de datos
-- - Rollback: Permite revertir cambios si es necesario usando datos_anteriores
-- 
-- Integración con ETL:
-- - Las funciones ETL del Data Warehouse consultan esta tabla para identificar
--   usuarios que han sido modificados desde la última actualización
-- - Esto mejora significativamente el rendimiento al evitar comparaciones completas
--   de tablas y permite actualizaciones incrementales eficientes
--
-- Notas técnicas importantes:
-- - El trigger es tipo AFTER para no interferir con la operación original
-- - Se utiliza JSONB para almacenamiento eficiente y consultas avanzadas sobre los datos
-- - La clave primaria se almacena como TEXT para mantener compatibilidad universal
-- - Los campos datos_anteriores y datos_nuevos contienen el registro completo
--   en formato JSON para máxima flexibilidad en consultas futuras
-- =====================================================================================