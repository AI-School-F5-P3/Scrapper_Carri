\encoding UTF8

\c postgres

-- Terminar las conexiones existentes a la base de datos 'quotes'
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'quotes' AND pid <> pg_backend_pid();

-- Conectar a la base de datos 'quotes'
\c quotes

SET client_encoding TO 'UTF8';

COMMENT ON DATABASE quotes IS 'Base de datos de frases';

CREATE SCHEMA IF NOT EXISTS quotes;

-- Eliminar las tablas existentes si existen
DROP TABLE IF EXISTS quotes.quote CASCADE;
DROP TABLE IF EXISTS quotes.tag CASCADE;
DROP TABLE IF EXISTS quotes.author CASCADE;

-- Crear la tabla 'tag'
CREATE TABLE quotes.tag (
    "id" SERIAL PRIMARY KEY,
    "tag" VARCHAR(100) UNIQUE NOT NULL
);

COMMENT ON TABLE quotes.tag IS 'Tabla para almacenar las etiquetas';

-- Crear la tabla 'author'
CREATE TABLE quotes.author (
    "id" SERIAL PRIMARY KEY,
    "author" VARCHAR(100) UNIQUE NOT NULL,
    "about" VARCHAR
);

COMMENT ON TABLE quotes.author IS 'Tabla que almacena la información sobre el autor de la cita';
COMMENT ON COLUMN quotes.author."about" IS 'Información sobre el autor';

-- Crear la tabla 'quote'
CREATE TABLE quotes.quote (
    "id" SERIAL PRIMARY KEY,
    "quote" VARCHAR,
    "author" INTEGER NOT NULL,
    "tag1" INTEGER NOT NULL,
    "tag2" INTEGER,
    "tag3" INTEGER, 
    "tag4" INTEGER,
    "tag5" INTEGER,
    "tag6" INTEGER,
    "tag7" INTEGER,
    "tag8" INTEGER,
    FOREIGN KEY ("author") REFERENCES quotes.author("id"),
    FOREIGN KEY ("tag1") REFERENCES quotes.tag("id"),
    FOREIGN KEY ("tag2") REFERENCES quotes.tag("id"),
    FOREIGN KEY ("tag3") REFERENCES quotes.tag("id"),
    FOREIGN KEY ("tag4") REFERENCES quotes.tag("id"),
    FOREIGN KEY ("tag5") REFERENCES quotes.tag("id"),
    FOREIGN KEY ("tag6") REFERENCES quotes.tag("id"),
    FOREIGN KEY ("tag7") REFERENCES quotes.tag("id"),
    FOREIGN KEY ("tag8") REFERENCES quotes.tag("id")
);

COMMENT ON TABLE quotes.quote IS 'Tabla para almacenar las citas y sus etiquetas';
COMMENT ON COLUMN quotes.quote."id" IS 'Identificador de cita';
COMMENT ON COLUMN quotes.quote."quote" IS 'Texto de la cita';
COMMENT ON COLUMN quotes.quote."author" IS 'Identificador del autor';
COMMENT ON COLUMN quotes.quote."tag1" IS 'Identificador para la etiqueta';

-- Crear el rol 'administrator' si no existe
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'administrator') THEN
        CREATE ROLE administrator;
    END IF;
END $$;

-- Conceder permiso de conexión a la base de datos 'quotes' para el rol 'administrator'
GRANT CONNECT ON DATABASE quotes TO administrator;

-- Conceder uso del esquema 'quotes' al rol 'administrator'
GRANT USAGE ON SCHEMA quotes TO administrator;

-- Conceder permisos de SELECT, INSERT, UPDATE y DELETE en todas las tablas del esquema 'quotes' al rol 'administrator'
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA quotes TO administrator;

-- Alterar los privilegios predeterminados para que el rol 'administrator' tenga permisos de SELECT, INSERT, UPDATE y DELETE en nuevas tablas
ALTER DEFAULT PRIVILEGES IN SCHEMA quotes GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO administrator;

-- Conceder uso de todas las secuencias en el esquema 'quotes' al rol 'administrator'
GRANT USAGE ON ALL SEQUENCES IN SCHEMA quotes TO administrator;

-- Alterar los privilegios predeterminados para que el rol 'administrator' tenga permisos de USAGE en nuevas secuencias
ALTER DEFAULT PRIVILEGES IN SCHEMA quotes GRANT USAGE ON SEQUENCES TO administrator;

-- Crear un usuario llamado 'admin_user' con una contraseña
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'admin_user') THEN
        CREATE USER admin_user WITH LOGIN PASSWORD '1234';
    END IF;
END $$;

-- Conceder el rol 'administrator' al usuario 'admin_user'
GRANT administrator TO admin_user;

-- Consultar los roles existentes y sus miembros, excluyendo roles del sistema
SELECT
    r.rolname,  -- Nombre del rol
    ARRAY(SELECT b.rolname  -- Array de nombres de roles a los que pertenece
          FROM pg_catalog.pg_auth_members m
          JOIN pg_catalog.pg_roles b ON (m.roleid = b.oid)
          WHERE m.member = r.oid) as memberof
FROM pg_catalog.pg_roles r
WHERE r.rolname NOT IN ('pg_signal_backend','rds_iam',
                         'rds_replication','rds_superuser',
                         'rdsadmin','rdsrepladmin')  -- Excluir roles del sistema
ORDER BY 1;  -- Ordenar por el nombre del rol