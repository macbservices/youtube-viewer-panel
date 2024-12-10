from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Configuração do app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Caminho para o banco de dados
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo do Banco de Dados
class ViewerTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    youtube_link = db.Column(db.String(255), nullable=False)
    instances = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

db.create_all()  # Cria o banco de dados e as tabelas automaticamente

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para criar tarefas
@app.route('/create', methods=['POST'])
def create_task():
    youtube_link = request.form['link']
    instances = int(request.form['instances'])
    duration = int(request.form['duration'])

    task = ViewerTask(youtube_link=youtube_link, instances=instances, duration=duration)
    db.session.add(task)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
