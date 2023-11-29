from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__) 
CORS(app)
path = os.path.dirname(os.path.abspath(__file__))
arquivobd = os.path.join(path, 'jogador.db')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+arquivobd
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app) 

class Jogador(db.Model):
    id = db.Columm(db.Integer, primary_key=True)
    nome = db.Columm(db.String(250))
    pontuacao = db.Columm(db.Integer)
    nome_foto = db.Column(db.Text)

    def __str__(self):
        return self.nome + "[id="+str(self.id)+ "], " +\
    self.pontuacao  + ", " + self.nome_foto
    
    def json(self):
        return {
            "id":self.id,
            "nome":self.nome,
            "pontuacao":self.pontuacao,
            "nome_foto": self.nome_foto
        }

@app.route("/")
def padrao():
    return "backend ok"

@app.route("/criar_tabelas")
def criar():
    #oxe pode isso
    if os.path.exists(arquivobd):
        os.remove(arquivobd)
    db.create_all()
    return "tabelas criadas, pode retornar à página anterior"

@app.route("/save_image", methods=['POST'])
def salvar_imagem():
    try:
        #print("comecando")
        file_val = request.files['foto']
        #print("vou salvar em: "+file_val.filename)
        arquivoimg = os.path.join(path, 'imagens/'+file_val.filename)
        file_val.save(arquivoimg)
        r = jsonify({"resultado":"ok", "detalhes": file_val.filename})
    except Exception as e:
        r = jsonify({"resultado":"erro", "detalhes": str(e)})

    return r

@app.route('/get_image/<int:id_jogador>')
def get_image(id_jogador):
    # livro = db.session.query(Pessoa).get(id_pessoa) VERSÃO OBSOLETA!!!
    p = db.session.get(Jogador, id_jogador)
    completo = os.path.join(path, 'imagens/'+ p.nome_foto)
    return send_file(completo, mimetype='image/gif')

@app.route("/incluir_jogador", methods=['post'])
def incluir_jogador():
    dados = request.get_json(force=True)
    try:
      nova = Jogador(**dados)
      db.session.add(nova) 
      db.session.commit() 
      return jsonify({"resultado": "ok", "detalhes": "oi"})
    except Exception as e:
      return jsonify({"resultado":"erro", "detalhes":str(e)})
    
@app.route("/retornar_jogadores")
def retornar_jogadores():
    try:
        jogadores = db.session.query(Jogador).all()
        jogadores_em_json = [ x.json() for x in jogadores ]
        retorno = {'resultado': 'ok'}
        retorno.update({'detalhes': jogadores_em_json}) # concatenar dois json's (dicionários)
        return jsonify(retorno)
    except Exception as e:
        return jsonify({"resultado":"erro", "detalhes":str(e)})

@app.route("/listar/<string:classe>")
def listar(classe):
    # obter os dados da classe informada
    dados = None
    if classe == "Jogador":
        dados = db.session.query(Jogador).all()
    if dados:
      # converter dados para json
      lista_jsons = [x.json() for x in dados]

      meujson = {"resultado": "ok"}
      meujson.update({"detalhes": lista_jsons})
      return jsonify(meujson)
    else:
      return jsonify({"resultado":"erro", "detalhes":"classe informada inválida: "+classe})


app.run(debug=True)