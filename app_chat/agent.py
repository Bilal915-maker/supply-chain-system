import os
import subprocess
import webbrowser
import requests
from bs4 import BeautifulSoup
import time

# Optional NLP tools (if installed)
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = None

# Optional transformers fallback
try:
    from transformers import pipeline
    gen = pipeline("text-generation", model="gpt2")
except Exception:
    gen = None

LOGFILE = "agent.log"

def log(msg):
    t = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOGFILE, "a") as f:
        f.write(f"[{t}] {msg}\n")
    print(msg)

class Agent:
    def __init__(self):
        self.installed_tools = []

    def handle(self, message):
        if self.is_task_unknown(message):
            return self.create_improvement_script(message)
        else:
            return self.process_message(message)

    def is_task_unknown(self, message):
        known_tasks = ["open_url", "search", "create_site", "send_email"]
        return not any(task in message for task in known_tasks)

    def create_improvement_script(self, message):
        script = f"# Script généré automatiquement pour améliorer Natacha\n"
        if "création d'un site complexe" in message:
            script += "pip install flask jinja2 sqlalchemy"
            self.installed_tools.append("flask jinja2 sqlalchemy")
        elif "analyse de texte avancée" in message:
            script += "pip install spacy transformers"
            self.installed_tools.append("spacy transformers")
        return f"Script généré : \n{script}"

    def execute_script(self, script):
        try:
            process = subprocess.Popen(script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            if process.returncode == 0:
                return f"Script exécuté avec succès : {out.decode()}"
            else:
                return f"Erreur lors de l'exécution du script : {err.decode()}"
        except Exception as e:
            return f"Erreur d'exécution : {str(e)}"

    def process_message(self, message):
        # Process the message and act accordingly
        pass
# agent.py  — cœur orchestrateur de Natacha
import os
import subprocess
import webbrowser
import requests
from bs4 import BeautifulSoup
import time
import json
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# optional NLP tools (if installed)
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = None

# optional transformers fallback
try:
    from transformers import pipeline
    gen = pipeline("text-generation", model="gpt2")
except Exception:
    gen = None

LOGFILE = "agent.log"

def log(msg):
    t = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOGFILE, "a") as f:
        f.write(f"[{t}] {msg}\n")
    print(msg)

class Agent:
    def __init__(self, safe_mode=False):
        self.safe_mode = safe_mode  # si True, bloque commandes risquées
        log("Agent initialisé (safe_mode=%s)" % self.safe_mode)

    def handle(self, message):
        log(f"Reçu message: {message}")
        intent, payload = self._parse_intent(message)
        try:
            if intent == "greet":
                return "Oui, ça va bien — prêt pour tes ordres."
            if intent == "open_url":
                url = payload.get("url")
                webbrowser.open(url)
                return f"J'ai ouvert {url}"
            if intent == "search":
                query = payload.get("q")
                return self._web_search(query)
            if intent == "create_site":
                name = payload.get("name","site_auto")
                return self._create_website(name, payload.get("details",""))
            if intent == "download_images":
                url = payload.get("url")
                path = self._download_images_from_page(url)
                return f"Images téléchargées dans {path}"
            if intent == "install":
                package = payload.get("package")
                return self._install_package(package)
            if intent == "run":
                cmd = payload.get("cmd")
                return self._run_shell(cmd)
            if intent == "send_email":
                to = payload.get("to")
                subj = payload.get("subject","")
                body = payload.get("body","")
                return self._send_email(to, subj, body)
            # fallback: generate text
            return self._generate_text(message)
        except Exception as e:
            log(f"Erreur lors de l'exécution intent={intent}: {e}")
            return f"Erreur: {str(e)}"

    def _parse_intent(self, text):
        t = text.lower()
        # règles simples en français / anglais
        if any(x in t for x in ["salut","bonjour","ça va","yo"]):
            return "greet", {}
        if t.startswith("ouvre ") or "ouvre " in t:
            # chercher url ou mot
            if "google" in t:
                return "open_url", {"url":"https://www.google.com"}
            if "youtube" in t:
                return "open_url", {"url":"https://www.youtube.com"}
            # si url explicite
            for part in t.split():
                if part.startswith("http"):
                    return "open_url", {"url": part}
            return "open_url", {"url":"https://www.google.com"}
        if t.startswith("cherche ") or t.startswith("search ") or "cherche " in t:
            q = t.replace("cherche","").replace("search","").strip()
            return "search", {"q": q}
        if "crée un site" in t or "create site" in t or "create website" in t:
            # parse a name
            parts = t.split()
            name = "site_auto"
            return "create_site", {"name": name, "details": t}
        if "télécharge les images" in t or "download images" in t:
            # extract url
            for part in t.split():
                if part.startswith("http"):
                    return "download_images", {"url": part}
            return "download_images", {"url": "https://www.google.com/search?tbm=isch&q=example"}
        if t.startswith("install ") or "installe " in t:
            pkg = t.replace("install","").replace("installe","").strip()
            return "install", {"package": pkg}
        if t.startswith("run ") or t.startswith("exécute "):
            cmd = t.replace("run","").replace("exécute","").strip()
            return "run", {"cmd": cmd}
        if "envoie un email" in t or "send email" in t:
            # pattern: send email to X subject Y body Z
            return "send_email", {"to":"", "subject":"", "body":""}
        # fallback
        return "fallback", {}

    def _web_search(self, query):
        log(f"Recherche web: {query}")
        url = f"https://www.google.com/search?q={requests.utils.requote_uri(query)}"
        webbrowser.open(url)
        return f"Recherche lancée pour : {query}"

    def _create_website(self, name, details=""):
        folder = f"./{name}"
        os.makedirs(folder, exist_ok=True)
        html = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{name}</title></head>
<body><h1>{name}</h1><p>Généré par Natacha. Détails: {details}</p></body></html>"""
        with open(os.path.join(folder,"index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        log(f"Site créé: {folder}/index.html")
        return f"Site créé dans le dossier {folder}"

    def _download_images_from_page(self, url):
        log(f"Download images from {url}")
        r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")
        imgs = soup.find_all("img")
        save_dir = "./downloads_images"
        os.makedirs(save_dir, exist_ok=True)
        count = 0
        for i,img in enumerate(imgs[:20]):
            src = img.get("src") or img.get("data-src")
            if not src: continue
            if src.startswith("//"):
                src = "https:" + src
            if src.startswith("http"):
                try:
                    data = requests.get(src, timeout=10).content
                    ext = ".jpg"
                    path = os.path.join(save_dir, f"img_{int(time.time())}_{i}{ext}")
                    with open(path, "wb") as f:
                        f.write(data)
                    count += 1
                except Exception as e:
                    log(f"Err dl img {src}: {e}")
        return f"{count} images téléchargées dans {save_dir}"

    def _install_package(self, package):
        if self.safe_mode:
            return "Mode sécurisé actif — installation bloquée."
        log(f"Installation package: {package}")
        # installer pip package (ou homebrew si détecté word 'brew:')
        if package.startswith("brew:"):
            pkg = package.split(":",1)[1]
            cmd = ["brew","install",pkg]
        else:
            cmd = ["pip","install", package]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = p.communicate()
        log(f"Install output: {out.decode()}\nErr: {err.decode()}")
        if p.returncode == 0:
            return f"Package {package} installé."
        else:
            return f"Échec installation {package}: {err.decode()}"

    def _run_shell(self, cmd):
        if self.safe_mode:
            return "Mode sécurisé actif — exécution shell bloquée."
        log(f"Exécution shell: {cmd}")
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = p.communicate()
        return out.decode() if out else err.decode()

    def _send_email(self, to_email, subject, body):
        # configure with env variables or fill here
        FROM = os.getenv("NATACHA_EMAIL")
        PWD = os.getenv("NATACHA_EMAIL_PWD")
        if not FROM or not PWD:
            return "Env NATACHA_EMAIL et NATACHA_EMAIL_PWD non définies."
        msg = MIMEMultipart()
        msg["From"] = FROM
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body,"plain"))
        try:
            s = smtplib.SMTP("smtp.gmail.com",587)
            s.starttls()
            s.login(FROM,PWD)
            s.sendmail(FROM,to_email,msg.as_string())
            s.quit()
            return f"Email envoyé à {to_email}"
        except Exception as e:
            return f"Erreur envoi email: {e}"

    def _generate_text(self, prompt):
        if gen:
            try:
                out = gen(prompt, max_length=80, do_sample=True, num_return_sequences=1)
                return out[0]["generated_text"]
            except Exception as e:
                log("Gen error: "+str(e))
        # fallback simple
        return "Je t'ai reçu : " + prompt

