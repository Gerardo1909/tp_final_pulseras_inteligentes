
-- Segmentar usuarios únicamente por su nivel de actividad, medido por el número de registros en la tabla hechos_actividad.

CREATE OR REPLACE FUNCTION segmentar_usuarios_por_actividad(
    min_actividades INT
)
RETURNS TABLE (
    id_usuario INT,
    nombre VARCHAR,
    cantidad_actividades BIGINT -- Se usa BIGINT porque COUNT() devuelve BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        dim_usuario.id_usuario,
        dim_usuario.nombre,
        actividades.conteo_actividades AS conteo_actividades
    FROM
        dim_usuario
    JOIN (
        SELECT
            hechos_actividad.id_usuario,
            COUNT(hechos_actividad.id_hecho) AS conteo_actividades
        FROM
            hechos_actividad 
        GROUP BY
            hechos_actividad.id_usuario
        HAVING COUNT(hechos_actividad.id_hecho) >= min_actividades

    ) AS actividades ON dim_usuario.id_usuario = actividades.id_usuario
    ORDER BY conteo_actividades DESC;
END;
$$ LANGUAGE plpgsql;


-- ejemplos de uso:

-- Segmentar usuarios con al menos 10 registros de actividad
SELECT * FROM segmentar_usuarios_por_actividad(10);

-- Segmentar usuarios con al menos 5 registros de actividad
SELECT * FROM segmentar_usuarios_por_actividad(5);

-- Segmentar usuarios con al menos 20 registros de actividad
SELECT * FROM segmentar_usuarios_por_actividad(20);