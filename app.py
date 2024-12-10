from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import threading
import subprocess

app = Flask(__name__)
app.secret_key = "chave_secreta"

DATABASE = "database.db"

# Função para conectar ao banco de dados
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Rota para inicializar o banco de dados
@app.route("/init_db")
def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        """)
        conn.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'admin123')")
    return "Banco de dados inicializado!"

# Rota para login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
        if user:
            session["user_id"] = user["id"]
            return redirect(url_for("dashboard"))
        else:
            flash("Credenciais inválidas!")
    return render_template("login.html")

# Rota para o painel
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        youtube_url = request.form["youtube_url"]
        num_instances = int(request.form["num_instances"])
        duration = int(request.form["duration"])

        # Inicia o processo de automação em uma thread separada
        threading.Thread(target=run_automation, args=(youtube_url, num_instances, duration)).start()
        flash("Automação iniciada com sucesso!")
    
    return render_template("dashboard.html")

# Função para rodar o script de Selenium
def run_automation(youtube_url, num_instances, duration):
    command = ["python3", "open_youtube.py", youtube_url, str(num_instances), str(duration)]
    subprocess.run(command)

# Rota para logout
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
