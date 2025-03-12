SELECT v.modelo, v.estado, v.tipo, r.ubicacionInicio, r.ubicacionFin, r.estado
FROM principal.Vehiculo v
JOIN rutas.Ruta r ON v.vehiculoId = r.vehiculoId;


SELECT v.modelo, v.estado, v.tipo, m.fechaServicio, m.tipoServicio, m.costo
FROM principal.Vehiculo v
JOIN mantenimiento.Mantenimiento m ON v.vehiculoId = m.vehiculoId;