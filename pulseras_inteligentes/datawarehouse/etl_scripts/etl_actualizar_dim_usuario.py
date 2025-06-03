"""
Script ETL para actualizar la dimensión de usuarios en la base de datos dimensional 
para análisis de negocio.

Este script extrae la información actualizada de usuarios desde la base de datos operacional
y realiza las actualizaciones pertinentes en la dimensión de usuarios de la base de datos dimensionala.
"""

from pulseras_inteligentes.utils.conexiones_db import conectar_db_transacciones, conectar_DW
from pulseras_inteligentes.utils.etl_funcs import manejo_errores_proceso, logger


def extraer_ultima_fecha_actualizacion_dim_usuarios(db_dw):
    """
    Obtiene la fecha de la última actualización en la tabla de dimensión de usuarios 
    utilizando la tabla de auditoría.
    
    Args:
        db_dw: Conexión a la base de datos.
        
    Returns:
        str: Fecha de la última actualización o None si no hay registros.
    """
    try:
        # Buscar la última actualización en la tabla de auditoría para dim_usuario
        respuesta_log = (
            db_dw.table("log_eventos")
            .select("fecha_operacion")
            .eq("tabla_afectada", "dim_usuario")
            .eq("operacion", "UPDATE")
            .order("fecha_operacion", desc=True)
            .limit(1)
            .execute()
        )
        
        if not respuesta_log.data:
            logger.info("No se registraron actualizaciones previas en la dimensión de usuarios según log_eventos.")
            return None
        
        # Extraer la fecha de operación del log
        fecha_operacion = respuesta_log.data[0]["fecha_operacion"]
        
        # Si la fecha viene como string, mantenerla así; si es datetime, convertir a string
        if isinstance(fecha_operacion, str):
            ultima_fecha = fecha_operacion
        else:
            # Convertir datetime a string en formato ISO
            ultima_fecha = fecha_operacion.isoformat()
            
        logger.info(f"Última fecha de actualización en dimensión usuarios (desde log_eventos): {ultima_fecha}")
        return ultima_fecha
    except Exception as e:
        logger.error(f"Error al extraer última fecha de actualización en dim_usuario desde log_eventos: {e}")
        raise
    

def obtener_usuarios_actualizados_por_fecha(db_transacciones, ultima_fecha_actualizacion):
    """
    Obtiene los usuarios que han sido actualizados después de una fecha específica.
    
    Args:
        db_transacciones: Conexión a la base de datos operacional.
        ultima_fecha_actualizacion: Fecha a partir de la cual buscar actualizaciones.
        
    Returns:
        list: Lista de diccionarios con datos de usuarios actualizados.
    """
    try:
        
        # Extraer los IDs de usuarios que han sido actualizados
        respuesta_logs = (
            db_transacciones.table("log_eventos")
            .select("clave_primaria")
            .eq("tabla_afectada", "usuarios")
            .eq("operacion", "UPDATE")
            .gt("fecha_operacion", ultima_fecha_actualizacion)
            .execute()
        )
        
        if not respuesta_logs.data:
            logger.info("No se encontraron usuarios actualizados después de la fecha especificada.")
            return []
        
        # Extraer los IDs únicos de usuarios actualizados
        ids_usuarios_actualizados = list(set([
            int(log["clave_primaria"]) for log in respuesta_logs.data
        ]))
        
        logger.info(f"Encontrados {len(ids_usuarios_actualizados)} usuarios con actualizaciones.")
        
        # Obtener los datos actuales de estos usuarios
        respuesta_usuarios = (
            db_transacciones.table("usuarios")
            .select(
                """
                id_usuario,
                nombre,
                genero:genero(genero),
                fecha_registro,
                fecha_nacimiento
                """
            )
            .in_("id_usuario", ids_usuarios_actualizados)
            .execute()
        )
        
        usuarios_actualizados = respuesta_usuarios.data
        logger.info(f"Extraídos {len(usuarios_actualizados)} usuarios actualizados desde la base operacional.")
        return usuarios_actualizados
        
    except Exception as e:
        logger.error(f"Error al obtener usuarios actualizados por fecha: {e}")
        return []


def actualizar_dim_usuario(db_dw, usuarios_a_actualizar):
    """
    Actualiza los registros de usuarios en la dimensión de usuarios del Data Warehouse.
    
    Args:
        db_dw: Conexión a la base de datos del Data Warehouse.
        usuarios_a_actualizar (list): Lista de diccionarios con datos actualizados de usuarios.
        
    Returns:
        int: Número de usuarios actualizados correctamente.
    """
    contador_exito = 0
    contador_error = 0
    
    for usuario in usuarios_a_actualizar:
        try:
            # Verificar que el usuario existe en la dimensión antes de actualizar
            respuesta_verificacion = (
                db_dw.table("dim_usuario")
                .select("id_usuario")
                .eq("id_usuario", usuario["id_usuario"])
                .execute()
            )
            
            if not respuesta_verificacion.data:
                logger.warning(f"Usuario ID {usuario['id_usuario']} no existe en dim_usuario. Saltando actualización.")
                contador_error += 1
                continue
            
            # Realizar la actualización
            respuesta_actualizacion = (
                db_dw.table("dim_usuario")
                .update({
                    "nombre": usuario["nombre"],
                    "genero": usuario["genero"]["genero"],
                    "fecha_registro": usuario["fecha_registro"],
                    "fecha_nacimiento": usuario["fecha_nacimiento"]
                })
                .eq("id_usuario", usuario["id_usuario"])
                .execute()
            )
            
            if respuesta_actualizacion.data:
                logger.info(f"Usuario {usuario['nombre']} (ID: {usuario['id_usuario']}) actualizado en dim_usuario.")
                contador_exito += 1
            else:
                logger.warning(f"No se pudo actualizar el usuario {usuario['nombre']} (ID: {usuario['id_usuario']}).")
                contador_error += 1
                
        except Exception as e:
            logger.error(f"Error al actualizar usuario {usuario.get('nombre', 'Sin nombre')} (ID: {usuario.get('id_usuario', 'Sin ID')}) en dim_usuario: {e}")
            contador_error += 1
    
    logger.info(f"Dimensión Usuarios actualizada: {contador_exito} usuarios actualizados correctamente, {contador_error} errores.")
    return contador_exito


def main():
    """
    Función principal que coordina el proceso ETL de actualizacion de la dimensión de usuarios.
    """
    nombre_proceso = "ETL_ACTUALIZAR_DIM_USUARIO"
    
    with manejo_errores_proceso(nombre_proceso):
        # Conexiones a bases de datos
        db_transacciones = conectar_db_transacciones()
        db_dw = conectar_DW()
        
        # Verificación de la última fecha de inserción
        ultima_fecha_actualizacion = extraer_ultima_fecha_actualizacion_dim_usuarios(db_dw)
        
        # Extraer usuarios actualizados desde la base de datos operacional
        usuarios_actualizados = obtener_usuarios_actualizados_por_fecha(db_transacciones, ultima_fecha_actualizacion)
        
        # Actualización de usuarios en la dimensión
        if usuarios_actualizados:
            actualizar_dim_usuario(db_dw, usuarios_actualizados)
            logger.info(f"{nombre_proceso}: Proceso completado con éxito.")
        else:
            logger.info("No hay usuarios para actualizar en la dimensión.")


if __name__ == "__main__":
    main()