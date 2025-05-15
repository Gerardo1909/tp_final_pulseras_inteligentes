# Documentación de base de datos orientada a grafos para el sistema de recomendaciones (Neo4j)

Este directorio contiene los scripts ETL necesarios para poblar y mantener actualizadas relaciones en la base de datos orientada a grafos Neo4j que alimenta el sistema de recomendaciones para la aplicación de pulseras inteligentes.

## Estructura del Grafo

La base de datos Neo4j almacena tres tipos principales de nodos y varias relaciones entre ellos, formando un grafo que permite el análisis de patrones y la generación de recomendaciones personalizadas.

### Nodos

#### 1. Nodo: `Usuario`

Representa a los usuarios registrados en la aplicación.

**Propiedades**:
- `id_usuario`: Identificador único del usuario
- `nombre`: Nombre del usuario
- `fecha_registro`: Fecha en la que el usuario se registró en el sistema

#### 2. Nodo: `Actividad`

Representa las diferentes actividades físicas que pueden realizar los usuarios.

**Propiedades**:
- `id_actividad`: Identificador único de la actividad
- `nombre`: Nombre de la actividad (ej. caminar, correr, ciclismo, etc.)
- `descripcion`: Descripción detallada de la actividad
- `tipo_dato`: Tipo de dato principal que se mide (ej. duracion_minutos, distancia_km, etc.)
- `unidad`: Unidad de medida (ej. minutos, km, sesiones, etc.)
- `frecuencia_minima`: Frecuencia mínima recomendada (veces por semana)

#### 3. Nodo: `Objetivo`

Representa los objetivos de salud que pueden alcanzar los usuarios.

**Propiedades**:
- `id_objetivo`: Identificador único del objetivo
- `nombre`: Nombre del objetivo (ej. Caminatas diarias, Sueño reparador, etc.)
- `descripcion`: Descripción detallada del objetivo
- `tipo_dato`: Tipo de dato que se evalúa (ej. cantidad_pasos, duracion_total_min, etc.)
- `umbral_minimo`: Valor mínimo para cumplir el objetivo
- `umbral_maximo`: Valor máximo para cumplir el objetivo (opcional)
- `unidad`: Unidad de medida (ej. pasos, minutos, mg/dL, etc.)
- `dias_consecutivos_minimos`: Cantidad mínima de días consecutivos que se debe cumplir

### Relaciones

#### 1. Relación: `REALIZA`

Conecta un `Usuario` con una `Actividad` que está realizando actualmente.

**Propiedades**:
- `desde`: Fecha desde la cual el usuario ha comenzado a realizar la actividad

**Condiciones para creación**:
- Se crea cuando el usuario registra al menos una instancia de la actividad en los últimos 30 días
- Se elimina cuando el usuario no registra ninguna instancia de la actividad en los últimos 30 días

#### 2. Relación: `TIENE_OBJETIVO`

Conecta un `Usuario` con un `Objetivo` que está intentando alcanzar.

**Propiedades**:
- `desde`: Fecha desde la cual el usuario está trabajando en el objetivo

**Condiciones para creación**:
- Se crea cuando el usuario comienza a mostrar registros relevantes para el objetivo pero aún no lo cumple completamente
- Se elimina cuando el usuario deja de mostrar datos relacionados con el objetivo o cuando cumple el objetivo

#### 3. Relación: `CUMPLIO`

Conecta un `Usuario` con un `Objetivo` que ha logrado cumplir.

**Propiedades**:
- `desde`: Fecha desde la cual el usuario cumplió el objetivo

**Condiciones para creación**:
- Se crea cuando el usuario cumple con los criterios del objetivo durante el período mínimo de días consecutivos
- Se elimina si el usuario deja de cumplir con los criterios del objetivo

#### 4. Relación: `CONTRIBUYE_A`

Conecta una `Actividad` con un `Objetivo` al que contribuye.

**Condiciones**:
- Es una relación estática configurada manualmente que indica qué actividades ayudan a alcanzar qué objetivos
- No tiene propiedades temporales ya que es una relación conceptual



