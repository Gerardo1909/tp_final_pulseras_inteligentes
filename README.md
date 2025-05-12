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
* **Separación modular del código por subsistema**: transaccional, de recomendación y analítico.

## 🧱 Arquitectura del Sistema

La arquitectura propuesta está organizada en tres subsistemas principales: **sistema transaccional**, **sistema de recomendación** y **data warehouse analítico**. Cada uno de estos módulos cumple una función específica dentro del ecosistema de datos, y están conectados mediante procesos ETL desarrollados en Python.

1. **Sistema Transaccional**
   Este componente gestiona toda la información operativa y transaccional. Se encuentra implementado en **PostgreSQL (a través de Supabase)** e incluye:

   * Datos de **usuarios**, suscripciones, pagos y estados asociados.
   * Un backend de **sensores** y **aplicación móvil**, cuyos datos son almacenados en **MongoDB**. Aquí se registran tanto las métricas biométricas recolectadas por las pulseras como las interacciones con la aplicación por parte de los usuarios (como tiempo de pantalla o uso de funciones).

2. **Data Warehouse Analítico**
   Los datos transaccionales y sensoriales son procesados mediante un flujo ETL y consolidados en un **Data Warehouse** alojado en **PostgreSQL (a través de Supabase)**. Este almacena dos grandes bloques:

   * Un conjunto de **tablas dimensionales** (usuarios, fechas, actividad, planes, etc.).
   * Dos **tablas de hechos**: una sobre **pagos** y otra sobre **actividad**, que permiten análisis de negocio y patrones de comportamiento.

   Esta capa sirve como fuente para herramientas de inteligencia de negocios como Power BI, donde se visualizan métricas clave sobre el uso del sistema, hábitos saludables y comportamiento de los usuarios.

3. **Sistema de Recomendación**
   Este módulo está construido sobre **Neo4j**, un motor de base de datos orientado a grafos. A partir de los datos recolectados por los sensores (desde MongoDB), se crean **nodos** representando a usuarios, actividades físicas y objetivos de salud. Además, se generan **relaciones** que modelan:

   * Qué actividades realiza cada usuario.
   * Qué objetivos se plantea alcanzar.
   * Qué actividades contribuyen a qué objetivos.

   Estas relaciones permiten desarrollar **recomendaciones personalizadas** que se adaptan dinámicamente al perfil de cada usuario y sus hábitos.


## 📂 Estructura del Proyecto

```bash
pulseras_inteligentes/
├── dashboards/                          # Dashboards generados (Power BI)
├── datawarehouse/
│   ├── etl_scripts/
│   │   ├── creacion_dw.sql             # Creación de tablas dimensionales y de hechos
│   │   └── insercion_datos_dimensiones.sql
│   └── README.md
├── sistema_recomendaciones/
│   ├── etl_scripts_nodos/              # Carga de nodos en Neo4j
│   ├── etl_scripts_relaciones/         # Carga de relaciones entre nodos
│   └── README.md
├── sistema_transaccional/
│   ├── pulsera_inteligente/            # Datos de sensores
│   ├── transacciones_negocio/          # Datos de usuarios, pagos, suscripciones
│   └── README.md
├── utils/                               # Funciones auxiliares
├── main.py                              # Ejecución principal de todo el flujo
├── requirements.txt                     # Requerimientos de Python
├── setup.py                             # Configuración del entorno
└── README.md                            # Este archivo
```

## ⚙️ Tecnologías Utilizadas

* **PostgreSQL (via Supabase):** Gestión transaccional y Data Warehouse
* **MongoDB:** Registro de datos biométricos y de aplicación
* **Neo4j:** Motor de grafos para recomendaciones contextuales
* **Python (ETL y Simulación):** Scripts de carga y transformación de datos
* **Power BI:** Dashboards con métricas de comportamiento y negocio



