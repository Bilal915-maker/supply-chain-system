import os
import subprocess
import sys
import traceback
import random
import requests
import pickle

class AutoAmelioration:
    def __init__(self, dossier_scripts="scripts_auto", fichier_memoire="memoire.pkl"):
        self.dossier_scripts = dossier_scripts
        self.fichier_memoire = fichier_memoire
        self.memoire = self.charger_memoire()
        if not os.path.exists(self.dossier_scripts):
            os.makedirs(self.dossier_scripts)

    def creer_script(self, nom_script, code):
        """Crée un script Python dans le dossier dédié"""
        chemin = os.path.join(self.dossier_scripts, nom_script + ".py")
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"[AutoAmelioration] Script créé : {chemin}")
        return chemin

    def executer_script(self, chemin_script):
        """Exécute un script Python et capture les erreurs"""
        try:
            result = subprocess.run([sys.executable, chemin_script],
                                    capture_output=True, text=True, check=True)
            print(f"[AutoAmelioration] Résultat :\n{result.stdout}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"[AutoAmelioration] Erreur : {e.stderr}")
            return e.stderr

    def tester_et_importer(self, nom_script):
        """Importe un script pour vérifier qu’il est valide avec exec"""
        try:
            chemin_script = os.path.join(self.dossier_scripts, nom_script + ".py")
            with open(chemin_script, "r", encoding="utf-8") as file:
                code = file.read()
                exec(code)  # Exécute le code du script
            print(f"[AutoAmelioration] Script importé et exécuté avec succès : {nom_script}")
            return True
        except Exception as e:
            print(f"[AutoAmelioration] Échec import : {traceback.format_exc()}")
            return False

    def charger_memoire(self):
        """Charge la mémoire des compétences acquises"""
        if os.path.exists(self.fichier_memoire):
            with open(self.fichier_memoire, "rb") as f:
                return pickle.load(f)
        return {}

    def sauvegarder_memoire(self):
        """Sauvegarde la mémoire des compétences acquises"""
        with open(self.fichier_memoire, "wb") as f:
            pickle.dump(self.memoire, f)

    def detecter_limite_avec_recherche(self, problematique):
        """Détecte la limite d'une tâche donnée et génère une solution automatiquement"""
        if problematique in self.memoire:
            print(f"[AutoAmelioration] Compétence déjà acquise pour {problematique}.")
        else:
            print(f"[AutoAmelioration] Problématique détectée : {problematique}")
            solution = self.rechercher_solution(problematique)
            if solution:
                nom_script = f"script_{problematique.replace(' ', '_').lower()}"
                self.creer_script(nom_script, solution)
                chemin_script = os.path.join(self.dossier_scripts, nom_script + ".py")
                self.executer_script(chemin_script)
                self.tester_et_importer(nom_script)
                self.memoire[problematique] = True  # Enregistre la compétence acquise
                self.sauvegarder_memoire()

    def rechercher_solution(self, problematique):
        """Recherche une solution sur Internet (ici, un exemple simple avec requests)"""
        try:
            query = f"comment {problematique}"
            response = requests.get(f"https://www.google.com/search?q={query}")
            if response.status_code == 200:
                # Exemple de solution valide avec l'API GitHub
                solution = f"""
import requests

def connecter_api_github():
    url = 'https://api.github.com/user'
    headers = {{
        'Authorization': 'Bearer your_github_token_here'
    }}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Connexion réussie à l'API GitHub!")
        print(response.json())  # Affiche les informations du compte GitHub
    else:
        print("Erreur de connexion à l'API GitHub")

connecter_api_github()
"""
                return solution
            else:
                print(f"[AutoAmelioration] Recherche échouée pour {problematique}")
                return None
        except Exception as e:
            print(f"[AutoAmelioration] Erreur de recherche : {traceback.format_exc()}")
            return None

if __name__ == "__main__":
    auto = AutoAmelioration()
    
    # Exemple d'utilisation : détecter un problème inconnu et générer un script pour le résoudre
    auto.detecter_limite_avec_recherche("connexion à une API avec OAuth2")

