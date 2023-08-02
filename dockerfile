# Utiliser une image Python officielle en tant qu'image de base
FROM python:3.10

# Exposer le port sur lequel votre application FastAPI écoute
EXPOSE 80

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier des dépendances et installer les dépendances
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copier tous les fichiers de l'application FastAPI dans le conteneur
COPY . /app

# Lancer Uvicorn lors de l'exécution du conteneur
CMD ["python", "main.py"]