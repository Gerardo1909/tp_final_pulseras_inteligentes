"""
Script ETL para crear relaciones entre actividades y objetivos en Neo4j.

Este script establece las relaciones CONTRIBUYE_A entre las actividades físicas
y los objetivos de salud en el grafo Neo4j, permitiendo identificar qué actividades
contribuyen al cumplimiento de determinados objetivos.
"""

from pulseras_inteligentes.utils.conexiones_db import conectar_db_grafo_usuarios
from pulseras_inteligentes.utils.etl_funcs import manejo_errores_proceso, logger


def crear_relacion_actividad_objetivo(db, id_actividad: int, id_objetivo: int) -> None:
    """
    Crea una relación CONTRIBUYE_A entre una Actividad y un Objetivo.
    
    Args:
        db: Conexión a la base de datos Neo4j.
        id_actividad: ID de la actividad.
        id_objetivo: ID del objetivo.
    """
    try:
        db.execute_query(
            """
            MATCH (a:Actividad {id_actividad: $id_actividad}), (o:Objetivo {id_objetivo: $id_objetivo})
            MERGE (a)-[:CONTRIBUYE_A]->(o)
            """,
            id_actividad=id_actividad,
            id_objetivo=id_objetivo,
        )
        logger.debug(f"Relación CONTRIBUYE_A creada entre Actividad {id_actividad} y Objetivo {id_objetivo}")
    except Exception as e:
        logger.error(f"Error al crear relación CONTRIBUYE_A entre Actividad {id_actividad} y Objetivo {id_objetivo}: {e}")
        raise


def obtener_relaciones_configuradas():
    """
    Obtiene la configuración de relaciones entre actividades y objetivos.
    
    En una implementación más avanzada, estas relaciones podrían venir de una 
    configuración o base de datos en lugar de estar codificadas.
    
    Returns:
        list: Lista de diccionarios con las relaciones actividad-objetivo.
    """
    # TODO: Esta información debería venir de una configuración o base de datos
    relaciones = [
        {"id_actividad": 1, "id_objetivo": 1},  # Caminar -> Caminatas diarias
        {"id_actividad": 2, "id_objetivo": 1},  # Correr -> Caminatas diarias
        {"id_actividad": 1, "id_objetivo": 2},  # Caminar -> Reposo consciente
        {"id_actividad": 2, "id_objetivo": 2},  # Correr -> Reposo consciente
        {"id_actividad": 4, "id_objetivo": 2},  # Entrenamiento de fuerza -> Reposo consciente
        {"id_actividad": 5, "id_objetivo": 2},  # Yoga -> Reposo consciente
        {"id_actividad": 1, "id_objetivo": 3},  # Caminar -> Control de glucosa
        {"id_actividad": 2, "id_objetivo": 3},  # Correr -> Control de glucosa
        {"id_actividad": 3, "id_objetivo": 3},  # Ciclismo -> Control de glucosa
        {"id_actividad": 4, "id_objetivo": 3},  # Entrenamiento de fuerza -> Control de glucosa
        {"id_actividad": 1, "id_objetivo": 4},  # Caminar -> Sueño reparador
        {"id_actividad": 2, "id_objetivo": 4},  # Correr -> Sueño reparador
        {"id_actividad": 3, "id_objetivo": 4},  # Ciclismo -> Sueño reparador
        {"id_actividad": 5, "id_objetivo": 4},  # Yoga -> Sueño reparador
    ]
    
    logger.info(f"Configuradas {len(relaciones)} relaciones actividad-objetivo")
    return relaciones


def main():
    """
    Función principal que coordina la creación de relaciones Actividad-Objetivo.
    """
    nombre_proceso = "ETL_RELACION_ACTIVIDAD_OBJETIVO"
    
    with manejo_errores_proceso(nombre_proceso):
        # Conexión a la base de datos Neo4j
        db_grafo = conectar_db_grafo_usuarios()
        
        try:
            # Obtener configuración de relaciones
            relaciones = obtener_relaciones_configuradas()
            
            # Contador para el resumen final
            contador = 0
            
            # Crear las relaciones
            for relacion in relaciones:
                crear_relacion_actividad_objetivo(
                    db_grafo, relacion["id_actividad"], relacion["id_objetivo"]
                )
                contador += 1
            
            # Resumen final
            logger.info(f"Relaciones Actividad-Objetivo creadas: {contador} en total")
        
        finally:
            # Cierre de conexión
            db_grafo.close()


if __name__ == "__main__":
    main()
