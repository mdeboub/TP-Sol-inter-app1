from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
import json
import os

class Niveau(str, Enum):
    FAIBLE = "Faible"
    MOYEN = "Moyen"
    FORT = "Fort"

class PersonnageInput(BaseModel):
    nom: str
    score: int

class PersonnageOutput(PersonnageInput):
    niveau: Niveau

def calculer_niveau(score: int) -> Niveau:
    if score < 50:
        return Niveau.FAIBLE
    elif score < 80:
        return Niveau.MOYEN
    else:
        return Niveau.FORT
def archiver_personnage(personnage: PersonnageOutput, fichier="webhook_log.json"):
    data = []
    if os.path.exists(fichier):
        try:
            with open(fichier, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            pass
    data.append(personnage.dict())
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def enregistrer_notification(message: str, fichier="notifications.txt"):
    with open(fichier, "a", encoding="utf-8") as f:
        f.write(message + "\n")
app = FastAPI()
notifications_activées = {"active": True}

@app.post("/webhook/personnage", response_model=PersonnageOutput)
def recevoir_personnage(p: PersonnageInput):
    niveau = calculer_niveau(p.score)
    personnage = PersonnageOutput(**p.dict(), niveau=niveau)
    archiver_personnage(personnage)
    print("✅ Personnage ajouté avec succès !")

    if notifications_activées["active"]:
        notifier(personnage)

    return personnage

@app.post("/notifier")
def notifier(personnage: PersonnageOutput):
    message = f"📣 Nouveau personnage : {personnage.nom} - Niveau {personnage.niveau}"
    print(message)
    enregistrer_notification(message)
    return {"message": "Notification envoyée"}

@app.post("/subscribe")
def subscribe(active: bool):
    notifications_activées["active"] = active
    return {"message": f"Notifications {'activées' if active else 'désactivées'}"}
