# Documentación para el sistema de base de datos transaccional (SQL)

Esta documentación detalla la estructura de la base de datos transaccional que soporta operaciones de negocio correspondientes a manejo
de usuarios, suscripciones, pagos, etc. 

Para estructurar esta documentación, hemos clasificado las tablas en grupos según el rol que desempeñan dentro de la base de datos. Estos grupos se dividen en: **entidades principales y entidades categóricas**.

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