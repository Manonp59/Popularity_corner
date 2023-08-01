# Utiliser une image Python officielle en tant qu'image de base
FROM python:3.8

# Exposer le port sur lequel votre application FastAPI écoute
EXPOSE 8000

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier des dépendances et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tous les fichiers de l'application FastAPI dans le conteneur
COPY . /app

# Définir les variables d'environnement pour Uvicorn
ENV MODULE_NAME=main
ENV VARIABLE_NAME=app
ARG API_KEY_BUDGET

# Lancer Uvicorn lors de l'exécution du conteneur
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
