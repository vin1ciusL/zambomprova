# Imagem base leve com Python 3.11
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código do projeto (inclusive app.py)
COPY . .

# Expor a porta interna do Flask
EXPOSE 5001

# Rodar o Flask direto (pra testar)
CMD ["python", "app.py"]
