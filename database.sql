CREATE DATABASE IF NOT EXISTS db_admision;
USE db_admision;
CREATE TABLE Claves (
  Lito VARCHAR(6),
  Tema VARCHAR(1),
  Solución VARCHAR(100),
  PRIMARY KEY (Lito, Tema)
);

CREATE TABLE Identificador (
  Lito VARCHAR(6),
  Tema VARCHAR(1),
  CodigoPotulante VARCHAR(6),
  PRIMARY KEY (Lito, Tema, CodigoPotulante),
  FOREIGN KEY (Lito, Tema) REFERENCES Claves(Lito, Tema)
);

CREATE TABLE Respuestas (
  Lito VARCHAR(6),
  Tema VARCHAR(1),
  Respuesta VARCHAR(100),
  PRIMARY KEY (Lito, Tema, Respuesta),
  FOREIGN KEY (Lito, Tema) REFERENCES Claves(Lito, Tema)
);