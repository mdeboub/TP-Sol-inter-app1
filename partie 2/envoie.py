import json
import time
import requests
from tqdm import tqdm

# 1. Lecture des données JSON
with open("organisations_chat.json", "r") as f:
    data = json.load(f)

# Préparer logs
log_file = open("log_envois.txt", "w", encoding="utf-8")

# 2. Transformation des données
donnees_transformees = []
for item in data:
    nouveau = {
        "nom": item.get("name", "Inconnu"),  # Renommage
        "ville": item.get("city", "Sans Ville"),
    }

    # Exemple de critère : si le nom contient "Chad" ou autre critère
    if "Chad" in nouveau["nom"]:
        nouveau["avis"] = "positif"
    elif "Center" in nouveau["nom"]:
        nouveau["avis"] = "neutre"
    else:
        nouveau["avis"] = "négatif"

    donnees_transformees.append(nouveau)

# 3. Envoi des données à l’API
url = "http://127.0.0.1:8000/scores"
headers = {
    "Content-Type": "application/json",
    # "Authorization": "Bearer VOTRE_TOKEN",  # si nécessaire
}

for item in tqdm(donnees_transformees, desc="Envoi des données à l'API..."):
    try:
        response = requests.post(url, headers=headers, json=item)
        if response.status_code == 200:
            log_file.write(f"✅ Succès : {item['nom']} à {item['ville']}\n")
        else:
            log_file.write(f"❌ Échec ({response.status_code}) : {item['nom']}\n")
    except Exception as e:
        log_file.write(f"⚠️ Erreur exception : {item['nom']} - {str(e)}\n")

    time.sleep(0.5)  # Pour éviter de saturer le serveur

log_file.close()
print("Tous les envois ont été traités. Voir log_envois.txt pour les détails.")
