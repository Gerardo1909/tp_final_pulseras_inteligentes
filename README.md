# Trabajo Práctico Final - Base de datos (Licenciatura en Ciencia de Datos)

## 📋 Enunciado del trabajo

Este proyecto corresponde al trabajo práctico final de la materia *Base de Datos*, y tiene como objetivo la implementación de un sistema analítico realista utilizando un enfoque **políglota**, combinando al menos **un motor SQL** y **dos motores NoSQL**. La consigna propone el diseño de una arquitectura de inteligencia de negocios (BI), incluyendo un Data Warehouse, un sistema de recomendaciones y la construcción de dashboards. El trabajo integra procesos ETL, modelado dimensional (estrella o copo de nieve), y técnicas de minería de datos, simulando un caso empresarial completo.

## 🧠 Nuestro caso de negocio

Somos parte del equipo de datos de la empresa **\[Nombre Empresa]**, una compañía que desarrolla una plataforma basada en **pulseras inteligentes** para monitorear métricas de salud y actividad física, al estilo de productos como [Whoop](https://www.whoop.com/us/en/). Nuestra responsabilidad es diseñar la infraestructura de datos que soporte tanto el análisis de negocio como el motor de recomendaciones personalizado.

Las pulseras inteligentes registran información biométrica como:

* Actividad física
* Duración y calidad del sueño
* Tiempo en reposo
* Niveles de glucosa

Además, se recolectan métricas de uso de la aplicación móvil asociada:

* Tiempo de pantalla
* Interacciones con botones y formularios
* Uso de funcionalidades específicas

El valor agregado del producto radica en su **sistema de recomendación personalizado**, que sugiere rutinas, descansos y hábitos saludables en función del comportamiento del usuario, con el objetivo de maximizar su bienestar y fomentar la fidelización.

Este ecosistema se completa con la **aplicación móvil**, cuya usabilidad también es monitoreada para detectar oportunidades de mejora y retroalimentar al equipo de desarrollo.

## 🧾 Requerimientos clave

Desde la perspectiva del área de datos, se establecen los siguientes requerimientos:

* **Modelado de un Data Warehouse** con enfoque dimensional (estrella o copo de nieve).
* **Implementación de procesos ETL** para la carga de datos provenientes de múltiples orígenes heterogéneos (SQL y NoSQL).
* **Diseño de un sistema de recomendaciones** basado en grafos y relaciones entre entidades (usuarios, objetivos, actividades).
* **Simulación de datos sintéticos** en cada capa del sistema, con scripts de generación y carga.
* **Dashboard interactivo en Power BI**, con al menos 4 elementos visuales claves para la toma de decisiones.
* **Separación modular del código por subsistema**: operacional, de recomendación y analítico.

## 🧱 Flujo de datos del Sistema

![Flujo de datos](./img/flujo_informacion_pulseras_inteligentes.png)

El flujo de datos de la aplicación está organizado en tres subsistemas principales: **Sistema Operacional**, **Data Warehouse** y **Capa de Business Inteligence**. Cada uno de estos módulos cumple una función específica dentro del ecosistema de datos, y están conectados mediante procesos ETL desarrollados en Python.

1. **Sistema operacional**
   Este componente gestiona toda la información operativa relacionada a transacciones comerciales y datos brutos de aplicación móvil y sensor de la pulsera. Se encuentra conformado por dos bases de datos:

   * **Una PostgreSQL (a través de Supabase)** que registra datos de **usuarios**, **suscripciones**, **pagos** y **estados asociados**.
   * **Y otra MongoDB** que registra los datos enviados por los **sensores de la pulsera** y la **aplicación móvil**. Aquí se registran tanto 
   las métricas biométricas recolectadas por las pulseras como las interacciones con la aplicación por parte de los usuarios (como tiempo de pantalla o uso de funciones).

2. **Data Warehouse**
   Los datos operacionales son procesados mediante un flujo ETL y consolidados en un **Data Warehouse** basado en **persistencia políglota**. El objetivo 
   del mismo es guardar toda la información histórica del negocio para luego poder ser explotada por analistas y así mejorar continuamente el producto. El mismo se encuentra conformado por las siguientes bases de datos:

   * **Una PostgreSQL (a través de Supabase)** la cual contiene el modelo dimensional utilizado para analizar hechos asociados a ventas/suscripciones del producto.
   * **Una MongoDB** que contiene una serie de colecciones las cuales están orientadas a responder preguntas de negocio en cuanto a usabilidad del producto y aplicación móvil.
   * **Y otra Neo4j** que contiene nodos los cuales representan usuarios, actividades físicas y objetivos relacionados a salud, además de relaciones
   entre los mismos que definen comportamientos en cuanto a uso de la pulsera en sí.  

3. **Capa de Business Inteligence**
   Una vez que los datos están consolidados en el **Data Warehouse** estos están listos para ser analizados y así obtener insights valiosos sobre el producto 
   en general. Entre los puntos clave del negocio que esta capa busca cubrir están:

   * Análisis de ventas del producto y suscripciones a lo largo del tiempo por parte de usuarios.
   * Análisis de usabilidad de la pulsera y aplicación móvil en tiempo real.
   * Desarrollo de sistemas de recomendación para mejorar la experiencia del usuario y garantizar fidelidad.


## 📂 Estructura del Proyecto

```bash
pulseras_inteligentes/
├── sistema_operacional/           # Sistema operacional (datos transaccionales)
│   ├── ingesta_sensor_mongo/      # Scripts para ingesta de datos de sensores y aplicación móvil en MongoDB
│   └── transacciones_postgres/    # Scripts para gestión de transacciones comerciales en PostgreSQL
│
├── datawarehouse/                 # Data Warehouse (persistencia políglota)
│   ├── dwh_ventas/                # Modelo dimensional para análisis de ventas (PostgreSQL)
│   ├── dwh_usabilidad/            # Colecciones para análisis de usabilidad (MongoDB)
│   └── sistema_recomendacion/     # Sistema de recomendación basado en grafos (Neo4j)
│
├── business_inteligence/          # Capa de Business Intelligence
│   └── dashboards/                # Dashboards de Power BI
│
├── utils/                         # Utilidades compartidas
│   ├── conexiones_db.py           # Funciones de conexión a bases de datos
│   └── etl_funcs.py               # Funciones comunes para procesos ETL
```

## ⚙️ Tecnologías Utilizadas

* [**PostgreSQL (via Supabase)**](https://supabase.com/) 
* [**MongoDB**](https://www.mongodb.com/) 
* [**Neo4j**](https://neo4j.com/) 
* [**Python (ETL y Simulación)** ](https://www.python.org/)
* [**Power BI** ](https://www.microsoft.com/es-es/power-platform/products/power-bi)

## ⚙️ Cómo clonar y correr este proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/Gerardo1909/tp_final_pulseras_inteligentes.git
cd tp_final_pulseras_inteligentes
```

### 2. Crear y activar un entorno virtual

```bash
python -m venv venv
source venv/bin/activate      # En Linux/macOS
venv\Scripts\activate.bat     # En Windows
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Instalar el proyecto en modo editable
Esto permite importar los módulos de `utils` desde cualquier notebook sin problemas:

```bash
pip install -e .
```



