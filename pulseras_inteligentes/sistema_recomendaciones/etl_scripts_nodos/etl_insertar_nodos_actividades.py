"""
Script ETL para insertar nodos de actividades en la base de datos de grafos Neo4j.

Este script crea nodos que representan las diferentes actividades físicas
que pueden realizar los usuarios, con sus propiedades como descripción,
tipo de dato a medir, unidad de medida y frecuencia mínima recomendada.
"""

from typing import List, Dict, Any
from pulseras_inteligentes.utils.conexiones_db import conectar_db_grafo_usuarios
from pulseras_inteligentes.utils.etl_funcs import manejo_errores_etl, logger


def insertar_actividad(db, actividad: dict) -> None:
    """
    Inserta un nodo de Actividad en la base de datos Neo4j.
    
    Args:
        db: Conexión a la base de datos Neo4j.
        actividad: Diccionario con los datos de la actividad.
    """
    try:
        db.execute_query(
            """
            MERGE (:Actividad {
                id_actividad: $id_actividad,
                nombre: $nombre,
                descripcion: $descripcion,
                tipo_dato: $tipo_dato,
                unidad: $unidad,
                frecuencia_minima: $frecuencia_minima
            })
            """,
            id_actividad=actividad["id_actividad"],
            nombre=actividad["nombre"],
            descripcion=actividad["descripcion"],
            tipo_dato=actividad["tipo_dato"],
            unidad=actividad["unidad"],
            frecuencia_minima=actividad["frecuencia_minima"],
        )
        logger.info(f"Actividad '{actividad['nombre']}' (ID: {actividad['id_actividad']}) insertada en Neo4j")
    except Exception as e:
        logger.error(f"Error al insertar actividad '{actividad['nombre']}': {e}")
        raise


def obtener_actividades() -> List[Dict[str, Any]]:
    """
    Obtiene la lista de actividades a insertar en la base de datos.
    
    En una implementación más avanzada, estas actividades podrían venir
    de una configuración externa o una base de datos.
    
    Returns:
        List[Dict[str, Any]]: Lista de diccionarios con datos de actividades.
    """
    actividades = [
        {
            "id_actividad": 1,
            "nombre": "caminar",
            "descripcion": "Realizar caminatas de al menos 30 minutos",
            "tipo_dato": "duracion_minutos",
            "unidad": "minutos",
            "frecuencia_minima": 3,  # Veces por semana
        },
        {
            "id_actividad": 2,
            "nombre": "correr",
            "descripcion": "Correr al menos 5 km",
            "tipo_dato": "distancia_km",
            "unidad": "km",
            "frecuencia_minima": 2,
        },
        {
            "id_actividad": 3,
            "nombre": "ciclismo",
            "descripcion": "Andar en bicicleta al menos 20 km",
            "tipo_dato": "distancia_km",
            "unidad": "km",
            "frecuencia_minima": 2,
        },
        {
            "id_actividad": 4,
            "nombre": "entrenamiento_fuerza",
            "descripcion": "Realizar entrenamiento de fuerza con pesas",
            "tipo_dato": "sesiones",
            "unidad": "sesiones",
            "frecuencia_minima": 2,
        },
        {
            "id_actividad": 5,
            "nombre": "yoga",
            "descripcion": "Practicar yoga",
            "tipo_dato": "sesiones",
            "unidad": "sesiones",
            "frecuencia_minima": 2,
        },
    ]
    
    logger.info(f"Configuradas {len(actividades)} actividades para inserción")
    return actividades


def main():
    """
    Función principal que coordina la inserción de nodos de actividades.
    """
    nombre_etl = "ETL_INSERTAR_NODOS_ACTIVIDADES"
    
    with manejo_errores_etl(nombre_etl):
        # Conexión a la base de datos Neo4j
        db_grafo_usuarios = conectar_db_grafo_usuarios()
        
        try:
            # Obtener lista de actividades a insertar
            actividades = obtener_actividades()
            
            # Contador para el resumen final
            contador = 0
            
            # Inserción de actividades
            for actividad in actividades:
                insertar_actividad(db_grafo_usuarios, actividad)
                contador += 1
            
            # Resumen final
            logger.info(f"Nodos de actividades insertados: {contador} en total")
        
        finally:
            # Cierre de conexión
            db_grafo_usuarios.close()
            
if __name__ == "__main__":
    main()