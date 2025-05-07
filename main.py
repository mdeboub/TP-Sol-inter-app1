from fastapi import FastAPI, Header, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from typing import Optional

app = FastAPI()

# Configuration CORS (pour accepter les requêtes du frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],  
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"], 
    allow_headers=["X-Auth-Token", "Content-Type"],
)

# Token valide
API_TOKEN = "token_secret_123"

# Modèle de données
class Personnage(BaseModel):
    id: int
    nom: str
    profession: str
    age: int
    univers: str
    score: int  # Ajout du champ score
    niveau: Optional[str] = None  # Ajout du champ niveau

# Données de test
personnages = [
    Personnage(
        id=1,
        nom="Harry Potter",
        profession="Sorcier",
        age=17,
        univers="Harry Potter",
        score=85,
    ),
    Personnage(
         id=2,
        nom="Ron Weasley",
        profession="Sorcier",
        age=17,
        univers="Harry Potter",
        score=75,
    ),
    Personnage(
        id=3,
        nom="Hermione Granger",
        profession="Sorcière",
        age=17,
        univers="Harry Potter",
        score=90,
    ),
    Personnage(
       id=4,
        nom="Albus Dumbledore",
        profession="Directeur de Poudlard",
        age=115,
        univers="Harry Potter",
        score=55,
    )
]

@app.get("/personnages", response_model=List[Personnage])
def get_personnages(
    token: str = Header(..., alias="x-auth-token"),
    prenom: Optional[str] = None
):
    if token != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide"
        )
    
    # Filtrage si le prénom est spécifié
    if prenom:
        return [p for p in personnages if p.nom.lower().startswith(prenom.lower())]
    
    return personnages

class Feedback(BaseModel):
    nom: str
    ville: str
    avis: str

@app.post("/scores")
def post_score(feedback: Feedback):
    print("Reçu :", feedback)
    return {"message": "Succès", "data": feedback}

# Endpoint /traitement
@app.post("/traitement")
async def traitement(personnages: List[Personnage]):
    # Calcul du niveau basé sur le score
    for personnage in personnages:
        if personnage.score >= 80:
            personnage.niveau = "expert"
        elif personnage.score >= 60:
            personnage.niveau = "intermédiaire"
        else:
            personnage.niveau = "débutant"
    
    # Retourne les données avec le niveau ajouté
    return personnages
