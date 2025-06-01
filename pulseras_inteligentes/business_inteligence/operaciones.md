# Operaciones clave sobre el Data Warehouse centradas en el Usuario

Presentamos las **operaciones clave** realizadas sobre el Data Warehouse, enfocadas en los **usuarios**, ya que los consideramos el núcleo del sistema por su rol transversal en la generación de datos transaccionales y biométricos. Estas operaciones se ilustran con consultas y procesos relacionados con la gestión de datos, particularmente sobre las tablas de hechos y dimensiones asociadas al comportamiento del usuario, como la tabla `dim_usuario` y las tablas de hechos `hechos_actividad` y `hechos_pagos`.

## Creación

Cuando un nuevo usuario se registra y contrata un plan a través del sistema transaccional, su información se almacena de forma estructurada en dicha base. Paralelamente, la información del usuario se guarda de forma resumida en la base de datos MongoDB. Esto es para poder referenciar los registros que este genere posteriormente mediante el uso de la pulsera inteligente y la aplicación móvil.

Luego, cada cierto periodo de tiempo, se ejecuta un proceso de integración que forma parte del pipeline ETL. El objetivo es:
- **Extraer** nuevos registros de usuarios desde la base de datos transaccional.
- **Transformar** la información para ajustarla al esquema del Data Warehouse, validando consistencia y aplicando las reglas de negocio necesarias.
- **Cargar** los registros depurados en la tabla `dim_usuario` del Data Warehouse, donde el registro correspondiente queda preparado para poder relacionarlo con hechos que luego el usuario genere.

Este flujo garantiza que la dimensión de usuarios se mantenga actualizada y alineada con las fuentes operativas, permitiendo obtener indicadores como la evolución del número de usuarios activos, la distribución por tipo de plan, o algún otro tipo de segmentación.

## Eliminación
En este sistema no se eliminan registros de forma definitiva con fines históricos y analíticos, salvo excepciones. En lugar de eliminar físicamente los registros de usuarios, se emplea una política de borrado lógico mediante el análisis de suscripciones activas por parte de los usuarios, que indica si el usuario sigue activo, se ha dado de baja o presenta un estado inactivo. Esta estrategia permite conservar el historial completo de interacciones y mantener la integridad de los análisis longitudinales, como el cálculo de tasas de retención o el análisis del ciclo de vida del cliente.

Dentro de las excepciones, contamos el borrado por motivos de cumplimiento de normativas vigentes y cumplimiento de lo acordado entre cada usuario y la empresa por medio de los Términos y Condiciones del uso de la pulsera (a delimitar por el equipo Legal de la empresa). Las normativas que podemos tener en cuenta son, por ejemplo, la Ley de Protección de Datos Personales en Argentina (Ley 25.326), GDPR en Europa y el CCPA en California, Estados Unidos. Además, por motivos de límite en las suscripciones activas a las bases de datos, se puede proceder a la eliminación de información, pero todo esto está fuera del alcance del MVP. Sugerimos implementar a futuro los métodos que guardaran información anonimizada y agregada del uso de las pulseras y la aplicación.

## Inserción

### Contexto y flujo ETL
Una vez que un usuario ha sido registrado en la dimensión `dim_usuario` del Data Warehouse y ha comenzado a interactuar con la aplicación y la pulsera inteligente, se genera un flujo constante de datos biométricos (como actividad física, sueño o niveles de glucosa) y de uso de la aplicación móvil. Esta información se simula y almacena inicialmente en la base de datos MongoDB, en formato semiestructurado.

Con frecuencia periódica, se ejecuta un proceso ETL que:
- **Extrae** los registros recientes desde MongoDB, filtrando por eventos biométricos y de interacción relevantes.
- **Transforma** los datos, mapeando los atributos de actividad y de tiempo a los identificadores definidos en el modelo dimensional (por ejemplo, `id_usuario`, `id_actividad` e `id_fecha`), y normalizando los formatos según el esquema del Data Warehouse.
- **Carga** la información procesada en las tablas de hechos: `hechos_pagos` y `hechos_actividad`.

Cada registro de hechos mantiene integridad referencial con las dimensiones correspondientes, especialmente `dim_usuario`, permitiendo realizar análisis cruzados entre comportamientos y atributos del usuario.

### Validación de integridad
El proceso ETL incluye controles que aseguran que los registros solo se inserten si el usuario asociado ya se encuentra registrado en la dimensión correspondiente. Esto previene inconsistencias y garantiza la confiabilidad de los datos analíticos generados a partir del Data Warehouse.

## Actualización

### Contexto y flujo ETL
En entornos reales, es común que los datos personales de los usuarios sufran correcciones posteriores a su carga inicial en el Data Warehouse. Por ejemplo, puede corregirse el nombre, género o fecha de nacimiento de un usuario en el sistema operacional.

Periódicamente, el proceso ETL:
- **Extrae** los registros recientemente modificados desde el sistema operacional, utilizando mecanismos de detección de cambios.
- **Transforma** los datos normalizando valores y validando que cumplan con el esquema de `dim_usuario`.
- **Carga** los cambios mediante operaciones de actualización sobre la dimensión `dim_usuario`, manteniendo la clave `id_usuario` como identificador constante.

### Impacto en el modelo
Estas actualizaciones permiten mantener actualizada la información descriptiva de los usuarios sin afectar los datos históricos almacenados en las tablas de hechos. De este modo, los análisis posteriores reflejan con precisión los atributos vigentes de cada usuario.

### Validación de integridad
El proceso ETL incluye validaciones para asegurar que los cambios aplicados correspondan únicamente a usuarios existentes. Esto evita la creación no intencional de registros huérfanos o duplicados, garantizando la coherencia del modelo dimensional.

## Búsquedas de una clave y de dos claves
Las siguientes consultas permiten acceder a información específica de los usuarios, y también pueden ser utilizadas en análisis cruzados con tablas de hechos. A continuación, dejamos dos ejemplos:

### a) Búsqueda por una clave (por ID de usuario)
```sql
SELECT * FROM dim_usuario
WHERE id_usuario = 19;
```
**Resultado:**
| id_usuario | nombre              | genero   | fecha_registro       | fecha_nacimiento |
|------------|---------------------|----------|---------------------|------------------|
| 19         | Milagros Dominguez  | Femenino | 2025-08-15 00:00:00 | 1982-07-19       |

Esta consulta permite obtener información específica del usuario presente en la tabla `dim_usuario`. Resulta útil para poder analizar datos demográficos, patrones en fechas de registro a la aplicación móvil, etc.

### b) Búsqueda por dos claves (por ID de usuario y actividad)
```sql
SELECT 
    u.nombre AS nombre_usuario,
    dim_a.descripcion AS nombre_actividad,
    a.hora_registro
FROM
    dim_usuario u
JOIN
    hechos_actividad a ON u.id_usuario = a.id_usuario
JOIN
    dim_activdad dim_a ON a.id_actividad = dim_a.id_actividad
WHERE
    u.id_usuario = 19 AND
    a.id_actividad = 5
LIMIT 5;
```
**Resultado:**
| nombre_usuario      | nombre_actividad | hora_registro |
|--------------------|------------------|--------------|
| Milagros Dominguez | caminar          | 09:54:18     |
| Milagros Dominguez | caminar          | 15:12:19     |
| Milagros Dominguez | caminar          | 17:47:21     |
| Milagros Dominguez | caminar          | 08:26:21     |
| Milagros Dominguez | caminar          | 15:26:22     |

Esta consulta permite obtener el nombre del usuario junto con registros de una actividad específica, útil para conocer detalles sobre su comportamiento e interacción con la aplicación y pulsera inteligente.