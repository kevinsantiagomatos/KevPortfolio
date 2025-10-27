-- MySQL dump 10.13  Distrib 8.0.40, for macos14 (arm64)
--
-- Host: localhost    Database: lucky_lures
-- ------------------------------------------------------
-- Server version	9.3.0

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
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `product_id` varchar(15) NOT NULL,
  `name` varchar(45) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `description` text NOT NULL,
  `brand` enum('Abu Garcia','Blue Fox','Daiwa','Rapala','Salmo','Shimano','Westin') NOT NULL,
  `stock` int NOT NULL,
  `cost` decimal(10,2) NOT NULL,
  `status` enum('Active','Inactive') NOT NULL DEFAULT 'Active',
  `material` enum('Stainless Steel','Metal','Plastic','Polycarbonate') NOT NULL,
  `buoyancy` enum('Floats','Sinks') NOT NULL,
  `weight` decimal(10,2) NOT NULL,
  `length` decimal(10,2) NOT NULL,
  `hooks` int NOT NULL,
  `color` enum('Red','Yellow','Blue','Black','White','Orange','Green','Purple','Pink','Copper','Silver') NOT NULL,
  `image` varchar(50) NOT NULL,
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`product_id`),
  UNIQUE KEY `product_id_UNIQUE` (`product_id`),
  KEY `fk_products_category` (`category_id`),
  CONSTRAINT `fk_products_category` FOREIGN KEY (`category_id`) REFERENCES `category` (`category_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES ('banwalleye','Bandit Walleye',6.99,'very good lure yes','Abu Garcia',10,3.87,'Inactive','Metal','Floats',4.50,7.50,3,'Purple','bandit_walleye.webp',1),('berchoppo','Berkley Choppo',4.55,'description here','Rapala',96,1.99,'Inactive','Metal','Sinks',8.00,7.00,2,'White','berkley_choppo.jpeg',2),('daiwaprorexmet','Daiwa Prorex Metal Vibe',5.99,'description 100% real','Daiwa',23,2.35,'Inactive','Metal','Sinks',8.00,3.40,2,'Blue','prorex_metal_vibe_blue_metallic.jpg',2),('prorexmetvib','Daiwa Prorex Metal Vibe',10.00,'Vibrating lures belong to the most successful lures for perch and asp at the moment – next to enormous casting distances, they offer various Prorex presentation strategies to convince even suspicious fish. The small Metal Vibe provides an excellent action with strong vibrations, which can be feltill the rod tip.','Daiwa',33,5.00,'Active','Metal','Sinks',10.00,4.30,2,'Pink','prorex_metal_vibe_pink_iwashi_1.jpg',1),('rpopr','Rebel Pop R',10.99,'description here','Salmo',1,4.20,'Inactive','Stainless Steel','Sinks',5.00,6.00,1,'Green','rebel_pop_r.png',3);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-15  0:29:06
