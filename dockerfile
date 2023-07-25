

# ARG AZURE_SERVER_NAME
# ARG AZURE_SERVER_USER
# ARG AZURE_SERVER_PASSWORD
# ARG AZURE_SERVER_HOST
# ARG AZURE_DB_NAME

# COPY odbc.sh /odbc.sh

# RUN chmod +x /odbc.sh

# # run the script as root
# RUN /odbc.sh

# # install necessary tools
# RUN apt-get update -y && apt-get install -y gcc curl gnupg build-essential

# Utilisez une image de base Python:3.10 (basée sur Debian)
FROM python:3.10

RUN apt install curl
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN exit
RUN apt-get update
RUN echo msodbcsql18 msodbcsql/ACCEPT_EULA boolean true | debconf-set-selections
RUN ACCEPT_EULA=Y apt-get install -y mssql-tools18
RUN echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc \
    && /bin/bash -c "source ~/.bashrc"

ENV PYTHONUNBUFFERED 1
WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/
