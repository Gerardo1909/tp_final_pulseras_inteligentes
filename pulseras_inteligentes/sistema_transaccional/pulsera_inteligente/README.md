# Documentación para el sistema de base de datos transaccional (MongoDB)

Este directorio contiene la estructura y configuración de la base de datos MongoDB utilizada para almacenar los datos transaccionales referentes a actividades e interacción de usuarios con la aplicación de pulseras inteligentes.

## Estructura de la Base de Datos

La base de datos `pulseras_inteligentes` se compone de las siguientes colecciones:

### 1. Colección `usuarios_sensor`

Esta colección almacena la información básica de los usuarios que utilizan el sensor de la pulsera inteligente.

**Esquema**:
```json
{
  "id_usuario": Number,  // ID único del usuario
  "nombre": String,      // Nombre del usuario
  "fecha_registro": Date // Fecha de registro del usuario
}
```

### 2. Colección `datos_sensor`

Esta colección almacena todas las lecturas y registros generados por los sensores de las pulseras inteligentes.

**Esquema**:
```json
{
  "id_usuario": Number,  // ID único del usuario
  "timestamp": Date,     // Fecha y hora de la lectura del sensor
  "tipo_registro": String, // Tipo de registro del sensor
  "datos": Object        // Objeto que contiene los datos específicos del registro
}
```

El campo `datos` puede contener diferentes propiedades según el `tipo_registro`. Algunos ejemplos comunes incluyen:

- Para registros de actividad física:
  ```json
  {
    "tipo_actividad": "caminar",
    "duracion_minutos": 30,
    "pasos": 3500,
    "distancia_km": 2.5
  }
  ```

- Para registros de sueño:
  ```json
  {
    "duracion_total_min": 480,
    "fase_rem_min": 120,
    "fase_profunda_min": 180,
    "fase_ligera_min": 180
  }
  ```

- Para registros de frecuencia cardíaca:
  ```json
  {
    "ritmo_cardiaco": 72,
    "variabilidad_cardiaca": 45
  }
  ```

### 3. Colección `datos_aplicacion`

Esta colección almacena los eventos y acciones de los usuarios dentro de la aplicación móvil o web que complementa a la pulsera inteligente.

**Esquema**:
```json
{
  "id_usuario": Number,       // ID único del usuario
  "timestamp": Date,          // Fecha y hora del evento
  "tipo_evento": String,      // Tipo de evento registrado en la aplicación
  "nombre_pantalla": String,  // Nombre de la pantalla (opcional)
  "nombre_boton": String,     // Nombre del botón (opcional)
  "nombre_formulario": String, // Nombre del formulario (opcional)
  "nombre_funcionalidad": String, // Nombre de la funcionalidad usada
  "detalles": Object,         // Datos adicionales específicos del evento
  "id_sesion": String,        // Identificador de la sesión del usuario
  "version_aplicacion": String, // Versión de la aplicación
  "version_os": String        // Versión del sistema operativo del dispositivo
}
```

El campo `tipo_evento` puede tener los siguientes valores:
- `tiempo_pantalla`: Registro de tiempo pasado en una pantalla
- `click_boton`: Registro de clicks/toques en botones
- `envio_formulario`: Registro de envío de formularios
- `uso_funcionalidad`: Registro de uso de funcionalidades específicas

## Uso de la Base de Datos

Esta base de datos transaccional se utiliza para registrar en tiempo real todos los datos generados por las pulseras inteligentes y la interacción de los usuarios con la aplicación. Estos datos son posteriormente procesados mediante scripts ETL para alimentar el sistema de recomendaciones basado en Neo4j y al Datawarehouse.

## Consultas Comunes

```javascript
// Obtener todos los usuarios registrados
db.usuarios_sensor.find()

// Obtener registros de actividad para un usuario específico
db.datos_sensor.find({
  id_usuario: 1,
  tipo_registro: "actividad"
})

// Obtener interacciones con la aplicación en un periodo específico
db.datos_aplicacion.find({
  timestamp: {
    $gte: ISODate("2023-01-01T00:00:00Z"),
    $lt: ISODate("2023-01-31T23:59:59Z")
  }
})
``` 