-- MySQL dump 10.18  Distrib 10.3.27-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: keadb
-- ------------------------------------------------------
-- Server version	10.3.27-MariaDB-0+deb10u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `dhcp4_audit`
--

DROP TABLE IF EXISTS `dhcp4_audit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp4_audit` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `object_type` varchar(256) NOT NULL,
  `object_id` bigint(20) unsigned NOT NULL,
  `modification_type` tinyint(1) NOT NULL,
  `revision_id` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_dhcp4_audit_modification_type` (`modification_type`),
  KEY `fk_dhcp4_audit_revision` (`revision_id`),
  CONSTRAINT `fk_dhcp4_audit_modification_type` FOREIGN KEY (`modification_type`) REFERENCES `modification` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_dhcp4_audit_revision` FOREIGN KEY (`revision_id`) REFERENCES `dhcp4_audit_revision` (`id`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp4_audit`
--

LOCK TABLES `dhcp4_audit` WRITE;
/*!40000 ALTER TABLE `dhcp4_audit` DISABLE KEYS */;
INSERT INTO `dhcp4_audit` VALUES (1,'dhcp4_server',2,0,1),(2,'dhcp4_subnet',2,0,2),(3,'dhcp4_shared_network',1,0,4),(4,'dhcp4_global_parameter',1,0,5),(5,'dhcp4_options',4,0,6),(6,'dhcp4_option_def',1,0,7);
/*!40000 ALTER TABLE `dhcp4_audit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dhcp4_audit_revision`
--

DROP TABLE IF EXISTS `dhcp4_audit_revision`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp4_audit_revision` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `modification_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `log_message` text DEFAULT NULL,
  `server_id` bigint(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `key_dhcp4_audit_revision_by_modification_ts` (`modification_ts`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp4_audit_revision`
--

LOCK TABLES `dhcp4_audit_revision` WRITE;
/*!40000 ALTER TABLE `dhcp4_audit_revision` DISABLE KEYS */;
INSERT INTO `dhcp4_audit_revision` VALUES (1,'2021-02-17 13:13:01','server set',1),(2,'2021-02-17 13:13:01','subnet set',2),(3,'2021-02-17 13:13:01','subnet specific option set',2),(4,'2021-02-17 13:13:01','shared network set',2),(5,'2021-02-17 13:13:01','global parameter set',2),(6,'2021-02-17 13:13:01','global option set',2),(7,'2021-02-17 13:13:01','option definition set',2);
/*!40000 ALTER TABLE `dhcp4_audit_revision` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dhcp4_global_parameter`
--

DROP TABLE IF EXISTS `dhcp4_global_parameter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp4_global_parameter` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `value` longtext NOT NULL,
  `modification_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `parameter_type` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `key_dhcp4_global_parameter_modification_ts` (`modification_ts`),
  KEY `key_dhcp4_global_parameter_name` (`name`),
  KEY `fk_dhcp4_global_parameter_type` (`parameter_type`),
  CONSTRAINT `fk_dhcp4_global_parameter_type` FOREIGN KEY (`parameter_type`) REFERENCES `parameter_data_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp4_global_parameter`
--

LOCK TABLES `dhcp4_global_parameter` WRITE;
/*!40000 ALTER TABLE `dhcp4_global_parameter` DISABLE KEYS */;
INSERT INTO `dhcp4_global_parameter` VALUES (1,'boot-file-name','/dev/null','2021-02-17 13:13:01',4);
/*!40000 ALTER TABLE `dhcp4_global_parameter` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp4_global_parameter_AINS AFTER INSERT ON dhcp4_global_parameter
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP4('dhcp4_global_parameter', NEW.id, "create");
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp4_global_parameter_AUPD AFTER UPDATE ON dhcp4_global_parameter
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP4('dhcp4_global_parameter', NEW.id, "update");
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp4_global_parameter_ADEL AFTER DELETE ON dhcp4_global_parameter
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP4('dhcp4_global_parameter', OLD.id, "delete");
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `dhcp4_global_parameter_server`
--

DROP TABLE IF EXISTS `dhcp4_global_parameter_server`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp4_global_parameter_server` (
  `parameter_id` bigint(20) unsigned NOT NULL,
  `server_id` bigint(20) unsigned NOT NULL,
  `modification_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`parameter_id`,`server_id`),
  KEY `fk_dhcp4_global_parameter_server_server_id` (`server_id`),
  KEY `key_dhcp4_global_parameter_server` (`modification_ts`),
  CONSTRAINT `fk_dhcp4_global_parameter_server_parameter_id` FOREIGN KEY (`parameter_id`) REFERENCES `dhcp4_global_parameter` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `fk_dhcp4_global_parameter_server_server_id` FOREIGN KEY (`server_id`) REFERENCES `dhcp4_server` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp4_global_parameter_server`
--

LOCK TABLES `dhcp4_global_parameter_server` WRITE;
/*!40000 ALTER TABLE `dhcp4_global_parameter_server` DISABLE KEYS */;
INSERT INTO `dhcp4_global_parameter_server` VALUES (1,2,'2021-02-17 13:13:01');
/*!40000 ALTER TABLE `dhcp4_global_parameter_server` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dhcp4_option_def`
--

DROP TABLE IF EXISTS `dhcp4_option_def`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp4_option_def` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `code` smallint(5) unsigned NOT NULL,
  `name` varchar(128) NOT NULL,
  `space` varchar(128) NOT NULL,
  `type` tinyint(3) unsigned NOT NULL,
  `modification_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `is_array` tinyint(1) NOT NULL,
  `encapsulate` varchar(128) NOT NULL,
  `record_types` varchar(512) DEFAULT NULL,
  `user_context` longtext DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `key_dhcp4_option_def_modification_ts` (`modification_ts`),
  KEY `key_dhcp4_option_def_code_space` (`code`,`space`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp4_option_def`
--

LOCK TABLES `dhcp4_option_def` WRITE;
/*!40000 ALTER TABLE `dhcp4_option_def` DISABLE KEYS */;
INSERT INTO `dhcp4_option_def` VALUES (1,222,'foo','dhcp4',8,'2021-02-17 13:13:01',0,'',NULL,NULL);
/*!40000 ALTER TABLE `dhcp4_option_def` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp4_option_def_AINS AFTER INSERT ON dhcp4_option_def
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP4('dhcp4_option_def', NEW.id, "create");
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp4_option_def_AUPD AFTER UPDATE ON dhcp4_option_def
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP4('dhcp4_option_def', NEW.id, "update");
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp4_option_def_ADEL AFTER DELETE ON dhcp4_option_def
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP4('dhcp4_option_def', OLD.id, "delete");
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `dhcp4_option_def_server`
--

DROP TABLE IF EXISTS `dhcp4_option_def_server`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp4_option_def_server` (
  `option_def_id` bigint(20) unsigned NOT NULL,
  `server_id` bigint(20) unsigned NOT NULL,
  `modification_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`option_def_id`,`server_id`),
  KEY `fk_dhcp4_option_def_server_server_id_idx` (`server_id`),
  KEY `key_dhcp4_option_def_server_modification_ts` (`modification_ts`),
  CONSTRAINT `fk_dhcp4_option_def_server_option_def_id` FOREIGN KEY (`option_def_id`) REFERENCES `dhcp4_option_def` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `fk_dhcp4_option_def_server_server_id` FOREIGN KEY (`server_id`) REFERENCES `dhcp4_server` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp4_option_def_server`
--

LOCK TABLES `dhcp4_option_def_server` WRITE;
/*!40000 ALTER TABLE `dhcp4_option_def_server` DISABLE KEYS */;
INSERT INTO `dhcp4_option_def_server` VALUES (1,2,'2021-02-17 13:13:01');
/*!40000 ALTER TABLE `dhcp4_option_def_server` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dhcp4_options`
--

DROP TABLE IF EXISTS `dhcp4_options`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp4_options` (
  `option_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `code` tinyint(3) unsigned NOT NULL,
  `value` blob DEFAULT NULL,
  `formatted_value` text DEFAULT NULL,
  `space` varchar(128) DEFAULT NULL,
  `persistent` tinyint(1) NOT NULL DEFAULT 0,
  `dhcp_client_class` varchar(128) DEFAULT NULL,
  `dhcp4_subnet_id` int(10) unsigned DEFAULT NULL,
  `host_id` int(10) unsigned DEFAULT NULL,
  `scope_id` tinyint(3) unsigned NOT NULL,
  `user_context` text DEFAULT NULL,
  `shared_network_name` varchar(128) DEFAULT NULL,
  `pool_id` bigint(20) unsigned DEFAULT NULL,
  `modification_ts` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`option_id`),
  UNIQUE KEY `option_id_UNIQUE` (`option_id`),
  KEY `fk_options_host1_idx` (`host_id`),
  KEY `fk_dhcp4_option_scope` (`scope_id`),
  CONSTRAINT `fk_dhcp4_option_scope` FOREIGN KEY (`scope_id`) REFERENCES `dhcp_option_scope` (`scope_id`),
  CONSTRAINT `fk_options_host1` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp4_options`
--

LOCK TABLES `dhcp4_options` WRITE;
/*!40000 ALTER TABLE `dhcp4_options` DISABLE KEYS */;
INSERT INTO `dhcp4_options` VALUES (1,6,NULL,'192.0.2.2','dhcp4',1,NULL,NULL,NULL,5,NULL,NULL,1,'2021-02-17 13:13:01'),(2,6,NULL,'192.0.2.1','dhcp4',1,NULL,2,NULL,1,NULL,NULL,NULL,'2021-02-17 13:13:01'),(3,6,NULL,'192.0.2.1','dhcp4',1,NULL,NULL,NULL,4,NULL,'net1',NULL,'2021-02-17 13:13:01'),(4,12,NULL,'isc.example.com','dhcp4',0,NULL,NULL,NULL,0,NULL,NULL,NULL,'2021-02-17 13:13:01'),(5,6,NULL,'10.1.1.202,10.1.1.203','dhcp4',0,'',NULL,1,3,NULL,NULL,NULL,'2021-02-17 13:13:01');
/*!40000 ALTER TABLE `dhcp4_options` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp4_options_AINS AFTER INSERT ON dhcp4_options
    FOR EACH ROW
    BEGIN
        CALL createOptionAuditDHCP4("create", NEW.scope_id, NEW.option_id, NEW.dhcp4_subnet_id,
                                    NEW.host_id, NEW.shared_network_name, NEW.pool_id,
                                    NEW.modification_ts);
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp4_options_AUPD AFTER UPDATE ON dhcp4_options
    FOR EACH ROW
    BEGIN
        CALL createOptionAuditDHCP4("update", NEW.scope_id, NEW.option_id, NEW.dhcp4_subnet_id,
                                    NEW.host_id, NEW.shared_network_name, NEW.pool_id,
                                    NEW.modification_ts);
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp4_options_ADEL AFTER DELETE ON dhcp4_options
    FOR EACH ROW
    BEGIN
        CALL createOptionAuditDHCP4("delete", OLD.scope_id, OLD.option_id, OLD.dhcp4_subnet_id,
                                    OLD.host_id, OLD.shared_network_name, OLD.pool_id,
                                    NOW());
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `dhcp4_options_server`
--

DROP TABLE IF EXISTS `dhcp4_options_server`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp4_options_server` (
  `option_id` bigint(20) unsigned NOT NULL,
  `server_id` bigint(20) unsigned NOT NULL,
  `modification_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`option_id`,`server_id`),
  KEY `fk_dhcp4_options_server_server_id` (`server_id`),
  KEY `key_dhcp4_options_server_modification_ts` (`modification_ts`),
  CONSTRAINT `fk_dhcp4_options_server_option_id` FOREIGN KEY (`option_id`) REFERENCES `dhcp4_options` (`option_id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `fk_dhcp4_options_server_server_id` FOREIGN KEY (`server_id`) REFERENCES `dhcp4_server` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp4_options_server`
--

LOCK TABLES `dhcp4_options_server` WRITE;
/*!40000 ALTER TABLE `dhcp4_options_server` DISABLE KEYS */;
INSERT INTO `dhcp4_options_server` VALUES (1,2,'2021-02-17 13:13:01'),(2,2,'2021-02-17 13:13:01'),(3,2,'2021-02-17 13:13:01'),(4,2,'2021-02-17 13:13:01');
/*!40000 ALTER TABLE `dhcp4_options_server` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dhcp4_pool`
--

DROP TABLE IF EXISTS `dhcp4_pool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp4_pool` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `start_address` int(10) unsigned NOT NULL,
  `end_address` int(10) unsigned NOT NULL,
  `subnet_id` int(10) unsigned NOT NULL,
  `modification_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `client_class` varchar(128) DEFAULT NULL,
  `require_client_classes` longtext DEFAULT NULL,
  `user_context` longtext DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `key_dhcp4_pool_modification_ts` (`modification_ts`),
  KEY `fk_dhcp4_pool_subnet_id` (`subnet_id`),
  CONSTRAINT `fk_dhcp4_pool_subnet_id` FOREIGN KEY (`subnet_id`) REFERENCES `dhcp4_subnet` (`subnet_id`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp4_pool`
--

LOCK TABLES `dhcp4_pool` WRITE;
/*!40000 ALTER TABLE `dhcp4_pool` DISABLE KEYS */;
INSERT INTO `dhcp4_pool` VALUES (1,3232248330,3232248330,2,'2021-02-17 13:13:01','','[  ]',NULL);
/*!40000 ALTER TABLE `dhcp4_pool` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp4_pool_BDEL BEFORE DELETE ON dhcp4_pool FOR EACH ROW

BEGIN
DELETE FROM dhcp4_options WHERE scope_id = 5 AND pool_id = OLD.id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `dhcp4_server`
--

DROP TABLE IF EXISTS `dhcp4_server`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp4_server` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `tag` varchar(256) NOT NULL,
  `description` text DEFAULT NULL,
  `modification_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `dhcp4_server_tag_UNIQUE` (`tag`),
  KEY `key_dhcp4_server_modification_ts` (`modification_ts`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp4_server`
--

LOCK TABLES `dhcp4_server` WRITE;
/*!40000 ALTER TABLE `dhcp4_server` DISABLE KEYS */;
INSERT INTO `dhcp4_server` VALUES (1,'all','special type: all servers','2021-02-17 13:12:52'),(2,'abc','','2021-02-17 13:13:01');
/*!40000 ALTER TABLE `dhcp4_server` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp4_server_AINS AFTER INSERT ON dhcp4_server
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP4('dhcp4_server', NEW.id, "create");
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp4_server_AUPD AFTER UPDATE ON dhcp4_server
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP4('dhcp4_server', NEW.id, "update");
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp4_server_ADEL AFTER DELETE ON dhcp4_server
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP4('dhcp4_server', OLD.id, "delete");
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `dhcp4_shared_network`
--

DROP TABLE IF EXISTS `dhcp4_shared_network`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp4_shared_network` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `client_class` varchar(128) DEFAULT NULL,
  `interface` varchar(128) DEFAULT NULL,
  `match_client_id` tinyint(1) DEFAULT NULL,
  `modification_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `rebind_timer` int(10) DEFAULT NULL,
  `relay` longtext DEFAULT NULL,
  `renew_timer` int(10) DEFAULT NULL,
  `require_client_classes` longtext DEFAULT NULL,
  `reservation_mode` tinyint(3) DEFAULT NULL,
  `user_context` longtext DEFAULT NULL,
  `valid_lifetime` int(10) DEFAULT NULL,
  `authoritative` tinyint(1) DEFAULT NULL,
  `calculate_tee_times` tinyint(1) DEFAULT NULL,
  `t1_percent` float DEFAULT NULL,
  `t2_percent` float DEFAULT NULL,
  `boot_file_name` varchar(512) DEFAULT NULL,
  `next_server` int(10) unsigned DEFAULT NULL,
  `server_hostname` varchar(512) DEFAULT NULL,
  `min_valid_lifetime` int(10) DEFAULT NULL,
  `max_valid_lifetime` int(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`),
  KEY `key_dhcp4_shared_network_modification_ts` (`modification_ts`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp4_shared_network`
--

LOCK TABLES `dhcp4_shared_network` WRITE;
/*!40000 ALTER TABLE `dhcp4_shared_network` DISABLE KEYS */;
INSERT INTO `dhcp4_shared_network` VALUES (1,'net1','abc','!serverinterface!',1,'2021-02-17 13:13:01',200,NULL,100,'[ \"XYZ\" ]',2,'{ \"some weird network\": 55 }',300,0,1,0.5,0.8,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `dhcp4_shared_network` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp4_shared_network_AINS AFTER INSERT ON dhcp4_shared_network
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP4('dhcp4_shared_network', NEW.id, "create");
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp4_shared_network_AUPD AFTER UPDATE ON dhcp4_shared_network
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP4('dhcp4_shared_network', NEW.id, "update");
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp4_shared_network_BDEL BEFORE DELETE ON dhcp4_shared_network
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP4('dhcp4_shared_network', OLD.id, "delete");
        DELETE FROM dhcp4_options WHERE shared_network_name = OLD.name;
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `dhcp4_shared_network_server`
--

DROP TABLE IF EXISTS `dhcp4_shared_network_server`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp4_shared_network_server` (
  `shared_network_id` bigint(20) unsigned NOT NULL,
  `server_id` bigint(20) unsigned NOT NULL,
  `modification_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`shared_network_id`,`server_id`),
  KEY `key_dhcp4_shared_network_server_modification_ts` (`modification_ts`),
  KEY `fk_dhcp4_shared_network_server_server_id` (`server_id`),
  CONSTRAINT `fk_dhcp4_shared_network_server_server_id` FOREIGN KEY (`server_id`) REFERENCES `dhcp4_server` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `fk_dhcp4_shared_network_server_shared_network_id` FOREIGN KEY (`shared_network_id`) REFERENCES `dhcp4_shared_network` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp4_shared_network_server`
--

LOCK TABLES `dhcp4_shared_network_server` WRITE;
/*!40000 ALTER TABLE `dhcp4_shared_network_server` DISABLE KEYS */;
INSERT INTO `dhcp4_shared_network_server` VALUES (1,2,'2021-02-17 13:13:01');
/*!40000 ALTER TABLE `dhcp4_shared_network_server` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dhcp4_subnet`
--

DROP TABLE IF EXISTS `dhcp4_subnet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp4_subnet` (
  `subnet_id` int(10) unsigned NOT NULL,
  `subnet_prefix` varchar(32) NOT NULL,
  `4o6_interface` varchar(128) DEFAULT NULL,
  `4o6_interface_id` varchar(128) DEFAULT NULL,
  `4o6_subnet` varchar(64) DEFAULT NULL,
  `boot_file_name` varchar(512) DEFAULT NULL,
  `client_class` varchar(128) DEFAULT NULL,
  `interface` varchar(128) DEFAULT NULL,
  `match_client_id` tinyint(1) DEFAULT NULL,
  `modification_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `next_server` int(10) unsigned DEFAULT NULL,
  `rebind_timer` int(10) DEFAULT NULL,
  `relay` longtext DEFAULT NULL,
  `renew_timer` int(10) DEFAULT NULL,
  `require_client_classes` longtext DEFAULT NULL,
  `reservation_mode` tinyint(3) DEFAULT NULL,
  `server_hostname` varchar(512) DEFAULT NULL,
  `shared_network_name` varchar(128) DEFAULT NULL,
  `user_context` longtext DEFAULT NULL,
  `valid_lifetime` int(10) DEFAULT NULL,
  `authoritative` tinyint(1) DEFAULT NULL,
  `calculate_tee_times` tinyint(1) DEFAULT NULL,
  `t1_percent` float DEFAULT NULL,
  `t2_percent` float DEFAULT NULL,
  `min_valid_lifetime` int(10) DEFAULT NULL,
  `max_valid_lifetime` int(10) DEFAULT NULL,
  PRIMARY KEY (`subnet_id`),
  UNIQUE KEY `subnet4_subnet_prefix` (`subnet_prefix`),
  KEY `fk_dhcp4_subnet_shared_network` (`shared_network_name`),
  KEY `key_dhcp4_subnet_modification_ts` (`modification_ts`),
  CONSTRAINT `fk_dhcp4_subnet_shared_network` FOREIGN KEY (`shared_network_name`) REFERENCES `dhcp4_shared_network` (`name`) ON DELETE SET NULL ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp4_subnet`
--

LOCK TABLES `dhcp4_subnet` WRITE;
/*!40000 ALTER TABLE `dhcp4_subnet` DISABLE KEYS */;
INSERT INTO `dhcp4_subnet` VALUES (2,'192.168.50.0/24','eth9','interf-id','2000::/64','file-name',NULL,'!serverinterface!',0,'2021-02-17 13:13:01',0,500,'[ \"192.168.5.5\" ]',200,'[  ]',3,'name-xyz',NULL,NULL,1000,0,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `dhcp4_subnet` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp4_subnet_AINS AFTER INSERT ON dhcp4_subnet
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP4('dhcp4_subnet', NEW.subnet_id, "create");
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp4_subnet_AUPD AFTER UPDATE ON dhcp4_subnet
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP4('dhcp4_subnet', NEW.subnet_id, "update");
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp4_subnet_BDEL BEFORE DELETE ON dhcp4_subnet
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP4('dhcp4_subnet', OLD.subnet_id, "delete");
        DELETE FROM dhcp4_pool WHERE subnet_id = OLD.subnet_id;
        DELETE FROM dhcp4_options WHERE dhcp4_subnet_id = OLD.subnet_id;
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `dhcp4_subnet_server`
--

DROP TABLE IF EXISTS `dhcp4_subnet_server`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp4_subnet_server` (
  `subnet_id` int(10) unsigned NOT NULL,
  `server_id` bigint(20) unsigned NOT NULL,
  `modification_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`subnet_id`,`server_id`),
  KEY `fk_dhcp4_subnet_server_server_id_idx` (`server_id`),
  KEY `key_dhcp4_subnet_server_modification_ts` (`modification_ts`),
  CONSTRAINT `fk_dhcp4_subnet_server_server_id` FOREIGN KEY (`server_id`) REFERENCES `dhcp4_server` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `fk_dhcp4_subnet_server_subnet_id` FOREIGN KEY (`subnet_id`) REFERENCES `dhcp4_subnet` (`subnet_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp4_subnet_server`
--

LOCK TABLES `dhcp4_subnet_server` WRITE;
/*!40000 ALTER TABLE `dhcp4_subnet_server` DISABLE KEYS */;
INSERT INTO `dhcp4_subnet_server` VALUES (2,2,'2021-02-17 13:13:01');
/*!40000 ALTER TABLE `dhcp4_subnet_server` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dhcp6_audit`
--

DROP TABLE IF EXISTS `dhcp6_audit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp6_audit` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `object_type` varchar(256) NOT NULL,
  `object_id` bigint(20) unsigned NOT NULL,
  `modification_type` tinyint(1) NOT NULL,
  `revision_id` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_dhcp6_audit_modification_type` (`modification_type`),
  KEY `fk_dhcp6_audit_revision` (`revision_id`),
  CONSTRAINT `fk_dhcp6_audit_modification_type` FOREIGN KEY (`modification_type`) REFERENCES `modification` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_dhcp6_audit_revision` FOREIGN KEY (`revision_id`) REFERENCES `dhcp6_audit_revision` (`id`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp6_audit`
--

LOCK TABLES `dhcp6_audit` WRITE;
/*!40000 ALTER TABLE `dhcp6_audit` DISABLE KEYS */;
/*!40000 ALTER TABLE `dhcp6_audit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dhcp6_audit_revision`
--

DROP TABLE IF EXISTS `dhcp6_audit_revision`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp6_audit_revision` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `modification_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `log_message` text DEFAULT NULL,
  `server_id` bigint(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `key_dhcp6_audit_revision_by_modification_ts` (`modification_ts`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp6_audit_revision`
--

LOCK TABLES `dhcp6_audit_revision` WRITE;
/*!40000 ALTER TABLE `dhcp6_audit_revision` DISABLE KEYS */;
/*!40000 ALTER TABLE `dhcp6_audit_revision` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dhcp6_global_parameter`
--

DROP TABLE IF EXISTS `dhcp6_global_parameter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp6_global_parameter` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `value` longtext NOT NULL,
  `modification_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `parameter_type` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `key_dhcp6_global_parameter_modification_ts` (`modification_ts`),
  KEY `key_dhcp6_global_parameter_name` (`name`),
  KEY `fk_dhcp6_global_parameter_type` (`parameter_type`),
  CONSTRAINT `fk_dhcp6_global_parameter_type` FOREIGN KEY (`parameter_type`) REFERENCES `parameter_data_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp6_global_parameter`
--

LOCK TABLES `dhcp6_global_parameter` WRITE;
/*!40000 ALTER TABLE `dhcp6_global_parameter` DISABLE KEYS */;
/*!40000 ALTER TABLE `dhcp6_global_parameter` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp6_global_parameter_AINS AFTER INSERT ON dhcp6_global_parameter
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP6('dhcp6_global_parameter', NEW.id, "create");
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp6_global_parameter_AUPD AFTER UPDATE ON dhcp6_global_parameter
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP6('dhcp6_global_parameter', NEW.id, "update");
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp6_global_parameter_ADEL AFTER DELETE ON dhcp6_global_parameter
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP6('dhcp6_global_parameter', OLD.id, "delete");
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `dhcp6_global_parameter_server`
--

DROP TABLE IF EXISTS `dhcp6_global_parameter_server`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp6_global_parameter_server` (
  `parameter_id` bigint(20) unsigned NOT NULL,
  `server_id` bigint(20) unsigned NOT NULL,
  `modification_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`parameter_id`,`server_id`),
  KEY `fk_dhcp6_global_parameter_server_server_id` (`server_id`),
  KEY `key_dhcp6_global_parameter_server` (`modification_ts`),
  CONSTRAINT `fk_dhcp6_global_parameter_server_parameter_id` FOREIGN KEY (`parameter_id`) REFERENCES `dhcp6_global_parameter` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `fk_dhcp6_global_parameter_server_server_id` FOREIGN KEY (`server_id`) REFERENCES `dhcp6_server` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp6_global_parameter_server`
--

LOCK TABLES `dhcp6_global_parameter_server` WRITE;
/*!40000 ALTER TABLE `dhcp6_global_parameter_server` DISABLE KEYS */;
/*!40000 ALTER TABLE `dhcp6_global_parameter_server` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dhcp6_option_def`
--

DROP TABLE IF EXISTS `dhcp6_option_def`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp6_option_def` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `code` smallint(5) unsigned NOT NULL,
  `name` varchar(128) NOT NULL,
  `space` varchar(128) NOT NULL,
  `type` tinyint(3) unsigned NOT NULL,
  `modification_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `is_array` tinyint(1) NOT NULL,
  `encapsulate` varchar(128) NOT NULL,
  `record_types` varchar(512) DEFAULT NULL,
  `user_context` longtext DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `key_dhcp6_option_def_modification_ts` (`modification_ts`),
  KEY `key_dhcp6_option_def_code_space` (`code`,`space`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp6_option_def`
--

LOCK TABLES `dhcp6_option_def` WRITE;
/*!40000 ALTER TABLE `dhcp6_option_def` DISABLE KEYS */;
/*!40000 ALTER TABLE `dhcp6_option_def` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp6_option_def_AINS AFTER INSERT ON dhcp6_option_def
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP6('dhcp6_option_def', NEW.id, "create");
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp6_option_def_AUPD AFTER UPDATE ON dhcp6_option_def
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP6('dhcp6_option_def', NEW.id, "update");
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp6_option_def_ADEL AFTER DELETE ON dhcp6_option_def
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP6('dhcp6_option_def', OLD.id, "delete");
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `dhcp6_option_def_server`
--

DROP TABLE IF EXISTS `dhcp6_option_def_server`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp6_option_def_server` (
  `option_def_id` bigint(20) unsigned NOT NULL,
  `server_id` bigint(20) unsigned NOT NULL,
  `modification_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`option_def_id`,`server_id`),
  KEY `fk_dhcp6_option_def_server_server_id_idx` (`server_id`),
  KEY `key_dhcp6_option_def_server_modification_ts` (`modification_ts`),
  CONSTRAINT `fk_dhcp6_option_def_server_option_def_id` FOREIGN KEY (`option_def_id`) REFERENCES `dhcp6_option_def` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `fk_dhcp6_option_def_server_server_id` FOREIGN KEY (`server_id`) REFERENCES `dhcp6_server` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp6_option_def_server`
--

LOCK TABLES `dhcp6_option_def_server` WRITE;
/*!40000 ALTER TABLE `dhcp6_option_def_server` DISABLE KEYS */;
/*!40000 ALTER TABLE `dhcp6_option_def_server` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dhcp6_options`
--

DROP TABLE IF EXISTS `dhcp6_options`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp6_options` (
  `option_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `code` smallint(5) unsigned NOT NULL,
  `value` blob DEFAULT NULL,
  `formatted_value` text DEFAULT NULL,
  `space` varchar(128) DEFAULT NULL,
  `persistent` tinyint(1) NOT NULL DEFAULT 0,
  `dhcp_client_class` varchar(128) DEFAULT NULL,
  `dhcp6_subnet_id` int(10) unsigned DEFAULT NULL,
  `host_id` int(10) unsigned DEFAULT NULL,
  `scope_id` tinyint(3) unsigned NOT NULL,
  `user_context` text DEFAULT NULL,
  `shared_network_name` varchar(128) DEFAULT NULL,
  `pool_id` bigint(20) unsigned DEFAULT NULL,
  `pd_pool_id` bigint(20) unsigned DEFAULT NULL,
  `modification_ts` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`option_id`),
  UNIQUE KEY `option_id_UNIQUE` (`option_id`),
  KEY `fk_options_host1_idx` (`host_id`),
  KEY `fk_dhcp6_option_scope` (`scope_id`),
  CONSTRAINT `fk_dhcp6_option_scope` FOREIGN KEY (`scope_id`) REFERENCES `dhcp_option_scope` (`scope_id`),
  CONSTRAINT `fk_options_host10` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp6_options`
--

LOCK TABLES `dhcp6_options` WRITE;
/*!40000 ALTER TABLE `dhcp6_options` DISABLE KEYS */;
/*!40000 ALTER TABLE `dhcp6_options` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp6_options_AINS AFTER INSERT ON dhcp6_options
    FOR EACH ROW
    BEGIN
        CALL createOptionAuditDHCP6("create", NEW.scope_id, NEW.option_id, NEW.dhcp6_subnet_id,
                                    NEW.host_id, NEW.shared_network_name, NEW.pool_id,
                                    NEW.pd_pool_id, NEW.modification_ts);
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp6_options_AUPD AFTER UPDATE ON dhcp6_options
    FOR EACH ROW
    BEGIN
        CALL createOptionAuditDHCP6("update", NEW.scope_id, NEW.option_id, NEW.dhcp6_subnet_id,
                                    NEW.host_id, NEW.shared_network_name, NEW.pool_id,
                                    NEW.pd_pool_id, NEW.modification_ts);
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp6_options_ADEL AFTER DELETE ON dhcp6_options
    FOR EACH ROW
    BEGIN
        CALL createOptionAuditDHCP6("delete", OLD.scope_id, OLD.option_id, OLD.dhcp6_subnet_id,
                                    OLD.host_id, OLD.shared_network_name, OLD.pool_id,
                                    OLD.pd_pool_id, NOW());
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `dhcp6_options_server`
--

DROP TABLE IF EXISTS `dhcp6_options_server`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp6_options_server` (
  `option_id` bigint(20) unsigned NOT NULL,
  `server_id` bigint(20) unsigned NOT NULL,
  `modification_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`option_id`,`server_id`),
  KEY `fk_dhcp6_options_server_server_id_idx` (`server_id`),
  KEY `key_dhcp6_options_server_modification_ts` (`modification_ts`),
  CONSTRAINT `fk_dhcp6_options_server_option_id` FOREIGN KEY (`option_id`) REFERENCES `dhcp6_options` (`option_id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `fk_dhcp6_options_server_server_id` FOREIGN KEY (`server_id`) REFERENCES `dhcp6_server` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp6_options_server`
--

LOCK TABLES `dhcp6_options_server` WRITE;
/*!40000 ALTER TABLE `dhcp6_options_server` DISABLE KEYS */;
/*!40000 ALTER TABLE `dhcp6_options_server` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dhcp6_pd_pool`
--

DROP TABLE IF EXISTS `dhcp6_pd_pool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp6_pd_pool` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `prefix` varchar(45) NOT NULL,
  `prefix_length` tinyint(3) NOT NULL,
  `delegated_prefix_length` tinyint(3) NOT NULL,
  `subnet_id` int(10) unsigned NOT NULL,
  `modification_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `excluded_prefix` varchar(45) DEFAULT NULL,
  `excluded_prefix_length` tinyint(3) NOT NULL,
  `client_class` varchar(128) DEFAULT NULL,
  `require_client_classes` longtext DEFAULT NULL,
  `user_context` longtext DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `key_dhcp6_pd_pool_modification_ts` (`modification_ts`),
  KEY `fk_dhcp6_pd_pool_subnet_id` (`subnet_id`),
  CONSTRAINT `fk_dhcp6_pd_pool_subnet_id` FOREIGN KEY (`subnet_id`) REFERENCES `dhcp6_subnet` (`subnet_id`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp6_pd_pool`
--

LOCK TABLES `dhcp6_pd_pool` WRITE;
/*!40000 ALTER TABLE `dhcp6_pd_pool` DISABLE KEYS */;
/*!40000 ALTER TABLE `dhcp6_pd_pool` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp6_pd_pool_BDEL BEFORE DELETE ON dhcp6_pd_pool FOR EACH ROW
BEGIN
DELETE FROM dhcp6_options WHERE scope_id = 6 AND pd_pool_id = OLD.id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `dhcp6_pool`
--

DROP TABLE IF EXISTS `dhcp6_pool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp6_pool` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `start_address` varchar(45) NOT NULL,
  `end_address` varchar(45) NOT NULL,
  `subnet_id` int(10) unsigned NOT NULL,
  `modification_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `client_class` varchar(128) DEFAULT NULL,
  `require_client_classes` longtext DEFAULT NULL,
  `user_context` longtext DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `key_dhcp6_pool_modification_ts` (`modification_ts`),
  KEY `fk_dhcp6_pool_subnet_id` (`subnet_id`),
  CONSTRAINT `fk_dhcp6_pool_subnet_id` FOREIGN KEY (`subnet_id`) REFERENCES `dhcp6_subnet` (`subnet_id`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp6_pool`
--

LOCK TABLES `dhcp6_pool` WRITE;
/*!40000 ALTER TABLE `dhcp6_pool` DISABLE KEYS */;
/*!40000 ALTER TABLE `dhcp6_pool` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp6_pool_BDEL BEFORE DELETE ON dhcp6_pool FOR EACH ROW

BEGIN
DELETE FROM dhcp6_options WHERE scope_id = 5 AND pool_id = OLD.id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `dhcp6_server`
--

DROP TABLE IF EXISTS `dhcp6_server`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp6_server` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `tag` varchar(256) NOT NULL,
  `description` text DEFAULT NULL,
  `modification_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `dhcp6_server_tag_UNIQUE` (`tag`),
  KEY `key_dhcp6_server_modification_ts` (`modification_ts`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp6_server`
--

LOCK TABLES `dhcp6_server` WRITE;
/*!40000 ALTER TABLE `dhcp6_server` DISABLE KEYS */;
INSERT INTO `dhcp6_server` VALUES (1,'all','special type: all servers','2021-02-17 13:12:53');
/*!40000 ALTER TABLE `dhcp6_server` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp6_server_AINS AFTER INSERT ON dhcp6_server
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP6('dhcp6_server', NEW.id, "create");
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp6_server_AUPD AFTER UPDATE ON dhcp6_server
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP6('dhcp6_server', NEW.id, "update");
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp6_server_ADEL AFTER DELETE ON dhcp6_server
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP6('dhcp6_server', OLD.id, "delete");
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `dhcp6_shared_network`
--

DROP TABLE IF EXISTS `dhcp6_shared_network`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp6_shared_network` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `client_class` varchar(128) DEFAULT NULL,
  `interface` varchar(128) DEFAULT NULL,
  `modification_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `preferred_lifetime` int(10) DEFAULT NULL,
  `rapid_commit` tinyint(1) DEFAULT NULL,
  `rebind_timer` int(10) DEFAULT NULL,
  `relay` longtext DEFAULT NULL,
  `renew_timer` int(10) DEFAULT NULL,
  `require_client_classes` longtext DEFAULT NULL,
  `reservation_mode` tinyint(3) DEFAULT NULL,
  `user_context` longtext DEFAULT NULL,
  `valid_lifetime` int(10) DEFAULT NULL,
  `calculate_tee_times` tinyint(1) DEFAULT NULL,
  `t1_percent` float DEFAULT NULL,
  `t2_percent` float DEFAULT NULL,
  `interface_id` varbinary(128) DEFAULT NULL,
  `min_preferred_lifetime` int(10) DEFAULT NULL,
  `max_preferred_lifetime` int(10) DEFAULT NULL,
  `min_valid_lifetime` int(10) DEFAULT NULL,
  `max_valid_lifetime` int(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`),
  KEY `key_dhcp6_shared_network_modification_ts` (`modification_ts`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp6_shared_network`
--

LOCK TABLES `dhcp6_shared_network` WRITE;
/*!40000 ALTER TABLE `dhcp6_shared_network` DISABLE KEYS */;
/*!40000 ALTER TABLE `dhcp6_shared_network` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp6_shared_network_AINS AFTER INSERT ON dhcp6_shared_network
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP6('dhcp6_shared_network', NEW.id, "create");
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp6_shared_network_AUPD AFTER UPDATE ON dhcp6_shared_network
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP6('dhcp6_shared_network', NEW.id, "update");
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp6_shared_network_BDEL BEFORE DELETE ON dhcp6_shared_network
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP6('dhcp6_shared_network', OLD.id, "delete");
        DELETE FROM dhcp6_options WHERE shared_network_name = OLD.name;
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `dhcp6_shared_network_server`
--

DROP TABLE IF EXISTS `dhcp6_shared_network_server`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp6_shared_network_server` (
  `shared_network_id` bigint(20) unsigned NOT NULL,
  `server_id` bigint(20) unsigned NOT NULL,
  `modification_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`shared_network_id`,`server_id`),
  KEY `key_dhcp6_shared_network_server_modification_ts` (`modification_ts`),
  KEY `fk_dhcp6_shared_network_server_server_id_idx` (`server_id`),
  CONSTRAINT `fk_dhcp6_shared_network_server_server_id` FOREIGN KEY (`server_id`) REFERENCES `dhcp6_server` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `fk_dhcp6_shared_network_server_shared_network_id` FOREIGN KEY (`shared_network_id`) REFERENCES `dhcp6_shared_network` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp6_shared_network_server`
--

LOCK TABLES `dhcp6_shared_network_server` WRITE;
/*!40000 ALTER TABLE `dhcp6_shared_network_server` DISABLE KEYS */;
/*!40000 ALTER TABLE `dhcp6_shared_network_server` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dhcp6_subnet`
--

DROP TABLE IF EXISTS `dhcp6_subnet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp6_subnet` (
  `subnet_id` int(10) unsigned NOT NULL,
  `subnet_prefix` varchar(64) NOT NULL,
  `client_class` varchar(128) DEFAULT NULL,
  `interface` varchar(128) DEFAULT NULL,
  `modification_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `preferred_lifetime` int(10) DEFAULT NULL,
  `rapid_commit` tinyint(1) DEFAULT NULL,
  `rebind_timer` int(10) DEFAULT NULL,
  `relay` longtext DEFAULT NULL,
  `renew_timer` int(10) DEFAULT NULL,
  `require_client_classes` longtext DEFAULT NULL,
  `reservation_mode` tinyint(3) DEFAULT NULL,
  `shared_network_name` varchar(128) DEFAULT NULL,
  `user_context` longtext DEFAULT NULL,
  `valid_lifetime` int(10) DEFAULT NULL,
  `calculate_tee_times` tinyint(1) DEFAULT NULL,
  `t1_percent` float DEFAULT NULL,
  `t2_percent` float DEFAULT NULL,
  `interface_id` varbinary(128) DEFAULT NULL,
  `min_preferred_lifetime` int(10) DEFAULT NULL,
  `max_preferred_lifetime` int(10) DEFAULT NULL,
  `min_valid_lifetime` int(10) DEFAULT NULL,
  `max_valid_lifetime` int(10) DEFAULT NULL,
  PRIMARY KEY (`subnet_id`),
  UNIQUE KEY `subnet_prefix_UNIQUE` (`subnet_prefix`),
  KEY `subnet6_subnet_prefix` (`subnet_prefix`),
  KEY `fk_dhcp6_subnet_shared_network` (`shared_network_name`),
  KEY `key_dhcp6_subnet_modification_ts` (`modification_ts`),
  CONSTRAINT `fk_dhcp6_subnet_shared_network` FOREIGN KEY (`shared_network_name`) REFERENCES `dhcp6_shared_network` (`name`) ON DELETE SET NULL ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp6_subnet`
--

LOCK TABLES `dhcp6_subnet` WRITE;
/*!40000 ALTER TABLE `dhcp6_subnet` DISABLE KEYS */;
/*!40000 ALTER TABLE `dhcp6_subnet` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp6_subnet_AINS AFTER INSERT ON dhcp6_subnet
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP6('dhcp6_subnet', NEW.subnet_id, "create");
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp6_subnet_AUPD AFTER UPDATE ON dhcp6_subnet
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP6('dhcp6_subnet', NEW.subnet_id, "update");
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER dhcp6_subnet_BDEL BEFORE DELETE ON dhcp6_subnet
    FOR EACH ROW
    BEGIN
        CALL createAuditEntryDHCP6('dhcp6_subnet', OLD.subnet_id, "delete");
        DELETE FROM dhcp6_pool WHERE subnet_id = OLD.subnet_id;
        DELETE FROM dhcp6_pd_pool WHERE subnet_id = OLD.subnet_id;
        DELETE FROM dhcp6_options WHERE dhcp6_subnet_id = OLD.subnet_id;
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `dhcp6_subnet_server`
--

DROP TABLE IF EXISTS `dhcp6_subnet_server`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp6_subnet_server` (
  `subnet_id` int(10) unsigned NOT NULL,
  `server_id` bigint(20) unsigned NOT NULL,
  `modification_ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`subnet_id`,`server_id`),
  KEY `fk_dhcp6_subnet_server_server_id` (`server_id`),
  KEY `key_dhcp6_subnet_server_modification_ts` (`modification_ts`),
  CONSTRAINT `fk_dhcp6_subnet_server_server_id` FOREIGN KEY (`server_id`) REFERENCES `dhcp6_server` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `fk_dhcp6_subnet_server_subnet_id` FOREIGN KEY (`subnet_id`) REFERENCES `dhcp6_subnet` (`subnet_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp6_subnet_server`
--

LOCK TABLES `dhcp6_subnet_server` WRITE;
/*!40000 ALTER TABLE `dhcp6_subnet_server` DISABLE KEYS */;
/*!40000 ALTER TABLE `dhcp6_subnet_server` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dhcp_option_scope`
--

DROP TABLE IF EXISTS `dhcp_option_scope`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dhcp_option_scope` (
  `scope_id` tinyint(3) unsigned NOT NULL,
  `scope_name` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`scope_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dhcp_option_scope`
--

LOCK TABLES `dhcp_option_scope` WRITE;
/*!40000 ALTER TABLE `dhcp_option_scope` DISABLE KEYS */;
INSERT INTO `dhcp_option_scope` VALUES (0,'global'),(1,'subnet'),(2,'client-class'),(3,'host'),(4,'shared-network'),(5,'pool'),(6,'pd-pool');
/*!40000 ALTER TABLE `dhcp_option_scope` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `host_identifier_type`
--

DROP TABLE IF EXISTS `host_identifier_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `host_identifier_type` (
  `type` tinyint(4) NOT NULL,
  `name` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `host_identifier_type`
--

LOCK TABLES `host_identifier_type` WRITE;
/*!40000 ALTER TABLE `host_identifier_type` DISABLE KEYS */;
INSERT INTO `host_identifier_type` VALUES (0,'hw-address'),(1,'duid'),(2,'circuit-id'),(3,'client-id'),(4,'flex-id');
/*!40000 ALTER TABLE `host_identifier_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hosts`
--

DROP TABLE IF EXISTS `hosts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hosts` (
  `host_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `dhcp_identifier` varbinary(128) NOT NULL,
  `dhcp_identifier_type` tinyint(4) NOT NULL,
  `dhcp4_subnet_id` int(10) unsigned DEFAULT NULL,
  `dhcp6_subnet_id` int(10) unsigned DEFAULT NULL,
  `ipv4_address` int(10) unsigned DEFAULT NULL,
  `hostname` varchar(255) DEFAULT NULL,
  `dhcp4_client_classes` varchar(255) DEFAULT NULL,
  `dhcp6_client_classes` varchar(255) DEFAULT NULL,
  `dhcp4_next_server` int(10) unsigned DEFAULT NULL,
  `dhcp4_server_hostname` varchar(64) DEFAULT NULL,
  `dhcp4_boot_file_name` varchar(128) DEFAULT NULL,
  `user_context` text DEFAULT NULL,
  `auth_key` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`host_id`),
  UNIQUE KEY `key_dhcp4_identifier_subnet_id` (`dhcp_identifier`,`dhcp_identifier_type`,`dhcp4_subnet_id`),
  UNIQUE KEY `key_dhcp6_identifier_subnet_id` (`dhcp_identifier`,`dhcp_identifier_type`,`dhcp6_subnet_id`),
  UNIQUE KEY `key_dhcp4_ipv4_address_subnet_id` (`ipv4_address`,`dhcp4_subnet_id`),
  KEY `fk_host_identifier_type` (`dhcp_identifier_type`),
  CONSTRAINT `fk_host_identifier_type` FOREIGN KEY (`dhcp_identifier_type`) REFERENCES `host_identifier_type` (`type`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hosts`
--

LOCK TABLES `hosts` WRITE;
/*!40000 ALTER TABLE `hosts` DISABLE KEYS */;
INSERT INTO `hosts` VALUES (1,'\n\r',0,2,NULL,3232248525,'','special_snowflake,office','',3221225985,'hal9000','/dev/null',NULL,'');
/*!40000 ALTER TABLE `hosts` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER host_BDEL BEFORE DELETE ON hosts FOR EACH ROW

BEGIN
DELETE FROM ipv6_reservations WHERE ipv6_reservations.host_id = OLD.host_id;
DELETE FROM dhcp4_options WHERE dhcp4_options.host_id = OLD.host_id;
DELETE FROM dhcp6_options WHERE dhcp6_options.host_id = OLD.host_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `ipv6_reservations`
--

DROP TABLE IF EXISTS `ipv6_reservations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ipv6_reservations` (
  `reservation_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `address` varchar(39) NOT NULL,
  `prefix_len` tinyint(3) unsigned NOT NULL DEFAULT 128,
  `type` tinyint(4) unsigned NOT NULL DEFAULT 0,
  `dhcp6_iaid` int(10) unsigned DEFAULT NULL,
  `host_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`reservation_id`),
  UNIQUE KEY `key_dhcp6_address_prefix_len` (`address`,`prefix_len`),
  KEY `fk_ipv6_reservations_host_idx` (`host_id`),
  CONSTRAINT `fk_ipv6_reservations_Host` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`host_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ipv6_reservations`
--

LOCK TABLES `ipv6_reservations` WRITE;
/*!40000 ALTER TABLE `ipv6_reservations` DISABLE KEYS */;
/*!40000 ALTER TABLE `ipv6_reservations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lease4`
--

DROP TABLE IF EXISTS `lease4`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lease4` (
  `address` int(10) unsigned NOT NULL,
  `hwaddr` varbinary(20) DEFAULT NULL,
  `client_id` varbinary(128) DEFAULT NULL,
  `valid_lifetime` int(10) unsigned DEFAULT NULL,
  `expire` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `subnet_id` int(10) unsigned DEFAULT NULL,
  `fqdn_fwd` tinyint(1) DEFAULT NULL,
  `fqdn_rev` tinyint(1) DEFAULT NULL,
  `hostname` varchar(255) DEFAULT NULL,
  `state` int(10) unsigned DEFAULT 0,
  `user_context` text DEFAULT NULL,
  PRIMARY KEY (`address`),
  KEY `lease4_by_hwaddr_subnet_id` (`hwaddr`,`subnet_id`),
  KEY `lease4_by_client_id_subnet_id` (`client_id`,`subnet_id`),
  KEY `lease4_by_state_expire` (`state`,`expire`),
  KEY `lease4_by_subnet_id` (`subnet_id`),
  CONSTRAINT `fk_lease4_state` FOREIGN KEY (`state`) REFERENCES `lease_state` (`state`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lease4`
--

LOCK TABLES `lease4` WRITE;
/*!40000 ALTER TABLE `lease4` DISABLE KEYS */;
INSERT INTO `lease4` VALUES (3232248330,'ÿÿ',NULL,1000,'2021-02-17 13:29:43',2,0,0,'',0,NULL);
/*!40000 ALTER TABLE `lease4` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER stat_lease4_insert AFTER INSERT ON lease4
    FOR EACH ROW
    BEGIN
        IF NEW.state = 0 OR NEW.state = 1 THEN
            UPDATE lease4_stat SET leases = leases + 1
            WHERE subnet_id = NEW.subnet_id AND state = NEW.state;
            IF ROW_COUNT() <= 0 THEN
                INSERT INTO lease4_stat VALUES (NEW.subnet_id, NEW.state, 1);
            END IF;
        END IF;
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER stat_lease4_update AFTER UPDATE ON lease4
    FOR EACH ROW
    BEGIN
        IF OLD.state != NEW.state THEN
            IF OLD.state = 0 OR OLD.state = 1 THEN
                UPDATE lease4_stat SET leases = leases - 1
                WHERE subnet_id = OLD.subnet_id AND state = OLD.state;
            END IF;
            IF NEW.state = 0 OR NEW.state = 1 THEN
                UPDATE lease4_stat SET leases = leases + 1
                WHERE subnet_id = NEW.subnet_id AND state = NEW.state;
                IF ROW_COUNT() <= 0 THEN
                    INSERT INTO lease4_stat VALUES (NEW.subnet_id, NEW.state, 1);
                END IF;
            END IF;
        END IF;
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER stat_lease4_delete AFTER DELETE ON lease4
    FOR EACH ROW
    BEGIN
        IF OLD.state = 0 OR OLD.state = 1 THEN
            UPDATE lease4_stat SET leases = leases - 1
            WHERE subnet_id = OLD.subnet_id AND OLD.state = state;
        END IF;
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `lease4_stat`
--

DROP TABLE IF EXISTS `lease4_stat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lease4_stat` (
  `subnet_id` int(10) unsigned NOT NULL,
  `state` int(10) unsigned NOT NULL,
  `leases` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`subnet_id`,`state`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lease4_stat`
--

LOCK TABLES `lease4_stat` WRITE;
/*!40000 ALTER TABLE `lease4_stat` DISABLE KEYS */;
INSERT INTO `lease4_stat` VALUES (2,0,1);
/*!40000 ALTER TABLE `lease4_stat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lease6`
--

DROP TABLE IF EXISTS `lease6`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lease6` (
  `address` varchar(39) NOT NULL,
  `duid` varbinary(128) DEFAULT NULL,
  `valid_lifetime` int(10) unsigned DEFAULT NULL,
  `expire` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `subnet_id` int(10) unsigned DEFAULT NULL,
  `pref_lifetime` int(10) unsigned DEFAULT NULL,
  `lease_type` tinyint(4) DEFAULT NULL,
  `iaid` int(10) unsigned DEFAULT NULL,
  `prefix_len` tinyint(3) unsigned DEFAULT NULL,
  `fqdn_fwd` tinyint(1) DEFAULT NULL,
  `fqdn_rev` tinyint(1) DEFAULT NULL,
  `hostname` varchar(255) DEFAULT NULL,
  `hwaddr` varbinary(20) DEFAULT NULL,
  `hwtype` smallint(5) unsigned DEFAULT NULL,
  `hwaddr_source` int(10) unsigned DEFAULT NULL,
  `state` int(10) unsigned DEFAULT 0,
  `user_context` text DEFAULT NULL,
  PRIMARY KEY (`address`),
  KEY `lease6_by_state_expire` (`state`,`expire`),
  KEY `fk_lease6_type` (`lease_type`),
  KEY `fk_lease6_hwaddr_source` (`hwaddr_source`),
  KEY `lease6_by_subnet_id_lease_type` (`subnet_id`,`lease_type`),
  KEY `lease6_by_duid_iaid_subnet_id` (`duid`,`iaid`,`subnet_id`),
  CONSTRAINT `fk_lease6_hwaddr_source` FOREIGN KEY (`hwaddr_source`) REFERENCES `lease_hwaddr_source` (`hwaddr_source`),
  CONSTRAINT `fk_lease6_state` FOREIGN KEY (`state`) REFERENCES `lease_state` (`state`),
  CONSTRAINT `fk_lease6_type` FOREIGN KEY (`lease_type`) REFERENCES `lease6_types` (`lease_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lease6`
--

LOCK TABLES `lease6` WRITE;
/*!40000 ALTER TABLE `lease6` DISABLE KEYS */;
/*!40000 ALTER TABLE `lease6` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER stat_lease6_insert AFTER INSERT ON lease6
    FOR EACH ROW
    BEGIN
        IF NEW.state = 0 OR NEW.state = 1 THEN
            UPDATE lease6_stat SET leases = leases + 1
            WHERE
                subnet_id = NEW.subnet_id AND lease_type = NEW.lease_type
                AND state = NEW.state;
            IF ROW_COUNT() <= 0 THEN
                INSERT INTO lease6_stat
                VALUES (NEW.subnet_id, NEW.lease_type, NEW.state, 1);
            END IF;
        END IF;
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER stat_lease6_update AFTER UPDATE ON lease6
    FOR EACH ROW
    BEGIN
        IF OLD.state != NEW.state THEN
            IF OLD.state = 0 OR OLD.state = 1 THEN
                UPDATE lease6_stat SET leases = leases - 1
                WHERE subnet_id = OLD.subnet_id AND lease_type = OLD.lease_type
                AND state = OLD.state;
            END IF;
            IF NEW.state = 0 OR NEW.state = 1 THEN
                UPDATE lease6_stat SET leases = leases + 1
                WHERE subnet_id = NEW.subnet_id AND lease_type = NEW.lease_type
                AND state = NEW.state;
                IF ROW_COUNT() <= 0 THEN
                    INSERT INTO lease6_stat
                    VALUES (NEW.subnet_id, NEW.lease_type, NEW.state, 1);
                END IF;
            END IF;
        END IF;
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`!db_user!`@`localhost`*/ /*!50003 TRIGGER stat_lease6_delete AFTER DELETE ON lease6
    FOR EACH ROW
    BEGIN
        IF OLD.state = 0 OR OLD.state = 1 THEN
            UPDATE lease6_stat SET leases = leases - 1
            WHERE subnet_id = OLD.subnet_id AND lease_type = OLD.lease_type
            AND state = OLD.state;
        END IF;
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `lease6_stat`
--

DROP TABLE IF EXISTS `lease6_stat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lease6_stat` (
  `subnet_id` int(10) unsigned NOT NULL,
  `lease_type` int(10) unsigned NOT NULL,
  `state` int(10) unsigned NOT NULL,
  `leases` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`subnet_id`,`lease_type`,`state`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lease6_stat`
--

LOCK TABLES `lease6_stat` WRITE;
/*!40000 ALTER TABLE `lease6_stat` DISABLE KEYS */;
/*!40000 ALTER TABLE `lease6_stat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lease6_types`
--

DROP TABLE IF EXISTS `lease6_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lease6_types` (
  `lease_type` tinyint(4) NOT NULL,
  `name` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`lease_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lease6_types`
--

LOCK TABLES `lease6_types` WRITE;
/*!40000 ALTER TABLE `lease6_types` DISABLE KEYS */;
INSERT INTO `lease6_types` VALUES (0,'IA_NA'),(1,'IA_TA'),(2,'IA_PD');
/*!40000 ALTER TABLE `lease6_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lease_hwaddr_source`
--

DROP TABLE IF EXISTS `lease_hwaddr_source`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lease_hwaddr_source` (
  `hwaddr_source` int(10) unsigned NOT NULL,
  `name` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`hwaddr_source`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lease_hwaddr_source`
--

LOCK TABLES `lease_hwaddr_source` WRITE;
/*!40000 ALTER TABLE `lease_hwaddr_source` DISABLE KEYS */;
INSERT INTO `lease_hwaddr_source` VALUES (0,'HWADDR_SOURCE_UNKNOWN'),(1,'HWADDR_SOURCE_RAW'),(2,'HWADDR_SOURCE_IPV6_LINK_LOCAL'),(4,'HWADDR_SOURCE_DUID'),(8,'HWADDR_SOURCE_CLIENT_ADDR_RELAY_OPTION'),(16,'HWADDR_SOURCE_REMOTE_ID'),(32,'HWADDR_SOURCE_SUBSCRIBER_ID'),(64,'HWADDR_SOURCE_DOCSIS_CMTS'),(128,'HWADDR_SOURCE_DOCSIS_MODEM');
/*!40000 ALTER TABLE `lease_hwaddr_source` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lease_state`
--

DROP TABLE IF EXISTS `lease_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lease_state` (
  `state` int(10) unsigned NOT NULL,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY (`state`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lease_state`
--

LOCK TABLES `lease_state` WRITE;
/*!40000 ALTER TABLE `lease_state` DISABLE KEYS */;
INSERT INTO `lease_state` VALUES (0,'default'),(1,'declined'),(2,'expired-reclaimed');
/*!40000 ALTER TABLE `lease_state` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logs`
--

DROP TABLE IF EXISTS `logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `logs` (
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `address` varchar(43) DEFAULT NULL,
  `log` text NOT NULL,
  KEY `timestamp_index` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs`
--

LOCK TABLES `logs` WRITE;
/*!40000 ALTER TABLE `logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `modification`
--

DROP TABLE IF EXISTS `modification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `modification` (
  `id` tinyint(3) NOT NULL,
  `modification_type` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modification`
--

LOCK TABLES `modification` WRITE;
/*!40000 ALTER TABLE `modification` DISABLE KEYS */;
INSERT INTO `modification` VALUES (0,'create'),(1,'update'),(2,'delete');
/*!40000 ALTER TABLE `modification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parameter_data_type`
--

DROP TABLE IF EXISTS `parameter_data_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `parameter_data_type` (
  `id` tinyint(3) unsigned NOT NULL,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parameter_data_type`
--

LOCK TABLES `parameter_data_type` WRITE;
/*!40000 ALTER TABLE `parameter_data_type` DISABLE KEYS */;
INSERT INTO `parameter_data_type` VALUES (0,'integer'),(1,'real'),(2,'boolean'),(4,'string');
/*!40000 ALTER TABLE `parameter_data_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schema_version`
--

DROP TABLE IF EXISTS `schema_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `schema_version` (
  `version` int(11) NOT NULL,
  `minor` int(11) DEFAULT NULL,
  PRIMARY KEY (`version`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schema_version`
--

LOCK TABLES `schema_version` WRITE;
/*!40000 ALTER TABLE `schema_version` DISABLE KEYS */;
INSERT INTO `schema_version` VALUES (8,2);
/*!40000 ALTER TABLE `schema_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'keadb'
--

--
-- Dumping routines for database 'keadb'
--
/*!50003 DROP PROCEDURE IF EXISTS `createAuditEntryDHCP4` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`!db_user!`@`localhost` PROCEDURE `createAuditEntryDHCP4`(IN object_type_val VARCHAR(256),
                                       IN object_id_val BIGINT(20) UNSIGNED,
                                       IN modification_type_val VARCHAR(32))
BEGIN
    IF @disable_audit IS NULL OR @disable_audit = 0 THEN
        INSERT INTO dhcp4_audit (object_type, object_id, modification_type, revision_id)
            VALUES (object_type_val, object_id_val,
               (SELECT id FROM modification WHERE modification_type = modification_type_val),
                @audit_revision_id);
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `createAuditEntryDHCP6` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`!db_user!`@`localhost` PROCEDURE `createAuditEntryDHCP6`(IN object_type_val VARCHAR(256),
                                       IN object_id_val BIGINT(20) UNSIGNED,
                                       IN modification_type_val VARCHAR(32))
BEGIN
    IF @disable_audit IS NULL OR @disable_audit = 0 THEN
        INSERT INTO dhcp6_audit (object_type, object_id, modification_type, revision_id)
            VALUES (object_type_val, object_id_val,
               (SELECT id FROM modification WHERE modification_type = modification_type_val),
                @audit_revision_id);
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `createAuditRevisionDHCP4` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`!db_user!`@`localhost` PROCEDURE `createAuditRevisionDHCP4`(IN audit_ts TIMESTAMP,
                                          IN server_tag VARCHAR(256),
                                          IN audit_log_message TEXT,
                                          IN cascade_transaction TINYINT(1))
BEGIN
    DECLARE srv_id BIGINT(20);
    IF @disable_audit IS NULL OR @disable_audit = 0 THEN
        SELECT id INTO srv_id FROM dhcp4_server WHERE tag = server_tag;
        INSERT INTO dhcp4_audit_revision (modification_ts, server_id, log_message)
            VALUES (audit_ts, srv_id, audit_log_message);
        SET @audit_revision_id = LAST_INSERT_ID();
        SET @cascade_transaction = cascade_transaction;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `createAuditRevisionDHCP6` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`!db_user!`@`localhost` PROCEDURE `createAuditRevisionDHCP6`(IN audit_ts TIMESTAMP,
                                          IN server_tag VARCHAR(256),
                                          IN audit_log_message TEXT,
                                          IN cascade_transaction TINYINT(1))
BEGIN
    DECLARE srv_id BIGINT(20);
    IF @disable_audit IS NULL OR @disable_audit = 0 THEN
        SELECT id INTO srv_id FROM dhcp6_server WHERE tag = server_tag;
        INSERT INTO dhcp6_audit_revision (modification_ts, server_id, log_message)
            VALUES (audit_ts, srv_id, audit_log_message);
        SET @audit_revision_id = LAST_INSERT_ID();
        SET @cascade_transaction = cascade_transaction;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `createOptionAuditDHCP4` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`!db_user!`@`localhost` PROCEDURE `createOptionAuditDHCP4`(IN modification_type VARCHAR(32),
                                        IN scope_id TINYINT(3) UNSIGNED,
                                        IN option_id BIGINT(20) UNSIGNED,
                                        IN subnet_id INT(10) UNSIGNED,
                                        IN host_id INT(10) UNSIGNED,
                                        IN network_name VARCHAR(128),
                                        IN pool_id BIGINT(20),
                                        IN modification_ts TIMESTAMP)
BEGIN
    DECLARE snid VARCHAR(128);
    DECLARE sid INT(10) UNSIGNED;
    IF @cascade_transaction IS NULL OR @cascade_transaction = 0 THEN
        IF scope_id = 0 THEN
            CALL createAuditEntryDHCP4('dhcp4_options', option_id, modification_type);
        ELSEIF scope_id = 1 THEN
            UPDATE dhcp4_subnet AS s SET s.modification_ts = modification_ts
                WHERE s.subnet_id = subnet_id;
        ELSEIF scope_id = 4 THEN
           SELECT id INTO snid FROM dhcp4_shared_network WHERE name = network_name LIMIT 1;
           UPDATE dhcp4_shared_network AS n SET n.modification_ts = modification_ts
                WHERE n.id = snid;
        ELSEIF scope_id = 5 THEN
            SELECT dhcp4_pool.subnet_id INTO sid FROM dhcp4_pool WHERE id = pool_id;
            UPDATE dhcp4_subnet AS s SET s.modification_ts = modification_ts
                WHERE s.subnet_id = sid;
        END IF;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `createOptionAuditDHCP6` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`!db_user!`@`localhost` PROCEDURE `createOptionAuditDHCP6`(IN modification_type VARCHAR(32),
                                        IN scope_id TINYINT(3) UNSIGNED,
                                        IN option_id BIGINT(20) UNSIGNED,
                                        IN subnet_id INT(10) UNSIGNED,
                                        IN host_id INT(10) UNSIGNED,
                                        IN network_name VARCHAR(128),
                                        IN pool_id BIGINT(20),
                                        IN pd_pool_id BIGINT(20),
                                        IN modification_ts TIMESTAMP)
BEGIN
    DECLARE snid VARCHAR(128);
    DECLARE sid INT(10) UNSIGNED;
    IF @cascade_transaction IS NULL OR @cascade_transaction = 0 THEN
        IF scope_id = 0 THEN
            CALL createAuditEntryDHCP6('dhcp6_options', option_id, modification_type);
        ELSEIF scope_id = 1 THEN
            UPDATE dhcp6_subnet AS s SET s.modification_ts = modification_ts
                WHERE s.subnet_id = subnet_id;
        ELSEIF scope_id = 4 THEN
           SELECT id INTO snid FROM dhcp6_shared_network WHERE name = network_name LIMIT 1;
           UPDATE dhcp6_shared_network AS n SET n.modification_ts = modification_ts
               WHERE n.id = snid;
        ELSEIF scope_id = 5 THEN
            SELECT dhcp6_pool.subnet_id INTO sid FROM dhcp6_pool WHERE id = pool_id;
            UPDATE dhcp6_subnet AS s SET s.modification_ts = modification_ts
                WHERE s.subnet_id = sid;
        ELSEIF scope_id = 6 THEN
            SELECT dhcp6_pd_pool.subnet_id INTO sid FROM dhcp6_pd_pool WHERE id = pd_pool_id;
            UPDATE dhcp6_subnet AS s SET s.modification_ts = modification_ts
                WHERE s.subnet_id = sid;
        END IF;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `lease4DumpData` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`!db_user!`@`localhost` PROCEDURE `lease4DumpData`()
BEGIN
SELECT
    INET_NTOA(l.address),
    IFNULL(HEX(l.hwaddr), ''),
    IFNULL(HEX(l.client_id), ''),
    l.valid_lifetime,
    l.expire,
    l.subnet_id,
    l.fqdn_fwd,
    l.fqdn_rev,
    l.hostname,
    s.name,
    IFNULL(l.user_context, '')
FROM
    lease4 l
    LEFT OUTER JOIN lease_state s on (l.state = s.state)
ORDER BY l.address;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `lease4DumpHeader` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`!db_user!`@`localhost` PROCEDURE `lease4DumpHeader`()
BEGIN
SELECT 'address,hwaddr,client_id,valid_lifetime,expire,subnet_id,fqdn_fwd,fqdn_rev,hostname,state,user_context';
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `lease6DumpData` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`!db_user!`@`localhost` PROCEDURE `lease6DumpData`()
BEGIN
SELECT
    l.address,
    IFNULL(HEX(l.duid), ''),
    l.valid_lifetime,
    l.expire,
    l.subnet_id,
    l.pref_lifetime,
    IFNULL(t.name, ''),
    l.iaid,
    l.prefix_len,
    l.fqdn_fwd,
    l.fqdn_rev,
    l.hostname,
    IFNULL(HEX(l.hwaddr), ''),
    IFNULL(l.hwtype, ''),
    IFNULL(h.name, ''),
    IFNULL(s.name, ''),
    IFNULL(l.user_context, '')
FROM lease6 l
    left outer join lease6_types t on (l.lease_type = t.lease_type)
    left outer join lease_state s on (l.state = s.state)
    left outer join lease_hwaddr_source h on (l.hwaddr_source = h.hwaddr_source)
ORDER BY l.address;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `lease6DumpHeader` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`!db_user!`@`localhost` PROCEDURE `lease6DumpHeader`()
BEGIN
SELECT 'address,duid,valid_lifetime,expire,subnet_id,pref_lifetime,lease_type,iaid,prefix_len,fqdn_fwd,fqdn_rev,hostname,hwaddr,hwtype,hwaddr_source,state,user_context';
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-02-17  5:13:05
