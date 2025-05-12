from datetime import datetime
from dateutil import parser
from typing import Optional, Union, Dict, Any
from contextlib import contextmanager
import logging
import traceback
import os
from pathlib import Path

# Configuración de directorios para logs
LOG_DIR = Path(__file__).parent.parent / "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def configurar_logger(nombre: str = __name__, nivel: int = logging.INFO, 
                     archivo_log: Optional[str] = None) -> logging.Logger:
    """
    Configura un logger con formatos consistentes para su uso en los procesos ETL.
    
    Args:
        nombre: Nombre del logger, normalmente el nombre del módulo.
        nivel: Nivel de logging (INFO, DEBUG, ERROR, etc.).
        archivo_log: Ruta al archivo de logs (opcional).
    
    Returns:
        logging.Logger: El logger configurado.
    """
    logger = logging.getLogger(nombre)
    logger.setLevel(nivel)
    
    # Si ya tiene handlers, no añadir más
    if logger.handlers:
        return logger
    
    # Formato estándar para todos los logs
    formato = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Handler de consola para mostrar información en tiempo real
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formato)
    logger.addHandler(console_handler)
    
    # Handler de archivo si se especifica o usar uno por defecto con fecha
    if not archivo_log:
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        archivo_log = LOG_DIR / f"etl_{fecha_actual}.log"
    
    file_handler = logging.FileHandler(archivo_log)
    file_handler.setFormatter(formato)
    logger.addHandler(file_handler)
    
    return logger

# Logger por defecto para su uso en todo el módulo
logger = configurar_logger()

def registrar_ejecucion_etl(nombre_etl: str, estado: str, detalles: str = "") -> None:
    """
    Registra la ejecución de un proceso ETL en el log.
    
    Args:
        nombre_etl: Nombre del proceso ETL
        estado: Estado de la ejecución ('INICIADO', 'COMPLETADO', 'ERROR')
        detalles: Detalles adicionales sobre la ejecución
    """
    mensaje = f"ETL {nombre_etl}: {estado}"
    if detalles:
        mensaje += f" - {detalles}"
    
    if estado == 'ERROR':
        logger.error(mensaje)
    elif estado == 'INICIADO':
        logger.info(mensaje)
    elif estado == 'COMPLETADO':
        logger.info(mensaje)
    else:
        logger.info(mensaje)
        
@contextmanager
def manejo_errores_etl(nombre_etl: str, raise_exception: bool = True):
    """
    Manejador de contexto para capturar y registrar errores en procesos ETL.
    
    Args:
        nombre_etl: Nombre del proceso ETL
        raise_exception: Si es True, re-lanza la excepción después de registrarla
        
    Ejemplo:
        with manejo_errores_etl("ETL_CARGA_USUARIOS"):
            # código que puede lanzar excepciones
            extraer_datos()
            transformar_datos()
            cargar_datos()
    """
    try:
        registrar_ejecucion_etl(nombre_etl, "INICIADO")
        yield
        registrar_ejecucion_etl(nombre_etl, "COMPLETADO")
    except Exception as e:
        error_detallado = traceback.format_exc()
        logger.error(f"Error en {nombre_etl}: {e}")
        logger.debug(f"Detalles del error: {error_detallado}")
        registrar_ejecucion_etl(nombre_etl, "ERROR", str(e))
        if raise_exception:
            raise

def extraer_ultima_fecha_insercion_hechos(db_dw, nombre_tabla_hechos: str) -> Optional[str]:
    """
    Extrae la fecha de la última inserción en una tabla de hechos.
    
    Args:
        db_dw: Conexión a la base de datos del Data Warehouse.
        nombre_tabla_hechos: Nombre de la tabla de hechos.
        
    Returns:
        str: Fecha en formato ISO o None si no hay registros.
    """
    try:
        # Registramos la operación
        logger.debug(f"Extrayendo última fecha de inserción para tabla {nombre_tabla_hechos}")
        
        # Primero extraigo el id de la fecha 
        id_fecha_respuesta = (
            db_dw.table(nombre_tabla_hechos)
            .select("id_fecha")
            .order("id_fecha", desc=True)
            .limit(1)
            .execute()
        )
        
        if not id_fecha_respuesta.data:
            logger.info(f"No se encontraron registros en la tabla {nombre_tabla_hechos}.")
            return None

        # Ahora busco dicho id en la dim_fecha
        id_fecha = id_fecha_respuesta.data[0]['id_fecha']
        respuesta_dim_fecha = (
            db_dw.table("dim_fecha")
            .select("id_fecha, fecha")
            .eq("id_fecha", id_fecha)
            .execute()
        )

        fecha = respuesta_dim_fecha.data[0]['fecha']
        # La convierto a un formato ISO
        fecha_iso = datetime.strptime(fecha, "%Y-%m-%d").isoformat()
        logger.debug(f"Última fecha de inserción para {nombre_tabla_hechos}: {fecha_iso}")
        return fecha_iso
    
    except Exception as e:
        logger.error(f"Error al extraer la última fecha de inserción para {nombre_tabla_hechos}: {e}")
        return None
    
def obtener_id_fecha(db_dw, fecha_transaccion: Union[str, datetime]) -> Optional[int]:
    """
    Obtiene el ID de fecha correspondiente desde la dimensión de fechas.
    
    Args:
        db_dw: Conexión a la base de datos del Data Warehouse.
        fecha_transaccion: Fecha en formato ISO o objeto datetime.
        
    Returns:
        int: ID de la fecha o None si hay un error.
    """
    try:
        # Solo parsear si no es datetime
        if not isinstance(fecha_transaccion, datetime):
            fecha_transaccion = parser.parse(fecha_transaccion)
        
        fecha_transaccion_str = fecha_transaccion.strftime("%Y-%m-%d")
        logger.debug(f"Buscando ID para fecha: {fecha_transaccion_str}")
        
        respuesta = (
            db_dw.table("dim_fecha")
            .select("id_fecha, fecha")
            .eq("fecha", fecha_transaccion_str)
            .execute()
        )
        
        if not respuesta.data:
            logger.warning(f"No se encontró ID para la fecha {fecha_transaccion_str}")
            return None
            
        return respuesta.data[0]["id_fecha"]
    except Exception as e:
        logger.error(f"Error al obtener ID de fecha: {e}")
        return None
    
def extraer_hora_fecha(fecha: Union[str, datetime]) -> Optional[str]:
    """
    Extrae la hora en formato HH:MM:SS desde una fecha en formato ISO 8601 o un objeto datetime.
    Compatible con Supabase (columna TIME).
    
    Args:
        fecha: Fecha en formato ISO o objeto datetime.
        
    Returns:
        str: Hora en formato HH:MM:SS o None si hay error.
    """
    try:
        # Si es un objeto datetime, usamos directamente
        if isinstance(fecha, datetime):
            dt = fecha
        else:
            # Si no es datetime, intentamos parsear la cadena ISO 8601
            if fecha.endswith("Z"):
                fecha = fecha[:-1]  # Eliminar la "Z" si está presente
            dt = parser.parse(fecha)

        # Retornar solo la hora en formato HH:MM:SS
        hora_formateada = dt.strftime("%H:%M:%S")
        logger.debug(f"Hora extraída: {hora_formateada}")
        return hora_formateada

    except Exception as e:
        logger.error(f"Error al extraer hora: {e}")
        return None