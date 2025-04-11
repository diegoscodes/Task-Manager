from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tarefas.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo da tabela
class Tarefa(db.Model):
    __tablename__ = "tarefas"
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(200), nullable=False)  # Nome da tarefa
    feita = db.Column(db.Boolean, default=False)  # Se foi concluída ou não
    data_criacao = db.Column(db.DateTime, default=db.func.current_timestamp())  # Data de criação
    prioridade = db.Column(db.String(50), default="Média")  # Prioridade da tarefa


# Criar banco e tabelas
with app.app_context():
    db.create_all()
    db.session.commit()

# Rota para criar tarefas
@app.route('/criar-tarefa', methods=['POST'])
def criar():
    if request.method == 'POST':
        conteudo_tarefa = request.form.get('conteudo_tarefa')  # Pegando o valor do input
        if not conteudo_tarefa:
            return "Erro: Campo vazio!", 400  # Retorna erro se o campo estiver vazio

        # Criar uma nova tarefa e adicionar ao banco
        nova_tarefa = Tarefa(conteudo=conteudo_tarefa, feita=False)
        db.session.add(nova_tarefa)
        db.session.commit()

        return redirect(url_for('home'))  # Redireciona para a página inicial

# Rota principal
@app.route('/')
def home():
    todas_as_tarefas = Tarefa.query.all()  # Consultamos e armazenamos todas as tarefas da base de dados
    return render_template("index.html", lista_de_tarefas=todas_as_tarefas)  # Envia os dados para o template

# Rota para marcar tarefa como feita
@app.route('/marcar-feita/<id>')
def marcar_feita(id):
    tarefa = Tarefa.query.get(int(id))  # Busca a tarefa com o ID fornecido
    if tarefa:
        tarefa.feita = True  # Marca a tarefa como feita
        db.session.commit()  # Salva a mudança na base de dados
    return redirect(url_for('home'))  # Redireciona de volta para a página inicial

# Rota para eliminar tarefa
@app.route('/eliminar-tarefa/<id>')
def eliminar(id):
    tarefa = Tarefa.query.filter_by(id=int(id)).delete()  # Pesquisa e deleta a tarefa com o ID correspondente
    db.session.commit()  # Salva a mudança na base de dados
    return redirect(url_for('home'))  # Redireciona de volta para a página inicial

if __name__ == '__main__':
    app.run(debug=True, port=5001)
