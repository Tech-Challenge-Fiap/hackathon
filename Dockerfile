# Use a imagem base do Python para desenvolvimento
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

COPY . .
COPY docker/* /usr/bin/

# Instale as dependências da aplicação
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Comando para iniciar a aplicação Flask em modo de desenvolvimento
CMD ["bash", "docker/start.sh"]

