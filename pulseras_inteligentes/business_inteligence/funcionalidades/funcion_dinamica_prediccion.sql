
-- Estimar los ingresos totales esperados para un mes futuro basándose en el promedio de ingresos de los n meses anteriores.

CREATE OR REPLACE FUNCTION predecir_ingresos_por_mes(
    meses_promedio INT
)
RETURNS TABLE (
    anio INT,
    mes INT,
    ingreso_total NUMERIC,
    prediccion_ingreso NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    WITH ingresos_mensuales AS (
        SELECT
            f.anio,
            f.mes,
            SUM(p.monto_pago) AS ingreso_total
        FROM
            hechos_pagos p
        JOIN
            dim_fecha f ON p.id_fecha = f.id_fecha
        GROUP BY
            f.anio, f.mes
    )
    SELECT
        im.anio,
        im.mes,
        im.ingreso_total,
        AVG(im.ingreso_total) OVER (
            ORDER BY im.anio, im.mes
            ROWS BETWEEN meses_promedio PRECEDING AND 1 PRECEDING
        ) AS prediccion_ingreso
    FROM ingresos_mensuales im;
END;
$$ LANGUAGE plpgsql;


-- ejemplos de uso:

-- Predecir los ingresos del próximo mes basándose en el promedio de los últimos 3 meses
SELECT * FROM predecir_ingresos_por_mes(3);

-- Predecir los ingresos del próximo mes basándose en el promedio de los últimos 6 meses
SELECT * FROM predecir_ingresos_por_mes(6);