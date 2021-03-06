-- MySQL dump 10.13  Distrib 8.0.13, for Win64 (x86_64)
--
-- Host: localhost    Database: stuadmin
-- ------------------------------------------------------
-- Server version	8.0.13

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `changes`
--

DROP TABLE IF EXISTS `changes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `changes` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `changess` char(4) NOT NULL,
  `recdate` date NOT NULL,
  `studentid` char(8) NOT NULL,
  PRIMARY KEY (`cid`),
  KEY `studentid` (`studentid`),
  CONSTRAINT `changes_ibfk_1` FOREIGN KEY (`studentid`) REFERENCES `student` (`studentid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `changes`
--

LOCK TABLES `changes` WRITE;
/*!40000 ALTER TABLE `changes` DISABLE KEYS */;
INSERT INTO `changes` VALUES (1,'绀轰緥绫诲瀷','2018-12-01','绀轰緥瀛﹀彿1');
/*!40000 ALTER TABLE `changes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class`
--

DROP TABLE IF EXISTS `class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `class` (
  `classid` char(6) NOT NULL,
  `classname` char(20) NOT NULL,
  `departid` char(2) NOT NULL,
  `begindate` date NOT NULL,
  `master` char(8) DEFAULT NULL,
  `mastertel` char(13) DEFAULT NULL,
  PRIMARY KEY (`classid`),
  KEY `departid` (`departid`),
  CONSTRAINT `class_ibfk_1` FOREIGN KEY (`departid`) REFERENCES `department` (`departid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class`
--

LOCK TABLES `class` WRITE;
/*!40000 ALTER TABLE `class` DISABLE KEYS */;
INSERT INTO `class` VALUES ('01','绀轰緥鐝骇鍚?','01','2018-12-01','绀轰緥鐝富浠?','00000000001');
/*!40000 ALTER TABLE `class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `department`
--

DROP TABLE IF EXISTS `department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `department` (
  `departid` char(2) NOT NULL,
  `departname` char(20) NOT NULL,
  `departhead` char(8) DEFAULT NULL,
  `telephone` char(13) DEFAULT NULL,
  PRIMARY KEY (`departid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `department`
--

LOCK TABLES `department` WRITE;
/*!40000 ALTER TABLE `department` DISABLE KEYS */;
INSERT INTO `department` VALUES ('01','绀轰緥闄㈢郴1','绀轰緥棰嗗1','绀轰緥鐢佃瘽1');
/*!40000 ALTER TABLE `department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `punish`
--

DROP TABLE IF EXISTS `punish`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `punish` (
  `pid` int(11) NOT NULL AUTO_INCREMENT,
  `studentid` char(8) NOT NULL,
  `punish` char(20) NOT NULL,
  `recdate` date NOT NULL,
  PRIMARY KEY (`pid`),
  KEY `studentid` (`studentid`),
  CONSTRAINT `punish_ibfk_1` FOREIGN KEY (`studentid`) REFERENCES `student` (`studentid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `punish`
--

LOCK TABLES `punish` WRITE;
/*!40000 ALTER TABLE `punish` DISABLE KEYS */;
INSERT INTO `punish` VALUES (1,'绀轰緥瀛﹀彿1','绀轰緥鎯╃綒绫诲瀷1','2018-12-01');
/*!40000 ALTER TABLE `punish` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reward`
--

DROP TABLE IF EXISTS `reward`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `reward` (
  `rid` int(11) NOT NULL AUTO_INCREMENT,
  `studentid` char(8) NOT NULL,
  `reward` char(20) NOT NULL,
  `recdate` date NOT NULL,
  PRIMARY KEY (`rid`),
  KEY `studentid` (`studentid`),
  CONSTRAINT `reward_ibfk_1` FOREIGN KEY (`studentid`) REFERENCES `student` (`studentid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reward`
--

LOCK TABLES `reward` WRITE;
/*!40000 ALTER TABLE `reward` DISABLE KEYS */;
INSERT INTO `reward` VALUES (1,'绀轰緥瀛﹀彿1','濂栧姳绫诲瀷','2018-12-01');
/*!40000 ALTER TABLE `reward` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `student` (
  `studentid` char(8) NOT NULL,
  `name` char(8) NOT NULL,
  `sex` char(2) NOT NULL,
  `classid` char(6) NOT NULL,
  `birthday` date DEFAULT NULL,
  `native` char(16) DEFAULT NULL,
  PRIMARY KEY (`studentid`),
  KEY `classid` (`classid`),
  CONSTRAINT `student_ibfk_1` FOREIGN KEY (`classid`) REFERENCES `class` (`classid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES ('绀轰緥瀛﹀彿1','濮撳悕1','濂?,'01','1999-01-01','绀轰緥绫嶈疮');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-12-07 10:21:20
