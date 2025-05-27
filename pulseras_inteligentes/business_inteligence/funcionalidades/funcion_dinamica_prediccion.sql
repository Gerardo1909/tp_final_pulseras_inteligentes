
-- Estimar los ingresos totales esperados para un mes futuro basándose en el promedio de ingresos de los n meses anteriores.

CREATE OR REPLACE FUNCTION predecir_ingresos_por_mes(
    meses_promedio INT
)
RETURNS NUMERIC AS $$
DECLARE
    ingreso_promedio NUMERIC;
BEGIN
    SELECT
        COALESCE(AVG(hechos_pagos.monto_pago), 0) INTO ingreso_promedio
    FROM
        hechos_pagos
    JOIN
        dim_fecha ON hechos_pagos.id_fecha = dim_fecha.id_fecha
    WHERE
        dim_fecha.fecha >= (CURRENT_DATE - INTERVAL '1 month' * meses_promedio);

    RETURN ingreso_promedio;
END;
$$ LANGUAGE plpgsql;



-- ejemplos de uso:

-- Predecir los ingresos del próximo mes basándose en el promedio de los últimos 3 meses
SELECT predecir_ingresos_por_mes(3);

-- Predecir los ingresos del próximo mes basándose en el promedio de los últimos 6 meses
SELECT predecir_ingresos_por_mes(6);