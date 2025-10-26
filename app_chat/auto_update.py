import subprocess
import schedule
import time

def auto_update():
    # Vérifie régulièrement si une mise à jour est nécessaire
    subprocess.call(["pip", "install", "--upgrade", "flask", "spacy", "transformers"])

# Exécution de la mise à jour automatique tous les jours
schedule.every(1).day.at("00:00").do(auto_update)

while True:
    schedule.run_pending()
    time.sleep(1)

