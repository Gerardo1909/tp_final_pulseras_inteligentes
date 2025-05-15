"""
Script ETL para crear y gestionar relaciones entre usuarios y actividades en Neo4j.

Este script evalúa los datos de actividad física de cada usuario para determinar
qué actividades ha realizado en el último periodo y establece las relaciones
correspondientes (REALIZA) en el grafo Neo4j.
"""

from datetime import datetime, timedelta
from pulseras_inteligentes.utils.conexiones_db import conectar_db_grafo_usuarios, conectar_db_sensor_pulsera
from pulseras_inteligentes.utils.etl_funcs import manejo_errores_proceso, logger


def crear_relacion_usuario_actividad(db, id_usuario: int, id_actividad: int, fecha_inicio: str) -> None:
    """
    Crea una relación REALIZA entre un Usuario y una Actividad.
    
    Args:
        db: Conexión a la base de datos Neo4j.
        id_usuario: ID del usuario.
        id_actividad: ID de la actividad.
        fecha_inicio: Fecha de inicio de la realización en formato YYYY-MM-DD.
    """
    try:
        db.execute_query(
            """
            MATCH (u:Usuario {id_usuario: $id_usuario}), (a:Actividad {id_actividad: $id_actividad})
            MERGE (u)-[r:REALIZA]->(a)
            SET r.desde = date($fecha_inicio)
            """,
            id_usuario=id_usuario,
            id_actividad=id_actividad,
            fecha_inicio=fecha_inicio,
        )
        logger.debug(f"Relación REALIZA creada entre Usuario {id_usuario} y Actividad {id_actividad}")
    except Exception as e:
        logger.error(f"Error al crear relación REALIZA entre Usuario {id_usuario} y Actividad {id_actividad}: {e}")
        raise


def eliminar_relacion_usuario_actividad(db, id_usuario: int, id_actividad: int) -> None:
    """
    Elimina una relación REALIZA entre un Usuario y una Actividad.
    
    Args:
        db: Conexión a la base de datos Neo4j.
        id_usuario: ID del usuario.
        id_actividad: ID de la actividad.
    """
    try:
        db.execute_query(
            """
            MATCH (u:Usuario {id_usuario: $id_usuario})-[r:REALIZA]->(a:Actividad {id_actividad: $id_actividad})
            DELETE r
            """,
            id_usuario=id_usuario,
            id_actividad=id_actividad,
        )
        logger.debug(f"Relación REALIZA eliminada entre Usuario {id_usuario} y Actividad {id_actividad}")
    except Exception as e:
        logger.error(f"Error al eliminar relación REALIZA entre Usuario {id_usuario} y Actividad {id_actividad}: {e}")
        raise


def obtener_usuarios_neo4j(db):
    """
    Obtiene la lista de IDs de usuarios desde Neo4j.
    
    Args:
        db: Conexión a la base de datos Neo4j.
        
    Returns:
        list: Lista de IDs de usuarios.
    """
    try:
        records, _, _ = db.execute_query("MATCH (u:Usuario) RETURN u.id_usuario AS id_usuario")
        usuarios = [r.data()["id_usuario"] for r in records]
        logger.info(f"Obtenidos {len(usuarios)} usuarios de Neo4j")
        return usuarios
    except Exception as e:
        logger.error(f"Error al obtener usuarios de Neo4j: {e}")
        raise


def obtener_actividades_neo4j(db):
    """
    Obtiene la lista de actividades desde Neo4j con sus atributos.
    
    Args:
        db: Conexión a la base de datos Neo4j.
        
    Returns:
        list: Lista de diccionarios con datos de actividades.
    """
    try:
        records, _, _ = db.execute_query(
            "MATCH (a:Actividad) RETURN a.id_actividad AS id_actividad, a.nombre AS nombre"
        )
        actividades = [r.data() for r in records]
        logger.info(f"Obtenidas {len(actividades)} actividades de Neo4j")
        return actividades
    except Exception as e:
        logger.error(f"Error al obtener actividades de Neo4j: {e}")
        raise


def usuario_realiza_actividad(db_sensor_pulsera, id_usuario: int, nombre_actividad: str, dias_atras: int = 30) -> bool:
    """
    Verifica si un usuario ha realizado una actividad específica en el periodo evaluado.
    
    Args:
        db_sensor_pulsera: Conexión a la base de datos MongoDB.
        id_usuario: ID del usuario a evaluar.
        nombre_actividad: Nombre de la actividad a buscar.
        dias_atras: Número de días hacia atrás a evaluar.
        
    Returns:
        bool: True si el usuario ha realizado la actividad, False en caso contrario.
    """
    try:
        fecha_inicio = datetime.now() - timedelta(days=dias_atras)
        
        # Buscar registros de actividad que coincidan con el nombre
        registros = db_sensor_pulsera.pulseras_inteligentes.datos_sensor.find({
            "id_usuario": id_usuario,
            "tipo_registro": "actividad",
            "datos.tipo_actividad": nombre_actividad,
            "timestamp": {
                "$gte": fecha_inicio,
                "$lt": datetime.now()
            }
        })
        
        # Convertir a lista para poder contar y verificar
        registros_lista = list(registros)
        return len(registros_lista) > 0
    
    except Exception as e:
        logger.error(f"Error al verificar si usuario {id_usuario} realiza actividad {nombre_actividad}: {e}")
        return False


def actualizar_relacion_usuario_actividad(db_grafo, db_sensor_pulsera, id_usuario: int, actividad: dict) -> bool:
    """
    Actualiza la relación entre un usuario y una actividad según los datos de sensores.
    
    Args:
        db_grafo: Conexión a la base de datos Neo4j.
        db_sensor_pulsera: Conexión a la base de datos MongoDB.
        id_usuario: ID del usuario.
        actividad: Diccionario con datos de la actividad.
        
    Returns:
        bool: True si se creó o mantuvo la relación, False si se eliminó.
    """
    id_actividad = actividad["id_actividad"]
    nombre_actividad = actividad["nombre"]
    
    # Verificar si el usuario realiza la actividad
    realiza = usuario_realiza_actividad(db_sensor_pulsera, id_usuario, nombre_actividad)
    
    if realiza:
        # Fecha de inicio (usamos la actual como aproximación)
        fecha_inicio = datetime.now().date().isoformat()
        crear_relacion_usuario_actividad(db_grafo, id_usuario, id_actividad, fecha_inicio)
        logger.debug(f"Usuario {id_usuario} REALIZA actividad {nombre_actividad}")
        return True
    else:
        eliminar_relacion_usuario_actividad(db_grafo, id_usuario, id_actividad)
        logger.debug(f"Usuario {id_usuario} NO realiza actividad {nombre_actividad}")
        return False


def main():
    """
    Función principal que coordina la actualización de relaciones Usuario-Actividad.
    """
    nombre_proceso = "ETL_RELACION_USUARIO_ACTIVIDAD"
    
    with manejo_errores_proceso(nombre_proceso):
        # Conexiones a bases de datos
        db_sensor_pulsera = conectar_db_sensor_pulsera()
        db_grafo = conectar_db_grafo_usuarios()
        
        try:
            # Obtener usuarios y actividades
            usuarios = obtener_usuarios_neo4j(db_grafo)
            actividades = obtener_actividades_neo4j(db_grafo)
            
            # Contadores para resumen final
            total_relaciones = 0
            total_eliminadas = 0
            
            # Iterar sobre usuarios y actividades para actualizar relaciones
            for id_usuario in usuarios:
                logger.info(f"Procesando usuario {id_usuario}")
                
                for actividad in actividades:
                    resultado = actualizar_relacion_usuario_actividad(
                        db_grafo, db_sensor_pulsera, id_usuario, actividad
                    )
                    
                    if resultado:
                        total_relaciones += 1
                    else:
                        total_eliminadas += 1
            
            # Resumen final
            logger.info(f"Relaciones Usuario-Actividad actualizadas: {total_relaciones} creadas/mantenidas, "
                       f"{total_eliminadas} eliminadas")
        
        finally:
            # Cierre de conexiones
            db_sensor_pulsera.close()
            db_grafo.close()


if __name__ == "__main__":
    main()