#!/bin/bash
apt-get update
apt-get install -y --no-install-recommends apt-transport-https ca-certificates curl

# Installer les dépendances pour ODBC
apt-get install -y --no-install-recommends odbcinst

# Télécharger et ajouter la clé publique Microsoft GPG
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

# Ajouter le référentiel Microsoft pour msodbcsql18
echo "deb [arch=amd64] https://packages.microsoft.com/ubuntu/22.10/prod impish main" | tee /etc/apt/sources.list.d/mssql-release.list

# Mettre à jour la liste des paquets
apt-get update

# Installer msodbcsql18
apt-get install -y --no-install-recommends msodbcsql18
