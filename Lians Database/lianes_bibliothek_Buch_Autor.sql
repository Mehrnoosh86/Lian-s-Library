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
-- Table structure for table `Buch_Autor`
--

DROP TABLE IF EXISTS `Buch_Autor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Buch_Autor` (
  `BuchID` int NOT NULL,
  `AutorID` int NOT NULL,
  PRIMARY KEY (`BuchID`,`AutorID`),
  KEY `AutorID` (`AutorID`),
  CONSTRAINT `buch_autor_ibfk_1` FOREIGN KEY (`BuchID`) REFERENCES `Buecher` (`BuchID`) ON DELETE CASCADE,
  CONSTRAINT `buch_autor_ibfk_2` FOREIGN KEY (`AutorID`) REFERENCES `Autoren` (`AutorID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Buch_Autor`
--

LOCK TABLES `Buch_Autor` WRITE;
/*!40000 ALTER TABLE `Buch_Autor` DISABLE KEYS */;
INSERT INTO `Buch_Autor` VALUES (1,1),(2,1),(3,2),(4,2),(5,2),(6,3),(7,4),(8,5),(9,6),(10,7),(11,8),(12,9),(13,10),(14,11),(15,11),(16,12),(17,13),(18,14),(19,15),(20,16),(21,16),(22,17),(23,18),(51,18),(24,19),(25,20),(26,20),(27,21),(28,22),(29,23),(30,24),(31,25),(32,25),(33,26),(34,27),(35,28),(36,29),(37,30),(38,31),(42,31),(39,32),(40,33),(41,34),(41,35),(43,36),(44,37),(45,38),(46,39),(47,40),(48,41),(49,41),(49,42),(50,42);
/*!40000 ALTER TABLE `Buch_Autor` ENABLE KEYS */;
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
