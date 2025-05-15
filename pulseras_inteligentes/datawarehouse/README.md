# Data Warehouse para Pulseras Inteligentes

Este directorio contiene los componentes del Data Warehouse para la aplicación de pulseras inteligentes. El Data Warehouse implementa un enfoque de persistencia políglota, combinando diferentes tecnologías de almacenamiento para abordar distintos aspectos del análisis de datos.

## Propósito del Data Warehouse

El Data Warehouse cumple varios roles fundamentales dentro de la aplicación:

1. **Análisis histórico de datos**: Almacena y organiza datos históricos para facilitar el análisis de tendencias y patrones a lo largo del tiempo.

2. **Soporte para inteligencia de negocios**: Proporciona una estructura optimizada para consultas analíticas que alimentan los dashboards y reportes utilizados en la toma de decisiones.

3. **Base para el sistema de recomendaciones**: Contiene los datos procesados y estructurados necesarios para generar recomendaciones personalizadas para los usuarios.

4. **Consolidación de fuentes heterogéneas**: Integra datos provenientes de diferentes sistemas operacionales en un modelo coherente y unificado.

## Estructura del Directorio

El Data Warehouse está organizado en tres componentes principales que implementan diferentes paradigmas de almacenamiento:

### 1. Base de datos dimensional para análisis de ventas (`dwh_ventas/`)

Este subdirectorio contiene el modelo dimensional para el análisis de ventas y suscripciones, implementado en **PostgreSQL (Supabase)** siguiendo un esquema en estrella.

**Principales componentes**:
- `creacion_db.sql`: Script para crear la estructura de la base de datos.
- `insercion_datos_dimensiones.sql`: Script para insertar datos dimensionales.
- `etl_ventas/`: Scripts ETL para extraer, transformar y cargar datos desde el sistema operacional.

Para más detalles sobre la estructura del modelo dimensional, consulte el [README específico](./dwh_ventas/README.md).

### 2. Base de datos MongoDB para análisis de usabilidad (`dwh_usabilidad/`)

Este subdirectorio contiene las colecciones de MongoDB diseñadas para analizar la usabilidad de la pulsera y la aplicación móvil, aprovechando la flexibilidad de los documentos JSON para datos semi-estructurados.

**Principales componentes**:
- `estructura_colecciones.mongodb`: Define la estructura de las colecciones analíticas.
- `etl_usabilidad/`: Scripts ETL para procesar y agregar los datos de usabilidad.

Para más detalles sobre las colecciones de análisis de usabilidad, consulte el [README específico](./dwh_usabilidad/README.md).

### 3. Base de datos Neo4j para alimentar sistema de recomendación (`sistema_recomendacion/`)

Este subdirectorio contiene el modelo de grafos implementado en Neo4j para alimentar el sistema de recomendaciones personalizadas basado en relaciones entre usuarios, actividades y objetivos de salud.

**Principales componentes**:
- `etl_scripts_nodos/`: Scripts ETL para procesar y cargar nodos a la base de datos.
- `etl_scripts_relaciones/`: Scripts ETL para procesar y cargar relaciones a la base de datos.

Para más detalles sobre el sistema de recomendación basado en grafos, consulte el [README específico](./sistema_recomendacion/README.md).

## Flujo de Datos

El flujo de datos en el Data Warehouse sigue estos pasos:

1. Los datos operacionales de PostgreSQL (transacciones, usuarios, suscripciones) son extraídos, transformados y cargados en el modelo dimensional (`dwh_ventas`) mediante procesos ETL.

2. Los datos de sensores y aplicación móvil almacenados en MongoDB son procesados, agregados y cargados en las colecciones analíticas (`dwh_usabilidad`) para soportar análisis de usabilidad.

3. Información relevante de ambas fuentes es transformada en nodos y relaciones para alimentar el modelo de grafos en Neo4j (`sistema_recomendacion`), que soporta el sistema de recomendaciones.
