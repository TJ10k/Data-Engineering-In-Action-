CREATE DATABASE  IF NOT EXISTS `creditcard_capstone` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `creditcard_capstone`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: creditcard_capstone
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `cdw_sapp_branch`
--

DROP TABLE IF EXISTS `cdw_sapp_branch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cdw_sapp_branch` (
  `BRANCH_CODE` int NOT NULL,
  `BRANCH_NAME` varchar(255) DEFAULT NULL,
  `BRANCH_STREET` varchar(255) DEFAULT NULL,
  `BRANCH_CITY` varchar(255) DEFAULT NULL,
  `BRANCH_STATE` varchar(255) DEFAULT NULL,
  `BRANCH_ZIP` varchar(9) DEFAULT NULL,
  `BRANCH_PHONE` varchar(20) DEFAULT NULL,
  `LAST_UPDATED` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`BRANCH_CODE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cdw_sapp_credit_card`
--

DROP TABLE IF EXISTS `cdw_sapp_credit_card`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cdw_sapp_credit_card` (
  `CREDIT_CARD_NO` varchar(255) DEFAULT NULL,
  `TIMEID` varchar(20) DEFAULT NULL,
  `CUST_SSN` varchar(11) NOT NULL,
  `BRANCH_CODE` int DEFAULT NULL,
  `TRANSACTION_TYPE` varchar(50) DEFAULT NULL,
  `TRANSACTION_VALUE` double DEFAULT NULL,
  `TRANSACTION_ID` int NOT NULL,
  PRIMARY KEY (`TRANSACTION_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cdw_sapp_customer`
--

DROP TABLE IF EXISTS `cdw_sapp_customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cdw_sapp_customer` (
  `SSN` int NOT NULL,
  `FIRST_NAME` varchar(50) NOT NULL,
  `MIDDLE_NAME` varchar(50) DEFAULT NULL,
  `LAST_NAME` varchar(50) NOT NULL,
  `CREDIT_CARD_NO` varchar(20) NOT NULL,
  `FULL_STREET_ADDRESS` varchar(100) DEFAULT NULL,
  `CUST_CITY` varchar(50) NOT NULL,
  `CUST_STATE` varchar(50) NOT NULL,
  `CUST_COUNTRY` varchar(50) NOT NULL,
  `CUST_ZIP` varchar(20) NOT NULL,
  `CUST_PHONE` varchar(20) NOT NULL,
  `CUST_EMAIL` varchar(100) NOT NULL,
  `LAST_UPDATED` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`SSN`),
  UNIQUE KEY `CREDIT_CARD_NO` (`CREDIT_CARD_NO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cdw_sapp_loan_application`
--

DROP TABLE IF EXISTS `cdw_sapp_loan_application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cdw_sapp_loan_application` (
  `Application_ID` varchar(50) NOT NULL,
  `Application_Status` varchar(20) DEFAULT NULL,
  `Credit_History` float DEFAULT NULL,
  `Dependents` varchar(10) DEFAULT NULL,
  `Education` varchar(50) DEFAULT NULL,
  `Gender` varchar(10) DEFAULT NULL,
  `Income` varchar(20) DEFAULT NULL,
  `Married` varchar(10) DEFAULT NULL,
  `Property_Area` varchar(50) DEFAULT NULL,
  `Self_Employed` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`Application_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-06 13:51:32
