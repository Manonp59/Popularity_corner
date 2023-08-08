# Popularity Corner - Outil d'aide à la décision pour la programmation cinématographique

![Popularity Corner Logo](app/main/static/media/popularity_corner.png)

Popularity Corner est un outil d'aide à la décision pour la programmation cinématographique, conçu pour maximiser les revenus d'un cinéma en optimisant la sélection des films à projeter chaque semaine.

## Fonctionnalités

- Estimation hebdomadaire des entrées des films à venir pour la semaine.
- Comparaison des performances réelles avec les prédictions du modèle.
- Interface utilisateur conviviale pour visualiser les prédictions.

## Méthodologie et Outils

- Méthodologie Agile avec des sprints d'une semaine et rotation du Scrum Master.
- Gestion du projet avec Jira et division avec User Story associée à une branche sur Github.
- Modèle de machine learning (ExtraTreeRegresor) pour prédire la popularité des films.

## Technologies Utilisées

- **Récupération de données et automatisation**:
  - Airflow pour la planification et l'automatisation des tâches.
  - Scrapy pour le scraping des données nécessaires à l'entraînement du modèle.

- **Backend et Machine Learning**:
  - Django pour le développement du backend.
  - Utilisation de données collectées et prétraitées pour l'entraînement du modèle.

- **Frontend**:
  - Application web (dashboard) développée avec Django pour visualiser les prédictions.

- **Déploiement**:
  - Docker pour l'encapsulation et le déploiement des applications.
  - Déploiement sur Azure avec une architecture Micro-service (API/application/db).

## Installation et Utilisation

1. Clonez ce dépôt : `git clone https://github.com/Manonp59/Popularity_corner`
2. Construire l'image docker: `docker-compose build`
3. Lancez l'application : `docker-compose up`

## Auteurs

- Antonin Lemullois : [@neevaiti](https://github.com/neevaiti)
- Manon Platteau : [@Manonp59](https://github.com/Manonp59)
- Maxime Rowel : [@MaximeR12](https://github.com/MaximeR12)
- Agathe Becquart : [@AgatheBecquart](https://github.com/AgatheBecquart)



