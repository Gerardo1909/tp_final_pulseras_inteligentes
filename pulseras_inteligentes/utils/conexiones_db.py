"""
Módulo para gestión de conexiones a bases de datos del sistema de pulseras inteligentes.

Este módulo proporciona funciones para conectar con las diferentes bases de datos
utilizadas en el proyecto.
"""

from neo4j import GraphDatabase
from pymongo import MongoClient
import supabase
from dotenv import load_dotenv
import os
from typing import Any
from pulseras_inteligentes.utils.etl_funcs import logger

# Carga de variables de entorno
load_dotenv()

# Credenciales y URLs de bases de datos
DB_OPERACIONAL_URL = os.getenv("DB_OPERACIONAL_URL")
DB_OPERACIONAL_API_KEY = os.getenv("DB_OPERACIONAL_API_KEY")
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
DW_API_KEY = os.getenv("DW_API_KEY")
DW_URL = os.getenv("DW_URL")
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

def conectar_db_sensor_pulsera() -> MongoClient:
    """
    Establece conexión con la base de datos MongoDB para datos de sensores.
    
    Returns:
        MongoClient: Cliente de conexión a MongoDB.
    
    Raises:
        Exception: Si ocurre un error durante la conexión.
    """
    try:
        mongo_client = MongoClient(MONGO_DB_URL)
        mongo_client.admin.command('ping')
        logger.info("Conexión con DB de sensores establecida correctamente.")
        return mongo_client
    except Exception as e:
        logger.error(f"Error al conectar con DB de sensores: {e}")
        raise

def conectar_db_grafo_usuarios() -> GraphDatabase.driver:
    """
    Establece conexión con la base de datos Neo4j para el grafo de usuarios.
    
    Returns:
        GraphDatabase.driver: Driver de conexión a Neo4j.
    
    Raises:
        Exception: Si ocurre un error durante la conexión.
    """
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)
        driver.verify_connectivity()
        logger.info("Conexión con DB de grafo de usuarios establecida correctamente.")
        return driver
    except Exception as e:
        logger.error(f"Error al conectar con DB de grafo de usuarios: {e}")
        raise

def conectar_db_transacciones() -> Any:
    """
    Establece conexión con la base de datos operacional en Supabase.
    
    Returns:
        Cliente de conexión a Supabase.
    
    Raises:
        Exception: Si ocurre un error durante la conexión.
    """
    try:
        supabase_client = supabase.create_client(DB_OPERACIONAL_URL, DB_OPERACIONAL_API_KEY)
        supabase_client.table('usuarios').select('*').execute()
        logger.info("Conexión con DB de transacciones establecida correctamente.")
        return supabase_client
    except Exception as e:
        logger.error(f"Error al conectar con DB de transacciones: {e}")
        raise

def conectar_DW() -> Any:
    """
    Establece conexión con el Data Warehouse en Supabase.
    
    Returns:
        Cliente de conexión a Supabase para el Data Warehouse.
    
    Raises:
        Exception: Si ocurre un error durante la conexión.
    """
    try:
        supabase_client = supabase.create_client(DW_URL, DW_API_KEY)
        supabase_client.table('hechos_pagos').select('*').execute()
        logger.info("Conexión con el DW establecida correctamente.")
        return supabase_client
    except Exception as e:
        logger.error(f"Error al conectar con el DW: {e}")
        raise

if __name__ == "__main__":
    # Pruebas de conexión
    try:
        mongo_client = conectar_db_sensor_pulsera()
        neo4j_client = conectar_db_grafo_usuarios()
        db_operacional_client = conectar_db_transacciones()
        dw_client = conectar_DW()
        
        logger.info("Todas las conexiones establecidas correctamente.")
    except Exception as e:
        logger.error(f"Error en las pruebas de conexión: {e}")


