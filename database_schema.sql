/*
	Dieses Script agiert nach einem sogennanten "Patch-Schema"
	Die verschiedenen Komponenten(Spalten, Tabellen, Views oder Trigger) werden nach Versionierungen erstellt.
	Die Initialversion beginnt mit der 1.0.0
	
	Versionierung:
	1.0.0
	Major, Patch, Fix
	
*/

-- #################### 1.0.0 ####################  
-- Nutzertabelle
CREATE TABLE nutzer (id VARCHAR(64) NOT NULL PRIMARY KEY);
ALTER TABLE nutzer ADD vorname VARCHAR(64);
ALTER TABLE nutzer ADD nachname VARCHAR(64);
ALTER TABLE nutzer ADD email VARCHAR(128);
ALTER TABLE nutzer ADD transponder VARCHAR(64);

-- View zum Helfen von "komplexen Abfragen" ;)
CREATE OR REPLACE VIEW user_operations(user_count) AS
	(SELECT COUNT(id) AS user_count FROM nutzer);

-- #################### 1.1.0 ####################

--	# Syntax anpassungen
ALTER TABLE nutzer DROP transponder;
ALTER TABLE nutzer ADD transponder_id VARCHAR(64);

-- Transponder Tabelle
CREATE TABLE transponder (id VARCHAR(64) NOT NULL PRIMARY KEY);
ALTER TABLE transponder ADD gesperrt BIT;

--	# Fügt einen Fremdschlüssel unter dem Namen (Constraint): nutzer_transponder_fk hinzu
ALTER TABLE nutzer
ADD CONSTRAINT nutzer_transponder_fk
FOREIGN KEY (transponder_id) 
	REFERENCES transponder(id)
	ON DELETE SET NULL 
	ON UPDATE SET NULL;

-- Transponder Historien Tabelle
CREATE TABLE transponder_historie(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY);
ALTER TABLE transponder_historie ADD transponder_id VARCHAR(64);
ALTER TABLE transponder_historie ADD erfassungsdatum TIMESTAMP;
ALTER TABLE transponder_historie ADD aktion TEXT;
	
--	# Wenn kein "gesperrt" mit übergeben wurde, wird dieser automatisch auf "0" gesetzt
ALTER TABLE transponder MODIFY gesperrt BIT NOT NULL DEFAULT 0;
--	# Standardmäßig wird hier der aktuelle Zeitpunkt eingetragen
ALTER TABLE transponder_historie MODIFY erfassungsdatum TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;

-- ############### 1.1.1 #################
ALTER TABLE nutzer ADD nutzer_no VARCHAR(64) AFTER id;
ALTER TABLE transponder MODIFY gesperrt BOOL DEFAULT 0; -- Da python einen BIT Datentyp als "\b'x01'" ansieht -> bool

-- ############### 1.2.0 #################
CREATE TABLE gebaeude(id VARCHAR(64) PRIMARY KEY);
ALTER TABLE gebaeude ADD beschreibung VARCHAR(512);

CREATE TABLE raum (id VARCHAR(64) PRIMARY KEY);
ALTER TABLE raum ADD beschreibung VARCHAR(512);
ALTER TABLE raum ADD gebaeude_id VARCHAR(64);

ALTER TABLE raum
ADD CONSTRAINT gebaeude_raum_fk
FOREIGN KEY (gebaeude_id) 
	REFERENCES gebaeude(id)
	ON DELETE SET NULL 
	ON UPDATE SET NULL;
	
CREATE TABLE tuer (id VARCHAR(64) PRIMARY KEY);
ALTER TABLE tuer ADD beschreibung VARCHAR(512);
ALTER TABLE tuer ADD raum_id VARCHAR(64);

ALTER TABLE tuer
ADD CONSTRAINT tuer_raum_fk
FOREIGN KEY (raum_id) 
	REFERENCES raum(id)
	ON DELETE SET NULL 
	ON UPDATE SET NULL;

DROP VIEW user_operations;
CREATE OR REPLACE VIEW jperations AS SELECT
	(SELECT COUNT(id) AS user_count FROM nutzer) AS count_user,
	(SELECT SUM((SELECT COUNT(id) FROM gebaeude) + (SELECT COUNT(id) FROM raum) + (SELECT COUNT(id) FROM tuer))) AS total_objects,
	(SELECT COUNT(id) FROM gebaeude) AS count_gebaeude,
	(SELECT COUNT(id) FROM raum) AS count_raum,
	(SELECT COUNT(id) FROM tuer) AS count_tuer;
	
-- ############### 1.3.0 #################
CREATE TABLE gruppe (id VARCHAR(64) PRIMARY KEY);
ALTER TABLE gruppe ADD `name` VARCHAR(128);

CREATE OR REPLACE VIEW jperations AS SELECT
	(SELECT COUNT(id) AS user_count FROM nutzer) AS count_user,
	(SELECT SUM((SELECT COUNT(id) FROM gebaeude) + (SELECT COUNT(id) FROM raum) + (SELECT COUNT(id) FROM tuer))) AS total_objects,
	(SELECT COUNT(id) FROM gebaeude) AS count_gebaeude,
	(SELECT COUNT(id) FROM raum) AS count_raum,
	(SELECT COUNT(id) FROM tuer) AS count_tuer,
	(SELECT COUNT(id) FROM gruppe) AS count_gruppe;

-- ############### 1.3.1 #################
ALTER TABLE gruppe ADD group_no VARCHAR(64) AFTER id;

-- ############### 1.4.0 #################
CREATE TABLE gruppe_tuer_zugriff(
	tuer_id VARCHAR(64),
	gruppen_id VARCHAR(64),
	erlaubt BOOL,
	CONSTRAINT tuer_gruppe_fk FOREIGN KEY (tuer_id) REFERENCES tuer(id),
	CONSTRAINT gruppe_tuer_fk FOREIGN KEY (gruppen_id) REFERENCES gruppe(id)
);

CREATE TABLE nutzer_tuer_zugriff(
	tuer_id VARCHAR(64),
	nutzer_id VARCHAR(64),
	erlaubt BOOL,
	CONSTRAINT tuer_nutzer_fk FOREIGN KEY (tuer_id) REFERENCES tuer(id),
	CONSTRAINT nutzer_tuer_fk FOREIGN KEY (nutzer_id) REFERENCES nutzer(id)
);

CREATE TABLE nutzer_gruppen(
	gruppen_id VARCHAR(64),
	nutzer_id VARCHAR(64),
	CONSTRAINT gruppen_nutzer_fk FOREIGN KEY (gruppen_id) REFERENCES gruppe(id),
	CONSTRAINT nutzer_gruppen_fk FOREIGN KEY (nutzer_id) REFERENCES nutzer(id)
);

-- ############### 1.5.0 #################
CREATE TABLE tuer_zugriff_historie(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY);
ALTER TABLE tuer_zugriff_historie ADD tuer_id VARCHAR(64);
ALTER TABLE tuer_zugriff_historie ADD zeitstempel TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE tuer_zugriff_historie ADD nutzer_id VARCHAR(64);
ALTER TABLE tuer_zugriff_historie ADD information TEXT;

ALTER TABLE tuer_zugriff_historie
ADD CONSTRAINT tuer_historie_fk
FOREIGN KEY (tuer_id) 
	REFERENCES tuer(id)
	ON DELETE SET NULL 
	ON UPDATE SET NULL;

ALTER TABLE tuer_zugriff_historie
ADD CONSTRAINT nutzer_tuer_zugriff_historie
FOREIGN KEY (nutzer_id) 
	REFERENCES nutzer(id)
	ON DELETE SET NULL 
	ON UPDATE SET NULL;
	
-- ############### 1.6.0 #################
-- Administrator - Darf alles
CREATE USER IF NOT EXISTS 'administrator'@'%' IDENTIFIED BY 'administrator';
GRANT EXECUTE, SELECT, SHOW VIEW, ALTER, ALTER ROUTINE, CREATE, CREATE ROUTINE, CREATE TEMPORARY TABLES, CREATE VIEW, DELETE, DROP, EVENT, INDEX, INSERT, REFERENCES, TRIGGER, UPDATE, LOCK TABLES  ON * TO 'personalmanager'@'%' WITH GRANT OPTION;

-- Personalmanager - Darf die nutzer/Gruppen/Transponder und Tür_Zugriff Historie auslesen 
CREATE USER IF NOT EXISTS 'personalmanager'@'%' IDENTIFIED BY 'personal';
GRANT SELECT, SHOW VIEW  ON TABLE tuer_zugriff_historie TO 'personalmanager'@'%';
GRANT SELECT ON TABLE gruppe TO 'personalmanager'@'%';
GRANT SELECT ON TABLE nutzer TO 'personalmanager'@'%';
GRANT SELECT ON TABLE nutzer_gruppen TO 'personalmanager'@'%';
GRANT SELECT ON TABLE transponder TO 'personalmanager'@'%';

-- Tuersteuerung - Darf lesen/löschen/hinzufügen
create user if not exists 'tuersteuerung'@'%' IDENTIFIED by 'tuersteuerung';
GRANT SELECT, show View, create, INSERT, UPDATE, DELETE, REFERENCES ON *.* TO 'tuersteuerung'@'%';