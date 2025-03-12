CREATE TABLE Flotilla
(
  flotillaId INT AUTO_INCREMENT UNIQUE,
  nombreEmpresa VARCHAR(100) NOT NULL,
  gestorFlotilla VARCHAR(100) NOT NULL,
  fechaCreacion DATE NOT NULL,
  PRIMARY KEY (flotillaId)
);


CREATE TABLE Vehiculo
(
  vehiculoId INT AUTO_INCREMENT UNIQUE,
  flotillaId INT NOT NULL,
  tipo VARCHAR(50) NOT NULL,
  modelo VARCHAR(50) NOT NULL,
  marca VARCHAR(50) NOT NULL,
  anio INT NOT NULL,
  estado VARCHAR(20) NOT NULL DEFAULT 'Activo',
  fechaVerificacion DATE,
  PRIMARY KEY (vehiculoId),
  FOREIGN KEY (flotillaId) REFERENCES Flotilla(flotillaId)
);


CREATE TABLE Documento
(
  documentoId INT AUTO_INCREMENT UNIQUE,
  vehiculoId INT NOT NULL,
  tipo VARCHAR(50) NOT NULL,
  fechaVencimiento DATE NOT NULL,
  estado VARCHAR(20) NOT NULL DEFAULT 'Vigente',
  rutaArchivo VARCHAR(255) NOT NULL,
  PRIMARY KEY (documentoId),
  FOREIGN KEY (vehiculoId) REFERENCES Vehiculo(vehiculoId)
);