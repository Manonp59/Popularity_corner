# Utiliser une image Python officielle en tant qu'image de base
FROM python:3.10

# Exposer le port sur lequel votre application FastAPI écoute
EXPOSE 8000

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier des dépendances et installer les dépendances
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copier tous les fichiers de l'application FastAPI dans le conteneur
COPY . /app

# Définir les variables d'environnement pour Uvicorn
ENV MODULE_NAME=main
ENV VARIABLE_NAME=app
ENV API_KEY_BUDGET=7de52660cd21bc098732e69e0d02651c

# Lancer Uvicorn lors de l'exécution du conteneur
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]