# Use uma imagem base Python oficial
<<<<<<< HEAD
FROM python:3.13-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar OWASP ZAP
RUN curl -L -o /tmp/zap.sh https://raw.githubusercontent.com/zaproxy/zaproxy/master/docker/zap.sh \
    && chmod +x /tmp/zap.sh \
    && /tmp/zap.sh
=======
FROM python:3.13.1-slim
>>>>>>> master

# Definir diretório de trabalho
WORKDIR /app

<<<<<<< HEAD
# Copiar arquivos do projeto
COPY requirements.txt .
COPY main.py .
COPY models.py .
COPY database.py .
COPY schemas.py .
=======
# Copiar requirements primeiro para aproveitar cache de camadas
COPY requirements.txt .
>>>>>>> master

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

<<<<<<< HEAD
=======
# Copiar o restante da aplicação
COPY . .

>>>>>>> master
# Variáveis de ambiente
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expor a porta 8080
EXPOSE 8080

# Comando para rodar a aplicação com Gunicorn
<<<<<<< HEAD
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
=======
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
>>>>>>> master
