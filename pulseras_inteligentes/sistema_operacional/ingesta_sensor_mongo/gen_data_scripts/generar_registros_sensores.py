"""
Script para generar e insertar datos simulados de sensores de pulsera en MongoDB.

Este script genera datos sintéticos para simular las mediciones de los sensores
de la pulsera inteligente, incluyendo actividad física, reposo, sueño y niveles 
de glucosa para los usuarios existentes en la base de datos.
"""

from datetime import datetime, timedelta
import random
from pymongo import MongoClient
from pulseras_inteligentes.utils.conexiones_db import conectar_db_sensor_pulsera
from pulseras_inteligentes.utils.etl_funcs import manejo_errores_proceso, logger


def generar_datos_actividad(id_usuario: int, fecha_base: datetime) -> dict:
    """
    Genera datos sintéticos de actividad física para un usuario en una fecha específica.
    
    Args:
        id_usuario: ID del usuario.
        fecha_base: Fecha base para la generación de datos.
    
    Returns:
        dict: Datos de actividad generados o None si no hay actividad.
    """
    tiene_actividad = random.random() > 0.2  # 80% de probabilidad de actividad
    if not tiene_actividad:
        return None
        
    tipo_actividad = random.choice(["caminar", "correr", "ciclismo", "entrenamiento_fuerza", "yoga"])
    hora_inicio = fecha_base.replace(hour=random.randint(7, 19), minute=random.randint(0, 59))
    duracion_min = int(random.expovariate(1/60)) + 1  # Duración media de 60 minutos
    calorias_quemadas = int(random.gauss(duracion_min * 7, duracion_min * 3))
    
    # Datos específicos según tipo de actividad
    distancia_km = round(duracion_min * 0.1, 2) if tipo_actividad in ["caminar", "correr", "ciclismo"] else None
    repeticiones = int(random.triangular(5, 15, 10)) if tipo_actividad == "entrenamiento_fuerza" else None
    peso_levantado_kg = round(random.uniform(20, 100), 2) if tipo_actividad == "entrenamiento_fuerza" else None
    ritmo_cardiaco_prom = int(random.gauss(100 + duracion_min * 0.5, 15)) if tipo_actividad in ["caminar", "correr", "ciclismo"] else None
    pasos = int(random.gauss(duracion_min * 100, duracion_min * 30)) if tipo_actividad in ["caminar","correr"] else None

    return {
        "id_usuario": id_usuario,
        "tipo_registro": "actividad",
        "timestamp": hora_inicio,
        "datos": {
            "tipo_actividad": tipo_actividad,
            "duracion_min": duracion_min,
            "distancia_km": distancia_km,
            "pasos": pasos,
            "calorias_quemadas": max(50, calorias_quemadas),
            "repeticiones": repeticiones,
            "peso_levantado_kg": peso_levantado_kg,
            "ritmo_cardiaco_prom": ritmo_cardiaco_prom
        }
    }

def generar_datos_reposo(id_usuario: int, fecha_base: datetime) -> dict:
    """
    Genera datos sintéticos de reposo para un usuario en una fecha específica.
    
    Args:
        id_usuario: ID del usuario.
        fecha_base: Fecha base para la generación de datos.
    
    Returns:
        dict: Datos de reposo generados o None si no hay registro.
    """
    if random.random() <= 0.1:  # 90% de probabilidad de tener datos de reposo
        return None
        
    hora_reposo = fecha_base.replace(hour=random.randint(12, 16), minute=random.randint(0, 59))
    minutos_sin_movimiento = int(random.expovariate(1/30)) + 1  # Media de 30 min
    frecuencia_respiratoria = round(random.gauss(12, 2), 1)
    hrv_ms = int(random.gauss(50, 15))  # Variabilidad de frecuencia cardíaca

    return {
        "id_usuario": id_usuario,
        "tipo_registro": "reposo",
        "timestamp": hora_reposo,
        "datos": {
            "minutos_sin_movimiento": minutos_sin_movimiento,
            "frecuencia_respiratoria": frecuencia_respiratoria,
            "hrv_ms": hrv_ms
        }
    }

def generar_datos_sueno(id_usuario: int, fecha_base: datetime) -> dict:
    """
    Genera datos sintéticos de sueño para un usuario en una fecha específica.
    
    Args:
        id_usuario: ID del usuario.
        fecha_base: Fecha base para la generación de datos.
    
    Returns:
        dict: Datos de sueño generados.
    """
    hora_sueno = fecha_base.replace(hour=random.randint(22, 23), minute=random.randint(0, 59))
    duracion_total_min = int(random.gauss(480, 30))  # Duración media de 8 horas
    sueño_profundo_min = int(random.triangular(90, 180, 120))
    sueño_ligero_min = int(random.triangular(180, 300, 240))
    interrupciones = random.choices([0, 1, 2, 3], weights=[0.6, 0.2, 0.15, 0.05])[0]
    latencia_sueno_min = int(random.expovariate(1/10)) + 1  # Tiempo para conciliar el sueño

    return {
        "id_usuario": id_usuario,
        "tipo_registro": "sueño",
        "timestamp": hora_sueno,
        "datos": {
            "duracion_total_min": duracion_total_min,
            "sueño_profundo_min": sueño_profundo_min,
            "sueño_ligero_min": sueño_ligero_min,
            "interrupciones": interrupciones,
            "latencia_sueno_min": latencia_sueno_min
        }
    }

def generar_datos_glucosa(id_usuario: int, fecha_base: datetime) -> dict:
    """
    Genera datos sintéticos de glucosa para un usuario en una fecha específica.
    
    Args:
        id_usuario: ID del usuario.
        fecha_base: Fecha base para la generación de datos.
    
    Returns:
        dict: Datos de glucosa generados.
    """
    hora_glucosa = fecha_base.replace(hour=random.randint(7, 10), minute=random.randint(0, 59))
    nivel_glucosa = int(random.gauss(90, 15))
    medicion_ayunas = random.choice([True, False])

    return {
        "id_usuario": id_usuario,
        "tipo_registro": "glucosa",
        "timestamp": hora_glucosa,
        "datos": {
            "nivel_glucosa": max(60, min(nivel_glucosa, 180)),  # Limitar a rango realista
            "unidad": "mg/dL",
            "medicion_ayunas": medicion_ayunas
        }
    }

def generar_datos_sensor_usuario(id_usuario: int, fecha_base: datetime, datos_db_sensor: MongoClient) -> int:
    """
    Genera y guarda todos los datos de sensores para un usuario en una fecha dada.
    
    Args:
        id_usuario: ID del usuario.
        fecha_base: Fecha base para la generación de datos.
        datos_db_sensor: Colección de MongoDB para almacenar los datos.
    
    Returns:
        int: Número de registros insertados.
    """
    registros = [
        generar_datos_sueno(id_usuario, fecha_base),
        generar_datos_actividad(id_usuario, fecha_base),
        generar_datos_reposo(id_usuario, fecha_base),
        generar_datos_glucosa(id_usuario, fecha_base),
    ]
    
    contador = 0
    for registro in registros:
        if registro:  # Solo inserta si no es None
            datos_db_sensor.insert_one(registro)
            contador += 1
    
    logger.debug(f"Usuario {id_usuario}, fecha {fecha_base.strftime('%Y-%m-%d')}: {contador} registros insertados")
    return contador

def generar_datos_actividades(n_dias: int, usuarios: list, datos_db_sensor: MongoClient) -> int:
    """
    Genera datos de sensores para un número de días y para todos los usuarios.
    
    Args:
        n_dias: Número de días para generar datos, comenzando desde hoy hacia atrás.
        usuarios: Lista de documentos de usuarios con sus IDs.
        datos_db_sensor: Colección de MongoDB para almacenar los datos.
    
    Returns:
        int: Total de registros insertados.
    """
    total_insertados = 0
    
    for usuario in usuarios:
        id_usuario = usuario["id_usuario"]
        logger.info(f"Generando datos para usuario {id_usuario} ({usuario.get('nombre', 'Sin nombre')})")
        
        for i in range(n_dias):
            fecha_base = datetime.now() - timedelta(days=i)
            insertados = generar_datos_sensor_usuario(id_usuario, fecha_base, datos_db_sensor)
            total_insertados += insertados
    
    logger.info(f"Total de registros de sensores insertados: {total_insertados}")
    return total_insertados

def main():
    """
    Función principal que coordina la generación e inserción de datos de sensores.
    """
    nombre_proceso = "GENERAR_REGISTROS_SENSORES"
    
    with manejo_errores_proceso(nombre_proceso):
        # Conexión a la base de datos
        db_sensor_pulsera = conectar_db_sensor_pulsera()
        
        try:
            # Obtención de la colección de datos y usuarios
            datos_db_sensor = db_sensor_pulsera.pulseras_inteligentes.datos_sensor
            usuarios = list(db_sensor_pulsera.pulseras_inteligentes.usuarios_sensor.find())
            
            logger.info(f"Iniciando generación de datos para {len(usuarios)} usuarios")
            
            # Generación de datos para 10 días
            n_dias = 10
            total_registros = generar_datos_actividades(n_dias, usuarios, datos_db_sensor)
            
            logger.info(f"{nombre_proceso}: Proceso completado con éxito. {total_registros} registros generados en total.")
        finally:
            # Cierre de conexión
            db_sensor_pulsera.close()

if __name__ == "__main__":
    main()
