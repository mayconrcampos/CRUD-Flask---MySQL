
from flask import Flask, Response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json

# instanciando classe Flask
app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:5DaJ10.,Xw,8@localhost/youtube"

# Instanciando classe SQLalchemy para banco de dados
db = SQLAlchemy(app)

# Criando headers
@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, PUT, GET, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Origin, Content-Type, Accept, Authorization, X-Request-With"
    return response

# Criando tabela
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(100))

    def to_json(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email
        }
"""
Rotas:
    
    - /usuarios     - GET    - SELECT
    - /usuario/id   - GET    - SELECT registro
    - /usuario      - POST   - INSERT
    - /usuario/id   - PUT    - UPDATE registro
    - /usuario/id   - DELETE - DELETE registro

    API funcionando corretamente, mas ainda faltam coisas a serem implementadas as quais eu ainda estou estudando, como:

    - Validações de tipo
    - Manipulação com dados vindos do front-end
    - Separação das funcionalidades do código (modularização)
    - entre outras coisas que preciso estudar.

"""

# Select all
@app.route("/usuarios", methods=["GET"])
def select_all():
    list_all = Usuario.query.all()
    usuarios_json = [usuario.to_json() for usuario in list_all]

    return gera_response(200, "usuarios", usuarios_json, "OK")

# seleciona um registro
@app.route("/usuario/<id>", methods=["GET"])
def select_user(id):
    usuario_obj = Usuario.query.filter_by(id=id).first()
    usuario_json = usuario_obj.to_json()

    return gera_response(200, "usuario", usuario_json, "OK")


# insert
@app.route("/usuario", methods=["POST"])
def insere_usuario():
    body = request.get_json()
    print(body)

    try:
        usuario = Usuario(nome = body["nome"], email = body["email"])

        # Dando insert no banco
        db.session.add(usuario)

        # Dando commit na operação
        db.session.commit()

        return gera_response(201, "usuario", usuario.to_json(), "Criado com Sucesso")

    except Exception as e:
        #print(usuario)
        print("erro", e)
        return gera_response(400, "", {}, "Erro ao inserir usuário")

# update
@app.route("/usuario/<id>", methods=["PUT"])
def atualiza_usuario(id):
    # pega o usuario
    usuario_obj = Usuario.query.filter_by(id=id).first()

    # pega as modificações
    body = request.get_json()

    try:
        if "nome" in body:
            usuario_obj.nome = body['nome']
        if "email" in body:
            usuario_obj.email = body['email']

        # Faz update
        db.session.add(usuario_obj)
        
        # Dá commit na transação
        db.session.commit()

        return gera_response(201, "usuario", usuario_obj.to_json(), "Atualizado com Sucesso")

    except Exception as e:
        return gera_response(400, "", {}, "Erro ao atualizar usuário")

# delete
@app.route("/usuario/<id>", methods=["DELETE"])
def delete_usuario(id):
    usuario_obj = Usuario.query.filter_by(id=id).first()


    try:
        db.session.delete(usuario_obj)
        db.session.commit()

        return gera_response(200, "", {}, "Usuário excluído com sucesso")
    except Exception as e:

        return gera_response(400, "", {}, "Erro ao deletar usuário")




def gera_response(status, nome_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_conteudo] = conteudo

    if mensagem:
        body["mensagem"] = mensagem
    

    return Response(json.dumps(body), status=status, mimetype="application/json")

# Executando

if __name__ == "__main__":
    app.run()