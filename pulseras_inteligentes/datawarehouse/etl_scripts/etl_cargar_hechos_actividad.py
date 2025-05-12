"""
Script ETL para cargar la tabla de hechos de actividad en el Data Warehouse.

Este script extrae datos de actividad física y uso de aplicación desde MongoDB,
obtiene los IDs correspondientes de la dimensión de actividad y fecha,
y carga los registros en la tabla de hechos de actividad en el Data Warehouse.
"""

from datetime import datetime
from pulseras_inteligentes.utils.conexiones_db import conectar_db_sensor_pulsera, conectar_DW
from pulseras_inteligentes.utils.etl_funcs import (
    extraer_ultima_fecha_insercion_hechos, 
    obtener_id_fecha, 
    extraer_hora_fecha,
    manejo_errores_etl,
    logger
)

def extraer_actividad_fisica(db_sensor_pulsera, id_usuario, fecha_base):
    """
    Extrae registros de actividad física para un usuario desde MongoDB,
    posteriores a una fecha determinada.
    
    Args:
        db_sensor_pulsera: Conexión a la base de datos MongoDB.
        id_usuario (int): ID del usuario.
        fecha_base (datetime): Fecha a partir de la cual extraer registros.
        
    Returns:
        list: Lista de documentos con datos de actividad física.
    """
    try:
        datos_db_sensor = db_sensor_pulsera.pulseras_inteligentes.datos_sensor
        
        actividades = list(datos_db_sensor.find({
            "id_usuario": id_usuario,
            "tipo_registro": "actividad", 
            "timestamp": {"$gt": fecha_base}
        }))
        
        logger.debug(f"Extraídos {len(actividades)} registros de actividad física para usuario {id_usuario}")
        return actividades
    except Exception as e:
        logger.error(f"Error al extraer actividad física para usuario {id_usuario}: {e}")
        return []

def extraer_actividad_aplicacion(db_sensor_pulsera, id_usuario, fecha_base):
    """
    Extrae registros de uso de aplicación para un usuario desde MongoDB,
    posteriores a una fecha determinada.
    
    Args:
        db_sensor_pulsera: Conexión a la base de datos MongoDB.
        id_usuario (int): ID del usuario.
        fecha_base (datetime): Fecha a partir de la cual extraer registros.
        
    Returns:
        list: Lista de documentos con datos de uso de aplicación.
    """
    try:
        datos_db_aplicacion = db_sensor_pulsera.pulseras_inteligentes.datos_aplicacion
        
        actividades = list(datos_db_aplicacion.find({
            "id_usuario": id_usuario,
            "timestamp": {"$gt": fecha_base}
        }))
        
        logger.debug(f"Extraídos {len(actividades)} registros de actividad de aplicación para usuario {id_usuario}")
        return actividades
    except Exception as e:
        logger.error(f"Error al extraer actividad de aplicación para usuario {id_usuario}: {e}")
        return []

def obtener_id_actividad(db_dw, nombre_actividad):
    """
    Obtiene el ID de una actividad desde la dimensión de actividad.
    
    Args:
        db_dw: Conexión al Data Warehouse.
        nombre_actividad (str): Nombre de la actividad.
        
    Returns:
        int: ID de la actividad o None si no se encuentra.
    """
    try:
        respuesta = (
            db_dw.table("dim_actividad")
            .select("id_actividad, descripcion")
            .eq("descripcion", nombre_actividad)
            .execute()
        )
        
        if not respuesta.data:
            logger.warning(f"No se encontró ID para la actividad: {nombre_actividad}")
            return None
            
        id_actividad = respuesta.data[0]['id_actividad']
        logger.debug(f"ID para actividad '{nombre_actividad}': {id_actividad}")
        return id_actividad
    except Exception as e:
        logger.error(f"Error al extraer ID de actividad '{nombre_actividad}': {e}")
        return None

def insertar_hecho_actividad(db_dw, id_usuario, id_actividad, id_fecha, hora_registro):
    """
    Inserta un registro en la tabla de hechos de actividad.
    
    Args:
        db_dw: Conexión al Data Warehouse.
        id_usuario (int): ID del usuario.
        id_actividad (int): ID de la actividad.
        id_fecha (int): ID de la fecha.
        hora_registro (str): Hora del registro en formato HH:MM:SS.
        
    Returns:
        bool: True si la inserción fue exitosa, False en caso contrario.
    """
    try:
        if not all([id_usuario, id_actividad, id_fecha, hora_registro]):
            logger.warning(f"Datos incompletos para inserción: usuario={id_usuario}, actividad={id_actividad}, fecha={id_fecha}")
            return False
            
        db_dw.table("hechos_actividad").insert({
            "id_usuario": id_usuario,
            "id_actividad": id_actividad,
            "id_fecha": id_fecha,
            "hora_registro": hora_registro
        }).execute()
        
        logger.debug(f"Hecho insertado: usuario={id_usuario}, actividad={id_actividad}, fecha={id_fecha}")
        return True
    except Exception as e:
        logger.error(f"Error al insertar hecho para usuario {id_usuario}: {e}")
        return False

def procesar_actividades_fisicas(db_dw, actividades, id_usuario):
    """
    Procesa y carga registros de actividad física en la tabla de hechos.
    
    Args:
        db_dw: Conexión al Data Warehouse.
        actividades (list): Lista de documentos con datos de actividad física.
        id_usuario (int): ID del usuario.
        
    Returns:
        int: Número de registros insertados correctamente.
    """
    contador = 0
    
    for actividad in actividades:
        # Nombre e ID de la actividad
        nombre_actividad = actividad["datos"]["tipo_actividad"]
        id_actividad = obtener_id_actividad(db_dw, nombre_actividad)
        
        # ID de fecha y hora de la actividad
        id_fecha = obtener_id_fecha(db_dw, actividad["timestamp"])
        hora_actividad = extraer_hora_fecha(actividad["timestamp"])
        
        # Inserción del hecho
        if insertar_hecho_actividad(db_dw, id_usuario, id_actividad, id_fecha, hora_actividad):
            contador += 1
    
    return contador

def procesar_actividades_aplicacion(db_dw, actividades, id_usuario):
    """
    Procesa y carga registros de uso de aplicación en la tabla de hechos.
    
    Args:
        db_dw: Conexión al Data Warehouse.
        actividades (list): Lista de documentos con datos de uso de aplicación.
        id_usuario (int): ID del usuario.
        
    Returns:
        int: Número de registros insertados correctamente.
    """
    contador = 0
    
    for actividad in actividades:
        # Nombre e ID de la actividad
        nombre_actividad = actividad["tipo_evento"]
        id_actividad = obtener_id_actividad(db_dw, nombre_actividad)
        
        # ID de fecha y hora de la actividad
        id_fecha = obtener_id_fecha(db_dw, actividad["timestamp"])
        hora_actividad = extraer_hora_fecha(actividad["timestamp"])
        
        # Inserción del hecho
        if insertar_hecho_actividad(db_dw, id_usuario, id_actividad, id_fecha, hora_actividad):
            contador += 1
    
    return contador

def main():
    """
    Función principal que coordina el proceso ETL de carga de hechos de actividad.
    """
    nombre_etl = "ETL_CARGAR_HECHOS_ACTIVIDAD"
    
    with manejo_errores_etl(nombre_etl):
        # Conexiones a bases de datos
        db_sensor_pulsera = conectar_db_sensor_pulsera()
        db_dw = conectar_DW()
        
        try:
            # Obtención de usuarios
            usuarios = list(db_sensor_pulsera.pulseras_inteligentes.usuarios_sensor.find())
            logger.info(f"Procesando {len(usuarios)} usuarios para carga de hechos de actividad")
            
            # Obtención de la última fecha de carga
            ultima_fecha_transaccion = extraer_ultima_fecha_insercion_hechos(db_dw, 'hechos_actividad')
            
            # Fecha por defecto para primera carga
            if not ultima_fecha_transaccion:
                ultima_fecha_transaccion = "2000-01-01T00:00:00Z"
                logger.info(f"Usando fecha por defecto para primera carga: {ultima_fecha_transaccion}")
            
            # Conversión a formato datetime
            if isinstance(ultima_fecha_transaccion, str):
                try:
                    ultima_fecha_transaccion = datetime.fromisoformat(ultima_fecha_transaccion.replace("Z", "+00:00"))
                except Exception as e:
                    logger.error(f"Error convirtiendo fecha: {e}")
            
            # Contadores para el resumen
            total_actividad_fisica = 0
            total_actividad_aplicacion = 0
            
            # Procesamiento por usuario
            for usuario in usuarios:
                id_usuario = usuario["id_usuario"]
                
                # Procesamiento de actividad física
                actividades_fisicas = extraer_actividad_fisica(db_sensor_pulsera, id_usuario, ultima_fecha_transaccion)
                registros_act_fisica = procesar_actividades_fisicas(db_dw, actividades_fisicas, id_usuario)
                total_actividad_fisica += registros_act_fisica
                
                # Procesamiento de uso de aplicación
                actividades_aplicacion = extraer_actividad_aplicacion(db_sensor_pulsera, id_usuario, ultima_fecha_transaccion)
                registros_act_aplicacion = procesar_actividades_aplicacion(db_dw, actividades_aplicacion, id_usuario)
                total_actividad_aplicacion += registros_act_aplicacion
            
            # Resumen final
            logger.info(f"Carga completada: {total_actividad_fisica} registros de actividad física, " 
                        f"{total_actividad_aplicacion} registros de actividad de aplicación")
        finally:
            # Cierre de conexiones
            db_sensor_pulsera.close()

if __name__ == "__main__":
    main()