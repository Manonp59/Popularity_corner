#!/bin/bash
sudo apt-get install odbcinst

sudo curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -

echo "deb [arch=amd64] https://packages.microsoft.com/ubuntu/21.10/prod impish main" | sudo tee /etc/apt/sources.list.d/mssql-release.list

sudo apt update

sudo apt install msodbcsql18