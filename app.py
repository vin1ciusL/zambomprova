import os
from dotenv import load_dotenv
from flask import Flask
from flask_pymongo import PyMongo

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)


# Configuração do MongoDB Atlas (ou local)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

@app.route("/test")
def home():
    return "placeholder"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)