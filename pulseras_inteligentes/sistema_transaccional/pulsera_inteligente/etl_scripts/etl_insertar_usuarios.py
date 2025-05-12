"""
Script ETL para transferir datos de usuarios desde la base de datos transaccional
a la base de datos de sensores de pulsera.

Este script extrae usuarios de la base de datos transaccional y los inserta en
la colección de usuarios de MongoDB, que sirve como fuente para los datos de sensores.
"""

from datetime import datetime
from pulseras_inteligentes.utils.conexiones_db import (
    conectar_db_sensor_pulsera, 
    conectar_db_transacciones
)
from pulseras_inteligentes.utils.etl_funcs import manejo_errores_etl, logger

def extraer_usuarios_transaccionales():
    """
    Extrae datos de usuarios desde la base de datos transaccional.
    
    Returns:
        list: Lista de diccionarios con datos de usuarios.
    """
    db_transacciones = conectar_db_transacciones()
    usuarios = db_transacciones.table('usuarios').select(
        'id_usuario', 'nombre', 'fecha_registro'
    ).execute()
    
    # Conversión de fecha de registro a formato datetime
    for usuario in usuarios.data:
        usuario['fecha_registro'] = datetime.fromisoformat(usuario['fecha_registro'])
    
    logger.info(f"Extraídos {len(usuarios.data)} usuarios de la base de datos transaccional.")
    return usuarios.data

def cargar_usuarios_mongodb(usuarios, db_sensor_pulsera):
    """
    Carga usuarios en la base de datos MongoDB de sensores.
    
    Args:
        usuarios (list): Lista de diccionarios con datos de usuarios.
        db_sensor_pulsera (MongoClient): Conexión a la base de datos MongoDB.
    
    Returns:
        tuple: (contador_insertados, contador_existentes) con el número de usuarios
               insertados y el número de usuarios que ya existían.
    """
    usuarios_db_sensor = db_sensor_pulsera.pulseras_inteligentes.usuarios_sensor
    
    contador_insertados = 0
    contador_existentes = 0
    
    for usuario in usuarios:
        if not usuarios_db_sensor.find_one({"id_usuario": usuario['id_usuario']}):
            usuarios_db_sensor.insert_one(usuario)
            logger.info(f"Usuario insertado: {usuario['nombre']} (ID: {usuario['id_usuario']})")
            contador_insertados += 1
        else:
            logger.debug(f"Usuario ya existe: {usuario['nombre']} (ID: {usuario['id_usuario']})")
            contador_existentes += 1
    
    logger.info(f"Usuarios insertados: {contador_insertados}, usuarios existentes: {contador_existentes}")
    return contador_insertados, contador_existentes

def main():
    """
    Función principal que coordina el proceso ETL de inserción de usuarios.
    """
    nombre_etl = "ETL_INSERTAR_USUARIOS"
    
    with manejo_errores_etl(nombre_etl):
        # Conexión a la base de datos MongoDB
        db_sensor_pulsera = conectar_db_sensor_pulsera()
        
        try:
            # Extracción de usuarios
            usuarios = extraer_usuarios_transaccionales()
            
            # Carga de usuarios en MongoDB
            cargar_usuarios_mongodb(usuarios, db_sensor_pulsera)
            
            logger.info(f"{nombre_etl}: Proceso completado con éxito.")
        finally:
            # Cerrar conexión
            db_sensor_pulsera.close()

if __name__ == "__main__":
    main()
