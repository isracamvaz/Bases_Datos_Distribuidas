LOAD DATA INFILE '/tmp/Flotilla.txt'
INTO TABLE Flotilla
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';

LOAD DATA INFILE '/tmp/carro.txt'
INTO TABLE Vehiculo
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';

LOAD DATA INFILE '/tmp/Documento1.txt'
INTO TABLE Documento
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';

