import requests
from datetime import date
import time

# -----------------------------
# Config depuis variables d'environnement
# -----------------------------
LOGIN_URL = os.environ.get("LOGIN_URL", "https://apiispdev.saas.cd/api/apps/auth/login/")
SYNC_URL = os.environ.get("SYNC_URL", "https://apiispdev.saas.cd/api/apps/isp_stage/sync-isp-paiements/")
USERNAME = os.environ.get("USERNAME", "chargerecherchebiologie@email.com")
PASSWORD = os.environ.get("PASSWORD", "1234")
INTERVAL_SECONDS = int(os.environ.get("INTERVAL_SECONDS", 5 * 60))  # 5 minutes par défaut

# -----------------------------
# Authentification
# -----------------------------
def get_access_token():
    login_payload = {
        "username": USERNAME,
        "password": PASSWORD
    }
    login_response = requests.post(LOGIN_URL, json=login_payload)
    if login_response.status_code != 200:
        print("Erreur d'authentification :", login_response.text)
        return None
    tokens = login_response.json()
    return tokens.get("access")


# -----------------------------
# Collecte des paiements pour aujourd'hui
# -----------------------------
def sync_today_payments(token):
    headers = {"Authorization": f"Bearer {token}"}
    today_str = date.today().strftime("%Y-%m-%d")
    payload = {"date": today_str}

    response = requests.post(SYNC_URL, json=payload, headers=headers)
    if response.status_code == 200:
        result = response.json()
        saved = result.get("records_saved", 0)
        print(f"{today_str}: {saved} paiements enregistrés")
    else:
        print(f"{today_str}: Erreur {response.status_code} -> {response.text}")


# -----------------------------
# Boucle principale
# -----------------------------
def main():
    print("🚀 Démarrage du script de collecte des paiements du jour...")
    token = get_access_token()
    if not token:
        print("Impossible de récupérer le token, arrêt du script.")
        return

    while True:
        try:
            sync_today_payments(token)
        except Exception as e:
            print("Erreur lors de la collecte :", e)

        print(f"⏱ Attente de {INTERVAL_SECONDS // 60} minutes avant la prochaine collecte...\n")
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()