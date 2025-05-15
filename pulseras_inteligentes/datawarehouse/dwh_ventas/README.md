# Documentación de base de datos dimensional para análisis de ventas (PostgreSQL)

Esta documentación detalla la estructura de la base de datos dimensional diseñada para realizar análisis sobre las ventas registradas desde el sistema
operacional.

Para estructurar esta documentación, hemos clasificado las tablas en grupos según su rol: **tablas de dimensiones y tabla de hechos**.

## Dominio de los Datos para las tablas de dimensiones

Las **tablas de dimensiones** contienen los datos descriptivos que proporcionan contexto a las medidas almacenadas en la tabla de hechos. Estas tablas forman la estructura fundamental de la base de datos y permiten realizar análisis multidimensionales.

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

4. **Tabla: `dim_usuario`**
   - **Dominio:** Almacena la información demográfica y de registro de los usuarios. Entre los campos que posee se encuentran:
     - `id_usuario` (**PK, INTEGER**): Identificador único para cada usuario.
     - `nombre` (**VARCHAR(50)**): Nombre del usuario.
     - `genero` (**VARCHAR(50)**): Género del usuario.
     - `fecha_registro` (**TIMESTAMP**): Fecha y hora en que el usuario se registró en el sistema.
     - `fecha_nacimiento` (**DATE**): Fecha de nacimiento del usuario.

5. **Tabla: `dim_fecha`**
   - **Dominio:** Contiene una representación dimensional del tiempo que permite realizar análisis temporales. Entre los campos que posee se encuentran:
     - `id_fecha` (**PK, SERIAL**): Identificador único para cada fecha.
     - `fecha` (**TIMESTAMP**): Fecha y hora completa.
     - `dia` (**INTEGER**): Día del mes.
     - `mes` (**INTEGER**): Mes del año.
     - `trimestre` (**INTEGER**): Trimestre del año.
     - `anio` (**INTEGER**): Año.

## Dominio de los Datos para las tablas de hechos

La **tabla de hechos** almacena las mediciones numéricas del negocio relacionadas a ventas y las claves foráneas a las tablas de dimensiones. Esta tabla es el centro del esquema en estrella y contiene los datos cuantitativos que permiten realizar análisis sobre patrones de compra, preferencias de planes y comportamiento de pago de los usuarios.

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