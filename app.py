from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "sgv_artes_2026_key"

# --- CONFIGURAÇÕES ---
app.config['WHATSAPP_NUMERO'] = "5511988664241" # Seu número de Salto/SP
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sgv910087@localhost/sgv_artes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)

# --- MODELOS ---
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    imagem = db.Column(db.String(200), nullable=False)

class Linha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_linha = db.Column(db.String(100), nullable=False)
    codigo_barras = db.Column(db.String(50), nullable=False)
    estoque_novelos = db.Column(db.Integer, nullable=False)
    imagem_linha = db.Column(db.String(200), nullable=False)

# --- ROTAS ---
@app.route('/')
def index():
    produtos = Produto.query.all()
    linhas = Linha.query.all()
    # Enviamos o número para o HTML
    zap = app.config['WHATSAPP_NUMERO']
    return render_template('index.html', produtos=produtos, linhas=linhas, zap=zap)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') == 'admin' and request.form.get('password') == '123':
            return redirect(url_for('admin'))
    return render_template('login.html')

@app.route('/admin')
def admin():
    produtos = Produto.query.all()
    linhas = Linha.query.all()
    return render_template('admin.html', produtos=produtos, linhas=linhas)

# Rotas de deletar permanecem as mesmas...
@app.route('/deletar_produto/<int:id>')
def deletar_produto(id):
    item = Produto.query.get(id); db.session.delete(item); db.session.commit()
    return redirect(url_for('admin'))

@app.route('/deletar_linha/<int:id>')
def deletar_linha(id):
    item = Linha.query.get(id); db.session.delete(item); db.session.commit()
    return redirect(url_for('admin'))

@app.route('/add_produto', methods=['POST'])
def add_produto():
    nome = request.form.get('nome'); preco = request.form.get('preco'); arquivo = request.files['imagem']
    if arquivo:
        nome_foto = arquivo.filename; arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], nome_foto))
        db.session.add(Produto(nome=nome, preco=float(preco), imagem=nome_foto)); db.session.commit()
    return redirect(url_for('admin'))

@app.route('/add_linha', methods=['POST'])
def add_linha():
    nome = request.form.get('nome_linha'); codigo = request.form.get('codigo_barras'); estoque = request.form.get('estoque'); arquivo = request.files['imagem_linha']
    if arquivo:
        nome_foto = arquivo.filename; arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], nome_foto))
        db.session.add(Linha(nome_linha=nome, codigo_barras=codigo, estoque_novelos=int(estoque), imagem_linha=nome_foto)); db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    with app.app_context(): db.create_all()
    app.run(debug=True)

