-- CREACION DE DW

CREATE TABLE "dim_plan" (
	"id_plan" SERIAL PRIMARY KEY,
	"nombre_plan" VARCHAR(100) NOT NULL,
	"descripcion" TEXT NOT NULL,
	"duracion_dias" INTEGER NOT NULL
);

CREATE TABLE "dim_metodo_pago" (
	"id_metodo_pago" SERIAL PRIMARY KEY,
	"descripcion" VARCHAR(100) NOT NULL
);

CREATE TABLE "dim_estado_pago" (
	"id_estado" SERIAL PRIMARY KEY,
	"descripcion" VARCHAR(50) NOT NULL
);

CREATE TABLE "dim_actividad" (
	"id_actividad" SERIAL PRIMARY KEY,
	"tipo_dato" VARCHAR(50) NOT NULL, 
	"descripcion" VARCHAR(100) NOT NULL 
);

CREATE TABLE "dim_usuario" (
	"id_usuario" INTEGER PRIMARY KEY,
	"nombre" VARCHAR(50) NOT NULL,
	"genero" VARCHAR(50) NOT NULL,
	"fecha_registro" TIMESTAMP NOT NULL,
	"fecha_nacimiento" DATE NOT NULL
);

CREATE TABLE "dim_fecha" (
	"id_fecha" SERIAL PRIMARY KEY,
	"fecha" TIMESTAMP NOT NULL,
	"dia" INTEGER NOT NULL,
	"mes" INTEGER NOT NULL,
	"trimestre" INTEGER NOT NULL,
	"anio" INTEGER NOT NULL
);


CREATE TABLE "hechos_pagos" (
	"id_hecho" SERIAL PRIMARY KEY,
	"id_usuario" INTEGER NOT NULL,
	"id_plan" INTEGER NOT NULL,
	"id_metodo_pago" INTEGER NOT NULL,
	"id_estado_pago" INTEGER NOT NULL,
	"id_fecha" INTEGER NOT NULL,
	"hora_registro" TIME NOT NULL,
	"monto_pago" DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_usuario FOREIGN KEY ("id_usuario") REFERENCES "dim_usuario"("id_usuario"),
    CONSTRAINT fk_plan FOREIGN KEY ("id_plan") REFERENCES "dim_plan"("id_plan"),
    CONSTRAINT fk_metodo_pago FOREIGN KEY ("id_metodo_pago") REFERENCES "dim_metodo_pago"("id_metodo_pago"),
    CONSTRAINT fk_estado_pago FOREIGN KEY ("id_estado_pago") REFERENCES "dim_estado_pago"("id_estado"),
    CONSTRAINT fk_fecha FOREIGN KEY ("id_fecha") REFERENCES "dim_fecha"("id_fecha")
);

CREATE TABLE "hechos_actividad" (
    "id_hecho" SERIAL PRIMARY KEY,
    "id_usuario" INTEGER NOT NULL,
    "id_actividad" INTEGER NOT NULL,  
    "id_fecha" INTEGER NOT NULL, 
	"hora_registro" TIME NOT NULL,       
    CONSTRAINT fk_usuario_actividad FOREIGN KEY ("id_usuario") REFERENCES "dim_usuario"("id_usuario"),
    CONSTRAINT fk_actividad FOREIGN KEY ("id_actividad") REFERENCES "dim_actividad"("id_actividad"),
    CONSTRAINT fk_fecha_actividad FOREIGN KEY ("id_fecha") REFERENCES "dim_fecha"("id_fecha")
);


-- TABLA DE LOGS PARA AUDITORÍA
CREATE TABLE log_eventos (
    "id_log" SERIAL PRIMARY KEY,
    "tabla_afectada" TEXT NOT NULL,
    "operacion" TEXT NOT NULL,              
    "fecha_operacion" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "clave_primaria" TEXT,                  
    "datos_anteriores" JSONB,              
    "datos_nuevos" JSONB                   
);