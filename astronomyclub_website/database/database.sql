-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: astroclub
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `member2research`
--

DROP TABLE IF EXISTS `member2research`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member2research` (
  `MemberID` int NOT NULL,
  `researchID` int NOT NULL,
  PRIMARY KEY (`MemberID`,`researchID`),
  KEY `member2research_ibfk_2` (`researchID`),
  CONSTRAINT `member2research_ibfk_1` FOREIGN KEY (`MemberID`) REFERENCES `members` (`MemberID`) ON DELETE CASCADE,
  CONSTRAINT `member2research_ibfk_2` FOREIGN KEY (`researchID`) REFERENCES `research` (`ResearchID`) ON DELETE CASCADE,
  CONSTRAINT `member2research_ibfk_3` FOREIGN KEY (`MemberID`) REFERENCES `members` (`MemberID`),
  CONSTRAINT `member2research_ibfk_4` FOREIGN KEY (`researchID`) REFERENCES `research` (`ResearchID`),
  CONSTRAINT `member2research_ibfk_5` FOREIGN KEY (`MemberID`) REFERENCES `members` (`MemberID`),
  CONSTRAINT `member2research_ibfk_6` FOREIGN KEY (`researchID`) REFERENCES `research` (`ResearchID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member2research`
--

LOCK TABLES `member2research` WRITE;
/*!40000 ALTER TABLE `member2research` DISABLE KEYS */;
INSERT INTO `member2research` VALUES (7,22);
/*!40000 ALTER TABLE `member2research` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `members`
--

DROP TABLE IF EXISTS `members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `members` (
  `MemberID` int NOT NULL,
  `MemberName` varchar(45) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `joinDate` date DEFAULT NULL,
  `Privilege` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`MemberID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `members`
--

LOCK TABLES `members` WRITE;
/*!40000 ALTER TABLE `members` DISABLE KEYS */;
INSERT INTO `members` VALUES (5,'marah','eve.martinez@example.com','2022-05-30','normal'),(7,'leen','leenanas778@gmail.com','2025-01-01','admin'),(10,'tasneem','tasneem778@gmail.com','2025-01-09','admin'),(11,'duha','duha666@gmail.com','2025-01-10','admin');
/*!40000 ALTER TABLE `members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `photo`
--

DROP TABLE IF EXISTS `photo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `photo` (
  `PhotoID` int NOT NULL,
  `Title` varchar(45) DEFAULT NULL,
  `photoURL` varchar(200) DEFAULT NULL,
  `DateTaken` date DEFAULT NULL,
  `resolution` varchar(45) DEFAULT NULL,
  `skyData` varchar(45) DEFAULT NULL,
  `TelescopeID` int DEFAULT NULL,
  PRIMARY KEY (`PhotoID`),
  KEY `TelescopeID_idx` (`TelescopeID`),
  CONSTRAINT `fk_photo_telescope` FOREIGN KEY (`TelescopeID`) REFERENCES `telescopes` (`TelescopeID`) ON DELETE SET NULL,
  CONSTRAINT `photo_ibfk_1` FOREIGN KEY (`TelescopeID`) REFERENCES `telescopes` (`TelescopeID`),
  CONSTRAINT `photo_ibfk_2` FOREIGN KEY (`TelescopeID`) REFERENCES `telescopes` (`TelescopeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `photo`
--

LOCK TABLES `photo` WRITE;
/*!40000 ALTER TABLE `photo` DISABLE KEYS */;
INSERT INTO `photo` VALUES (2,'C/2023 A3','static/assets/images/uploads/photo/2.jpg','2024-10-15','919x625','2.0 arcsec',2),(3,'polar star','static/assets/images/uploads/photo/3.jpg','2025-01-01','1024x682','1.1 arcsec',1),(5,'hh','static/assets/images/uploads/photo/5.jpg','2025-01-15','919x625','1.1 arcsec',1),(6,'IC 1396A','static/assets/images/uploads/photo/6.jpg','2025-01-09','950x670','1.1 arcsec',1);
/*!40000 ALTER TABLE `photo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `research`
--

DROP TABLE IF EXISTS `research`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `research` (
  `ResearchID` int NOT NULL,
  `Title` varchar(45) DEFAULT NULL,
  `summary` varchar(200) DEFAULT NULL,
  `FileURL` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ResearchID`),
  KEY `ResearchID_idx` (`ResearchID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `research`
--

LOCK TABLES `research` WRITE;
/*!40000 ALTER TABLE `research` DISABLE KEYS */;
INSERT INTO `research` VALUES (1,'Hyperbolic Meteoroids Impacting the Moon','talks about the Hyperbolic Meteoroids Impacting the Moon','static/assets/pdfs/1.pdf'),(2,'Hydropower\'s hidden ','Hydropower’s hidden transformation of rivers in the Mekong','static/assets/pdfs/2.pdf'),(3,'moon phases','talks about all the phases of the moon together','static/assets/pdfs/3.pdf'),(22,'moon','moon phases','static/assets/pdfs/22.pdf');
/*!40000 ALTER TABLE `research` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resources`
--

DROP TABLE IF EXISTS `resources`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resources` (
  `resourceID` int NOT NULL,
  `resourceName` varchar(45) DEFAULT NULL,
  `URL` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`resourceID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resources`
--

LOCK TABLES `resources` WRITE;
/*!40000 ALTER TABLE `resources` DISABLE KEYS */;
INSERT INTO `resources` VALUES (1,'Nasa','https://www.nasa.gov/astronomy/'),(2,'nasa3333333333','https://www.nasa.gov/astronomy/'),(12,'Nasa','https://www.nasa.gov/astronomy/'),(13,'Nasa','https://www.nasa.gov/astronomy/'),(123,'nasa2','https://www.nasa.gov/astronomy/'),(1111,'Nasa','https://www.nasa.gov/astronomy/');
/*!40000 ALTER TABLE `resources` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `telescopes`
--

DROP TABLE IF EXISTS `telescopes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `telescopes` (
  `TelescopeID` int NOT NULL,
  `TheName` varchar(45) DEFAULT NULL,
  `Thecondition` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`TelescopeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `telescopes`
--

LOCK TABLES `telescopes` WRITE;
/*!40000 ALTER TABLE `telescopes` DISABLE KEYS */;
INSERT INTO `telescopes` VALUES (1,'Hubble Telescope','Operational'),(2,'The largest telescope in palestine','usable');
/*!40000 ALTER TABLE `telescopes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `theevents`
--

DROP TABLE IF EXISTS `theevents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `theevents` (
  `EventID` int NOT NULL,
  `EventName` varchar(45) DEFAULT NULL,
  `TheDate` date DEFAULT NULL,
  `numberOFPeople` int DEFAULT NULL,
  `location` varchar(45) DEFAULT NULL,
  `startTime` time DEFAULT NULL,
  `endTime` time DEFAULT NULL,
  `PhotoURL` varchar(200) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`EventID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `theevents`
--

LOCK TABLES `theevents` WRITE;
/*!40000 ALTER TABLE `theevents` DISABLE KEYS */;
INSERT INTO `theevents` VALUES (1,'the fish moon','2025-01-21',300,'tarbeh','20:02:00','22:02:00','static/assets/images/uploads/theevents/1.jpg','we will see a very special phase for the moon'),(2,'stars','2025-01-23',33,'tarbeh','18:00:00','22:00:00','static/assets/images/uploads/theevents/2.jpg','stargazing'),(3,'sky','2024-01-30',33,'tarbeh','19:04:00','21:05:00','static/assets/images/uploads/theevents/3.jpg','stargazing');
/*!40000 ALTER TABLE `theevents` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-07  1:54:08
