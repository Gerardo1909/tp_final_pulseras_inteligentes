# Sistema Transaccional para Pulseras Inteligentes

Este directorio contiene los componentes del sistema transaccional para la aplicación de pulseras inteligentes. El sistema transaccional es responsable de gestionar todos los datos operativos del negocio, incluyendo información de sensores, interacciones de usuario y transacciones comerciales.

## Propósito del Sistema Transaccional

El sistema transaccional cumple varios roles fundamentales dentro de la aplicación:

1. **Captura de datos en tiempo real**: Registra todos los datos generados por los sensores de las pulseras inteligentes y las interacciones de los usuarios con la aplicación.

2. **Procesamiento de operaciones comerciales**: Gestiona las transacciones de negocio como suscripciones, pagos y planes.

3. **Alimentación del sistema de recomendaciones y Data Warehouse**: Proporciona los datos necesarios que, mediante procesos ETL, se transforman y cargan en el sistema de recomendaciones Neo4j y en el Data Warehouse.

4. **Persistencia de datos operativos**: Garantiza el almacenamiento seguro y eficiente de todos los datos operativos necesarios para el funcionamiento del negocio.

## Estructura del Directorio

El sistema transaccional está organizado en dos componentes principales:

### 1. Pulsera Inteligente (`pulsera_inteligente/`)

Este subdirectorio contiene los componentes relacionados con la captura y almacenamiento de datos de sensores y de la aplicación utilizando MongoDB como base de datos NoSQL.

**Principales componentes**:
- `estructura_bd.mongodb`: Define la estructura de las colecciones en MongoDB.
- `etl_scripts/`: Scripts para procesar los datos de sensores y aplicación móvil.

Para más detalles sobre la estructura de la base de datos MongoDB, consulte el [README específico](./pulsera_inteligente/README.md).

### 2. Transacciones de Negocio (`transacciones_negocio/`)

Este subdirectorio contiene los componentes relacionados con las operaciones comerciales del sistema, utilizando PostgreSQL (Supabase) como base de datos relacional.

**Principales componentes**:
- `creacion_db.sql`: Script para crear la estructura de tablas en PostgreSQL.
- `insercion_datos.sql`: Script para insertar datos iniciales en las tablas.

Para más detalles sobre la estructura de la base de datos que soporta las transacciones, consulte el [README específico](./transacciones_negocio/README.md).

## Flujo de Datos

El flujo de datos en el sistema transaccional sigue estos pasos:

1. Los usuarios generan datos a través de sus pulseras inteligentes y la interacción con la aplicación.
2. Estos datos se almacenan en tiempo real en las colecciones de MongoDB (`usuarios_sensor`, `datos_sensor`, `datos_aplicacion`).
3. Las transacciones de negocio (suscripciones, pagos) se registran en las tablas de PostgreSQL.
4. Los scripts ETL procesan periódicamente estos datos para alimentar el sistema de recomendaciones Neo4j y al Datawarehouse respectivamente.

