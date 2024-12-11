from kafka import KafkaConsumer
from pymongo import MongoClient
import json
import logging
import re
from urllib.parse import quote_plus

# Configuration des logs pour debug
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration Kafka
kafka_bootstrap_servers = "100.78.197.35:9092"  # Adresse du serveur Kafka (ou localhost)
kafka_topic_pattern = r"^METEOFRANCE\.station\..+"  # Pattern pour les topics Kafka

# Configuration MongoDB
username = "admin"
password = "@Ipadpro8@"  # Mot de passe avec caractères spéciaux
encoded_password = quote_plus(password)  # Encode le mot de passe pour l'URI MongoDB
mongo_uri = f"mongodb://{username}:{encoded_password}@localhost:27017"  # URI encodé
mongo_db = "meteoDB"  # Nom de la base de données MongoDB
mongo_collection = "testCollection"  # Nom de la collection MongoDB

# Connexion à MongoDB
try:
    logging.info("Connexion à MongoDB...")
    client = MongoClient(mongo_uri)
    db = client[mongo_db]
    collection = db[mongo_collection]
    logging.info("Connexion à MongoDB réussie.")
except Exception as e:
    logging.error(f"Erreur lors de la connexion à MongoDB : {e}")
    exit(1)

# Connexion à Kafka
try:
    logging.info("Connexion à Kafka...")
    consumer = KafkaConsumer(
        bootstrap_servers=kafka_bootstrap_servers,
        auto_offset_reset='earliest',  # Lire depuis le début du topic
        enable_auto_commit=True,       # Auto-commit des offsets
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Désérialisation JSON
    )

    # S'abonner à tous les topics correspondant au pattern
    consumer.subscribe(pattern=kafka_topic_pattern)
    logging.info("Connexion à Kafka réussie et abonné aux topics correspondant au pattern.")
except Exception as e:
    logging.error(f"Erreur lors de la connexion à Kafka : {e}")
    client.close()
    exit(1)

# Lire les messages de Kafka et les insérer dans MongoDB
try:
    logging.info("Début de la consommation des données de Kafka vers MongoDB...")
    message_count = 0  # Compteur pour les messages

    for message in consumer:
        try:
            # Extraire le contenu du message
            document = message.value
            message_count += 1
            logging.info(f"Message reçu depuis le topic {message.topic} : {document}")

            # Insérer dans MongoDB
            collection.insert_one(document)
            logging.info("Message inséré dans MongoDB avec succès.")
        except Exception as e:
            logging.error(f"Erreur lors de l'insertion du message : {e}")

    if message_count == 0:
        logging.warning("Aucun message trouvé dans les topics Kafka correspondant au pattern.")

    logging.info("Transfert terminé.")
except Exception as e:
    logging.error(f"Erreur lors de la consommation des données : {e}")
finally:
    # Fermer les connexions
    logging.info("Fermeture des connexions...")
    client.close()
