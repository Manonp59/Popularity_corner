#!/bin/bash

# Définit les variables
resourceGroup="RG_LEMULLOIS"
name="api-popu"
location="francecentral"
image="neevaiti/test_api:latest"

# Crée le groupe de ressources
az group create --name $resourceGroup --location $location

# Crée l'instance du conteneur
az container create \
    --resource-group $resourceGroup \
    --memory 8 \
    --cpu 2 \
    --name $name \
    --image $image \
    --environment-variables "API_KEY_BUDGET=7de52660cd21bc098732e69e0d02651c" \
    --dns-name-label $name \
    --ports 80
