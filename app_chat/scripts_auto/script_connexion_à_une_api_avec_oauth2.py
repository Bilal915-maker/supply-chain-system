
import requests

def connecter_api_github():
    url = 'https://api.github.com/user'
    headers = {
        'Authorization': 'Bearer your_github_token_here'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Connexion réussie à l'API GitHub!")
        print(response.json())  # Affiche les informations du compte GitHub
    else:
        print("Erreur de connexion à l'API GitHub")

connecter_api_github()
