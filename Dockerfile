# Utiliser l'image officielle de MongoDB comme base
FROM mongo:latest

# Installer Python3 et pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Copier le fichier d'archive dans le conteneur (si nécessaire)
COPY dump/mongodb.archive /data/mongodb.archive

# Copier le dossier 'scripts' dans le conteneur
COPY scripts /usr/src/app/scripts

# Démarrer MongoDB sans l'authentification pour créer un utilisateur
CMD ["bash", "-c", "\
  mongod --bind_ip 127.0.0.1 --fork --logpath /var/log/mongodb.log && \
  sleep 5 && \
  mongosh --eval 'db.createUser({user: \"admin\", pwd: \"strongpassword\", roles: [{role: \"root\", db: \"admin\"}]} )' && \
  mongorestore --archive=/data/mongodb.archive && \
  mongod --auth --bind_ip 127.0.0.1 --fork --logpath /var/log/mongodb.log && \
  tail -f /dev/null \
"]
