# Documentación para el Data Warehouse (PostgreSQL)

Esta documentación detalla la estructura del Data Warehouse diseñado para el sistema de Pulseras Inteligentes. El Data Warehouse es un componente fundamental para el análisis de datos y la mejora constante de la aplicación. A continuación mostramos una imagen de su diagrama entidad-relación: 

![DER Data Warehouse](/img/DER_datawarehouse_pulseras_inteligentes.png)

Para estructurar esta documentación, hemos clasificado las tablas en grupos según su rol: **tablas de dimensiones, tablas de hechos y tablas de auditoría**.

## Dominio de los Datos para las tablas de dimensiones

Las **tablas de dimensiones** contienen los datos descriptivos que proporcionan contexto a las medidas almacenadas en las tablas de hechos. Estas tablas forman la estructura fundamental del Data Warehouse y permiten realizar análisis multidimensionales.

1. **Tabla: `dim_plan`**
   - **Dominio:** Esta tabla almacena la información de los planes disponibles para los usuarios. Entre los campos que posee se encuentran:
     - `id_plan` (**PK, SERIAL**): Identificador único para cada plan.
     - `nombre_plan` (**VARCHAR(100)**): Nombre que identifica al plan.
     - `descripcion` (**TEXT**): Descripción detallada del plan y sus beneficios.
     - `duracion_dias` (**INTEGER**): Duración del plan expresada en días.

2. **Tabla: `dim_metodo_pago`**
   - **Dominio:** Almacena los diferentes métodos de pago que pueden utilizar los usuarios. Entre los campos que posee se encuentran:
     - `id_metodo_pago` (**PK, SERIAL**): Identificador único para cada método de pago.
     - `descripcion` (**VARCHAR(100)**): Descripción del método de pago (tarjeta de crédito, transferencia, etc.).

3. **Tabla: `dim_estado_pago`**
   - **Dominio:** Contiene los posibles estados en los que puede encontrarse un pago. Entre los campos que posee se encuentran:
     - `id_estado` (**PK, SERIAL**): Identificador único para cada estado de pago.
     - `descripcion` (**VARCHAR(50)**): Descripción del estado del pago (pendiente, completado, rechazado, etc.).

4. **Tabla: `dim_actividad`**
   - **Dominio:** Registra las diferentes actividades que los usuarios pueden realizar con la pulsera o la aplicación. Entre los campos que posee se encuentran:
     - `id_actividad` (**PK, SERIAL**): Identificador único para cada tipo de actividad.
     - `descripcion` (**VARCHAR(100)**): Descripción de la actividad (caminar, correr, monitoreo de sueño, etc.).

5. **Tabla: `dim_usuario`**
   - **Dominio:** Almacena la información demográfica y de registro de los usuarios. Entre los campos que posee se encuentran:
     - `id_usuario` (**PK, INTEGER**): Identificador único para cada usuario.
     - `nombre` (**VARCHAR(50)**): Nombre del usuario.
     - `genero` (**VARCHAR(50)**): Género del usuario.
     - `fecha_registro` (**TIMESTAMP**): Fecha y hora en que el usuario se registró en el sistema.
     - `fecha_nacimiento` (**DATE**): Fecha de nacimiento del usuario.

6. **Tabla: `dim_fecha`**
   - **Dominio:** Contiene una representación dimensional del tiempo que permite realizar análisis temporales. Entre los campos que posee se encuentran:
     - `id_fecha` (**PK, SERIAL**): Identificador único para cada fecha.
     - `fecha` (**TIMESTAMP**): Fecha y hora completa.
     - `dia` (**INTEGER**): Día del mes.
     - `mes` (**INTEGER**): Mes del año.
     - `trimestre` (**INTEGER**): Trimestre del año.
     - `anio` (**INTEGER**): Año.

## Dominio de los Datos para las tablas de hechos

Las **tablas de hechos** almacenan las mediciones numéricas del negocio y las claves foráneas a las tablas de dimensiones. Estas tablas son el centro del esquema en estrella y contienen los datos cuantitativos que serán analizados.

1. **Tabla: `hechos_pagos`**
   - **Dominio:** Esta tabla registra todas las transacciones de pago realizadas por los usuarios al adquirir planes. Entre los campos que posee se encuentran:
     - `id_hecho` (**PK, SERIAL**): Identificador único para cada registro de pago.
     - `id_usuario` (**FK, INTEGER**): Clave foránea que conecta el pago con un usuario específico.
     - `id_plan` (**FK, INTEGER**): Clave foránea que identifica el plan adquirido.
     - `id_metodo_pago` (**FK, INTEGER**): Clave foránea que indica el método de pago utilizado.
     - `id_estado_pago` (**FK, INTEGER**): Clave foránea que refleja el estado del pago.
     - `id_fecha` (**FK, INTEGER**): Clave foránea que conecta con la dimensión de tiempo.
     - `hora_registro` (**TIME**): Hora exacta del registro del pago.
     - `monto_pago` (**DECIMAL(10,2)**): Monto del pago realizado.

   Esta tabla permite realizar análisis sobre patrones de compra, preferencias de planes y comportamiento de pago de los usuarios.

2. **Tabla: `hechos_actividad`**
   - **Dominio:** Registra las actividades realizadas por los usuarios con sus pulseras inteligentes a lo largo del tiempo. Entre los campos que posee se encuentran:
     - `id_hecho` (**PK, SERIAL**): Identificador único para cada registro de actividad.
     - `id_usuario` (**FK, INTEGER**): Clave foránea que conecta la actividad con un usuario específico.
     - `id_actividad` (**FK, INTEGER**): Clave foránea que identifica el tipo de actividad realizada.
     - `id_fecha` (**FK, INTEGER**): Clave foránea que conecta con la dimensión de tiempo.
     - `hora_registro` (**TIME**): Hora exacta del registro de la actividad.

   Esta tabla es fundamental para el análisis de patrones de uso, preferencias de actividades y generación de recomendaciones personalizadas basadas en el comportamiento de los usuarios.

## Dominio de los datos para la tabla de auditoría:

La **tabla de auditoría** del Data Warehouse mantiene un registro histórico completo de todas las operaciones críticas que se realizan sobre las tablas de hechos y dimensiones. Este sistema de auditoría es fundamental para garantizar la **integridad**, **trazabilidad** y **monitoreo** de las operaciones del Data Warehouse, permitiendo realizar seguimientos detallados de los procesos ETL y análisis de rendimiento.

1. **Tabla: `log_eventos`**
   - **Propósito:** Registra automáticamente todos los eventos de modificación (INSERT, UPDATE) que ocurren en las tablas críticas del Data Warehouse, proporcionando un historial completo de operaciones para auditoría, monitoreo y optimización de procesos ETL.
   - **Campos principales:**
     - `id_log` (**PK, SERIAL**): Identificador único para cada evento registrado.
     - `tabla_afectada` (**VARCHAR(100)**): Nombre de la tabla donde ocurrió la operación.
     - `operacion` (**VARCHAR(10)**): Tipo de operación realizada (INSERT, UPDATE).
     - `fecha_operacion` (**TIMESTAMP**): Fecha y hora exacta cuando se ejecutó la operación.
     - `clave_primaria` (**TEXT**): Valor de la clave primaria del registro afectado.
     - `datos_anteriores` (**JSONB**): Estado anterior del registro (para operaciones UPDATE).
     - `datos_nuevos` (**JSONB**): Estado posterior del registro (para operaciones INSERT y UPDATE).

## Sistema de triggers y funciones para auditoría del Data Warehouse:

Para automatizar el proceso de auditoría en el Data Warehouse, el sistema incluye un conjunto completo de **funciones PL/pgSQL y triggers** definidos en el archivo `funciones_eventos.sql`. Estas funciones se ejecutan automáticamente durante los procesos ETL para monitorear todas las operaciones críticas.

### Funcionalidades implementadas:

1. **Función: `registrar_insert_hechos_pagos()`**
   - **Propósito:** Captura automáticamente cada inserción en la tabla `hechos_pagos` durante los procesos ETL.
   - **Tipo de trigger:** AFTER INSERT - Se ejecuta después de que la inserción se haya completado exitosamente.
   - **Información capturada:**
     - Datos completos del nuevo registro de pago insertado
     - Timestamp preciso de la operación ETL
     - ID del hecho de pago para trazabilidad

2. **Función: `registrar_insert_hechos_actividad()`**
   - **Propósito:** Registra automáticamente cada inserción en la tabla `hechos_actividad` durante la carga ETL.
   - **Tipo de trigger:** AFTER INSERT - Garantiza que no interfiera con el proceso de carga.
   - **Información capturada:**
     - Datos completos del nuevo registro de actividad
     - Metadata de la operación ETL
     - ID del hecho de actividad para seguimiento

3. **Función: `registrar_insert_dim_usuario()`**
   - **Propósito:** Monitorea las inserciones en la dimensión `dim_usuario` durante la carga inicial de usuarios.
   - **Tipo de trigger:** AFTER INSERT - Se ejecuta tras completar la inserción dimensional.
   - **Información capturada:**
     - Datos demográficos y de registro del nuevo usuario
     - Timestamp de incorporación al Data Warehouse
     - ID del usuario para correlación con sistema operacional

4. **Función: `registrar_update_dim_usuario()`**
   - **Propósito:** Rastrea las actualizaciones en la dimensión `dim_usuario` durante procesos de sincronización.
   - **Tipo de trigger:** AFTER UPDATE - Se ejecuta después de cada actualización dimensional.
   - **Información capturada:**
     - Estado anterior y posterior del registro de usuario
     - Timestamp de la actualización ETL
     - ID del usuario modificado para trazabilidad

### Triggers implementados:

- **`trg_insert_hechos_pagos`:** Se activa en cada INSERT sobre `hechos_pagos`
- **`trg_insert_hechos_actividad`:** Se activa en cada INSERT sobre `hechos_actividad`
- **`trg_insert_dim_usuario`:** Se activa en cada INSERT sobre `dim_usuario`
- **`trg_update_dim_usuario`:** Se activa en cada UPDATE sobre `dim_usuario`

### Beneficios del sistema de auditoría del Data Warehouse:

- **Monitoreo de procesos ETL:** Permite rastrear exactamente cuándo y cómo se ejecutaron los procesos de carga y actualización de datos.
- **Detección de anomalías:** Facilita la identificación de problemas en los procesos ETL, como cargas duplicadas o actualizaciones incorrectas.
- **Análisis de rendimiento:** Los logs permiten identificar cuellos de botella y optimizar los tiempos de ejecución de los procesos ETL.
- **Integridad referencial:** Garantiza que todos los cambios en el Data Warehouse estén documentados y sean trazables.
- **Cumplimiento y auditoría:** Proporciona evidencia completa para auditorías de calidad de datos y cumplimiento normativo.
- **Recuperación de datos:** Permite identificar y corregir problemas específicos usando los datos anteriores registrados.

### Casos de uso en procesos ETL:

Los scripts ETL del Data Warehouse se benefician de este sistema de auditoría para:
- **Validación de cargas:** Confirmar que los procesos ETL se ejecutaron correctamente
- **Análisis de volúmenes:** Monitorear la cantidad de registros procesados en cada ejecución
- **Detección de cambios:** Identificar patrones en las actualizaciones de dimensiones
- **Optimización de rendimiento:** Analizar tiempos de ejecución y volúmenes de datos procesados
- **Troubleshooting:** Diagnosticar problemas específicos en los procesos de sincronización

### Integración con el sistema operacional:

El sistema de auditoría del Data Warehouse se complementa con el sistema de auditoría del sistema operacional para proporcionar **trazabilidad end-to-end**:
- Los triggers del sistema operacional capturan cambios en la fuente de datos
- Los triggers del Data Warehouse registran cuando esos cambios son sincronizados
- Esta combinación permite rastrear el flujo completo de datos desde la transacción original hasta el análisis final
