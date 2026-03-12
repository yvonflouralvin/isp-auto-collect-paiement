import requests
from datetime import date, timedelta
import os

# -----------------------------
# Config
# -----------------------------
# -----------------------------
# Config depuis variables d'environnement
# -----------------------------

LOGIN_URL = os.environ.get("LOGIN_URL", "https://apiisp.saas.cd/api/apps/auth/login/")
SYNC_URL = os.environ.get("SYNC_URL", "https://apiisp.saas.cd/api/apps/isp_stage/sync-isp-paiements/")
USERNAME = os.environ.get("USERNAME", "chargerecherchebiologie@email.com")
PASSWORD = os.environ.get("PASSWORD", "1234")
INTERVAL_SECONDS = int(os.environ.get("INTERVAL_SECONDS", 5 * 60))  # 5 minutes par défaut

# Dates de début et fin pour le script historique
START_DATE_STR = os.environ.get("START_DATE", "2026-01-01")
END_DATE_STR = os.environ.get("END_DATE", "2026-03-30")

# Convertir les strings en objets date
START_DATE = date.fromisoformat(START_DATE_STR)
END_DATE = date.fromisoformat(END_DATE_STR)


# -----------------------------
# 1️⃣ Authentification
# -----------------------------
login_payload = {
    "username": USERNAME,
    "password": PASSWORD
}

login_response = requests.post(LOGIN_URL, json=login_payload)

if login_response.status_code != 200:
    print("Erreur d'authentification :", login_response.text)
    exit(1)

tokens = login_response.json()
access_token = tokens.get("access")

if not access_token:
    print("Impossible de récupérer le token d'accès")
    exit(1)

headers = {
    "Authorization": f"Bearer {access_token}"
}

print("✅ Authentification réussie, token récupéré !")

# -----------------------------
# 2️⃣ Collecte des paiements
# -----------------------------
current_date = START_DATE
total_records = 0

while current_date <= END_DATE:
    payload = {
        "date": current_date.strftime("%Y-%m-%d")
    }

    response = requests.post(SYNC_URL, json=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()
        saved = result.get("records_saved", 0)
        print(f"{current_date}: {saved} paiements enregistrés")
        total_records += saved
    else:
        print(f"{current_date}: Erreur {response.status_code} -> {response.text}")

    current_date += timedelta(days=1)

print(f"\n✅ Synchronisation terminée. Total de paiements enregistrés: {total_records}")