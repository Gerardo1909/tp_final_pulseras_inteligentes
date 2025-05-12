"""
Script ETL para cargar la dimensión de usuarios en el Data Warehouse.

Este script extrae la información de usuarios desde la base de datos transaccional
y la carga en la dimensión de usuarios del Data Warehouse, considerando solo
los usuarios nuevos desde la última carga.
"""

from pulseras_inteligentes.utils.conexiones_db import conectar_db_transacciones, conectar_DW
from pulseras_inteligentes.utils.etl_funcs import manejo_errores_etl, logger

def extraer_ultima_fecha_insercion_dim_usuarios(db_dw):
    """
    Obtiene la fecha del último registro insertado en la dimensión de usuarios.
    
    Args:
        db_dw: Conexión al Data Warehouse.
        
    Returns:
        str: Fecha del último registro o None si no hay registros.
    """
    try:
        respuesta = (
            db_dw.table("dim_usuario")
            .select("fecha_registro")
            .order("fecha_registro", desc=True)
            .limit(1)
            .execute()
        )
        
        if not respuesta.data:
            logger.info("No existen registros previos en la dimensión de usuarios.")
            return None
            
        ultima_fecha = respuesta.data[0]["fecha_registro"]
        logger.info(f"Última fecha de inserción en dimensión usuarios: {ultima_fecha}")
        return ultima_fecha
    except Exception as e:
        logger.error(f"Error al extraer última fecha de inserción en dim_usuario: {e}")
        raise

def extraer_usuarios_por_fecha(db_transacciones, fecha_registro):
    """
    Extrae usuarios de la base de datos transaccional que fueron registrados
    después de la fecha especificada.
    
    Args:
        db_transacciones: Conexión a la base de datos transaccional.
        fecha_registro (str): Fecha de registro a partir de la cual extraer usuarios.
        
    Returns:
        list: Lista de diccionarios con datos de usuarios.
    """
    try:
        respuesta = (
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
            .gt("fecha_registro", fecha_registro)
            .execute()
        )
        
        usuarios = respuesta.data
        logger.info(f"Extraídos {len(usuarios)} usuarios nuevos desde la base transaccional.")
        return usuarios
    except Exception as e:
        logger.error(f"Error al extraer usuarios por fecha: {e}")
        raise

def insertar_usuarios_dim(db_dw, usuarios):
    """
    Inserta usuarios en la dimensión de usuarios del Data Warehouse.
    
    Args:
        db_dw: Conexión al Data Warehouse.
        usuarios (list): Lista de diccionarios con datos de usuarios a insertar.
        
    Returns:
        int: Número de usuarios insertados correctamente.
    """
    contador_exito = 0
    contador_error = 0
    
    for usuario in usuarios:
        try:
            db_dw.table("dim_usuario").insert(
                {
                    "id_usuario": usuario["id_usuario"],
                    "nombre": usuario["nombre"],
                    "genero": usuario["genero"]["genero"],
                    "fecha_registro": usuario["fecha_registro"],
                    "fecha_nacimiento": usuario["fecha_nacimiento"],
                }
            ).execute()
            logger.info(f"Usuario {usuario['nombre']} (ID: {usuario['id_usuario']}) insertado en dim_usuario.")
            contador_exito += 1
        except Exception as e:
            logger.error(f"Error al insertar usuario {usuario['nombre']} (ID: {usuario['id_usuario']}) en dim_usuario: {e}")
            contador_error += 1
    
    logger.info(f"Dimensión Usuarios: {contador_exito} usuarios insertados, {contador_error} errores.")
    return contador_exito

def main():
    """
    Función principal que coordina el proceso ETL de carga de la dimensión de usuarios.
    """
    nombre_etl = "ETL_CARGAR_DIM_USUARIO"
    
    with manejo_errores_etl(nombre_etl):
        # Conexiones a bases de datos
        db_transacciones = conectar_db_transacciones()
        db_dw = conectar_DW()
        
        # Verificación de la última fecha de inserción
        ultima_fecha_registro = extraer_ultima_fecha_insercion_dim_usuarios(db_dw)
        
        # Colocamos una fecha por defecto para la primera carga
        if not ultima_fecha_registro:
            ultima_fecha_registro = "2000-01-01T00:00:00Z"
            logger.info(f"Usando fecha por defecto para primera carga: {ultima_fecha_registro}")
        
        # Extracción de usuarios nuevos
        usuarios_nuevos = extraer_usuarios_por_fecha(db_transacciones, ultima_fecha_registro)
        
        # Inserción de usuarios en la dimensión
        if usuarios_nuevos:
            insertar_usuarios_dim(db_dw, usuarios_nuevos)
            logger.info(f"{nombre_etl}: Proceso completado con éxito.")
        else:
            logger.info("No hay usuarios nuevos para insertar en la dimensión.")

if __name__ == "__main__":
    main()