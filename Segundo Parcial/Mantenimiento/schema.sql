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
  FOREIGN KEY (flotillaId) REFERENCES Principal.Flotilla(flotillaId)
);

CREATE TABLE Mantenimiento
(
  mantenimientoId INT AUTO_INCREMENT UNIQUE,
  vehiculoId INT NOT NULL,
  fechaServicio DATE NOT NULL,
  tipoServicio VARCHAR(100) NOT NULL,
  descripcion VARCHAR(200) NOT NULL,
  costo DECIMAL(10,2) NOT NULL,
  estado VARCHAR(20) NOT NULL DEFAULT 'Completado',
  PRIMARY KEY (mantenimientoId),
  FOREIGN KEY (vehiculoId) REFERENCES Vehiculo(vehiculoId)
);

