# Trabajo Práctico Final - Base de datos (Licenciatura en Ciencia de Datos)

**Participantes del proyecto:**

* Gerardo Toboso - getobosobarrios@estudiantes.unsam.edu.ar
* Gianni Bevilacqua - gbevilacqua@estudiantes.unsam.edu.ar
* Javier Spina - jaspina@estudiantes.unsam.edu.ar
* Bautista Turri - Turribautista551@gmail.com

Este proyecto corresponde al trabajo práctico final de la materia **Base de Datos** de la Lienciatura en Ciencia de Datos (1er cuatrimestre 2025). Tiene como objetivo la implementación de un sistema analítico realista utilizando un enfoque **políglota**, combinando al menos **un motor SQL** y **un motor NoSQL**. La consigna propone el diseño de una arquitectura de inteligencia de negocios (BI), incluyendo un Data Warehouse y la construcción de dashboards para realizar análisis de datos. El trabajo integra procesos ETL, modelado dimensional de tablas, y técnicas de minería de datos, simulando un caso empresarial completo.

## 🧠 Nuestro caso de negocio

Somos parte del **equipo de datos** de una compañía que desarrolla una plataforma basada en **pulseras inteligentes** para monitorear métricas de salud y actividad física, al estilo de productos como [Whoop](https://www.whoop.com/us/en/). Nuestra responsabilidad es diseñar la infraestructura de datos que soporte tanto el análisis de negocio como el flujo de información constante.

Las pulseras inteligentes registran información biométrica como:

* Actividad física
* Duración y calidad del sueño
* Tiempo en reposo
* Niveles de glucosa

Además, se recolectan métricas de uso de la aplicación móvil asociada:

* Tiempo de pantalla
* Interacciones con botones y formularios
* Uso de funcionalidades específicas

## 🧾 Requerimientos clave

Desde la perspectiva del área de datos, se establecen los siguientes requerimientos:

* **Modelado de un Data Warehouse** con enfoque dimensional (estrella o copo de nieve).
* **Implementación de procesos ETL** para la carga de datos provenientes de múltiples orígenes heterogéneos (SQL y NoSQL).
* **Dashboard interactivo en Power BI**, con al menos 4 elementos visuales claves para la toma de decisiones.
* **Separación modular del código por subsistema**: operacional y analítico.

## 🧱 Flujo de datos del Sistema

![Flujo de datos](./img/flujo_informacion_pulseras_inteligentes.png)

El flujo de datos de la aplicación está organizado en tres subsistemas principales: **Sistema Operacional**, **Data Warehouse** y **Capa de Business Inteligence**. Cada uno de estos módulos cumple una función específica dentro del ecosistema de datos, y están conectados mediante procesos ETL desarrollados en Python.

1. **Sistema operacional**
   Este componente gestiona toda la información operativa relacionada a transacciones comerciales y datos brutos de aplicación móvil y sensor de la pulsera. Se encuentra conformado por dos bases de datos:

   * **Una PostgreSQL (a través de Supabase)** que registra datos de **usuarios**, **suscripciones**, **pagos** y **estados asociados**.
   * **Y otra MongoDB** que registra los datos enviados por los **sensores de la pulsera** y la **aplicación móvil**. Aquí se registran tanto 
   las métricas biométricas recolectadas por las pulseras como las interacciones con la aplicación por parte de los usuarios (como tiempo de pantalla o uso de funciones).

2. **Data Warehouse**
   Los datos operacionales son procesados mediante un flujo ETL y consolidados en un **Data Warehouse**. El objetivo 
   del mismo es guardar toda la información histórica del negocio para luego poder ser explotada por analistas y así mejorar continuamente el producto. El mismo se encuentra alojado en una base de datos **PostgreSQL (a través de Supabase)** la cual registra dos tipos de hechos de especial interés para la compañia:

   * **Hechos asociados a ventas/suscripciones del producto**.
   * **Hechos asociados a usabilidad del producto**, esto hace referencia a uso de la aplicación por parte de los usuarios y el uso de la pulsera por igual.

3. **Capa de Business Inteligence**
   Una vez que los datos están consolidados en el **Data Warehouse** estos están listos para ser analizados y así obtener insights valiosos sobre el producto 
   en general. Entre los puntos clave del negocio que esta capa busca cubrir están:

   * Análisis de ventas del producto y suscripciones a lo largo del tiempo por parte de usuarios.
   * Análisis de usabilidad de la pulsera y aplicación móvil en tiempo real.


## 📂 Estructura del Proyecto

```bash
pulseras_inteligentes/
├── sistema_operacional/           # Sistema operacional (datos transaccionales)
│   ├── ingesta_sensor_mongo/      # Scripts para ingesta de datos de sensores y aplicación móvil en MongoDB
│   └── transacciones_postgres/    # Scripts para gestión de transacciones comerciales en PostgreSQL
│
├── datawarehouse/                 # Data Warehouse (Hechos de ventas y usabilidad)
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



