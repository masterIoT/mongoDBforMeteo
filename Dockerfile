# Utiliser l'image officielle de MongoDB comme base
FROM mongo:latest

# Installer Python3 et pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Copier le fichier d'archive dans le conteneur (si nécessaire)
COPY dump/mongodb.archive /data/mongodb.archive

#remplacer par : ADD <AZURE_LINK> /data/mongodb.archive

# Copier le dossier 'scripts' dans le conteneur
COPY scripts /usr/src/app/scripts

# Démarrer MongoDB avec l'accès limité à localhost (aucune connexion extérieure possible)
CMD ["bash", "-c", "\
  mongod --bind_ip 127.0.0.1 --fork --logpath /var/log/mongodb.log && \
  tail -f /dev/null \
"]
