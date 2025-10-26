from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add_user", methods=["POST"])
def add_user():
    username = request.form["username"]
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return f"Utilisateur {username} ajouté"

if __name__ == "__main__":
    app.run(debug=True)

