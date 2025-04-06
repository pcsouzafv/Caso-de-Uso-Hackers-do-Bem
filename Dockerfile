# Use uma imagem base Python oficial
FROM python:3.13.1-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro para aproveitar cache de camadas
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante da aplicação
COPY . .

# Variáveis de ambiente
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expor a porta 8080
EXPOSE 8080

# Comando para rodar a aplicação com Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
