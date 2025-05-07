from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from typing import List
import os

app = FastAPI()

# Modèle de données
class Personnage(BaseModel):
    nom: str
    score: int

# Fichier de stockage
WEBHOOK_LOG = "webhook_log.json"

@app.post("/webhook/personnage")
async def recevoir_personnage(p: Personnage):
    # Étape 1 : Ajout du champ niveau
    niveau = "Débutant" if p.score < 50 else "Intermédiaire" if p.score < 80 else "Expert"
    personnage_enrichi = {**p.dict(), "niveau": niveau}
    
    # Étape 2 : Enregistrement dans le fichier JSON
    try:
        donnees_existantes = []
        if os.path.exists(WEBHOOK_LOG):
            with open(WEBHOOK_LOG, "r") as f:
                donnees_existantes = json.load(f)
        
        donnees_existantes.append(personnage_enrichi)
        
        with open(WEBHOOK_LOG, "w") as f:
            json.dump(donnees_existantes, f, indent=2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur fichier: {str(e)}")
    
    # Étape 3 : Notification (simulée)
    print(f"Notification: Nouveau personnage {p.nom} (niveau: {niveau})")
    
    return {
        "message": "Personnage enregistré avec succès",
        "data": personnage_enrichi
    }