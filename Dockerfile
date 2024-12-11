# Utiliser l'image officielle de MongoDB comme base
FROM mongo:latest

# Installer Python3, pip, et les outils nécessaires
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# Créer un environnement virtuel pour Python
RUN python3 -m venv /opt/venv

# Activer l'environnement virtuel et installer les dépendances
RUN /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install kafka-python pymongo six

# Ajouter l'environnement virtuel au PATH
ENV PATH="/opt/venv/bin:$PATH"

# Copier le dump MongoDB dans l'image
COPY ./dump /dump

# Copier les scripts Python dans l'image
COPY ./scripts /scripts

# Restaurer la base MongoDB et démarrer MongoDB
CMD mongorestore --username=admin --password=@Ipadpro8@@Ipadpro8@ --authenticationDatabase admin /dump && \
    mongod --bind_ip_all
