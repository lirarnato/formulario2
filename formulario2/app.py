## Autor Renato Lira
## Calculo de Investimento
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)

class Projeto(db.Model):
    __tablename__='cliente'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    projeto = db.Column(db.String)
    dataInicio = db.Column(db.String)
    dataFim = db.Column(db.String)
    valorProjeto = db.Column(db.String)
    risco = db.Column(db.String)
    telefone = db.Column(db.String)
    
    def __init__(self, projeto, dataInicio, dataFim, valorProjeto, risco, telefone):
        self.projeto = projeto
        self.dataInicio = dataInicio
        self.dataFim = dataFim
        self.valorProjeto = valorProjeto
        self.risco = risco
        self.telefone = telefone
        
        
db.create_all()

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html")

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        projeto = request.form.get("projeto")
        dataInicio = request.form.get("dataInicio")
        dataFim = request.form.get("dataFim")
        valorProjeto = request.form.get("valorProjeto")
        risco = request.form.get("risco")
        telefone = request.form.get("telefone")
        
        if projeto and dataInicio and dataFim and valorProjeto and risco and telefone:
            p = Projeto(projeto, dataInicio, dataFim, valorProjeto, risco, telefone)
            db.session.add(p)
            db.session.commit()
    
    return redirect(url_for("index"))

@app.route("/lista")
def lista():
    projetos = Projeto.query.all()
    return render_template("lista.html", projetos=projetos)

@app.route("/simularInvestimento")
def simularInvestimento():
    content = request.json
    ganho = content['ganho']
    valorProjeto = content['valorProjeto']
    
    rip = (ganho - valorProjeto)/valorProjeto
    
    return render_template("list.html",rip=str(rip))

@app.route("/excluir/<int:id>")
def excluir(id):
    projeto = Projeto.query.filter_by(_id=id).first()
    
    db.session.delete(projeto)
    db.session.commit()
    
    
    projetos = Projeto.query.all()
    return render_template("lista.html", projetos=projetos)


if __name__ == "__main__":
    app.run(debug=True)
    