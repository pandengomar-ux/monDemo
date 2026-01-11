import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",  # ton mot de passe MySQL
    "database": "meilleurprof"
}

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    print("Connexion MySQL réussie !")
    conn.close()
except mysql.connector.Error as err:
    print("Erreur MySQL :", err)
