import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime


# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configuração do MongoDB Atlas (ou local)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

# ---------------- ROTAS ---------------- #

# GET - Listar todos os filmes
@app.route("/filmes", methods=["GET"])
def listar_filmes():
    filmes = mongo.db.filmes.find()
    saida = []
    for filme in filmes:
        saida.append({
            "id": str(filme["_id"]),
            "titulo": filme["titulo"],
            "descricao": filme["descricao"],
            "duracao": filme["duracao"],
            "diretor": filme["diretor"],
            "dataCadastro": filme.get("dataCadastro")
        })
    return jsonify(saida), 200

# POST - Cadastrar novo filme
@app.route("/filmes", methods=["POST"])
def criar_filme():
    dados = request.json
    if not dados or "titulo" not in dados or "descricao" not in dados or "duracao" not in dados or "diretor" not in dados:
        return jsonify({"erro": "Campos obrigatórios: titulo, descricao, duracao, diretor"}), 400

    agora = datetime.utcnow()
    filme_id = mongo.db.filmes.insert_one({
        "titulo": dados["titulo"],
        "descricao": dados["descricao"],
        "duracao": dados["duracao"],
        "diretor": dados["diretor"],
        "dataCadastro": agora.isoformat()
    }).inserted_id

    return jsonify({
        "id": str(filme_id),
        "titulo": dados["titulo"],
        "descricao": dados["descricao"],
        "duracao": dados["duracao"],
        "diretor": dados["diretor"],
        "dataCadastro": agora.isoformat()
    }), 201

# DELETE - Excluir filme por ID
@app.route("/filmes/<id>", methods=["DELETE"])
def deletar_filme(id):
    resultado = mongo.db.filmes.delete_one({"_id": ObjectId(id)})
    if resultado.deleted_count == 0:
        return jsonify({"erro": "Filme não encontrado"}), 404
    return jsonify({"mensagem": "Filme deletado com sucesso"}), 200

# --------------------------------------- #

@app.route("/test")
def home():
    return "placeholder"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)