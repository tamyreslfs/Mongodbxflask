from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient

app = Flask(__name__)

# Configuração do banco de dados MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:9541@localhost/meu_banco'

# Crie uma instância do SQLAlchemy vinculada ao aplicativo Flask
db = SQLAlchemy(app)

# Configuração do banco de dados MongoDB
client = MongoClient('mongodb+srv://mirynhalopes:9541@cluster.dqfj2m5.mongodb.net/')
mongodb_db = client.db_name

# Defina seus modelos SQLAlchemy aqui
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

# Defina os modelos de dados
class Setor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

class Cargo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    id_setor = db.Column(db.Integer, db.ForeignKey('setor.id'), nullable=False)
    setor = db.relationship('Setor', backref=db.backref('cargos', lazy=True))

class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    primeiro_nome = db.Column(db.String(100), nullable=False)
    sobrenome = db.Column(db.String(100), nullable=False)
    data_admissao = db.Column(db.Date, nullable=False)
    status_funcionario = db.Column(db.String(20))
    id_setor = db.Column(db.Integer, db.ForeignKey('setor.id'), nullable=False)
    id_cargo = db.Column(db.Integer, db.ForeignKey('cargo.id'), nullable=False)
    setor = db.relationship('Setor', backref=db.backref('funcionarios', lazy=True))
    cargo = db.relationship('Cargo', backref=db.backref('funcionarios', lazy=True))

# Rotas para adicionar setor, cargo e funcionário
@app.route('/')
def index():
    return render_template('base.html')

@app.route('/adicionar_setor', methods=['GET', 'POST'])
def adicionar_setor():
    if request.method == 'POST':
        nome = request.form['nome']
        novo_setor = Setor(nome=nome)
        db.session.add(novo_setor)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('setor.html')

@app.route('/adicionar_cargo', methods=['GET', 'POST'])
def adicionar_cargo():
    if request.method == 'POST':
        nome = request.form['nome']
        id_setor = request.form['id_setor']
        novo_cargo = Cargo(nome=nome, id_setor=id_setor)
        db.session.add(novo_cargo)
        db.session.commit()
        return redirect(url_for('index'))
    setores = Setor.query.all()
    return render_template('cargo.html', setores=setores)

@app.route('/adicionar_funcionario', methods=['GET', 'POST'])
def adicionar_funcionario():
    if request.method == 'POST':
        primeiro_nome = request.form['primeiro_nome']
        sobrenome = request.form['sobrenome']
        data_admissao = request.form['data_admissao']
        status_funcionario = request.form.get('status_funcionario')
        id_setor = request.form['id_setor']
        id_cargo = request.form['id_cargo']
        novo_funcionario = Funcionario(primeiro_nome=primeiro_nome, sobrenome=sobrenome, data_admissao=data_admissao,
                                       status_funcionario=status_funcionario, id_setor=id_setor, id_cargo=id_cargo)
        db.session.add(novo_funcionario)
        db.session.commit()
        return redirect(url_for('index'))
    setores = Setor.query.all()
    cargos = Cargo.query.all()
    return render_template('funcionario.html', setores=setores, cargos=cargos)

# Rota para exibir tabelas
@app.route('/visualizar_tabelas')
def visualizar_tabelas():
    setores = Setor.query.all()
    cargos = Cargo.query.all()
    funcionarios = Funcionario.query.all()
    return render_template('visualizar_tabelas.html', setores=setores, cargos=cargos, funcionarios=funcionarios)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
