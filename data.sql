-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: localhost    Database: imdb
-- ------------------------------------------------------
-- Server version	8.0.28

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
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'sha256$LDtDtf4i6MVoHGgx$85a2591a63b7d6bd88fde651a89ea0a0d21bd4e5cf3c349e7c1dbf87fc8d85cc');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movie`
--

DROP TABLE IF EXISTS `movie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movie` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(150) DEFAULT NULL,
  `genre` varchar(150) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `director` varchar(150) DEFAULT NULL,
  `actors` varchar(150) DEFAULT NULL,
  `year` int DEFAULT NULL,
  `runtime` int DEFAULT NULL,
  `rating` float DEFAULT NULL,
  `votes` int DEFAULT NULL,
  `image_path` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movie`
--

LOCK TABLES `movie` WRITE;
/*!40000 ALTER TABLE `movie` DISABLE KEYS */;
INSERT INTO `movie` VALUES (1,'Guardians of the Galaxy','Action,Adventure,Sci-Fi','A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe.','James Gunn','Chris Pratt, Vin Diesel, Bradley Cooper, Zoe Saldana',2014,121,8,757074,'./static/images/gotg.jpg'),(2,'John Wick','Action,Crime,Thriller','An ex-hitman comes out of retirement to track down the gangsters that took everything from him.','Chad Stahelski','Keanu Reeves, Michael Nyqvist, Alfie Allen, Willem Dafoe',2014,101,7.4,321933,'./static/images/johnwick.jpg'),(3,'Furious 7','Action,Crime,Thriller','Deckard Shaw seeks revenge against Dominic Toretto and his family for his comatose brother.','James Wan','Vin Diesel, Paul Walker, Dwayne Johnson, Jason Statham',2015,137,7.1,301249,'./static/images/f7.jpg'),(4,'Joker','Crime,Drama,Thriller','The rise of Arthur Fleck, from aspiring stand-up comedian and pariah to Gotham\'s clown prince and leader of the revolution.','Todd Phillips','Joaquin Phoenix, Robert De Niro, Zazie Beetz',2019,122,8.4,1325739,'./static/images/joker.jpg'),(5,'Squid Game','Action,Drama,Mystery','Hundreds of cash-strapped players accept a strange invitation to compete in children\'s games. Inside, a tempting prize awaits with deadly high stakes. A survival game that has a whopping 45.6 billion-won prize at stake.','Hwang Dong-hyuk','Lee Jung-jae, Park Hae-soo, Yasushi Iwaki',2021,55,8,476814,'./static/images/squid_game.jpg'),(6,'Avatar: The Way of Water','Action,Adventure,Fantasy','Jake Sully lives with his newfound family formed on the extrasolar moon Pandora. Once a familiar threat returns to finish what was previously started, Jake must work with Neytiri and the army of the Na\'vi race to protect their home.','James Cameron','Sam Worthington, Zoe Saldana, Sigourney Weaver',2022,192,7.7,378682,'./static/images/avatar.jpg'),(7,'Frozen','Animation,Adventure,Comedy','When the newly crowned Queen Elsa accidentally uses her power to turn things into ice to curse her home in infinite winter, her sister Anna teams up with a mountain man, his playful reindeer, and a snowman to change the weather condition.','Chris Buck, Jennifer Lee','Kristen Bell, Idina Menzel, Jonathan Groff',2013,102,7.4,639517,'./static/images/frozen.jpg'),(8,'Avengers: Endgame','Action,Adventure,Drama','After the devastating events of Avengers: Infinity War (2018), the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos\' actions and restore balance to the universe.','Anthony Russo, Joe Russo','Robert Downey Jr., Chris Evans, Mark Ruffalo',2019,181,8.4,1267388,'./static/images/avengers_endgame.jpg'),(9,'Spider-Man: No Way Home','Action,Adventure,Fantasy','With Spider-Man\'s identity now revealed, Peter asks Doctor Strange for help. When a spell goes wrong, dangerous foes from other worlds start to appear, forcing Peter to discover what it truly means to be Spider-Man.','Jon Watts','Tom Holland, Zendaya, Benedict Cumberbatch',2021,148,8.2,794502,'./static/images/spiderman_nwh.jpg'),(10,'Star Wars: The Force Awakens','Action,Adventure,Sci-Fi','As a new threat to the galaxy rises, Rey, a desert scavenger, and Finn, an ex-stormtrooper, must join Han Solo and Chewbacca to search for the one hope of restoring peace.','J.J. Abrams','Daisy Ridley, John Boyega, Oscar Isaac',2015,138,7.8,946826,'./static/images/starwars.jpg'),(11,'Jurassic World','Action,Adventure,Sci-Fi','A new theme park, built on the original site of Jurassic Park, creates a genetically modified hybrid dinosaur, the Indominus Rex, which escapes containment and goes on a killing spree.','Colin Trevorrow','Chris Pratt, Bryce Dallas Howard, Ty Simpkins',2015,124,6.9,656729,'./static/images/jurassicworld.jpg'),(12,'The Lion King','Animation,Adventure,Drama','After the murder of his father, a young lion prince flees his kingdom only to learn the true meaning of responsibility and bravery.','Jon Favreau','Donald Glover, Beyonce, Seth Rogen',2019,118,6.8,253647,'./static/images/lionking.jpg'),(13,'Black Panther','Action,Adventure,Sci-Fi','T\'Challa, heir to the hidden but advanced kingdom of Wakanda, must step forward to lead his people into a new future and must confront a challenger from his country\'s past.','Ryan Coogler','Chadwick Boseman, Michael B. Jordan, Lupita Nyong\'o',2018,134,7.3,801597,'./static/images/blackpanther.jpg'),(14,'It','Horror','In the summer of 1989, a group of bullied kids band together to destroy a shape-shifting monster, which disguises itself as a clown and preys on the children of Derry, their small Maine town.','Andy Muschietti','Bill Skarsgard, Jaeden Martell, Finn Wolfhard',2017,135,7.3,568237,'./static/images/it.jpg'),(15,'Skyfall','Action,Adventure,Thriller','James Bond\'s loyalty to M is tested when her past comes back to haunt her. When MI6 comes under attack, 007 must track down and destroy the threat, no matter how personal the cost.','Sam Mendes','Daniel Craig, Javier Bardem, Naomie Harris',2012,143,7.8,709558,'./static/images/skyfall.jpg'),(16,'Transformers: Dark of the Moon','Action,Adventure,Sci-Fi','The Autobots learn of a Cybertronian spacecraft hidden on the moon, and race against the Decepticons to reach it and to learn its secrets.','Michael Bay','Shia LaBeouf, Rosie Huntington-Whiteley, Tyrese Gibson',2011,154,6.2,417902,'./static/images/transformers_dotm.jpg');
/*!40000 ALTER TABLE `movie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `review`
--

DROP TABLE IF EXISTS `review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `review` (
  `user_id` int NOT NULL,
  `movie_id` int NOT NULL,
  `rating` float DEFAULT NULL,
  `comment` varchar(800) DEFAULT NULL,
  `likes` int DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`,`movie_id`),
  KEY `movie_id` (`movie_id`),
  CONSTRAINT `review_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `review_ibfk_2` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `review`
--

LOCK TABLES `review` WRITE;
/*!40000 ALTER TABLE `review` DISABLE KEYS */;
/*!40000 ALTER TABLE `review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(150) DEFAULT NULL,
  `password` varchar(150) DEFAULT NULL,
  `username` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'123@gmail.com','sha256$BvamceVgU6LkvRlI$e4078f4649438b3cff5e698fc2942e29fe6bc932e090458cfde255ad76dcbfd3','123');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `watched`
--

DROP TABLE IF EXISTS `watched`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `watched` (
  `user_id` int NOT NULL,
  `movie_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`movie_id`),
  KEY `movie_id` (`movie_id`),
  CONSTRAINT `watched_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `watched_ibfk_2` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `watched`
--

LOCK TABLES `watched` WRITE;
/*!40000 ALTER TABLE `watched` DISABLE KEYS */;
/*!40000 ALTER TABLE `watched` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `watchlist`
--

DROP TABLE IF EXISTS `watchlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `watchlist` (
  `user_id` int NOT NULL,
  `movie_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`movie_id`),
  KEY `movie_id` (`movie_id`),
  CONSTRAINT `watchlist_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `watchlist_ibfk_2` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `watchlist`
--

LOCK TABLES `watchlist` WRITE;
/*!40000 ALTER TABLE `watchlist` DISABLE KEYS */;
INSERT INTO `watchlist` VALUES (1,2),(1,5),(1,6);
/*!40000 ALTER TABLE `watchlist` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-23 23:45:34
