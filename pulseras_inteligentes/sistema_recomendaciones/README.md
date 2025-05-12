# Documentación de base de datos para el sistema de recomendaciones (Neo4j)

Este directorio contiene los scripts ETL necesarios para poblar y mantener actualizada la base de datos de grafos Neo4j que alimenta el sistema de recomendaciones para la aplicación de pulseras inteligentes.

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

## Algoritmos de Recomendación

El sistema utiliza el grafo para generar recomendaciones utilizando varios algoritmos:

1. **Recomendación de Actividades**: Sugiere actividades que el usuario no realiza actualmente pero que contribuyen a los objetivos que está intentando alcanzar.

2. **Recomendación de Objetivos**: Sugiere nuevos objetivos que son similares a los que el usuario ya ha cumplido o está intentando alcanzar.

3. **Recomendación por Similitud**: Identifica usuarios similares basados en sus patrones de actividad y objetivos, y recomienda actividades que estos usuarios similares realizan pero que el usuario objetivo no.

## Consultas Cypher Comunes

```cypher
// Obtener todos los usuarios
MATCH (u:Usuario) RETURN u

// Obtener todas las actividades que contribuyen a un objetivo específico
MATCH (a:Actividad)-[:CONTRIBUYE_A]->(o:Objetivo {nombre: "Sueño reparador"})
RETURN a.nombre, a.descripcion

// Encontrar todos los objetivos que un usuario está intentando alcanzar
MATCH (u:Usuario {id_usuario: 1})-[:TIENE_OBJETIVO]->(o:Objetivo)
RETURN o.nombre, o.descripcion

// Encontrar actividades recomendadas para un usuario
MATCH (u:Usuario {id_usuario: 1})-[:TIENE_OBJETIVO]->(o:Objetivo),
      (a:Actividad)-[:CONTRIBUYE_A]->(o)
WHERE NOT (u)-[:REALIZA]->(a)
RETURN a.nombre, a.descripcion, COUNT(o) AS relevancia
ORDER BY relevancia DESC

// Obtener usuarios similares
MATCH (u1:Usuario {id_usuario: 1})-[:REALIZA]->(a:Actividad)<-[:REALIZA]-(u2:Usuario)
WHERE u1 <> u2
RETURN u2.nombre, COUNT(a) AS actividades_comunes
ORDER BY actividades_comunes DESC
```

## Estructura del Directorio

Este directorio contiene dos subdirectorios principales:

- **etl_scripts_nodos**: Contiene scripts para la creación y actualización de los nodos en el grafo
  - `etl_insertar_nodos_usuarios.py`: Inserta nodos de usuarios desde MongoDB
  - `etl_insertar_nodos_actividades.py`: Inserta nodos de actividades físicas
  - `etl_insertar_nodos_objetivos.py`: Inserta nodos de objetivos de salud

- **etl_scripts_relaciones**: Contiene scripts para gestionar las relaciones entre nodos
  - `etl_relacion_usuario_actividad.py`: Gestiona relaciones REALIZA entre usuarios y actividades
  - `etl_relacion_usuario_objetivo.py`: Gestiona relaciones TIENE_OBJETIVO y CUMPLIO entre usuarios y objetivos
  - `etl_relacion_actividad_objetivo.py`: Establece relaciones CONTRIBUYE_A entre actividades y objetivos
