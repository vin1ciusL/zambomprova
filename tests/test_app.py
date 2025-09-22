import pytest
import mongomock
import sys
import os
from bson.objectid import ObjectId
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app, mongo


@pytest.fixture
def client():
    app.config["TESTING"] = True

    mongo.cx = mongomock.MongoClient()
    mongo.db = mongo.cx["filmes_testdb"]

    client = app.test_client()
    yield client

    mongo.db.filmes.delete_many({})


# Testes do placeholder
def test_placeholder(client):
    response = client.get("/test")
    assert response.status_code == 200
    assert b"placeholder" in response.data

# Testes do cadastro de filmes
def test_criar_filme_sucesso(client):
    res = client.post("/filmes", json={
        "titulo": "Matrix",
        "descricao": "Sci-fi clássico",
        "duracao": 2,
        "diretor": "Wachowski"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["titulo"] == "Matrix"
    assert "id" in data


def test_criar_filme_campos_faltando(client):
    res = client.post("/filmes", json={
        "titulo": "Filme Sem Diretor",
        "descricao": "Teste",
        "duracao": 1
    })
    assert res.status_code == 400
    assert "erro" in res.get_json()

# Testes da listagem de filmes
def test_listar_filmes(client):
    client.post("/filmes", json={
        "titulo": "Inception",
        "descricao": "Sonhos dentro de sonhos",
        "duracao": 3,
        "diretor": "Christopher Nolan"
    })
    res = client.get("/filmes")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "titulo" in data[0]

# Testes da exclusão de filmes
def test_deletar_filme_sucesso(client):
    filme_id = mongo.db.filmes.insert_one({
        "titulo": "Interestelar",
        "descricao": "Viagem espacial",
        "duracao": 3,
        "diretor": "Christopher Nolan"
    }).inserted_id

    res = client.delete(f"/filmes/{filme_id}")
    assert res.status_code == 200
    assert res.get_json()["mensagem"] == "Filme deletado com sucesso"


def test_deletar_filme_inexistente(client):
    fake_id = ObjectId()
    res = client.delete(f"/filmes/{fake_id}")
    assert res.status_code == 404
    assert "erro" in res.get_json()
