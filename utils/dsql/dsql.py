import mariadb as db
import sys

# Wenn True, wird die lokale Datenbank verwendet, wenn "False" dann wird die Test-Datenbank verwendet 
use_pi_mode = False
enable_logging = False

# Erstelle den Datenbank Connector
def createDatabaseService():
    global use_pi_mode
    if use_pi_mode is True:
        conn = db.connect(
            user="root",
            password="root",
            host="127.0.0.1",
            port=3306,
            database="rfid_ex"
        )
        return conn
    else:
        conn = db.connect(
            user="root",
            password="",
            host="127.0.0.1",
            port=3306,
            database="rfid_pi"
        )
        return conn

# Erstelle eine Abfrage, welche einen Abfragecursor mit dem Result return 
def query(sql):
    with createDatabaseService() as con:
        with con.cursor() as cur:
            if enable_logging == True:
                print(f'[LOG] - {sql}')
            cur.execute(sql)
            return cur.fetchall()

# Führt ein execute Statment aus(INSERT, UPDATE) - commands welche keinen direkten Result zurück geben
# Schließt nach dem ausführen die Transaktion der aktuellen Verbindung
def execute(sql):
    with createDatabaseService() as con:
        with con.cursor() as cur:
            if enable_logging == True:
                print(f'[LOG] - {sql}')
                cur.execute(sql)
            con.commit()