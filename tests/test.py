import requests

# Configuration de l'URL et des données
url = "http://127.0.0.1:8000/auth/login"  # Remplacez par l'URL de votre API si nécessaire
data = {
    "username": "hern",  # Remplacez par le nom d'utilisateur
    "password": "password"     # Remplacez par le mot de passe
}

# En-tête spécifiant le type de contenu
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

# Envoi de la requête POST
response = requests.post(url, data=data, headers=headers)

# Affichage des résultats
if response.status_code == 200:
    print("Requête réussie ! Voici le token d'accès :")
    print(response.json())  # Contient 'access_token' et 'token_type'
else:
    print(f"Erreur {response.status_code} :")
    print(response.json())  # Affiche les détails de l'erreur
