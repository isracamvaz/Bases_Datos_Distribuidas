CREATE TABLE Conductor
(
  conductorId INT AUTO_INCREMENT UNIQUE,
  nombre VARCHAR(100) NOT NULL,
  numeroLicencia VARCHAR(50) NOT NULL,
  vencimientoLicencia DATE NOT NULL,
  estado VARCHAR(20) NOT NULL DEFAULT 'Activo',
  PRIMARY KEY (conductorId)
);

CREATE TABLE Ruta
(
  rutaId INT AUTO_INCREMENT UNIQUE,
  vehiculoId INT NOT NULL,
  conductorId INT NOT NULL,
  horaInicio DATETIME NOT NULL,
  horaFin DATETIME NOT NULL,
  distancia DECIMAL(10,2) NOT NULL,
  ubicacionInicio VARCHAR(100) NOT NULL,
  ubicacionFin VARCHAR(100) NOT NULL,
  estado VARCHAR(20) NOT NULL DEFAULT 'Pendiente',
  PRIMARY KEY (rutaId),
  FOREIGN KEY (vehiculoId) REFERENCES Vehiculo(vehiculoId),
  FOREIGN KEY (conductorId) REFERENCES Conductor(conductorId)
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
  FOREIGN KEY (flotillaId) REFERENCES Principal.Flotilla(flotillaId)
);


CREATE TABLE TransaccionCombustible
(
  transaccionId INT AUTO_INCREMENT UNIQUE,
  vehiculoId INT NOT NULL,
  conductorId INT NOT NULL,
  monto DECIMAL(10,2) NOT NULL,
  cantidad DECIMAL(10,2) NOT NULL,
  tipoCombustible VARCHAR(20) NOT NULL,
  fechaTransaccion DATETIME NOT NULL,
  ubicacion VARCHAR(100) NOT NULL,
  PRIMARY KEY (transaccionId),
  FOREIGN KEY (vehiculoId) REFERENCES Vehiculo(vehiculoId),
  FOREIGN KEY (conductorId) REFERENCES Conductor (conductorId)
);