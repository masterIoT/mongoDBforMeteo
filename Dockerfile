# Utiliser l'image officielle de MongoDB comme base
FROM mongo:latest

# Installer Python3, pip, wget, curl, et les outils nécessaires
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv wget

# Créer un environnement virtuel pour Python
RUN python3 -m venv /opt/venv

# Activer l'environnement virtuel et installer les dépendances
RUN /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install kafka-python pymongo six

# Ajouter l'environnement virtuel au PATH
ENV PATH="/opt/venv/bin:$PATH"

# Créer le dossier dump/meteoDB
RUN mkdir -p /dump/meteoDB

# Télécharger le fichier depuis le lien web
#ADD https://myaccountdestorage.blob.core.windows.net/siteweb/meteoCollection.bson /dump/meteoDB/
ADD https://myaccountdestorage.blob.core.windows.net/siteweb/Dockerfile /dump/meteoDB/

# Copier les scripts Python dans l'image
COPY ./scripts /scripts

# Restaurer la base MongoDB et démarrer MongoDB
CMD mongorestore --username=admin --password=@Ipadpro8@@Ipadpro8@ --authenticationDatabase admin /dump && \
    mongod --bind_ip_all
