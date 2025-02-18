-- MySQL dump 10.13  Distrib 9.2.0, for macos15.2 (arm64)
--
-- Host: 127.0.0.1    Database: flotilla
-- ------------------------------------------------------
-- Server version	8.4.3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Combustible`
--

DROP TABLE IF EXISTS `Combustible`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Combustible` (
  `idCombustible` int NOT NULL,
  `tipo` varchar(80) NOT NULL,
  `precioPorLitro` float NOT NULL,
  PRIMARY KEY (`idCombustible`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Combustible`
--

LOCK TABLES `Combustible` WRITE;
/*!40000 ALTER TABLE `Combustible` DISABLE KEYS */;
INSERT INTO `Combustible` VALUES (1,'Magna',24.79),(2,'Premium',25.55),(3,'Diesel',26.8);
/*!40000 ALTER TABLE `Combustible` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Conductor`
--

DROP TABLE IF EXISTS `Conductor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Conductor` (
  `nombre` varchar(80) NOT NULL,
  `licenciaVigente` tinyint(1) NOT NULL,
  `telefono` char(15) NOT NULL,
  `curp` varchar(20) NOT NULL,
  `disponibilidad` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`curp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Conductor`
--

LOCK TABLES `Conductor` WRITE;
/*!40000 ALTER TABLE `Conductor` DISABLE KEYS */;
INSERT INTO `Conductor` VALUES ('Antonio Cruz Rosas',1,'5590436712','CRRA040227HDFMZSA1',1),('Pedro Fuentes Herrera',0,'5553681243','FUHP040227HDFMZSA1',1),('Alejandro Gonzalez Cruz',1,'5546986133','GOCA040227HDFMZSA1',1),('Ruben Ruiz Diaz',1,'5546236512','RUDR040227HDFMZSA1',0),('Luis Torres Lopez',0,'5598683214','TOLL040227HDFMZSA1',1);
/*!40000 ALTER TABLE `Conductor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Mantenimiento`
--

DROP TABLE IF EXISTS `Mantenimiento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Mantenimiento` (
  `fecha` date NOT NULL,
  `costo` float NOT NULL,
  `idMantenimiento` int NOT NULL,
  `descripción` varchar(100) NOT NULL,
  `placa` varchar(15) NOT NULL,
  PRIMARY KEY (`idMantenimiento`),
  KEY `placa` (`placa`),
  CONSTRAINT `mantenimiento_ibfk_1` FOREIGN KEY (`placa`) REFERENCES `Vehículo` (`placa`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Mantenimiento`
--

LOCK TABLES `Mantenimiento` WRITE;
/*!40000 ALTER TABLE `Mantenimiento` DISABLE KEYS */;
INSERT INTO `Mantenimiento` VALUES ('2024-10-12',5000,1,'Servicio completo','AS12-AS3'),('2024-12-20',3000,2,'Servicio parcial','FDS32-12'),('2025-01-10',4000,3,'Servicio completo','FD3-45G'),('2024-08-29',3500,4,'Servicio parcial','FDL-42K'),('2025-02-01',4500,5,'Servicio completo','SDF-12'),('2025-03-10',4000,6,'Mantenimiento parcial','AS12-AS3'),('2025-01-12',5000,7,'Servicio completo','AS12-AS3'),('2025-01-12',5000,8,'Servicio completo','FDL-42K');
/*!40000 ALTER TABLE `Mantenimiento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Refaccion`
--

DROP TABLE IF EXISTS `Refaccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Refaccion` (
  `fecha` date NOT NULL,
  `idRefaccion` int NOT NULL,
  `placa` varchar(15) NOT NULL,
  `tipo` varchar(80) NOT NULL,
  `costo` float NOT NULL,
  PRIMARY KEY (`idRefaccion`),
  KEY `placa` (`placa`),
  CONSTRAINT `refaccion_ibfk_1` FOREIGN KEY (`placa`) REFERENCES `Vehículo` (`placa`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Refaccion`
--

LOCK TABLES `Refaccion` WRITE;
/*!40000 ALTER TABLE `Refaccion` DISABLE KEYS */;
INSERT INTO `Refaccion` VALUES ('2025-01-19',1,'AS12-AS3','Motor',20000),('2025-01-20',2,'FDS32-12','Valvulas',3000),('2025-01-18',3,'FD3-45G','Llantas',6000),('2025-01-10',4,'FDL-42K','Caja',10000),('2025-01-22',5,'SDF-12','Frenos',8000);
/*!40000 ALTER TABLE `Refaccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `resumenviaje`
--

DROP TABLE IF EXISTS `resumenviaje`;
/*!50001 DROP VIEW IF EXISTS `resumenviaje`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `resumenviaje` AS SELECT 
 1 AS `nombre`,
 1 AS `placa`,
 1 AS `idRuta`,
 1 AS `fecha`,
 1 AS `horaLlegada`,
 1 AS `horaSalida`,
 1 AS `destino`,
 1 AS `costo`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `Ruta`
--

DROP TABLE IF EXISTS `Ruta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Ruta` (
  `kilometraje` float NOT NULL,
  `destino` varchar(80) NOT NULL,
  `origen` varchar(80) NOT NULL,
  `fecha` date NOT NULL,
  `idRuta` int NOT NULL,
  `horaSalida` time NOT NULL,
  `horaLlegada` time NOT NULL,
  `placa` varchar(15) NOT NULL,
  `curp` varchar(20) NOT NULL,
  `costoViaje` float NOT NULL DEFAULT '0',
  PRIMARY KEY (`idRuta`),
  KEY `placa` (`placa`),
  KEY `curp` (`curp`),
  CONSTRAINT `ruta_ibfk_1` FOREIGN KEY (`placa`) REFERENCES `Vehículo` (`placa`),
  CONSTRAINT `ruta_ibfk_2` FOREIGN KEY (`curp`) REFERENCES `Conductor` (`curp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Ruta`
--

LOCK TABLES `Ruta` WRITE;
/*!40000 ALTER TABLE `Ruta` DISABLE KEYS */;
INSERT INTO `Ruta` VALUES (200,'Cuautitlan','Toreo','2025-02-07',1,'17:55:59','21:55:59','AS12-AS3','GOCA040227HDFMZSA1',247.9),(100,'Coapa','Toreo','2025-02-06',2,'14:31:45','15:55:59','FDS32-12','RUDR040227HDFMZSA1',141.944),(40,'Santa Fe','Toreo','2025-02-06',3,'13:55:12','14:55:59','FD3-45G','CRRA040227HDFMZSA1',67),(50,'Lomas Verdes','San Mateo','2025-02-08',4,'18:51:39','19:55:59','FDL-42K','GOCA040227HDFMZSA1',88.5357),(60,'Satelite','San Mateo','2025-02-08',5,'19:52:13','20:55:59','SDF-12','RUDR040227HDFMZSA1',102.2),(200,'Cuautitlan','Toreo','2025-02-07',6,'17:55:59','21:55:59','AS12-AS3','GOCA040227HDFMZSA1',247.9),(100,'Coapa','Toreo','2025-02-06',7,'14:31:45','15:55:59','FDS32-12','RUDR040227HDFMZSA1',141.944),(340,'Santa Fe','Toreo','2025-02-06',8,'13:55:12','14:55:59','FD3-45G','CRRA040227HDFMZSA1',569.5),(550,'Lomas Verdes','San Mateo','2025-02-08',9,'18:51:39','19:55:59','FDL-42K','GOCA040227HDFMZSA1',973.893),(460,'Satelite','San Mateo','2025-02-08',10,'19:52:13','20:55:59','SDF-12','RUDR040227HDFMZSA1',783.533),(200,'Cuautitlan','Toreo','2025-02-07',11,'17:55:59','21:55:59','SDF-12','GOCA040227HDFMZSA1',340.667),(100,'Coapa','Toreo','2025-02-06',12,'14:31:45','15:55:59','SDF-12','RUDR040227HDFMZSA1',170.333),(340,'Santa Fe','Toreo','2025-02-06',13,'13:55:12','14:55:59','SDF-12','CRRA040227HDFMZSA1',579.133),(550,'Lomas Verdes','San Mateo','2025-02-08',14,'18:51:39','19:55:59','SDF-12','GOCA040227HDFMZSA1',936.833),(200,'Cuautitlan','Toreo','2025-02-07',15,'17:55:59','21:55:59','AS12-AS3','GOCA040227HDFMZSA1',247.9),(460,'Satelite','San Mateo','2025-02-08',16,'19:52:13','20:55:59','SDF-12','RUDR040227HDFMZSA1',783.533);
/*!40000 ALTER TABLE `Ruta` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `costoViaje` BEFORE INSERT ON `ruta` FOR EACH ROW BEGIN
    DECLARE rendimiento FLOAT DEFAULT 0;
    DECLARE precioLitro FLOAT DEFAULT 0;
    DECLARE kilometros FLOAT DEFAULT 0;
    DECLARE vehiculo VARCHAR(15) DEFAULT NULL;
    DECLARE combustible INT DEFAULT NULL;
    SELECT idCombustible, rendimientoCombustible INTO combustible, rendimiento FROM Vehículo WHERE placa = NEW.placa;
    SELECT precioPorLitro INTO precioLitro FROM Combustible WHERE idCombustible = combustible;
    IF rendimiento > 0 THEN
        SET NEW.costoViaje = (NEW.kilometraje / rendimiento) * precioLitro;
    ELSE
        SET NEW.costoViaje = 0;
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `Vehículo`
--

DROP TABLE IF EXISTS `Vehículo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Vehículo` (
  `modelo` varchar(80) NOT NULL,
  `placa` varchar(15) NOT NULL,
  `año` year NOT NULL,
  `disponibilidad` tinyint(1) NOT NULL DEFAULT '1',
  `marca` varchar(80) NOT NULL,
  `seguro` varchar(80) NOT NULL,
  `idCombustible` int NOT NULL,
  `rendimientoCombustible` float DEFAULT '0',
  PRIMARY KEY (`placa`),
  KEY `idCombustible` (`idCombustible`),
  CONSTRAINT `vehículo_ibfk_1` FOREIGN KEY (`idCombustible`) REFERENCES `Combustible` (`idCombustible`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Vehículo`
--

LOCK TABLES `Vehículo` WRITE;
/*!40000 ALTER TABLE `Vehículo` DISABLE KEYS */;
INSERT INTO `Vehículo` VALUES ('Rifter','AS12-AS3',2020,1,'Peugeot','Qualitas',1,20),('Oroch','FD3-45G',2020,1,'Renault','GNP',3,16),('RAM 1200','FDL-42K',2023,1,'RAM','GNP',1,14),('Saveiro','FDS32-12',2021,1,'Volkswagen','Qualitas',2,18),('Rifter','SDF-12',2024,1,'Peugeot','Qualitas',2,15);
/*!40000 ALTER TABLE `Vehículo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Verificacion`
--

DROP TABLE IF EXISTS `Verificacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Verificacion` (
  `fecha` date NOT NULL,
  `idVerificacion` int NOT NULL,
  `placa` varchar(15) NOT NULL,
  PRIMARY KEY (`idVerificacion`),
  KEY `placa` (`placa`),
  CONSTRAINT `verificacion_ibfk_1` FOREIGN KEY (`placa`) REFERENCES `Vehículo` (`placa`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Verificacion`
--

LOCK TABLES `Verificacion` WRITE;
/*!40000 ALTER TABLE `Verificacion` DISABLE KEYS */;
INSERT INTO `Verificacion` VALUES ('2025-03-10',1,'AS12-AS3'),('2025-03-15',2,'FDS32-12'),('2025-03-20',3,'FD3-45G'),('2025-04-10',4,'FDL-42K'),('2025-10-20',5,'SDF-12');
/*!40000 ALTER TABLE `Verificacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `resumenviaje`
--

/*!50001 DROP VIEW IF EXISTS `resumenviaje`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `resumenviaje` AS select `C`.`nombre` AS `nombre`,`V`.`placa` AS `placa`,`R`.`idRuta` AS `idRuta`,`R`.`fecha` AS `fecha`,`R`.`horaLlegada` AS `horaLlegada`,`R`.`horaSalida` AS `horaSalida`,`R`.`destino` AS `destino`,`costoViaje`(`R`.`idRuta`) AS `costo` from ((`ruta` `R` join `vehículo` `V` on((`R`.`placa` = `V`.`placa`))) join `conductor` `C` on((`R`.`curp` = `C`.`curp`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-02-17 20:08:44
