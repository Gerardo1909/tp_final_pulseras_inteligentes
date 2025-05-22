"""
Script ETL para cargar la tabla de hechos de pagos en la base de datos dimensional 
para análisis de venta.

Este script extrae información de pagos de la base de datos operacional,
obtiene los datos asociados de plan de suscripción y carga los registros
en la tabla de hechos de pagos de la base de datos dimensional.
"""

from pulseras_inteligentes.utils.conexiones_db import conectar_db_transacciones, conectar_DW
from pulseras_inteligentes.utils.etl_funcs import (
    extraer_ultima_fecha_insercion_hechos, 
    obtener_id_fecha, 
    extraer_hora_fecha,
    manejo_errores_proceso,
    logger
)


def extraer_pagos_por_fecha(db_transacciones, fecha_transaccion):
    """
    Extrae información de pagos posteriores a una fecha específica desde la base operacional.
    
    Args:
        db_transacciones: Conexión a la base de datos operacional.
        fecha_transaccion: Fecha a partir de la cual extraer pagos.
        
    Returns:
        list: Lista de diccionarios con datos de pagos o lista vacía si hay error.
    """
    try:
        response = (
            db_transacciones.table("pagos")
            .select(
                """
                id_pago,
                monto,
                fecha_transaccion,
                id_metodo_pago,
                id_estado_pago,
                id_usuario
                """
            )
            .gt("fecha_transaccion", fecha_transaccion)
            .execute()
        )
        
        pagos = response.data
        logger.info(f"Extraídos {len(pagos)} pagos nuevos desde la base operacional")
        return pagos
    except Exception as e:
        logger.error(f"Error al extraer información de pagos: {e}")
        return []


def extraer_id_plan(db_transacciones, id_pago):
    """
    Extrae el ID del plan asociado a un pago desde la tabla de suscripciones.
    
    Args:
        db_transacciones: Conexión a la base de datos operacional.
        id_pago: ID del pago para el que buscar el plan.
        
    Returns:
        int: ID del plan o None si no se encuentra o hay error.
    """
    try:
        response = (
            db_transacciones.table("suscripcion")
            .select("id_pago, id_plan")
            .eq("id_pago", id_pago)
            .execute()
        )
        
        if not response.data:
            logger.warning(f"No se encontró plan asociado al pago ID: {id_pago}")
            return None
            
        id_plan = response.data[0]['id_plan']
        logger.debug(f"Plan ID: {id_plan} asociado al pago ID: {id_pago}")
        return id_plan
    except Exception as e:
        logger.error(f"Error al extraer ID del plan para pago ID {id_pago}: {e}")
        return None


def insertar_hecho_pago(db_dw, id_usuario, id_plan, id_metodo_pago, id_estado_pago, id_fecha, hora_registro, monto_pago):
    """
    Inserta un registro en la tabla de hechos de pagos.
    
    Args:
        db_dw: Conexión al Data Warehouse.
        id_usuario: ID del usuario.
        id_plan: ID del plan de suscripción.
        id_metodo_pago: ID del método de pago.
        id_estado_pago: ID del estado del pago.
        id_fecha: ID de la fecha.
        hora_registro: Hora del registro en formato HH:MM:SS.
        monto_pago: Monto del pago.
        
    Returns:
        bool: True si la inserción fue exitosa, False en caso contrario.
    """
    try:
        db_dw.table("hechos_pagos").insert(
            {
                "id_usuario": id_usuario,
                "id_plan": id_plan,
                "id_metodo_pago": id_metodo_pago,
                "id_estado_pago": id_estado_pago,
                'id_fecha': id_fecha,
                'hora_registro': hora_registro,
                "monto_pago": monto_pago
            }
        ).execute()
        
        logger.debug(f"Hecho de pago insertado para usuario ID: {id_usuario}, plan ID: {id_plan}")
        return True
    except Exception as e:
        logger.error(f"Error al insertar hecho de pago para usuario ID: {id_usuario}: {e}")
        return False


def main():
    """
    Función principal que coordina el proceso ETL de carga de hechos de pagos.
    """
    nombre_proceso = "ETL_CARGAR_HECHOS_PAGOS"
    
    with manejo_errores_proceso(nombre_proceso):
        # Conexiones a bases de datos
        db_transacciones = conectar_db_transacciones()
        db_dw = conectar_DW()
        
        try:
            # Verificación de la última fecha de inserción
            ultima_fecha_transaccion = extraer_ultima_fecha_insercion_hechos(db_dw, 'hechos_pagos')
            
            # Fecha por defecto para primera carga
            if not ultima_fecha_transaccion:
                ultima_fecha_transaccion = "2000-01-01T00:00:00Z"
                logger.info(f"Usando fecha por defecto para primera carga: {ultima_fecha_transaccion}")
            
            # Extracción de pagos nuevos
            pagos = extraer_pagos_por_fecha(db_transacciones, ultima_fecha_transaccion)
            
            if not pagos:
                logger.info("No hay nuevos pagos para insertar en la tabla de hechos")
                return
            
            # Contador para el resumen final
            contador_insertados = 0
            
            # Procesamiento de cada pago
            for pago in pagos:
                # Obtener ID de fecha y hora para el hecho
                fecha_transaccion_str = pago['fecha_transaccion']
                hora_registro = extraer_hora_fecha(fecha_transaccion_str)
                id_fecha = obtener_id_fecha(db_dw, fecha_transaccion_str)
                
                if not id_fecha:
                    logger.warning(f"No se encontró dimensión de fecha para {fecha_transaccion_str}")
                    continue
                
                # Extraer ID del plan (si existe)
                id_plan = extraer_id_plan(db_transacciones, pago['id_pago'])
                
                # Insertar hecho de pago
                if insertar_hecho_pago(
                    db_dw,
                    id_usuario=pago['id_usuario'],
                    id_plan=id_plan,
                    id_metodo_pago=pago['id_metodo_pago'],
                    id_estado_pago=pago['id_estado_pago'],
                    id_fecha=id_fecha,
                    hora_registro=hora_registro,
                    monto_pago=pago['monto']
                ):
                    contador_insertados += 1
            
            # Resumen final
            logger.info(f"Hechos de pagos insertados: {contador_insertados} de {len(pagos)} procesados")
                
        except Exception as e:
            logger.error(f"Error en proceso ETL de hechos de pagos: {e}")
            raise

if __name__ == "__main__":
    main()