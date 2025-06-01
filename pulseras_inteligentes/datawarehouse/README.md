# Documentación para el Data Warehouse (PostgreSQL)

Esta documentación detalla la estructura del Data Warehouse diseñado para el sistema de Pulseras Inteligentes. El Data Warehouse es un componente fundamental para el análisis de datos y la mejora constante de la aplicación. A continuación mostramos una imagen de su diagrama entidad-relación: 

![DER Data Warehouse](/img/DER_datawarehouse_pulseras_inteligentes.png)

Para estructurar esta documentación, hemos clasificado las tablas en grupos según su rol: **tablas de dimensiones y tablas de hechos**.

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
