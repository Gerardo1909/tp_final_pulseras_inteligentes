"""
Script ETL para cargar la dimensión fecha en la base de datos dimensional 
para análisis de ventas.

Este script genera un rango de fechas para un período específico y las inserta
en la tabla de dimensión de fechas de la base de datos dimensional, incluyendo atributos
como día, mes, trimestre y año para facilitar consultas analíticas.
"""

import pandas as pd
from datetime import datetime
from typing import List, Dict, Any
from pulseras_inteligentes.utils.conexiones_db import conectar_DW
from pulseras_inteligentes.utils.etl_funcs import manejo_errores_proceso, logger


def generar_fechas_desde_hasta(desde_anio: int, hasta_anio: int) -> List[Dict[str, Any]]:
    """
    Genera un rango de fechas entre los años especificados.
    
    Args:
        desde_anio: Año de inicio.
        hasta_anio: Año de fin (inclusive).
        
    Returns:
        List[Dict[str, Any]]: Lista de diccionarios con datos de fechas y sus atributos.
    """
    try:
        # Generar fechas diarias para el rango de años
        fechas = pd.date_range(start=f"{desde_anio}-01-01", end=f"{hasta_anio}-12-31", freq="D")
        
        lista_dict_fechas = []
        
        # Crear diccionario con atributos para cada fecha
        for fecha in fechas:
            fecha = fecha.to_pydatetime()
            
            lista_dict_fechas.append({
                "fecha": fecha,
                "dia": fecha.day,
                "mes": fecha.month,
                "trimestre": (fecha.month - 1) // 3 + 1,
                "anio": fecha.year
            })
        
        logger.info(f"Generadas {len(lista_dict_fechas)} fechas desde {desde_anio} hasta {hasta_anio}")
        return lista_dict_fechas
    except Exception as e:
        logger.error(f"Error al generar fechas: {e}")
        raise


def insertar_dim_fecha(db_dw, fechas: List[Dict[str, Any]]) -> int:
    """
    Inserta fechas en la tabla de dimensión de fecha.
    
    Args:
        db_dw: Conexión a la base de datos.
        fechas: Lista de diccionarios con datos de fechas.
        
    Returns:
        int: Número de fechas insertadas correctamente.
    """
    contador_exito = 0
    contador_error = 0
    
    for fecha in fechas:
        try:
            db_dw.table("dim_fecha").insert(
                {
                    "fecha": fecha["fecha"].isoformat(),
                    "dia": fecha["dia"],
                    "mes": fecha["mes"],
                    "trimestre": fecha["trimestre"],
                    "anio": fecha["anio"]
                }
            ).execute()
            contador_exito += 1
            
            # Logging detallado cada 100 fechas para no saturar los logs
            if contador_exito % 100 == 0:
                logger.debug(f"Insertadas {contador_exito} fechas hasta ahora")
                
        except Exception as e:
            logger.warning(f"Error al insertar fecha {fecha['fecha'].isoformat()}: {e}")
            contador_error += 1
    
    logger.info(f"Dimensión Fecha: {contador_exito} fechas insertadas, {contador_error} errores")
    return contador_exito


def main():
    """
    Función principal que coordina la carga de la dimensión de fecha.
    """
    nombre_proceso = "ETL_CARGAR_DIM_FECHA"
    
    with manejo_errores_proceso(nombre_proceso):
        # Conexión a la base de datos
        db_dw = conectar_DW()
        
        try:
            # Definir años para generar fechas (configurables según necesidad)
            desde_anio = 2025
            hasta_anio = 2025
            
            logger.info(f"Iniciando carga de dimensión fecha desde {desde_anio} hasta {hasta_anio}")
            
            # Generar fechas para el rango especificado
            fechas = generar_fechas_desde_hasta(desde_anio, hasta_anio)
            
            # Insertar fechas en la dimensión
            total_insertadas = insertar_dim_fecha(db_dw, fechas)
            
            # Resumen final
            logger.info(f"{nombre_proceso}: Proceso completado con éxito. {total_insertadas} de {len(fechas)} fechas insertadas.")
            
        except Exception as e:
            logger.error(f"Error en proceso ETL de dimensión fecha: {e}")
            raise


if __name__ == "__main__":
    main()