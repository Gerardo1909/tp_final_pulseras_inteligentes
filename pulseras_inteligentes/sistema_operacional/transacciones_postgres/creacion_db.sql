CREATE TABLE "genero" (
	"id_genero" SERIAL PRIMARY KEY,
	"genero" VARCHAR(50) NOT NULL
);

CREATE TABLE "planes" (
	"id_plan" SERIAL PRIMARY KEY,
	"nombre_plan" VARCHAR(100) NOT NULL,
	"descripcion" TEXT NOT NULL,
	"duracion_dias" INTEGER NOT NULL
);

CREATE TABLE "metodo_pago" (
	"id_metodo" SERIAL PRIMARY KEY,
	"descripcion" VARCHAR(100) NOT NULL
);

CREATE TABLE "estado_pago" (
	"id_estado" SERIAL PRIMARY KEY,
	"descripcion" VARCHAR(50) NOT NULL
);

CREATE TABLE "estado_suscripcion" (
	"id_estado" SERIAL PRIMARY KEY,
	"descripcion" VARCHAR(50) NOT NULL
);

CREATE TABLE "usuarios" (
	"id_usuario" SERIAL PRIMARY KEY,
	"nombre" VARCHAR(50) NOT NULL,
	"email" VARCHAR(255) NOT NULL,
	"fecha_nacimiento" DATE NOT NULL,
	"id_genero" INTEGER NOT NULL,
	"fecha_registro" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT fk_genero FOREIGN KEY ("id_genero") REFERENCES "genero"("id_genero")
);

CREATE TABLE "pagos" (
	"id_pago" SERIAL PRIMARY KEY,
	"id_metodo_pago" INTEGER NOT NULL,
	"monto" DECIMAL(10,2) NOT NULL,
	"fecha_transaccion" TIMESTAMP NOT NULL,
	"id_estado_pago" INTEGER NOT NULL,
	"id_usuario" INTEGER NOT NULL,
	CONSTRAINT fk_metodo_pago FOREIGN KEY ("id_metodo_pago") REFERENCES "metodo_pago"("id_metodo"),
	CONSTRAINT fk_estado_pago FOREIGN KEY ("id_estado_pago") REFERENCES "estado_pago"("id_estado"),
	CONSTRAINT fk_usuario_pago FOREIGN KEY ("id_usuario") REFERENCES "usuarios"("id_usuario")
);

CREATE TABLE "suscripcion" (
	"id_suscripcion" SERIAL PRIMARY KEY,
	"id_usuario" INTEGER NOT NULL,
	"id_plan" INTEGER NOT NULL,
	"fecha_inicio" TIMESTAMP NOT NULL,
	"fecha_fin" TIMESTAMP NOT NULL,
	"id_estado" INTEGER NOT NULL,
	"id_pago" INTEGER NOT NULL,
	CONSTRAINT fk_usuario FOREIGN KEY ("id_usuario") REFERENCES "usuarios"("id_usuario"),
	CONSTRAINT fk_plan FOREIGN KEY ("id_plan") REFERENCES "planes"("id_plan"),
	CONSTRAINT fk_estado FOREIGN KEY ("id_estado") REFERENCES "estado_suscripcion"("id_estado"),
	CONSTRAINT fk_pago FOREIGN KEY ("id_pago") REFERENCES "pagos"("id_pago")
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





