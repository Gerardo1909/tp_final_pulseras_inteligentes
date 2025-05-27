
-- Segmentar usuarios únicamente por su nivel de actividad, medido por el número de registros en la tabla hechos_actividad.

CREATE OR REPLACE FUNCTION segmentar_usuarios_por_actividad(
    min_actividades INT
)
RETURNS TABLE (
    id_usuario INT,
    nombre VARCHAR,
    cantidad_total BIGINT,
    cantidad_biometricos BIGINT,
    cantidad_aplicacion BIGINT
) AS $$
BEGIN
    RETURN QUERY
    WITH actividades_contadas AS (
        SELECT
            ha.id_usuario,
            COUNT(*) AS cantidad_total,
            COUNT(CASE WHEN da.tipo_dato = 'Dato Biométrico' THEN 1 END) AS cantidad_biometricos,
            COUNT(CASE WHEN da.tipo_dato = 'Dato Aplicación' THEN 1 END) AS cantidad_aplicacion
        FROM
            hechos_actividad ha
        JOIN dim_actividad da ON ha.id_actividad = da.id_actividad
        GROUP BY ha.id_usuario
        HAVING COUNT(*) >= min_actividades
    )
    SELECT
        u.id_usuario,
        u.nombre,
        a.cantidad_total,
        a.cantidad_biometricos,
        a.cantidad_aplicacion
    FROM actividades_contadas a
    JOIN dim_usuario u ON u.id_usuario = a.id_usuario
    ORDER BY a.cantidad_total DESC;
END;
$$ LANGUAGE plpgsql;

-- ejemplos de uso:

-- Segmentar usuarios con al menos 10 registros de actividad
SELECT * FROM segmentar_usuarios_por_actividad(10);

-- Segmentar usuarios con al menos 5 registros de actividad
SELECT * FROM segmentar_usuarios_por_actividad(5);

-- Segmentar usuarios con al menos 20 registros de actividad
SELECT * FROM segmentar_usuarios_por_actividad(20);