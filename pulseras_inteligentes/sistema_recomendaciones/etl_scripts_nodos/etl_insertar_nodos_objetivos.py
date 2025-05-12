from pulseras_inteligentes.utils.conexiones_db import conectar_db_grafo_usuarios

def insertar_objetivo(db, objetivo: dict):
    """
    Inserta un nodo de Objetivo en la base de datos Neo4j.

    Parámetros:
        db: Conexión a la base de datos Neo4j.
        objetivo (dict): Diccionario con los datos del objetivo.
    """
    db.execute_query(
        """
        CREATE (:Objetivo {
            id_objetivo: $id_objetivo,
            nombre: $nombre,
            descripcion: $descripcion,
            tipo_dato: $tipo_dato,
            umbral_minimo: $umbral_minimo,
            umbral_maximo: $umbral_maximo,
            unidad: $unidad,
            dias_consecutivos_minimos: $dias_consecutivos_minimos
        })
        """,
        id_objetivo=objetivo["id_objetivo"],
        nombre=objetivo["nombre"],
        descripcion=objetivo["descripcion"],
        tipo_dato=objetivo["tipo_dato"],
        umbral_minimo=objetivo["umbral_minimo"],
        umbral_maximo=objetivo["umbral_maximo"],
        unidad=objetivo["unidad"],
        dias_consecutivos_minimos=objetivo["dias_consecutivos_minimos"],
    )
    print(f'Objetivo {objetivo["nombre"]} insertado en la base de datos Neo4j.')


def main():
    """
    Función principal para insertar objetivos en la base de datos Neo4j.
    """
    objetivos = [
        {
            "id_objetivo": 1,
            "nombre": "Caminatas diarias",
            "descripcion": "Acumular más de 7000 pasos por día",
            "tipo_dato": "cantidad_pasos",
            "umbral_minimo": 7000,
            "umbral_maximo": None,
            "unidad": "pasos",
            "dias_consecutivos_minimos": 7,
        },
        {
            "id_objetivo": 2,
            "nombre": "Reposo consciente",
            "descripcion": "Tener períodos prolongados de reposo con respiración controlada",
            "tipo_dato": "minutos_sin_movimiento",
            "umbral_minimo": 30,
            "umbral_maximo": None,
            "unidad": "minutos",
            "dias_consecutivos_minimos": 7,
        },
        {
            "id_objetivo": 3,
            "nombre": "Control de glucosa",
            "descripcion": "Mantener niveles estables de glucosa en sangre",
            "tipo_dato": "nivel_glucosa",
            "umbral_minimo": 80,
            "umbral_maximo": 120,
            "unidad": "mg/dL",
            "dias_consecutivos_minimos": 7,
        },
        {
            "id_objetivo": 4,
            "nombre": "Sueño reparador",
            "descripcion": "Dormir más de 7 horas diarias",
            "tipo_dato": "duracion_total_min",
            "umbral_minimo": 420,  # 7 horas
            "umbral_maximo": None,
            "unidad": "minutos",
            "dias_consecutivos_minimos": 7,
        },
    ]

    try:
        # Conexión a la base de datos Neo4j
        db_grafo_usuarios = conectar_db_grafo_usuarios()

        # Inserción de objetivos
        for objetivo in objetivos:
            insertar_objetivo(db_grafo_usuarios, objetivo)

    except Exception as e:
        print(f"Error al insertar objetivos: {e}")
    finally:
        db_grafo_usuarios.close()


if __name__ == "__main__":
    main()