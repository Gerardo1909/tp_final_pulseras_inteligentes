# Sistema operacional para Pulseras Inteligentes

Este directorio contiene los componentes del sistema operacional para la aplicación de pulseras inteligentes. El sistema operacional es responsable de gestionar todos los datos operativos del negocio, incluyendo información de sensores, interacciones de usuario y transacciones comerciales.

## Propósito del Sistema operacional

El sistema operacional cumple varios roles fundamentales dentro de la aplicación:

1. **Procesamiento de operaciones comerciales**: Gestiona las transacciones de negocio como suscripciones, pagos y planes.

2. **Captura de datos en tiempo real**: Registra todos los datos generados por los sensores de las pulseras inteligentes y las interacciones de los usuarios con la aplicación.

3. **Alimentación del Data Warehouse**: Proporciona los datos necesarios que, mediante procesos ETL, se transforman y cargan en el Data Warehouse.

4. **Persistencia de datos operativos**: Garantiza el almacenamiento seguro y eficiente de todos los datos operativos necesarios para el funcionamiento del negocio.

## Estructura del Directorio

El sistema operacional está organizado en dos componentes principales:

### 1. Transacciones de Negocio (`transacciones_postgres/`)

Este subdirectorio contiene los componentes relacionados con las operaciones comerciales del sistema, utilizando PostgreSQL (Supabase) como base de datos relacional.

**Principales componentes**:
- `creacion_db.sql`: Script para crear la estructura de tablas en PostgreSQL.
- `insercion_datos.sql`: Script para insertar datos iniciales en las tablas.

Para más detalles sobre la estructura de la base de datos que soporta las transacciones comerciales, consulte el [README específico](./transacciones_postgres/README.md).

### 2. Datos de aplicación móvil y de sensor de pulsera (`ingesta_sensor_mongo/`)

Este subdirectorio contiene los componentes relacionados con la captura y almacenamiento de datos de sensores y de la aplicación utilizando MongoDB como base de datos NoSQL.

**Principales componentes**:
- `estructura_bd.mongodb`: Define la estructura de las colecciones en MongoDB.
- `gen_data_scripts/`: Scripts para generar los datos de sensores y aplicación móvil.
- `etl_scripts/`: Scripts para procesar los datos desde el sistema de transacciones comerciales hacía MongoDB.

Para más detalles sobre la estructura de la base de datos transaccional MongoDB, consulte el [README específico](./ingesta_sensor_mongo/README.md).

## Flujo de Datos

El flujo de datos en el sistema operacional sigue estos pasos:

1. Las transacciones de negocio (suscripciones, pagos) se registran en las tablas de PostgreSQL.

2. Una vez un usuario es registrado al sistema, se inserta una versión resumida de sus datos a 
   la colección `usuarios_sensor` en MongoDB para poder identificar los datos generados por el mismo posteriormente.

3. Los usuarios generan datos a través de sus pulseras inteligentes y la interacción con la aplicación.

4. Estos datos se almacenan en tiempo real en las colecciones de MongoDB correspondientes (`datos_sensor` y `datos_aplicacion`).

