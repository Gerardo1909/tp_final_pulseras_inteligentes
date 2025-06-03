# Documentación de base de datos operacional para transacciones comerciales (PostgreSQL)

Esta documentación detalla la estructura de la base de datos operacional que soporta operaciones de negocio correspondientes a manejo
de usuarios, suscripciones, pagos, etc. A continuación mostramos una imagen de su diagrama entidad-relación: 

![DER sistema operacional](/img/DER_sistema_operacional_pulseras_inteligentes.png)

Para estructurar esta documentación, hemos clasificado las tablas en grupos según el rol que desempeñan dentro de la base de datos. Estos grupos se dividen en: **entidades principales, entidades categóricas y auditoría**.

## Dominio de los Datos para las entidades principales

Las **entidades principales** representan los objetos centrales del sistema y son aquellas tablas que contienen la **información más relevante y completa** sobre los elementos clave del modelo. Estas tablas forman la base sobre la cual se estructuran las relaciones en la base de datos.

1. **Tabla: `usuarios`**
   - **Dominio:** Esta tabla almacena la información esencial de cada usuario registrado en el sistema de Pulseras Inteligentes. Entre los campos que posee se encuentran:
     - `id_usuario` (**PK, SERIAL**): Identificador único para cada usuario.
     - `nombre` (**VARCHAR(50)**): Nombre completo del usuario.
     - `email` (**VARCHAR(255)**): Correo electrónico del usuario, utilizado para comunicaciones y autenticación.
     - `fecha_nacimiento` (**DATE**): Fecha de nacimiento del usuario.
     - `id_genero` (**FK, INTEGER**): Clave foránea que referencia a la tabla de géneros.
     - `fecha_registro` (**TIMESTAMP**): Fecha y hora en que el usuario se registró en el sistema.

2. **Tabla: `pagos`**
   - **Dominio:** Esta tabla registra todas las transacciones de pago realizadas por los usuarios. Entre los campos que posee se encuentran:
     - `id_pago` (**PK, SERIAL**): Identificador único para cada transacción de pago.
     - `id_metodo_pago` (**FK, INTEGER**): Clave foránea que conecta el pago con el método utilizado.
     - `monto` (**DECIMAL(10,2)**): Importe del pago realizado.
     - `fecha_transaccion` (**TIMESTAMP**): Fecha y hora en que se realizó la transacción.
     - `id_estado_pago` (**FK, INTEGER**): Clave foránea que indica el estado actual del pago.
     - `id_usuario` (**FK, INTEGER**): Clave foránea que conecta el pago con el usuario que lo realizó.

3. **Tabla: `suscripcion`**
   - **Dominio:** Almacena la información de las suscripciones de los usuarios a los diferentes planes ofrecidos. Entre los campos que posee se encuentran:
     - `id_suscripcion` (**PK, SERIAL**): Identificador único para cada suscripción.
     - `id_usuario` (**FK, INTEGER**): Clave foránea que conecta la suscripción con un usuario específico.
     - `id_plan` (**FK, INTEGER**): Clave foránea que identifica el plan al que el usuario está suscrito.
     - `fecha_inicio` (**TIMESTAMP**): Fecha y hora en que inicia la suscripción.
     - `fecha_fin` (**TIMESTAMP**): Fecha y hora en que finaliza la suscripción.
     - `id_estado` (**FK, INTEGER**): Clave foránea que refleja el estado actual de la suscripción.
     - `id_pago` (**FK, INTEGER**): Clave foránea que conecta la suscripción con el pago correspondiente.

4. **Tabla: `planes`**
   - **Dominio:** Contiene los detalles de los planes de suscripción disponibles para los usuarios. Entre los campos que posee se encuentran:
     - `id_plan` (**PK, SERIAL**): Identificador único para cada plan.
     - `nombre_plan` (**VARCHAR(100)**): Nombre que identifica al plan.
     - `descripcion` (**TEXT**): Descripción detallada del plan y sus beneficios.
     - `duracion_dias` (**INTEGER**): Duración del plan expresada en días.

## Dominio de los datos para las entidades categóricas:

Las **entidades categóricas** contienen información que organiza los datos de la base de datos en diferentes categorías. Estas tablas se crean con el objetivo de normalizar la base de datos, alcanzando la **Tercera Forma Normal (3FN)**. Esto permite que cada categoría esté almacenada de manera independiente y no dependa de otras entidades que podrían ser eliminadas, evitando así la pérdida de información relacionada.

1. **Tabla: `genero`**
   - **Propósito:** Almacena los diferentes géneros con los que pueden identificarse los usuarios del sistema.
   - **Campo clave:** `id_genero` (**PK, SERIAL**)
   - **Campo categórico:** `genero` (**VARCHAR(50)**)
   - **Valores:** 
     - *Masculino*: Para usuarios que se identifican como hombres.
     - *Femenino*: Para usuarios que se identifican como mujeres.
     - *Prefiero no decirlo*: Para usuarios que prefieren no especificar su género.

2. **Tabla: `metodo_pago`**
   - **Propósito:** Define los diferentes métodos de pago que los usuarios pueden utilizar para adquirir suscripciones.
   - **Campo clave:** `id_metodo` (**PK, SERIAL**)
   - **Campo categórico:** `descripcion` (**VARCHAR(100)**)
   - **Valores:** 
     - *Tarjeta de crédito*: Pagos realizados con tarjeta de crédito.
     - *Tarjeta de débito*: Pagos realizados con tarjeta de débito.
     - *Transferencia bancaria*: Pagos realizados mediante transferencia desde una cuenta bancaria.
     - *Billetera digital*: Pagos realizados a través de servicios como PayPal, Mercado Pago, etc.

3. **Tabla: `estado_pago`**
   - **Propósito:** Indica los posibles estados en los que puede encontrarse un pago.
   - **Campo clave:** `id_estado` (**PK, SERIAL**)
   - **Campo categórico:** `descripcion` (**VARCHAR(50)**)
   - **Valores:** 
     - *Pendiente*: El pago está en proceso pero aún no se ha completado.
     - *Completado*: El pago se ha procesado correctamente.
     - *Rechazado*: El pago ha sido rechazado por el sistema o la entidad bancaria.
     - *Reembolsado*: El pago ha sido devuelto al usuario.

4. **Tabla: `estado_suscripcion`**
   - **Propósito:** Describe los diferentes estados en los que puede encontrarse una suscripción.
   - **Campo clave:** `id_estado` (**PK, SERIAL**)
   - **Campo categórico:** `descripcion` (**VARCHAR(50)**)
   - **Valores:** 
     - *Activa*: La suscripción está en vigor y el usuario puede acceder a todos los beneficios.
     - *Cancelada*: La suscripción ha finalizado o ha sido cancelada.


## Dominio de los datos para la tabla de auditoría:

La **tabla de auditoría** tiene como objetivo mantener un registro histórico completo de todas las operaciones críticas que se realizan sobre las entidades principales del sistema. Esta funcionalidad es esencial para garantizar la **trazabilidad**, **integridad** y **transparencia** de las operaciones del negocio, permitiendo realizar seguimientos detallados y análisis retrospectivos.

1. **Tabla: `log_eventos`**
   - **Propósito:** Registra automáticamente todos los eventos de modificación (INSERT, UPDATE, DELETE) que ocurren en las tablas principales del sistema, proporcionando un historial completo de cambios para auditoría y análisis.
   - **Campos principales:**
     - `id_log` (**PK, SERIAL**): Identificador único para cada evento registrado.
     - `tabla_afectada` (**TEXT**): Nombre de la tabla donde ocurrió la operación.
     - `operacion` (**TEXT**): Tipo de operación realizada ('INSERT', 'UPDATE', 'DELETE').
     - `fecha_operacion` (**TIMESTAMP**): Fecha y hora exacta en que se ejecutó la operación.
     - `clave_primaria` (**TEXT**): Valor de la clave primaria del registro afectado.
     - `datos_anteriores` (**JSONB**): Estado previo del registro (para operaciones UPDATE y DELETE).
     - `datos_nuevos` (**JSONB**): Estado posterior del registro (para operaciones INSERT y UPDATE).

## Sistema de triggers y funciones para auditoría:

Para automatizar el proceso de auditoría, el sistema incluye un conjunto de **funciones PL/pgSQL y triggers** definidos en el archivo `funciones_eventos.sql`. Estas funciones se ejecutan automáticamente cada vez que ocurre una operación relevante en las tablas monitoreadas.

### Funcionalidades implementadas:

1. **Función: `registrar_update_usuarios()`**
   - **Propósito:** Captura automáticamente cualquier actualización realizada en la tabla `usuarios` y registra el evento en `log_eventos`.
   - **Tipo de trigger:** AFTER UPDATE - Se ejecuta después de que la actualización se haya completado exitosamente.
   - **Información capturada:**
     - Estado anterior del registro (`OLD` record)
     - Estado actualizado del registro (`NEW` record)
     - Timestamp exacto de la operación
     - ID del usuario afectado

2. **Trigger: `trg_update_usuarios`**
   - **Vinculación:** Se activa automáticamente en cada operación UPDATE sobre la tabla `usuarios`.
   - **Granularidad:** FOR EACH ROW - Registra cada fila individual que sea modificada.
   - **Funcionamiento:** Invoca la función `registrar_update_usuarios()` para cada actualización detectada.

### Beneficios del sistema de auditoría:

- **Trazabilidad completa:** Permite rastrear exactamente qué cambios se realizaron, cuándo y qué datos fueron modificados.
- **Integridad de datos:** Facilita la detección de modificaciones no autorizadas o erróneas.
- **Análisis de patrones:** Los logs permiten identificar tendencias y patrones en las actualizaciones de usuarios.
- **Soporte para ETL:** Los procesos de extracción, transformación y carga del Data Warehouse utilizan estos logs para identificar registros que requieren sincronización.
- **Cumplimiento normativo:** Proporciona evidencia auditable para cumplir con regulaciones de protección de datos y auditorías internas/externas.

### Casos de uso en el sistema ETL:

El script `etl_actualizar_dim_usuario.py` del Data Warehouse utiliza directamente esta tabla de auditoría para:
- Identificar qué usuarios han sido modificados desde la última sincronización
- Extraer únicamente los registros que requieren actualización en la dimensión de usuarios
- Optimizar el proceso de sincronización evitando procesamientos innecesarios de datos no modificados


