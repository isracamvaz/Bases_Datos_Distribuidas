DELIMITER //
CREATE PROCEDURE ObtenerRutasPorVehiculo(IN vehiculoId INT)
BEGIN
    SELECT *
    FROM rutas.Ruta
    WHERE rutas.Ruta.vehiculoId = vehiculoId;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE ContarMantenimientosPorVehiculo(IN vehiculoId INT, OUT total INT)
BEGIN
    SELECT COUNT(*) INTO total FROM mantenimiento.Mantenimiento WHERE mantenimiento.Mantenimiento.vehiculoId = vehiculoId;
END //
DELIMITER ;

call ObtenerRutasPorVehiculo(2);

call ContarMantenimientosPorVehiculo(2, @total);
select @total;


