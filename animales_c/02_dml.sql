-- ============================================================
-- PROYECTO FAUNAVISION - SCRIPT DML (02_dml.sql)
-- Base de Datos: MariaDB (faunavision_db)
-- Descripción: Inserción de datos de prueba con casos límite
-- adaptados al esquema DDL provisto.
-- ============================================================

USE faunavision_db;

-- Desactivar temporalmente la verificación de claves foráneas para orden de inserción
SET FOREIGN_KEY_CHECKS = 0;

-- ------------------------------------------------------------
-- 1. TABLA: animalescautiverio (10 registros)
-- ------------------------------------------------------------
INSERT INTO animalescautiverio (id_animal, Especie, Peso, Edad, Tamano, observaciones) VALUES
(1, 'Canis lupus baileyi (Lobo Mexicano)', 32.50, '4 años', 1.20, 'En buen estado de salud general.'),
(2, 'Odocoileus virginianus (Venado Cola Blanca)', 65.00, '3 años', 1.50, 'Aclimatado al área de sabana.'),
(3, 'Urocyon cinereoargenteus (Zorro Gris)', 4.20, '2 años', 0.60, 'Monitoreo preventivo por muda de pelaje.'),
(4, 'Aquila chrysaetos (Águila Real)', 4.50, '5 años', 0.90, 'Resguardada con férula leve en ala derecha.'),
(5, 'Lynx rufus (Gato Montés)', 9.80, '3 años', 0.75, 'Ejemplar rescatado de zona urbana.'),
(6, 'Puma concolor (Puma)', 55.00, '6 años', 1.80, 'Comportamiento territorial estable.'),
(7, 'Ursus americanus (Oso Negro)', 120.00, '8 años', 2.10, 'En periodo de seguimiento nutricional.'),
(8, 'Bassariscus astutus (Cacomixtle)', 1.10, '1 año', 0.40, 'Hábitos nocturnos registrados en fototrampeo.'),
(9, 'Nasua narica (Tejón / Coatí)', 5.50, '2 años', 0.85, 'Integrado recientemente a manada.'),
(10, 'Tayassu tajacu (Pecarí de Collar)', 20.00, '4 años', 0.95, 'Caso Límite: Sin observaciones médicas previas.');

-- ------------------------------------------------------------
-- 2. TABLA: clase (Personal / Veterinarios) (10 registros)
-- Nota: La PK es 'Telefono' (VARCHAR)
-- ------------------------------------------------------------
INSERT INTO clase (Telefono, Nombre, Apellido1, Apellido2, Cargo, Calle, Col, Num, Codigo_postal, correo) VALUES
('6181234567', 'Carlos', 'Mendoza', 'Rivas', 'Médico Veterinario Titular', 'Av. Cima', 'Lomas del Parque', 120, 34100, 'carlos.mendoza@faunavision.org'),
('6182345678', 'Ana', 'Rosa', 'Gómez', 'Especialista en Fauna Silvestre', 'Calle Roble', 'Sahuatoba', 45, 34107, 'ana.gomez@faunavision.org'),
('6183456789', 'Roberto', 'Silva', 'Pérez', 'Cirujano Veterinario', 'Blvd. Guadiana', 'Fracc. Real del Parque', 300, 34110, 'roberto.silva@faunavision.org'),
('6184567890', 'Lucía', 'Torres', 'Medrano', 'Nutrióloga Animal', 'Paseo de las Rosas', 'Jardines de Durango', 88, 34200, 'lucia.torres@faunavision.org'),
('6185678901', 'Javier', 'Hernández', 'Soto', 'Técnico de Campo', 'Calle 5 de Febrero', 'Centro', 512, 34000, 'javier.hernandez@faunavision.org'),
('6186789012', 'Elena', 'Ramos', 'Luna', 'Patóloga Veterinaria', 'Av. Universidad', 'Burócratas', 102, 34140, 'elena.ramos@faunavision.org'),
('6187890123', 'Miguel', 'Ángel', 'Ortiz', 'Anestesiólogo', 'Calle Aluminio', 'Industrial', 15, 34220, 'miguel.ortiz@faunavision.org'),
('6188901234', 'Sofía', 'Morales', 'Díaz', 'Coordinadora de Biología', 'Prolongación
