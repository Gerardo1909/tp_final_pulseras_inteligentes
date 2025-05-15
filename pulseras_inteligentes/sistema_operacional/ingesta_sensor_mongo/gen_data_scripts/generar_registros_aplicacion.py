"""
Script para generar e insertar datos simulados de uso de la aplicación en MongoDB.

Este script genera datos sintéticos para simular el uso de la aplicación móvil
por parte de los usuarios, incluyendo diferentes tipos de eventos como tiempo
en pantalla, clicks en botones, envío de formularios y uso de funcionalidades.
"""

from datetime import datetime, timedelta
import random
from pymongo import MongoClient
from pulseras_inteligentes.utils.conexiones_db import conectar_db_sensor_pulsera
from pulseras_inteligentes.utils.etl_funcs import manejo_errores_proceso, logger


def generar_datos_aplicacion_usuario(id_usuario: int, fecha_base: datetime) -> dict:
    """
    Genera datos sintéticos de uso de la aplicación para un usuario en una fecha específica.
    
    Args:
        id_usuario: ID del usuario.
        fecha_base: Fecha base para la generación de datos.
    
    Returns:
        dict: Datos de uso de la aplicación generados.
    """
    # Selección del tipo de evento
    tipos_evento = ["tiempo_pantalla", "click_boton", "envio_formulario", "uso_funcionalidad"]
    tipo_evento = random.choice(tipos_evento)
    
    # Datos comunes para todos los tipos de evento
    registro_aplicacion = {
        "id_usuario": id_usuario,
        "timestamp": fecha_base.replace(
            hour=random.randint(8, 21), 
            minute=random.randint(0, 59), 
            second=random.randint(0, 59)
        ),
        "tipo_evento": tipo_evento,
        "id_sesion": f"ses-{random.randint(100000, 999999)}",
        "version_aplicacion": f"{random.randint(1, 2)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
        "version_os": f"Android {random.randint(9, 13)}"
    }

    # Datos específicos según el tipo de evento
    if tipo_evento == "tiempo_pantalla":
        registro_aplicacion["nombre_pantalla"] = random.choice([
            "inicio", "perfil", "entrenamiento", "progreso", "ajustes"
        ])
        registro_aplicacion["detalles"] = {
            "duracion_segundos": random.randint(5, 600),  # Entre 5 segundos y 10 minutos
        }
    
    elif tipo_evento == "click_boton":
        registro_aplicacion["nombre_boton"] = random.choice([
            "iniciar", "detener", "guardar", "cancelar", "enviar", "ver_mas"
        ])
        registro_aplicacion["nombre_pantalla"] = random.choice([
            "inicio", "perfil", "entrenamiento", "progreso", "ajustes"
        ])
        registro_aplicacion["detalles"] = {}
    
    elif tipo_evento == "envio_formulario":
        registro_aplicacion["nombre_formulario"] = random.choice([
            "login", "registro", "buscar_alimentos", "configurar_objetivos"
        ])
        registro_aplicacion["detalles"] = {
            "campos_completados": random.randint(1, 5),  # Número de campos llenados
        }
    
    else:  # uso_funcionalidad
        registro_aplicacion["nombre_funcionalidad"] = random.choice([
            "iniciar_entrenamiento", "registrar_comida", "ver_estadisticas", "configurar_notificaciones"
        ])
        
        # Detalles específicos según la funcionalidad
        if registro_aplicacion["nombre_funcionalidad"] == "iniciar_entrenamiento":
            registro_aplicacion["detalles"] = {
                "tipo_entrenamiento": random.choice(["correr", "caminar", "pesas", "yoga"]),
                "duracion_minutos": random.randint(10, 120),
            }
        elif registro_aplicacion["nombre_funcionalidad"] == "registrar_comida":
            registro_aplicacion["detalles"] = {
                "alimentos": [
                    {"nombre": "Pollo asado", "cantidad": 200, "unidad": "gramos"},
                    {"nombre": "Ensalada mixta", "cantidad": 1, "unidad": "plato"}
                ],
                "calorias_totales": 450
            }
        elif registro_aplicacion["nombre_funcionalidad"] == "ver_estadisticas":
            registro_aplicacion["detalles"] = {
                "tipo_estadistica": random.choice(["pasos", "sueño", "calorias", "distancia"]),
                "periodo": random.choice(["diario", "semanal", "mensual"]),
            }
        else:  # configurar_notificaciones
            registro_aplicacion["detalles"] = {
                "notificaciones_activadas": random.choice([True, False]),
                "frecuencia": random.choice(["inmediato", "diario", "semanal"])
            }
    
    return registro_aplicacion


def generar_datos_aplicacion(n_dias: int, usuarios: list, datos_db_aplicacion: MongoClient) -> int:
    """
    Genera datos de uso de la aplicación para un número de días y para todos los usuarios.
    
    Args:
        n_dias: Número de días para generar datos, comenzando desde hoy hacia atrás.
        usuarios: Lista de documentos de usuarios con sus IDs.
        datos_db_aplicacion: Colección de MongoDB para almacenar los datos.
    
    Returns:
        int: Total de registros insertados.
    """
    contador_total = 0
    
    for usuario in usuarios:
        id_usuario = usuario["id_usuario"]
        logger.info(f"Generando datos de aplicación para usuario {id_usuario} ({usuario.get('nombre', 'Sin nombre')})")
        
        # Para cada día, generamos entre 1 y 5 registros
        for i in range(n_dias):
            fecha_base = datetime.now() - timedelta(days=i)
            num_registros = random.randint(1, 5)
            
            for _ in range(num_registros):
                registro_aplicacion = generar_datos_aplicacion_usuario(id_usuario, fecha_base)
                datos_db_aplicacion.insert_one(registro_aplicacion)
                contador_total += 1
    
    logger.info(f"Total de registros de uso de aplicación insertados: {contador_total}")
    return contador_total


def main():
    """
    Función principal que coordina la generación e inserción de datos de uso de la aplicación.
    """
    nombre_proceso = "GENERAR_REGISTROS_APLICACION"
    
    with manejo_errores_proceso(nombre_proceso):
        # Conexión a la base de datos
        db_sensor_pulsera = conectar_db_sensor_pulsera()
        
        try:
            # Obtención de la colección de datos y usuarios
            datos_db_aplicacion = db_sensor_pulsera.pulseras_inteligentes.datos_aplicacion
            usuarios = list(db_sensor_pulsera.pulseras_inteligentes.usuarios_sensor.find())
            
            logger.info(f"Iniciando generación de datos de aplicación para {len(usuarios)} usuarios")
            
            # Generación de datos para 10 días
            n_dias = 10
            total_registros = generar_datos_aplicacion(n_dias, usuarios, datos_db_aplicacion)
            
            logger.info(f"{nombre_proceso}: Proceso completado con éxito. {total_registros} registros generados en total.")
        finally:
            # Cierre de conexión
            db_sensor_pulsera.close()


if __name__ == "__main__":
    main()