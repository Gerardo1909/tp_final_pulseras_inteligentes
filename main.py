"""
Script principal para la ejecución del flujo de datos del sistema de pulseras inteligentes.

Este script coordina la ejecución de todos los procesos en el orden correcto:
1. Carga de usuarios desde la base operacional Postgres a MongoDB (Sistema Operacional)
2. Ingesta de datos: datos de sensor de la pulsera y uso de aplicación móvil (Sistema Operacional)
3. Carga de dimensiones y hechos en la base de datos postgres dedicada al análisis de ventas y actividad (Data Warehouse) 
"""

import time
from pulseras_inteligentes.utils.etl_funcs import configurar_logger, registrar_ejecucion_proceso

# Módulos de ingesta de datos del sistema operacional
from pulseras_inteligentes.sistema_operacional.ingesta_sensor_mongo.gen_data_scripts import (
    generar_registros_aplicacion,
    generar_registros_sensores
)

# Módulos ETL del sistema operacional
from pulseras_inteligentes.sistema_operacional.ingesta_sensor_mongo.etl_scripts import (
    etl_insertar_usuarios
)
# Módulos ETL del data warehouse
from pulseras_inteligentes.datawarehouse.etl_scripts import (
    etl_cargar_dim_fecha,
    etl_cargar_dim_usuario,
    etl_cargar_hechos_pagos,
    etl_cargar_hechos_actividad
)

# Configuración del logger para el script principal
logger = configurar_logger("ETL_PRINCIPAL")

def ejecutar_proceso(nombre, funcion):
    """
    Ejecuta un proceso específico con registro de tiempo y resultado.
    
    Args:
        nombre (str): Nombre descriptivo del proceso.
        funcion: Función main() del módulo a ejecutar.
    """
    inicio = time.time()
    registrar_ejecucion_proceso(nombre, "INICIADO")
    
    try:
        funcion()
        fin = time.time()
        tiempo_ejecucion = round(fin - inicio, 2)
        registrar_ejecucion_proceso(nombre, "COMPLETADO", f"Tiempo: {tiempo_ejecucion}s")
    except Exception as e:
        fin = time.time()
        tiempo_ejecucion = round(fin - inicio, 2)
        registrar_ejecucion_proceso(nombre, "ERROR", f"Error: {str(e)}, Tiempo: {tiempo_ejecucion}s")
        raise

def main():
    """
    Función principal que coordina la ejecución de todos los procesos ETL
    siguiendo el flujo definido para el sistema.
    """
    logger.info("INICIANDO FLUJO ETL COMPLETO DEL SISTEMA")
    inicio_total = time.time()
    
    try:
        
        # FASE 1: CARGA DE DATOS OPERACIONALES A MONGODB
        logger.info("FASE 1: Carga de datos operacionales de usuarios a MongoDB")
        ejecutar_proceso("ETL_INSERTAR_USUARIOS", etl_insertar_usuarios.main)
        
        # FASE 2: INGESTA DE DATOS DE APLICACIÓN MÓVIL Y SENSOR DE PULSERA
        logger.info("FASE 2: Generación de datos de sensores y aplicación")
        ejecutar_proceso("GENERAR_REGISTROS_APLICACION", generar_registros_aplicacion.main)
        ejecutar_proceso("GENERAR_REGISTROS_SENSORES", generar_registros_sensores.main)
        
        # FASE 3: CARGA DE DIMENSIONES Y HECHOS EN BASE DE DATOS DE ANÁLISIS DE VENTAS  
        logger.info("FASE 3: Carga de dimensiones y hechos en modelo dimensional de ventas")
        # Nota: La dimensión fecha es costosa y solo se ejecuta cuando es necesario
        ejecutar_proceso("ETL_CARGAR_DIM_FECHA", etl_cargar_dim_fecha.main)
        ejecutar_proceso("ETL_CARGAR_DIM_USUARIO", etl_cargar_dim_usuario.main)
        ejecutar_proceso("ETL_CARGAR_HECHOS_ACTIVIDAD", etl_cargar_hechos_actividad.main)
        ejecutar_proceso("ETL_CARGAR_HECHOS_PAGOS", etl_cargar_hechos_pagos.main)
        
        fin_total = time.time()
        tiempo_total = round((fin_total - inicio_total) / 60, 2)
        logger.info(f"FLUJO ETL COMPLETO FINALIZADO. Tiempo total: {tiempo_total} minutos")
        
    except Exception as e:
        fin_total = time.time()
        tiempo_total = round((fin_total - inicio_total) / 60, 2)
        logger.error(f"ERROR EN FLUJO ETL: {str(e)}. Tiempo transcurrido: {tiempo_total} minutos")

if __name__ == "__main__":
    main()