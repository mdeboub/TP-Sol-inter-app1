import requests
import json
import time

def main():
    # 1. Choisir une API paginée
    url_base = "https://projects.propublica.org/nonprofits/api/v2/search.json"
    query = "chat"
    
    # 3. Stocker tous les résultats dans une liste Python
    toutes_donnees = []
    current_page = 0
    max_pages = 100  # Protection contre une boucle infinie
    
    print(f"Extraction des données pour la requête '{query}'...")
    
    # 2. Écrire une boucle while pour appeler chaque page
    while current_page < max_pages:
        url = f"{url_base}?q={query}&page={current_page}"
        print(f"Récupération de la page {current_page}...")
        
        # Appel à l'API
        response = requests.get(url)
        
        # Vérification du code de statut
        if response.status_code != 200:
            print(f"Erreur lors de la requête: Code {response.status_code}")
            break
            
        data = response.json()
        
        # Vérification si on a des résultats
        if "organizations" in data:
            organizations = data["organizations"]
            if not organizations:  # Si la liste est vide, on a atteint la fin
                print("Plus de résultats disponibles.")
                break
                
            # Ajout des résultats à notre liste
            toutes_donnees.extend(organizations)
            print(f"Page {current_page}: {len(organizations)} résultats récupérés")
            
            # Passer à la page suivante
            current_page += 1
            
            # Pause pour éviter les limitations de l'API
            time.sleep(0.5)
        else:
            print("Format de réponse inattendu.")
            break
    
    print(f"Extraction terminée. {len(toutes_donnees)} résultats récupérés au total.")
    
    # 4. Filtrer les données
    print("Filtrage des données...")
    donnees_filtrees = [org for org in toutes_donnees if org.get("city")]
    print(f"Filtrage terminé: {len(donnees_filtrees)} résultats sur {len(toutes_donnees)} conservés.")
    
    # 5. Écrire la liste dans un fichier JSON
    nom_fichier = "organisations_chat.json"
    print(f"Enregistrement des données dans {nom_fichier}...")
    
    with open(nom_fichier, "w", encoding="utf-8") as f:
        json.dump(donnees_filtrees, f, indent=2, ensure_ascii=False)
    
    print(f"Données enregistrées avec succès dans {nom_fichier}")

if __name__ == "__main__":
    main()