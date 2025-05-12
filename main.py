"""
Script principal para la ejecución del flujo ETL del sistema de pulseras inteligentes.

Este script coordina la ejecución de todos los procesos ETL en el orden correcto:
1. Carga de usuarios desde la base transaccional a MongoDB
2. Carga de nodos en el sistema de recomendaciones (Neo4j)
3. Generación de datos de sensores y aplicación
4. Generación de relaciones en el sistema de recomendaciones
5. Carga de dimensiones y hechos en el Data Warehouse
"""

import time
from pulseras_inteligentes.utils.etl_funcs import configurar_logger, registrar_ejecucion_etl

# Módulos ETL del sistema transaccional
from pulseras_inteligentes.sistema_transaccional.pulsera_inteligente.etl_scripts import (
    etl_insertar_registros_aplicacion,
    etl_insertar_registros_sensores,
    etl_insertar_usuarios
)

# Módulos ETL del sistema de recomendaciones (nodos)
from pulseras_inteligentes.sistema_recomendaciones.etl_scripts_nodos import (
    etl_insertar_nodos_actividades,
    etl_insertar_nodos_objetivos,
    etl_insertar_nodos_usuarios
)

# Módulos ETL del sistema de recomendaciones (relaciones)
from pulseras_inteligentes.sistema_recomendaciones.etl_scripts_relaciones import (
    etl_relacion_actividad_objetivo,
    etl_relacion_usuario_actividad,
    etl_relacion_usuario_objetivo
)

# Módulos ETL del data warehouse
from pulseras_inteligentes.datawarehouse.etl_scripts import (
    etl_cargar_dim_fecha,
    etl_cargar_dim_usuario,
    etl_cargar_hechos_actividad,
    etl_cargar_hechos_pagos
)

# Configuración del logger para el script principal
logger = configurar_logger("ETL_PRINCIPAL")

def ejecutar_etl(nombre, funcion):
    """
    Ejecuta un proceso ETL específico con registro de tiempo y resultado.
    
    Args:
        nombre (str): Nombre descriptivo del proceso ETL.
        funcion: Función main() del módulo ETL a ejecutar.
    """
    inicio = time.time()
    registrar_ejecucion_etl(nombre, "INICIADO")
    
    try:
        funcion()
        fin = time.time()
        tiempo_ejecucion = round(fin - inicio, 2)
        registrar_ejecucion_etl(nombre, "COMPLETADO", f"Tiempo: {tiempo_ejecucion}s")
    except Exception as e:
        fin = time.time()
        tiempo_ejecucion = round(fin - inicio, 2)
        registrar_ejecucion_etl(nombre, "ERROR", f"Error: {str(e)}, Tiempo: {tiempo_ejecucion}s")
        raise

def main():
    """
    Función principal que coordina la ejecución de todos los procesos ETL
    siguiendo el flujo definido para el sistema.
    """
    logger.info("INICIANDO FLUJO ETL COMPLETO DEL SISTEMA")
    inicio_total = time.time()
    
    try:
        # FASE 1: CARGA DE DATOS TRANSACCIONALES A MONGODB
        logger.info("FASE 1: Carga de datos transaccionales")
        ejecutar_etl("ETL_INSERTAR_USUARIOS", etl_insertar_usuarios.main)
        
        # FASE 2: CREACIÓN DE NODOS EN NEO4J
        logger.info("FASE 2: Creación de nodos en sistema de recomendaciones")
        ejecutar_etl("ETL_INSERTAR_NODOS_USUARIOS", etl_insertar_nodos_usuarios.main)
        ejecutar_etl("ETL_INSERTAR_NODOS_OBJETIVOS", etl_insertar_nodos_objetivos.main)
        ejecutar_etl("ETL_INSERTAR_NODOS_ACTIVIDADES", etl_insertar_nodos_actividades.main)
        
        # FASE 3: GENERACIÓN DE REGISTROS DE SENSORES Y APLICACIÓN
        logger.info("FASE 3: Generación de datos de sensores y aplicación")
        ejecutar_etl("ETL_INSERTAR_REGISTROS_APLICACION", etl_insertar_registros_aplicacion.main)
        ejecutar_etl("ETL_INSERTAR_REGISTROS_SENSORES", etl_insertar_registros_sensores.main)
        
        # FASE 4: CREACIÓN DE RELACIONES EN NEO4J
        logger.info("FASE 4: Creación de relaciones en sistema de recomendaciones")
        ejecutar_etl("ETL_RELACION_USUARIO_ACTIVIDAD", etl_relacion_usuario_actividad.main)
        ejecutar_etl("ETL_RELACION_USUARIO_OBJETIVO", etl_relacion_usuario_objetivo.main)
        ejecutar_etl("ETL_RELACION_ACTIVIDAD_OBJETIVO", etl_relacion_actividad_objetivo.main)
        
        # FASE 5: CARGA DE DIMENSIONES Y HECHOS EN DATA WAREHOUSE
        logger.info("FASE 5: Carga de dimensiones y hechos en Data Warehouse")
        # Nota: La dimensión fecha es costosa y solo se ejecuta cuando es necesario
        # ejecutar_etl("ETL_CARGAR_DIM_FECHA", etl_cargar_dim_fecha.main)
        ejecutar_etl("ETL_CARGAR_DIM_USUARIO", etl_cargar_dim_usuario.main)
        ejecutar_etl("ETL_CARGAR_HECHOS_ACTIVIDAD", etl_cargar_hechos_actividad.main)
        ejecutar_etl("ETL_CARGAR_HECHOS_PAGOS", etl_cargar_hechos_pagos.main)
        
        fin_total = time.time()
        tiempo_total = round((fin_total - inicio_total) / 60, 2)
        logger.info(f"FLUJO ETL COMPLETO FINALIZADO. Tiempo total: {tiempo_total} minutos")
        
    except Exception as e:
        fin_total = time.time()
        tiempo_total = round((fin_total - inicio_total) / 60, 2)
        logger.error(f"ERROR EN FLUJO ETL: {str(e)}. Tiempo transcurrido: {tiempo_total} minutos")

if __name__ == "__main__":
    main()