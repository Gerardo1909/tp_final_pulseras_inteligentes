"""
Script ETL para crear y gestionar relaciones entre usuarios y objetivos en Neo4j.

Este script evalúa los datos de los sensores de cada usuario para determinar si
están cumpliendo o no ciertos objetivos de salud, y establece las relaciones
correspondientes (TIENE_OBJETIVO o CUMPLIO) en el grafo Neo4j.
"""

from datetime import datetime, timedelta
from pulseras_inteligentes.utils.conexiones_db import conectar_db_grafo_usuarios, conectar_db_sensor_pulsera
from pulseras_inteligentes.utils.etl_funcs import manejo_errores_proceso, logger


def cumple_objetivo(valor: float, umbral_minimo: float, umbral_maximo: float | None) -> bool:
    """
    Verifica si un valor cumple con los requisitos de un objetivo.
    
    Args:
        valor: Valor a evaluar.
        umbral_minimo: Umbral mínimo del objetivo.
        umbral_maximo: Umbral máximo del objetivo (opcional).
    
    Returns:
        bool: True si el valor cumple con el objetivo, False en caso contrario.
    """
    if umbral_maximo is not None:
        return umbral_minimo <= valor <= umbral_maximo
    return valor >= umbral_minimo


def crear_relacion_tiene_objetivo(db, id_usuario: int, id_objetivo: int) -> None:
    """
    Crea una relación TIENE_OBJETIVO entre un Usuario y un Objetivo.
    
    Args:
        db: Conexión a la base de datos Neo4j.
        id_usuario: ID del usuario.
        id_objetivo: ID del objetivo.
    """
    try:
        fecha_actual = datetime.now().date().isoformat()
        db.execute_query(
            """
            MATCH (u:Usuario {id_usuario: $id_usuario}), (o:Objetivo {id_objetivo: $id_objetivo})
            MERGE (u)-[r:TIENE_OBJETIVO]->(o)
            SET r.desde = date($fecha_actual)
            """,
            id_usuario=id_usuario,
            id_objetivo=id_objetivo,
            fecha_actual=fecha_actual,
        )
        logger.debug(f"Relación TIENE_OBJETIVO creada entre Usuario {id_usuario} y Objetivo {id_objetivo}")
    except Exception as e:
        logger.error(f"Error al crear relación TIENE_OBJETIVO entre Usuario {id_usuario} y Objetivo {id_objetivo}: {e}")
        raise
    
def crear_relacion_cumplio(db, id_usuario: int, id_objetivo: int) -> None:
    """
    Crea una relación CUMPLIO entre un Usuario y un Objetivo.
    
    Args:
        db: Conexión a la base de datos Neo4j.
        id_usuario: ID del usuario.
        id_objetivo: ID del objetivo.
    """
    try:
        fecha_actual = datetime.now().date().isoformat()
        db.execute_query(
            """
            MATCH (u:Usuario {id_usuario: $id_usuario}), (o:Objetivo {id_objetivo: $id_objetivo})
            MERGE (u)-[r:CUMPLIO]->(o)
            SET r.desde = date($fecha_actual)
            """,
            id_usuario=id_usuario,
            id_objetivo=id_objetivo,
            fecha_actual=fecha_actual,
        )
        logger.debug(f"Relación CUMPLIO creada entre Usuario {id_usuario} y Objetivo {id_objetivo}")
    except Exception as e:
        logger.error(f"Error al crear relación CUMPLIO entre Usuario {id_usuario} y Objetivo {id_objetivo}: {e}")
        raise


def eliminar_relacion_tiene_objetivo(db, id_usuario: int, id_objetivo: int) -> None:
    """
    Elimina una relación TIENE_OBJETIVO entre un Usuario y un Objetivo.
    
    Args:
        db: Conexión a la base de datos Neo4j.
        id_usuario: ID del usuario.
        id_objetivo: ID del objetivo.
    """
    try:
        db.execute_query(
            """
            MATCH (u:Usuario {id_usuario: $id_usuario})-[r:TIENE_OBJETIVO]->(o:Objetivo {id_objetivo: $id_objetivo})
            DELETE r
            """,
            id_usuario=id_usuario,
            id_objetivo=id_objetivo,
        )
        logger.debug(f"Relación TIENE_OBJETIVO eliminada entre Usuario {id_usuario} y Objetivo {id_objetivo}")
    except Exception as e:
        logger.error(f"Error al eliminar relación TIENE_OBJETIVO entre Usuario {id_usuario} y Objetivo {id_objetivo}: {e}")
        raise

def eliminar_relacion_cumplio(db, id_usuario: int, id_objetivo: int) -> None:
    """
    Elimina una relación CUMPLIO entre un Usuario y un Objetivo.
    
    Args:
        db: Conexión a la base de datos Neo4j.
        id_usuario: ID del usuario.
        id_objetivo: ID del objetivo.
    """
    try:
        db.execute_query(
            """
            MATCH (u:Usuario {id_usuario: $id_usuario})-[r:CUMPLIO]->(o:Objetivo {id_objetivo: $id_objetivo})
            DELETE r
            """,
            id_usuario=id_usuario,
            id_objetivo=id_objetivo,
        )
        logger.debug(f"Relación CUMPLIO eliminada entre Usuario {id_usuario} y Objetivo {id_objetivo}")
    except Exception as e:
        logger.error(f"Error al eliminar relación CUMPLIO entre Usuario {id_usuario} y Objetivo {id_objetivo}: {e}")
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


def obtener_objetivos_neo4j(db):
    """
    Obtiene la lista de objetivos desde Neo4j con sus atributos.
    
    Args:
        db: Conexión a la base de datos Neo4j.
        
    Returns:
        list: Lista de diccionarios con datos de objetivos.
    """
    try:
        records, _, _ = db.execute_query(
            """
            MATCH (o:Objetivo)
            RETURN o.id_objetivo AS id_objetivo, o.tipo_dato AS tipo_dato,
                o.umbral_minimo AS umbral_minimo, o.umbral_maximo AS umbral_maximo,
                o.dias_consecutivos_minimos AS dias_minimos
            """
        )
        objetivos = [r.data() for r in records]
        logger.info(f"Obtenidos {len(objetivos)} objetivos de Neo4j")
        return objetivos
    except Exception as e:
        logger.error(f"Error al obtener objetivos de Neo4j: {e}")
        raise


def evaluar_cumplimiento_objetivo(db_sensor_pulsera, id_usuario, objetivo):
    """
    Evalúa si un usuario cumple un objetivo específico según los datos de sensores.
    
    Args:
        db_sensor_pulsera: Conexión a la base de datos MongoDB.
        id_usuario: ID del usuario a evaluar.
        objetivo: Diccionario con datos del objetivo a evaluar.
        
    Returns:
        bool: True si el usuario cumple el objetivo, False en caso contrario.
    """
    try:
        # Fecha límite basada en los días mínimos del objetivo
        fecha_limite = datetime.now() - timedelta(days=objetivo["dias_minimos"])
        
        # Buscar registros relevantes para el objetivo
        registros = db_sensor_pulsera.pulseras_inteligentes.datos_sensor.find({
            "id_usuario": id_usuario,
            "timestamp": {"$gte": fecha_limite},
            f"datos.{objetivo['tipo_dato']}": {"$exists": True},
        })
        
        # Extraer los valores del tipo de dato específico
        valores = [
            registro["datos"].get(objetivo["tipo_dato"])
            for registro in registros
            if objetivo["tipo_dato"] in registro["datos"]
        ]
        
        # Verificar cumplimiento
        if len(valores) >= objetivo["dias_minimos"]:
            valor_promedio = sum(valores) / len(valores)
            return cumple_objetivo(
                valor_promedio,
                objetivo["umbral_minimo"],
                objetivo["umbral_maximo"]
            )
        return False
    
    except Exception as e:
        logger.error(f"Error al evaluar cumplimiento del objetivo {objetivo['id_objetivo']} para usuario {id_usuario}: {e}")
        return False


def actualizar_relaciones_usuario_objetivo(db_grafo, db_sensor_pulsera, id_usuario, objetivo):
    """
    Actualiza las relaciones entre un usuario y un objetivo según su cumplimiento.
    
    Args:
        db_grafo: Conexión a la base de datos Neo4j.
        db_sensor_pulsera: Conexión a la base de datos MongoDB.
        id_usuario: ID del usuario.
        objetivo: Diccionario con datos del objetivo.
        
    Returns:
        tuple: (cumplimiento, mensaje) donde cumplimiento es un booleano y mensaje
               es un string descriptivo del resultado.
    """
    cumplimiento = evaluar_cumplimiento_objetivo(db_sensor_pulsera, id_usuario, objetivo)
    id_objetivo = objetivo["id_objetivo"]
    
    if cumplimiento:
        crear_relacion_cumplio(db_grafo, id_usuario, id_objetivo)
        eliminar_relacion_tiene_objetivo(db_grafo, id_usuario, id_objetivo)
        return True, f"Usuario {id_usuario} CUMPLE objetivo {id_objetivo}"
    else:
        crear_relacion_tiene_objetivo(db_grafo, id_usuario, id_objetivo)
        eliminar_relacion_cumplio(db_grafo, id_usuario, id_objetivo)
        return False, f"Usuario {id_usuario} NO CUMPLE objetivo {id_objetivo}"


def main():
    """
    Función principal que coordina la actualización de relaciones Usuario-Objetivo.
    """
    nombre_proceso = "ETL_RELACION_USUARIO_OBJETIVO"
    
    with manejo_errores_proceso(nombre_proceso):
        # Conexiones a bases de datos
        db_sensor_pulsera = conectar_db_sensor_pulsera()
        db_grafo = conectar_db_grafo_usuarios()
        
        try:
            # Obtener usuarios y objetivos
            usuarios = obtener_usuarios_neo4j(db_grafo)
            objetivos = obtener_objetivos_neo4j(db_grafo)
            
            # Contadores para resumen final
            total_cumplidos = 0
            total_pendientes = 0
            
            # Iterar sobre usuarios y objetivos para actualizar relaciones
            for id_usuario in usuarios:
                logger.info(f"Procesando usuario {id_usuario}")
                
                for objetivo in objetivos:
                    cumplimiento, mensaje = actualizar_relaciones_usuario_objetivo(
                        db_grafo, db_sensor_pulsera, id_usuario, objetivo
                    )
                    
                    if cumplimiento:
                        total_cumplidos += 1
                        logger.debug(mensaje)
                    else:
                        total_pendientes += 1
                        logger.debug(mensaje)
            
            # Resumen final
            logger.info(f"Relaciones Usuario-Objetivo actualizadas: {total_cumplidos + total_pendientes} total, "
                       f"{total_cumplidos} cumplidos, {total_pendientes} pendientes")
        
        finally:
            # Cierre de conexiones
            db_sensor_pulsera.close()
            db_grafo.close()


if __name__ == "__main__":
    main()
