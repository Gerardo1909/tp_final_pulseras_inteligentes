"""
Script ETL para insertar nodos de objetivos en la base de datos de grafos Neo4j.

Este script crea nodos que representan los diferentes objetivos de salud
que pueden alcanzar los usuarios, con sus propiedades como tipo de dato,
umbrales, unidad de medida y cantidad mínima de días consecutivos.
"""

from typing import List, Dict, Any
from pulseras_inteligentes.utils.conexiones_db import conectar_db_grafo_usuarios
from pulseras_inteligentes.utils.etl_funcs import manejo_errores_proceso, logger


def insertar_objetivo(db, objetivo: Dict[str, Any]) -> None:
    """
    Inserta un nodo de Objetivo en la base de datos Neo4j.

    Args:
        db: Conexión a la base de datos Neo4j.
        objetivo: Diccionario con los datos del objetivo.
    """
    try:
        db.execute_query(
            """
            CREATE (:Objetivo {
                id_objetivo: $id_objetivo,
                nombre: $nombre,
                descripcion: $descripcion,
                tipo_dato: $tipo_dato,
                umbral_minimo: $umbral_minimo,
                umbral_maximo: $umbral_maximo,
                unidad: $unidad,
                dias_consecutivos_minimos: $dias_consecutivos_minimos
            })
            """,
            id_objetivo=objetivo["id_objetivo"],
            nombre=objetivo["nombre"],
            descripcion=objetivo["descripcion"],
            tipo_dato=objetivo["tipo_dato"],
            umbral_minimo=objetivo["umbral_minimo"],
            umbral_maximo=objetivo["umbral_maximo"],
            unidad=objetivo["unidad"],
            dias_consecutivos_minimos=objetivo["dias_consecutivos_minimos"],
        )
        logger.info(f"Objetivo '{objetivo['nombre']}' (ID: {objetivo['id_objetivo']}) insertado en Neo4j")
    except Exception as e:
        logger.error(f"Error al insertar objetivo '{objetivo['nombre']}': {e}")
        raise


def obtener_objetivos() -> List[Dict[str, Any]]:
    """
    Obtiene la lista de objetivos a insertar en la base de datos.
    
    En una implementación más avanzada, estos objetivos podrían venir
    de una configuración externa o una base de datos.
    
    Returns:
        List[Dict[str, Any]]: Lista de diccionarios con datos de objetivos.
    """
    objetivos = [
        {
            "id_objetivo": 1,
            "nombre": "Caminatas diarias",
            "descripcion": "Acumular más de 7000 pasos por día",
            "tipo_dato": "cantidad_pasos",
            "umbral_minimo": 7000,
            "umbral_maximo": None,
            "unidad": "pasos",
            "dias_consecutivos_minimos": 7,
        },
        {
            "id_objetivo": 2,
            "nombre": "Reposo consciente",
            "descripcion": "Tener períodos prolongados de reposo con respiración controlada",
            "tipo_dato": "minutos_sin_movimiento",
            "umbral_minimo": 30,
            "umbral_maximo": None,
            "unidad": "minutos",
            "dias_consecutivos_minimos": 7,
        },
        {
            "id_objetivo": 3,
            "nombre": "Control de glucosa",
            "descripcion": "Mantener niveles estables de glucosa en sangre",
            "tipo_dato": "nivel_glucosa",
            "umbral_minimo": 80,
            "umbral_maximo": 120,
            "unidad": "mg/dL",
            "dias_consecutivos_minimos": 7,
        },
        {
            "id_objetivo": 4,
            "nombre": "Sueño reparador",
            "descripcion": "Dormir más de 7 horas diarias",
            "tipo_dato": "duracion_total_min",
            "umbral_minimo": 420,  # 7 horas
            "umbral_maximo": None,
            "unidad": "minutos",
            "dias_consecutivos_minimos": 7,
        },
    ]
    
    logger.info(f"Configurados {len(objetivos)} objetivos para inserción")
    return objetivos


def main():
    """
    Función principal que coordina la inserción de nodos de objetivos.
    """
    nombre_proceso = "ETL_INSERTAR_NODOS_OBJETIVOS"
    
    with manejo_errores_proceso(nombre_proceso):
        # Conexión a la base de datos Neo4j
        db_grafo_usuarios = conectar_db_grafo_usuarios()
        
        try:
            # Obtener lista de objetivos a insertar
            objetivos = obtener_objetivos()
            
            # Contador para el resumen final
            contador = 0
            
            # Inserción de objetivos
            for objetivo in objetivos:
                insertar_objetivo(db_grafo_usuarios, objetivo)
                contador += 1
            
            # Resumen final
            logger.info(f"Nodos de objetivos insertados: {contador} en total")
        
        finally:
            # Cierre de conexión
            db_grafo_usuarios.close()


if __name__ == "__main__":
    main()