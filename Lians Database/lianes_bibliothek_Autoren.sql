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
-- Table structure for table `Autoren`
--

DROP TABLE IF EXISTS `Autoren`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Autoren` (
  `AutorID` int NOT NULL AUTO_INCREMENT,
  `Vorname` varchar(100) NOT NULL,
  `Nachname` varchar(100) NOT NULL,
  PRIMARY KEY (`AutorID`),
  UNIQUE KEY `Vorname` (`Vorname`,`Nachname`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Autoren`
--

LOCK TABLES `Autoren` WRITE;
/*!40000 ALTER TABLE `Autoren` DISABLE KEYS */;
INSERT INTO `Autoren` VALUES (25,'Agatha','Christie'),(23,'Andy','Weir'),(26,'Arthur','Conan Doyle'),(5,'Bernhard','Schlink'),(12,'Bram','Stoker'),(3,'Cornelia','Funke'),(28,'Dan','Brown'),(39,'Daniel','Glattauer'),(33,'Daniel','Kahneman'),(8,'Daniel','Kehlmann'),(18,'Douglas','Adams'),(37,'Ernest','Hemingway'),(19,'Frank','Herbert'),(1,'Franz','Kafka'),(7,'Friedrich','Dürrenmatt'),(20,'George','Orwell'),(40,'George R. R.','Martin'),(30,'Gillian','Flynn'),(36,'J. D.','Salinger'),(17,'J. K.','Rowling'),(16,'J. R. R.','Tolkien'),(38,'Jane','Austen'),(9,'Jostein','Gaarder'),(15,'Ken','Follett'),(24,'Margaret','Atwood'),(13,'Mary','Shelley'),(6,'Max','Frisch'),(2,'Michael','Ende'),(42,'Neil','Gaiman'),(4,'Patrick','Süskind'),(10,'Paulo','Coelho'),(21,'Ray','Bradbury'),(35,'Stephen','Dubner'),(32,'Stephen','Hawking'),(11,'Stephen','King'),(34,'Steven','Levitt'),(27,'Stieg','Larsson'),(41,'Terry','Pratchett'),(29,'Thomas','Harris'),(14,'Umberto','Eco'),(22,'William','Gibson'),(31,'Yuval Noah','Harari');
/*!40000 ALTER TABLE `Autoren` ENABLE KEYS */;
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
