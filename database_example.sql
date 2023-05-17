-- --------------------------------------------------------
-- Host:                         10.254.6.225
-- Server Version:               10.5.15-MariaDB-0+deb11u1 - Raspbian 11
-- Server Betriebssystem:        debian-linux-gnueabihf
-- HeidiSQL Version:             11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Exportiere Datenbank Struktur für rfid_ex
CREATE DATABASE IF NOT EXISTS `rfid_ex` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `rfid_ex`;

-- Exportiere Struktur von Tabelle rfid_ex.gebaeude
CREATE TABLE IF NOT EXISTS `gebaeude` (
  `id` varchar(64) NOT NULL,
  `beschreibung` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Exportiere Daten aus Tabelle rfid_ex.gebaeude: ~2 rows (ungefähr)
DELETE FROM `gebaeude`;
/*!40000 ALTER TABLE `gebaeude` DISABLE KEYS */;
INSERT INTO `gebaeude` (`id`, `beschreibung`) VALUES
	('1', 'Schule'),
	('2', 'Schule-2');
/*!40000 ALTER TABLE `gebaeude` ENABLE KEYS */;

-- Exportiere Struktur von Tabelle rfid_ex.gruppe
CREATE TABLE IF NOT EXISTS `gruppe` (
  `id` varchar(64) NOT NULL,
  `group_no` varchar(64) DEFAULT NULL,
  `name` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Exportiere Daten aus Tabelle rfid_ex.gruppe: ~0 rows (ungefähr)
DELETE FROM `gruppe`;
/*!40000 ALTER TABLE `gruppe` DISABLE KEYS */;
INSERT INTO `gruppe` (`id`, `group_no`, `name`) VALUES
	('080b9a67-6c3d-4bdf-ae6c-78a9855a957a', '001', 'Admin');
/*!40000 ALTER TABLE `gruppe` ENABLE KEYS */;

-- Exportiere Struktur von Tabelle rfid_ex.gruppe_tuer_zugriff
CREATE TABLE IF NOT EXISTS `gruppe_tuer_zugriff` (
  `tuer_id` varchar(64) DEFAULT NULL,
  `gruppen_id` varchar(64) DEFAULT NULL,
  KEY `tuer_gruppe_fk` (`tuer_id`),
  KEY `gruppe_tuer_fk` (`gruppen_id`),
  CONSTRAINT `gruppe_tuer_fk` FOREIGN KEY (`gruppen_id`) REFERENCES `gruppe` (`id`),
  CONSTRAINT `tuer_gruppe_fk` FOREIGN KEY (`tuer_id`) REFERENCES `tuer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Exportiere Daten aus Tabelle rfid_ex.gruppe_tuer_zugriff: ~0 rows (ungefähr)
DELETE FROM `gruppe_tuer_zugriff`;
/*!40000 ALTER TABLE `gruppe_tuer_zugriff` DISABLE KEYS */;
/*!40000 ALTER TABLE `gruppe_tuer_zugriff` ENABLE KEYS */;

-- Exportiere Struktur von View rfid_ex.jperations
-- Erstelle temporäre Tabelle um View Abhängigkeiten zuvorzukommen
CREATE TABLE `jperations` (
	`count_user` BIGINT(21) NULL,
	`total_objects` DECIMAL(44,0) NULL,
	`count_gebaeude` BIGINT(21) NULL,
	`count_raum` BIGINT(21) NULL,
	`count_tuer` BIGINT(21) NULL,
	`count_gruppe` BIGINT(21) NULL
) ENGINE=MyISAM;

-- Exportiere Struktur von Tabelle rfid_ex.nutzer
CREATE TABLE IF NOT EXISTS `nutzer` (
  `id` varchar(64) NOT NULL,
  `nutzer_no` varchar(64) DEFAULT NULL,
  `vorname` varchar(64) DEFAULT NULL,
  `nachname` varchar(64) DEFAULT NULL,
  `email` varchar(128) DEFAULT NULL,
  `transponder_id` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `nutzer_transponder_fk` (`transponder_id`),
  CONSTRAINT `nutzer_transponder_fk` FOREIGN KEY (`transponder_id`) REFERENCES `transponder` (`id`) ON DELETE SET NULL ON UPDATE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Exportiere Daten aus Tabelle rfid_ex.nutzer: ~1 rows (ungefähr)
DELETE FROM `nutzer`;
/*!40000 ALTER TABLE `nutzer` DISABLE KEYS */;
INSERT INTO `nutzer` (`id`, `nutzer_no`, `vorname`, `nachname`, `email`, `transponder_id`) VALUES
	('1e40436b-6206-4009-861a-bc63305a532b', '1', 'Jason', 'Meyer', 'hsvbuh11@gmail.com', '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ');
/*!40000 ALTER TABLE `nutzer` ENABLE KEYS */;

-- Exportiere Struktur von Tabelle rfid_ex.nutzer_gruppen
CREATE TABLE IF NOT EXISTS `nutzer_gruppen` (
  `gruppen_id` varchar(64) DEFAULT NULL,
  `nutzer_id` varchar(64) DEFAULT NULL,
  KEY `gruppen_nutzer_fk` (`gruppen_id`),
  KEY `nutzer_gruppen_fk` (`nutzer_id`),
  CONSTRAINT `gruppen_nutzer_fk` FOREIGN KEY (`gruppen_id`) REFERENCES `gruppe` (`id`),
  CONSTRAINT `nutzer_gruppen_fk` FOREIGN KEY (`nutzer_id`) REFERENCES `nutzer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Exportiere Daten aus Tabelle rfid_ex.nutzer_gruppen: ~0 rows (ungefähr)
DELETE FROM `nutzer_gruppen`;
/*!40000 ALTER TABLE `nutzer_gruppen` DISABLE KEYS */;
INSERT INTO `nutzer_gruppen` (`gruppen_id`, `nutzer_id`) VALUES
	('080b9a67-6c3d-4bdf-ae6c-78a9855a957a', '1e40436b-6206-4009-861a-bc63305a532b');
/*!40000 ALTER TABLE `nutzer_gruppen` ENABLE KEYS */;

-- Exportiere Struktur von Tabelle rfid_ex.nutzer_tuer_zugriff
CREATE TABLE IF NOT EXISTS `nutzer_tuer_zugriff` (
  `tuer_id` varchar(64) DEFAULT NULL,
  `nutzer_id` varchar(64) DEFAULT NULL,
  `erlaubt` tinyint(1) DEFAULT NULL,
  KEY `tuer_nutzer_fk` (`tuer_id`),
  KEY `nutzer_tuer_fk` (`nutzer_id`),
  CONSTRAINT `nutzer_tuer_fk` FOREIGN KEY (`nutzer_id`) REFERENCES `nutzer` (`id`),
  CONSTRAINT `tuer_nutzer_fk` FOREIGN KEY (`tuer_id`) REFERENCES `tuer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Exportiere Daten aus Tabelle rfid_ex.nutzer_tuer_zugriff: ~0 rows (ungefähr)
DELETE FROM `nutzer_tuer_zugriff`;
/*!40000 ALTER TABLE `nutzer_tuer_zugriff` DISABLE KEYS */;
INSERT INTO `nutzer_tuer_zugriff` (`tuer_id`, `nutzer_id`, `erlaubt`) VALUES
	('2', '1e40436b-6206-4009-861a-bc63305a532b', 1);
/*!40000 ALTER TABLE `nutzer_tuer_zugriff` ENABLE KEYS */;

-- Exportiere Struktur von Tabelle rfid_ex.raum
CREATE TABLE IF NOT EXISTS `raum` (
  `id` varchar(64) NOT NULL,
  `beschreibung` varchar(512) DEFAULT NULL,
  `gebaeude_id` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gebaeude_raum_fk` (`gebaeude_id`),
  CONSTRAINT `gebaeude_raum_fk` FOREIGN KEY (`gebaeude_id`) REFERENCES `gebaeude` (`id`) ON DELETE SET NULL ON UPDATE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Exportiere Daten aus Tabelle rfid_ex.raum: ~3 rows (ungefähr)
DELETE FROM `raum`;
/*!40000 ALTER TABLE `raum` DISABLE KEYS */;
INSERT INTO `raum` (`id`, `beschreibung`, `gebaeude_id`) VALUES
	('S10', 'Test', '1'),
	('S11', 'Hallo-Welt', '2'),
	('S45', 'Computertechnikraum', NULL);
/*!40000 ALTER TABLE `raum` ENABLE KEYS */;

-- Exportiere Struktur von Tabelle rfid_ex.transponder
CREATE TABLE IF NOT EXISTS `transponder` (
  `id` varchar(64) NOT NULL,
  `gesperrt` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Exportiere Daten aus Tabelle rfid_ex.transponder: ~0 rows (ungefähr)
DELETE FROM `transponder`;
/*!40000 ALTER TABLE `transponder` DISABLE KEYS */;
INSERT INTO `transponder` (`id`, `gesperrt`) VALUES
	('\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0', 0),
	('', 0),
	('3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', 0),
	('4123                                            ', 0);
/*!40000 ALTER TABLE `transponder` ENABLE KEYS */;

-- Exportiere Struktur von Tabelle rfid_ex.transponder_historie
CREATE TABLE IF NOT EXISTS `transponder_historie` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `transponder_id` varchar(64) DEFAULT NULL,
  `erfassungsdatum` timestamp NOT NULL DEFAULT current_timestamp(),
  `aktion` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8mb4;

-- Exportiere Daten aus Tabelle rfid_ex.transponder_historie: ~37 rows (ungefähr)
DELETE FROM `transponder_historie`;
/*!40000 ALTER TABLE `transponder_historie` DISABLE KEYS */;
INSERT INTO `transponder_historie` (`id`, `transponder_id`, `erfassungsdatum`, `aktion`) VALUES
	(54, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-11 23:03:21', 'CREATED'),
	(55, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-11 23:03:26', 'MOVED - RECIEVED_001'),
	(56, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-11 23:03:26', 'UNLOCKED - TRANSFER'),
	(57, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-11 23:04:35', 'MOVED - NEW_OWNER_002'),
	(58, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-11 23:04:35', 'MOVED - RECIEVED_002'),
	(59, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-11 23:04:35', 'UNLOCKED - TRANSFER'),
	(60, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-12 17:49:38', 'MOVED - NEW_OWNER_004'),
	(61, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-12 17:49:38', 'MOVED - RECIEVED_004'),
	(62, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-12 17:49:38', 'UNLOCKED - TRANSFER'),
	(63, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-12 17:49:57', 'MOVED - NEW_OWNER_1'),
	(64, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-12 17:49:57', 'MOVED - RECIEVED_1'),
	(65, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-12 17:49:57', 'UNLOCKED - TRANSFER'),
	(66, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-12 18:20:08', 'LOCKED - ACCOUNT DELETION'),
	(67, 'None', '2023-05-12 18:21:16', 'CREATED'),
	(68, '64b35647-f2a0-4cf4-a16b-9815ec282aca', '2023-05-12 18:21:16', 'LOCKED - ACCOUNT DELETION'),
	(69, 'None', '2023-05-12 18:21:48', 'CREATED'),
	(70, '3196e719-67bc-4049-b851-dfef330264e6', '2023-05-12 18:21:48', 'LOCKED - ACCOUNT DELETION'),
	(71, 'None', '2023-05-12 18:21:51', 'CREATED'),
	(72, 'fca63517-ef27-4b62-b14b-8088072969d2', '2023-05-12 18:21:51', 'LOCKED - ACCOUNT DELETION'),
	(73, 'None', '2023-05-12 18:36:43', 'CREATED'),
	(74, 'None', '2023-05-12 18:36:56', 'CREATED'),
	(75, 'None', '2023-05-12 18:36:58', 'CREATED'),
	(76, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-12 18:48:28', 'MOVED - RECIEVED_001'),
	(77, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-12 18:48:28', 'UNLOCKED - TRANSFER'),
	(78, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-12 18:55:50', 'LOCKED'),
	(79, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-12 18:55:54', 'LOCKED'),
	(80, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-12 18:55:57', 'LOCKED'),
	(81, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-12 18:56:11', 'LOCKED'),
	(82, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-12 18:56:17', 'LOCKED'),
	(83, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-12 18:57:35', 'LOCKED'),
	(84, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-12 18:57:54', 'LOCKED'),
	(85, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-12 19:01:37', 'LOCKED'),
	(86, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-12 19:06:02', 'LOCKED'),
	(87, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-12 19:06:04', 'LOCKED'),
	(88, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-12 19:06:04', 'LOCKED'),
	(89, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-12 19:06:05', 'LOCKED'),
	(90, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-12 19:06:05', 'LOCKED'),
	(91, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-12 19:06:06', 'LOCKED'),
	(92, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-12 19:06:06', 'LOCKED'),
	(93, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-15 21:08:18', 'LOCKED'),
	(94, '3e0c94c9-6b5e-44d0-9a13-416d61568d00            ', '2023-05-15 21:08:19', 'UNLOCKED'),
	(95, '', '2023-05-17 10:52:21', 'CREATED'),
	(96, '\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0', '2023-05-17 11:07:15', 'CREATED'),
	(97, '4123                                            ', '2023-05-17 11:37:36', 'CREATED');
/*!40000 ALTER TABLE `transponder_historie` ENABLE KEYS */;

-- Exportiere Struktur von Tabelle rfid_ex.tuer
CREATE TABLE IF NOT EXISTS `tuer` (
  `id` varchar(64) NOT NULL,
  `beschreibung` varchar(512) DEFAULT NULL,
  `raum_id` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tuer_raum_fk` (`raum_id`),
  CONSTRAINT `tuer_raum_fk` FOREIGN KEY (`raum_id`) REFERENCES `raum` (`id`) ON DELETE SET NULL ON UPDATE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Exportiere Daten aus Tabelle rfid_ex.tuer: ~2 rows (ungefähr)
DELETE FROM `tuer`;
/*!40000 ALTER TABLE `tuer` DISABLE KEYS */;
INSERT INTO `tuer` (`id`, `beschreibung`, `raum_id`) VALUES
	('2', 'Test', 'S11'),
	('99', '1', NULL);
/*!40000 ALTER TABLE `tuer` ENABLE KEYS */;

-- Exportiere Struktur von Tabelle rfid_ex.tuer_zugriff_historie
CREATE TABLE IF NOT EXISTS `tuer_zugriff_historie` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tuer_id` varchar(64) DEFAULT NULL,
  `zeitstempel` timestamp NOT NULL DEFAULT current_timestamp(),
  `nutzer_id` varchar(64) DEFAULT NULL,
  `information` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tuer_historie_fk` (`tuer_id`),
  KEY `nutzer_tuer_zugriff_historie` (`nutzer_id`),
  CONSTRAINT `nutzer_tuer_zugriff_historie` FOREIGN KEY (`nutzer_id`) REFERENCES `nutzer` (`id`) ON DELETE SET NULL ON UPDATE SET NULL,
  CONSTRAINT `tuer_historie_fk` FOREIGN KEY (`tuer_id`) REFERENCES `tuer` (`id`) ON DELETE SET NULL ON UPDATE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Exportiere Daten aus Tabelle rfid_ex.tuer_zugriff_historie: ~0 rows (ungefähr)
DELETE FROM `tuer_zugriff_historie`;
/*!40000 ALTER TABLE `tuer_zugriff_historie` DISABLE KEYS */;
/*!40000 ALTER TABLE `tuer_zugriff_historie` ENABLE KEYS */;

-- Exportiere Struktur von View rfid_ex.jperations
-- Entferne temporäre Tabelle und erstelle die eigentliche View
DROP TABLE IF EXISTS `jperations`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `jperations` AS select (select count(`nutzer`.`id`) AS `user_count` from `nutzer`) AS `count_user`,(select sum((select count(`gebaeude`.`id`) from `gebaeude`) + (select count(`raum`.`id`) from `raum`) + (select count(`tuer`.`id`) from `tuer`))) AS `total_objects`,(select count(`gebaeude`.`id`) from `gebaeude`) AS `count_gebaeude`,(select count(`raum`.`id`) from `raum`) AS `count_raum`,(select count(`tuer`.`id`) from `tuer`) AS `count_tuer`,(select count(`gruppe`.`id`) from `gruppe`) AS `count_gruppe`;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
