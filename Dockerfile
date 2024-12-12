# Utiliser l'image officielle MongoDB comme base
FROM mongo:latest

# Définir les variables d'environnement pour l'utilisateur administrateur
ENV MONGO_INITDB_ROOT_USERNAME=admin
ENV MONGO_INITDB_ROOT_PASSWORD=@Ipadpro8@

# Installer Python 3, pip et les outils nécessaires
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Créer un environnement virtuel pour Python
RUN python3 -m venv /opt/venv

# Activer l'environnement virtuel et installer les dépendances
#RUN /opt/venv/bin/pip install --upgrade pip && \
#    /opt/venv/bin/pip install kafka-python pymongo six

# Ajouter l'environnement virtuel au PATH
ENV PATH="/opt/venv/bin:$PATH"

# Copier les dossiers 'dump' et 'scripts' dans le conteneur
COPY dump /data/dump
COPY scripts /data/scripts

# Commande pour démarrer MongoDB et restaurer les données
CMD ["bash", "-c", "\
  mongod --bind_ip_all --fork --logpath /var/log/mongodb.log && \
  mongorestore --archive=/data/dump/mongodb.archive && \
  mongod --shutdown && \
  mongod --bind_ip_all --auth --logpath /var/log/mongodb.log \
"]
