# Operaciones sobre el Data Warehouse: Ejemplos centrados en el Usuario

Este documento describe y ejemplifica operaciones típicas sobre el Data Warehouse (DW) del proyecto Pulseras Inteligentes, enfocadas en la entidad principal: el usuario. Cada operación se contextualiza dentro del flujo ETL y la arquitectura del sistema, mostrando cómo los datos viajan desde el sistema operacional hasta el DW.


## 1. Creación de la tabla de usuarios (`dim_usuario`)

### Contexto y ETL
- **Flujo:**
    1. Un usuario se registra y paga una suscripción en el sistema transaccional (PostgreSQL).
    2. Su información se replica en MongoDB para registrar eventos y datos biométricos.
    3. Al final del día, un proceso ETL extrae los usuarios nuevos y los carga en la dimensión `dim_usuario` del DW (PostgreSQL).

### SQL de creación
```sql
CREATE TABLE "dim_usuario" (
    "id_usuario" INTEGER PRIMARY KEY,
    "nombre" VARCHAR(50) NOT NULL,
    "genero" VARCHAR(50) NOT NULL,
    "fecha_registro" TIMESTAMP NOT NULL,
    "fecha_nacimiento" DATE NOT NULL
);
```

### Explicación ETL
- El script `etl_cargar_dim_usuario.py` extrae usuarios nuevos desde la base operacional y los inserta en el DW, asegurando que no se dupliquen registros y que la información esté normalizada para análisis.


## 2. Eliminación de usuarios

**Política del sistema:**
- En este esquema de negocio **NO se elimina información histórica**. Si un usuario deja de usar el sistema, su información persiste en el DW para mantener la trazabilidad y el análisis histórico.
- No existen scripts ni procesos ETL que realicen borrados sobre la dimensión de usuarios.


## 3. Inserción de información generada por usuarios (ETL)

### Contexto y ETL
- **Flujo:**
    1. Una vez que un usuario tiene un registro en la dimensión `dim_usuario` del Data Warehouse, comienza a generar información biométrica (actividad física, sueño, glucosa, reposo) y de interacción con la aplicación móvil.
    2. Estos datos se simulan y almacenan inicialmente en MongoDB mediante los scripts ubicados en `pulseras_inteligentes/sistema_operacional/ingesta_sensor_mongo/gen_data_scripts/`:
        - `generar_registros_sensores.py` (datos biométricos)
        - `generar_registros_aplicacion.py` (datos de uso de la aplicación)
    3. Un proceso ETL extrae periódicamente estos datos simulados y los inserta en las tablas de hechos del Data Warehouse:
        - `hechos_actividad` (actividad física y eventos de aplicación)
        - `hechos_pagos` (pagos y suscripciones, si corresponde)
    4. Cada registro de hechos referencia al usuario mediante la clave foránea `id_usuario`, permitiendo el análisis cruzado de la información generada por cada usuario.

### Ejemplo de inserción en tabla de hechos (fragmento ETL)
```python
def insertar_hecho_actividad(db_dw, id_usuario, id_actividad, id_fecha, hora_registro):
    db_dw.table("hechos_actividad").insert({
        "id_usuario": id_usuario,
        "id_actividad": id_actividad,
        "id_fecha": id_fecha,
        "hora_registro": hora_registro
    }).execute()
```

### Explicación ETL
- El proceso ETL recorre los registros generados en MongoDB, obtiene los identificadores necesarios (usuario, actividad, fecha) y los inserta en las tablas de hechos del DW.
- Se asegura la integridad referencial: solo se insertan hechos para usuarios existentes en la dimensión usuario.
- Los datos generados permiten analizar patrones de comportamiento, actividad física y uso de la aplicación a nivel individual y agregado.

## 4. Actualización de usuarios (ETL)

### Contexto y ETL
- **Flujo típico:**
    1. Si la información de un usuario cambia en el sistema operacional (por ejemplo, corrección de nombre o género), el proceso ETL debe detectar y actualizar el registro correspondiente en el DW.
    2. Aunque el script actual solo inserta nuevos usuarios, una extensión natural sería agregar lógica para actualizar campos modificados.

### Ejemplo de SQL de actualización
```sql
UPDATE dim_usuario
SET nombre = 'Nuevo Nombre', genero = 'Otro'
WHERE id_usuario = 123;
```

### Ejemplo de lógica ETL (propuesta)
```python
def actualizar_usuario_dim(db_dw, usuario):
    db_dw.table("dim_usuario").update({
        "nombre": usuario["nombre"],
        "genero": usuario["genero"]["genero"]
    }).eq("id_usuario", usuario["id_usuario"]).execute()
```

### Explicación ETL
- Se recomienda implementar una comparación de campos para detectar cambios y solo actualizar cuando sea necesario.
- Toda actualización debe quedar registrada para auditoría.


## 5. Búsquedas de una clave y de dos claves

### a) Búsqueda por una clave (por ID de usuario)
```sql
SELECT * FROM dim_usuario WHERE id_usuario = 123;
```

### b) Búsqueda por dos claves (por ID de usuario y género)
```sql
SELECT * FROM dim_usuario WHERE id_usuario = 123 AND genero = 'Femenino';
```

---

**Nota:** Todas las operaciones y ejemplos están centrados en el usuario, siguiendo la política de no eliminación y asegurando la trazabilidad histórica en el Data Warehouse. 