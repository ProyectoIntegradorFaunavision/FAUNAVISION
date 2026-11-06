
-- =============================================
-- FAUNAVISION
-- 01_ddl.sql
-- Sistema gestor: MariaDB
-- =============================================

CREATE DATABASE IF NOT EXISTS faunavision_db;
USE faunavision_db;

-- =============================================
-- TABLA: ANIMALES EN CAUTIVERIO
-- =============================================

CREATE TABLE animalescautiverio (
    id_animal INT AUTO_INCREMENT PRIMARY KEY,
    Especie VARCHAR(100) NOT NULL,
    Peso DECIMAL(8,2),
    Edad VARCHAR(50),
    Tamano DECIMAL(8,2),
    observaciones VARCHAR(255),

    CONSTRAINT chk_animal_peso
        CHECK (Peso IS NULL OR Peso > 0),

    CONSTRAINT chk_animal_tamano
        CHECK (Tamano IS NULL OR Tamano > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =============================================
-- TABLA: PERSONAL
-- =============================================

CREATE TABLE clase (
    Telefono VARCHAR(20) PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Apellido1 VARCHAR(100) NOT NULL,
    Apellido2 VARCHAR(100),
    Cargo VARCHAR(100) NOT NULL,
    Calle VARCHAR(100),
    Col VARCHAR(100),
    Num INT,
    Codigo_postal INT,
    correo VARCHAR(100) UNIQUE,

    CONSTRAINT chk_personal_num
        CHECK (Num IS NULL OR Num > 0),

    CONSTRAINT chk_personal_cp
        CHECK (Codigo_postal IS NULL OR Codigo_postal > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =============================================
-- TABLA: MEDICAMENTOS
-- =============================================

CREATE TABLE medicamentos (
    Nombre VARCHAR(100) PRIMARY KEY,
    Stock INT NOT NULL DEFAULT 0,
    Principio_activo VARCHAR(100),
    Cant_concentrado DECIMAL(8,2),
    Tamano DECIMAL(8,2),
    via_administracion VARCHAR(50),

    CONSTRAINT chk_medicamento_stock
        CHECK (Stock >= 0),

    CONSTRAINT chk_medicamento_concentrado
        CHECK (Cant_concentrado IS NULL OR Cant_concentrado >= 0),

    CONSTRAINT chk_medicamento_tamano
        CHECK (Tamano IS NULL OR Tamano > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =============================================
-- TABLA: EXPEDIENTE MEDICO
-- =============================================

CREATE TABLE expediente (
    id_expediente INT AUTO_INCREMENT PRIMARY KEY,
    Animal INT NOT NULL,
    Medicamento VARCHAR(100) NOT NULL,
    Veterinario VARCHAR(20) NOT NULL,
    Fecha_aplicacion DATE NOT NULL,
    Fecha_proxima DATE,
    Dosis VARCHAR(50),
    observaciones VARCHAR(255),

    CONSTRAINT chk_fecha_proxima
        CHECK (
            Fecha_proxima IS NULL
            OR Fecha_proxima >= Fecha_aplicacion
        ),

    CONSTRAINT fk_expediente_animal
        FOREIGN KEY (Animal)
        REFERENCES animalescautiverio(id_animal)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_expediente_medicamento
        FOREIGN KEY (Medicamento)
        REFERENCES medicamentos(Nombre)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_expediente_personal
        FOREIGN KEY (Veterinario)
        REFERENCES clase(Telefono)
        ON DELETE RESTRICT
        ON UPDATE CASCADE

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =============================================
-- FIN DEL SCRIPT DDL
-- =============================================
