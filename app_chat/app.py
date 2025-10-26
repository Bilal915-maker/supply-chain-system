# app.py  — interface web minimale + point d'entrée vers l'agent
from flask import Flask, request, jsonify, render_template, send_from_directory
from agent import Agent

app = Flask(__name__, template_folder="templates", static_folder="static")
agent = Agent()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    message = data.get("message", "")
    # ask agent to process
    result = agent.handle(message)
    return jsonify({"response": result})

@app.route("/upload", methods=["POST"])
def upload():
    # handle file upload (images)
    f = request.files.get("file")
    if not f:
        return jsonify({"error":"No file"}), 400
    filename = f.filename
    path = f"./static/{filename}"
    f.save(path)
    return jsonify({"response": f"Fichier {filename} reçu.", "path": path})

if __name__ == "__main__":
    # port 5001 pour éviter conflits, reloader désactivé pour stabilité
    app.run(debug=True, port=5001, use_reloader=False)
from flask import Flask, request, jsonify, render_template
import webbrowser
import subprocess
import threading

app = Flask(__name__)

# Fonction pour exécuter les commandes
def executer_commande(message):
    response = ""
    msg = message.lower()
    
    if "ouvre google" in msg:
        webbrowser.open("https://www.google.com")
        response = "J'ai ouvert Google pour toi."
    elif "cherche" in msg:
        mot_cle = msg.split("cherche")[-1].strip()
        webbrowser.open(f"https://www.google.com/search?q={mot_cle}")
        response = f"J'ai cherché '{mot_cle}' sur Google."
    elif "ouvre youtube" in msg:
        webbrowser.open("https://www.youtube.com")
        response = "J'ai ouvert YouTube."
    elif "liste fichiers" in msg:
        fichiers = subprocess.getoutput("ls")
        response = f"Voici les fichiers dans le dossier: {fichiers}"
    else:
        response = f"Je suis Natacha, j'ai reçu : {message}"
    
    return response

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    response = executer_commande(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    return jsonify({"response": f"Je suis Natacha, j'ai reçu : {user_input}"})

if __name__ == "__main__":
    # FORCER le port à 5001 et désactiver le reloader
    app.run(debug=True, port=5001, use_reloader=False)
from flask import Flask, request, jsonify

app = Flask(__name__)

# Fonction de base pour répondre aux messages
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    # Ici on pourra ajouter la compréhension du langage naturel + actions automatiques
    response = f"Je suis Natacha, j'ai reçu : {user_input}"
    return jsonify({"response": response})

if __name__ == "__main__":
    # Utiliser le port 5001 pour éviter les conflits
    app.run(debug=True, port=5001)
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Récupère le message envoyé
        user_input = request.json["message"]
        
        # Retourne une réponse formatée
        return jsonify({"response": f"Je suis Natacha, j'ai reçu : {user_input}"})
    except Exception as e:
        # En cas d'erreur, retourne un message d'erreur
        return jsonify({"error": f"Une erreur est survenue : {str(e)}"}), 400

if __name__ == "__main__":
    # Lance l'application Flask sur le port 5000
    app.run(debug=True)
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    return jsonify({"response": f"Je suis Natacha, j'ai reçu : {user_input}"})

if __name__ == "__main__":
    app.run(debug=True)

