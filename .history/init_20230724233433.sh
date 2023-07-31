#!/bin/bash
apt list --up
apt-get install odbcinst

curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

echo "deb [arch=amd64] https://packages.microsoft.com/ubuntu/22.10/prod impish main" | apt tee /etc/apt/sources.list.d/mssql-release.list

apt update

apt install msodbcsql18