"""
Script ETL para insertar nodos de usuarios en la base de datos de grafos Neo4j.

Este script extrae información de usuarios desde la base de datos MongoDB
y crea nodos correspondientes en la base de datos Neo4j para el sistema de recomendaciones.
"""

from pulseras_inteligentes.utils.conexiones_db import (
    conectar_db_grafo_usuarios, 
    conectar_db_sensor_pulsera
)
from pulseras_inteligentes.utils.etl_funcs import manejo_errores_proceso, logger

def extraer_usuarios_mongodb(db_sensor_pulsera):
    """
    Extrae datos de usuarios desde la base de datos MongoDB.
    
    Args:
        db_sensor_pulsera: Conexión a la base de datos MongoDB.
        
    Returns:
        list: Lista de documentos con datos de usuarios.
    """
    usuarios = list(db_sensor_pulsera.pulseras_inteligentes.usuarios_sensor.find())
    logger.info(f"Extraídos {len(usuarios)} usuarios de MongoDB.")
    return usuarios

def insertar_usuario_neo4j(db_grafo, id_usuario, nombre, fecha_registro):
    """
    Inserta un usuario como nodo en la base de datos Neo4j.
    
    Args:
        db_grafo: Conexión a la base de datos Neo4j.
        id_usuario (int): ID del usuario.
        nombre (str): Nombre del usuario.
        fecha_registro (str): Fecha de registro del usuario en formato YYYY-MM-DD.
    """
    try:
        db_grafo.execute_query(
            """
            MERGE (:Usuario {nombre: $nombre, fecha_registro: $fecha_registro, id_usuario: $id_usuario})
            """,
            id_usuario=id_usuario, nombre=nombre, fecha_registro=fecha_registro
        )
        logger.info(f"Usuario {nombre} (ID: {id_usuario}) insertado en Neo4j.")
    except Exception as e:
        logger.error(f"Error al insertar usuario {nombre} (ID: {id_usuario}) en Neo4j: {e}")
        raise

def cargar_usuarios_neo4j(usuarios, db_grafo):
    """
    Carga todos los usuarios en la base de datos Neo4j.
    
    Args:
        usuarios (list): Lista de documentos con datos de usuarios.
        db_grafo: Conexión a la base de datos Neo4j.
        
    Returns:
        int: Número de usuarios insertados.
    """
    contador = 0
    for usuario in usuarios:
        insertar_usuario_neo4j(
            db_grafo,
            usuario["id_usuario"],
            usuario["nombre"],
            usuario["fecha_registro"].strftime("%Y-%m-%d")
        )
        contador += 1
    
    logger.info(f"Total de {contador} usuarios cargados en Neo4j.")
    return contador

def main():
    """
    Función principal que coordina el proceso ETL de inserción de nodos de usuarios.
    """
    nombre_proceso = "ETL_INSERTAR_NODOS_USUARIOS"
    
    with manejo_errores_proceso(nombre_proceso):
        # Conexiones a bases de datos
        db_sensor_pulsera = conectar_db_sensor_pulsera()
        db_grafo_usuarios = conectar_db_grafo_usuarios()
        
        try:
            # Extracción de usuarios desde MongoDB
            usuarios = extraer_usuarios_mongodb(db_sensor_pulsera)
            
            # Carga de usuarios en Neo4j
            cargar_usuarios_neo4j(usuarios, db_grafo_usuarios)
            
            logger.info(f"{nombre_proceso}: Proceso completado con éxito.")
        finally:
            # Cierre de conexiones
            db_grafo_usuarios.close()
            db_sensor_pulsera.close()

if __name__ == "__main__":
    main()
