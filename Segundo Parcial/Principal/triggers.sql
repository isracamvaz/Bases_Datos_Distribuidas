DELIMITER //
CREATE TRIGGER insertar_vehiculo
AFTER INSERT ON Vehiculo
FOR EACH ROW
BEGIN
    DECLARE vehiculoId, flotillaId, anio int;
    DECLARE tipo, modelo, marca varchar(50);
    DECLARE estado varchar(20) default 'Activo';
    DECLARE fechaVerificacion date;

    SET vehiculoId = NEW.vehiculoId;
    SET flotillaId = NEW.flotillaId;
    SET anio = NEW.anio;
    SET tipo = NEW.tipo;
    SET modelo = NEW.modelo;
    SET marca = NEW.marca;
    SET estado = NEW.estado;
    SET fechaVerificacion = NEW.fechaVerificacion;

    INSERT INTO mantenimiento.Vehiculo
    VALUES(vehiculoId,flotillaId,tipo,modelo,marca,anio,estado,fechaVerificacion);

    INSERT INTO rutas.Vehiculo
    VALUES(vehiculoId,flotillaId,tipo,modelo,marca,anio,estado,fechaVerificacion);
end //
DELIMITER ;


DELIMITER //
CREATE TRIGGER actualizar_vehiculo
AFTER UPDATE ON Vehiculo
FOR EACH ROW
BEGIN
    UPDATE mantenimiento.Vehiculo
    SET flotillaId = NEW.flotillaId,
        tipo = NEW.tipo,
        modelo = NEW.modelo,
        marca = NEW.marca,
        anio = NEW.anio,
        estado = NEW.estado,
        fechaVerificacion = NEW.fechaVerificacion
    WHERE vehiculoId = OLD.vehiculoId;

    UPDATE rutas.Vehiculo
    SET flotillaId = NEW.flotillaId,
        tipo = NEW.tipo,
        modelo = NEW.modelo,
        marca = NEW.marca,
        anio = NEW.anio,
        estado = NEW.estado,
        fechaVerificacion = NEW.fechaVerificacion
    WHERE vehiculoId = OLD.vehiculoId;
END //
DELIMITER ;


DELIMITER //
CREATE TRIGGER eliminar_vehiculo
AFTER DELETE ON Vehiculo
FOR EACH ROW
BEGIN
    DELETE FROM mantenimiento.Vehiculo
    WHERE vehiculoId = OLD.vehiculoId;

    DELETE FROM rutas.Vehiculo
    WHERE vehiculoId = OLD.vehiculoId;
END //
DELIMITER ;

