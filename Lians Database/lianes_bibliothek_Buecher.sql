-- MySQL dump 10.13  Distrib 8.0.46, for macos15 (arm64)
--
-- Host: localhost    Database: lianes_bibliothek
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Buecher`
--

DROP TABLE IF EXISTS `Buecher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Buecher` (
  `BuchID` int NOT NULL AUTO_INCREMENT,
  `ISBN` varchar(13) DEFAULT NULL,
  `Titel` varchar(255) NOT NULL,
  `GenreID` int NOT NULL,
  `StandortID` int NOT NULL,
  `Verleihbar` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`BuchID`),
  UNIQUE KEY `ISBN` (`ISBN`),
  KEY `GenreID` (`GenreID`),
  KEY `StandortID` (`StandortID`),
  CONSTRAINT `buecher_ibfk_1` FOREIGN KEY (`GenreID`) REFERENCES `Genres` (`GenreID`),
  CONSTRAINT `buecher_ibfk_2` FOREIGN KEY (`StandortID`) REFERENCES `Standorte` (`StandortID`),
  CONSTRAINT `buecher_chk_1` CHECK ((`Verleihbar` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Buecher`
--

LOCK TABLES `Buecher` WRITE;
/*!40000 ALTER TABLE `Buecher` DISABLE KEYS */;
INSERT INTO `Buecher` VALUES (1,'9783900000011','Die Verwandlung',2,1,1),(2,'9783900000028','Der Prozess',2,1,1),(3,'9783900000035','Momo',3,2,1),(4,'9783900000042','Die unendliche Geschichte',3,2,1),(5,'9783900000059','Jim Knopf und Lukas der Lokomotivführer',3,2,1),(6,'9783900000066','Tintenherz',3,2,1),(7,'9783900000073','Das Parfum',5,4,1),(8,'9783900000080','Der Vorleser',1,1,1),(9,'9783900000097','Homo Faber',1,1,1),(10,'9783900000103','Die Physiker',2,1,1),(11,'9783900000110','Die Vermessung der Welt',8,2,1),(12,'9783900000127','Sophies Welt',1,1,1),(13,'9783900000134','Der Alchimist',1,1,1),(14,'9783900000141','Es',5,4,1),(15,'9783900000158','Shining',5,4,1),(16,'9783900000165','Dracula',5,4,1),(17,'9783900000172','Frankenstein',5,4,1),(18,'9783900000189','Der Name der Rose',8,2,1),(19,'9783900000196','Die Säulen der Erde',8,2,1),(20,'9783900000202','Der Herr der Ringe',3,2,0),(21,'9783900000219','Der Hobbit',3,2,1),(22,'9783900000226','Harry Potter und der Stein der Weisen',3,2,1),(23,'9783900000233','Per Anhalter durch die Galaxis',6,2,1),(24,'9783900000240','Dune – Der Wüstenplanet',6,2,0),(25,'9783900000257','1984',6,2,1),(26,'9783900000264','Farm der Tiere',2,1,1),(27,'9783900000271','Fahrenheit 451',6,2,1),(28,'9783900000288','Neuromancer',6,2,1),(29,'9783900000295','Der Marsianer',6,2,1),(30,'9783900000301','Der Report der Magd',6,2,1),(31,'9783900000318','Mord im Orient-Express',4,1,1),(32,'9783900000325','Und dann gab\'s keines mehr',4,1,1),(33,'9783900000332','Der Hund der Baskervilles',4,1,1),(34,'9783900000349','Verblendung',4,1,1),(35,'9783900000356','Sakrileg',4,1,1),(36,'9783900000363','Das Schweigen der Lämmer',4,1,1),(37,'9783900000370','Gone Girl',4,1,1),(38,'9783900000387','Eine kurze Geschichte der Menschheit',7,3,1),(39,'9783900000394','Eine kurze Geschichte der Zeit',7,3,0),(40,'9783900000400','Schnelles Denken, langsames Denken',7,3,1),(41,'9783900000417','Freakonomics',7,3,1),(42,'9783900000424','Homo Deus',7,3,1),(43,'9783900000431','Der Fänger im Roggen',2,1,1),(44,'9783900000448','Der alte Mann und das Meer',2,1,1),(45,'9783900000455','Stolz und Vorurteil',2,1,1),(46,'9783900000462','Gut gegen Nordwind',1,1,1),(47,'9783900000479','Das Lied von Eis und Feuer',3,2,1),(48,'9783900000486','Die Farben der Magie',3,2,1),(49,'9783900000493','Ein gutes Omen',3,2,1),(50,'9783900000509','Der Ozean am Ende der Straße',3,2,1),(51,'121232345','book mehrnoosh test',4,1,1);
/*!40000 ALTER TABLE `Buecher` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-16  9:53:18
