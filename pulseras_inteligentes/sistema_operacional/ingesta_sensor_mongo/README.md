# Documentación de base de datos operacional para manejo de datos de aplicación móvil y sensor de pulsera (MongoDB)

Este directorio contiene la estructura y configuración de la base de datos MongoDB utilizada para almacenar los datos operacionales referentes a actividades realizadas usando la pulsera e interacción con la aplicación móvil por parte de los usuarios.

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