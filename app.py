from http.server import BaseHTTPRequestHandler, HTTPServer
import mysql.connector
from urllib.parse import parse_qs
import json
import smtplib
from email.message import EmailMessage

# =========================
# 1️⃣ FONCTION EMAIL
# =========================
def send_confirmation_email(to_email, fullname, langage, pack):
    msg = EmailMessage()
    msg["Subject"] = "Confirmation de réservation - MeilleurProf"
    msg["From"] = "pandengomar@gmail.com"
    msg["To"] = to_email

    msg.set_content(f"""
Bonjour {fullname},

Votre réservation a été confirmée avec succès ✅

Langue : {langage}
Pack : {pack}

Merci de votre confiance.
MeilleurProf | Langues Africaines
""")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("pandengomar@gmail.com", "gwbjewyhuqfvtsuq")
            smtp.send_message(msg)
            print("✅ Email envoyé")
    except Exception as e:
        print("❌ Erreur email :", e)

# =========================
# 2️⃣ CONFIG BASE DE DONNÉES
# =========================
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "meilleurprof"
}

# =========================
# 3️⃣ SERVEUR HTTP
# =========================
class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/reserve":
            try:
                length = int(self.headers.get("Content-Length", 0))
                post_data = self.rfile.read(length).decode()
                data = parse_qs(post_data)

                fullname = data.get("fullname", [""])[0]
                email = data.get("email", [""])[0]
                langage = data.get("langage", [""])[0]
                pack = data.get("pack", [""])[0]

                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()

                sql = """
                    INSERT INTO reservations (fullname, email, langage, pack)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (fullname, email, langage, pack))
                conn.commit()

                cursor.close()
                conn.close()

                # 📩 envoi email APRÈS insertion
                send_confirmation_email(email, fullname, langage, pack)

                response = {"status": "success", "message": "Réservation réussie"}

            except Exception as e:
                response = {"status": "error", "message": str(e)}

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

# =========================
# 4️⃣ TEST EMAIL (TEMPORAIRE)
# =========================
send_confirmation_email(
    "pandengomar@gmail.com",
    "Test User",
    "Test Langue",
    "Test Pack"
)

# =========================
# 5️⃣ LANCEMENT SERVEUR
# =========================
server = HTTPServer(("localhost", 8000), Handler)
print("Serveur lancé sur http://localhost:8000")
server.serve_forever()