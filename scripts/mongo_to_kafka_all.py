from pymongo import MongoClient
from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
import json
from urllib.parse import quote_plus
import logging

# Configuration des logs pour debug
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration MongoDB
username = "admin"
password = "@Ipadpro8@"  # Mot de passe avec caractères spéciaux
encoded_password = quote_plus(password)  # Encode le mot de passe pour l'URI MongoDB
mongo_uri = f"mongodb://{username}:{encoded_password}@localhost:27017"  # URI encodé
mongo_db = "meteoDB"  # Nom de la base de données MongoDB
mongo_collection = "meteoCollection"  # Nom de la collection MongoDB

# Configuration Kafka
kafka_bootstrap_servers = "100.78.197.35:9092"  # Adresse du serveur Kafka #OU LOCALHOST
base_kafka_topic = "METEOFRANCE.station."  # Base du nom du topic Kafka

# Vérification de la connexion MongoDB
try:
    logging.info("Connexion à MongoDB...")
    client = MongoClient(mongo_uri)
    db = client[mongo_db]
    collection = db[mongo_collection]
    logging.info("Connexion à MongoDB réussie.")
except Exception as e:
    logging.error(f"Erreur lors de la connexion à MongoDB : {e}")
    exit(1)

# Vérification de la connexion Kafka
try:
    logging.info("Connexion à Kafka...")
    admin_client = KafkaAdminClient(bootstrap_servers=kafka_bootstrap_servers)
    cluster_metadata = admin_client.describe_cluster()
    logging.info(f"Cluster Kafka détecté : {cluster_metadata}")

    # Initialisation du producteur Kafka
    producer = KafkaProducer(
        bootstrap_servers=kafka_bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),  # Sérialisation JSON
        request_timeout_ms=20000,  # Timeout en millisecondes (20 secondes)
        retries=5  # Nombre de tentatives en cas d'échec
    )
    logging.info("Connexion à Kafka réussie.")
except Exception as e:
    logging.error(f"Erreur lors de la connexion à Kafka : {e}")
    client.close()
    exit(1)

# Transférer les documents de MongoDB à Kafka
try:
    logging.info("Début du transfert des données de MongoDB vers Kafka...")
    document_count = 0  # Compteur pour les documents

    for document in collection.find():
        try:
            document_count += 1
            document['_id'] = str(document['_id'])  # Convertir ObjectId en chaîne

            # Vérifier si le champ NUM_POSTE existe dans le document
            if 'NUM_POSTE' in document:
                topic_name = f"{base_kafka_topic}{document['NUM_POSTE']}"

                # Vérifier si le topic existe, sinon le créer
                existing_topics = admin_client.list_topics()
                if topic_name not in existing_topics:
                    logging.info(f"Le topic '{topic_name}' n'existe pas. Création du topic...")
                    new_topic = NewTopic(name=topic_name, num_partitions=1, replication_factor=1)
                    admin_client.create_topics(new_topics=[new_topic], validate_only=False)
                    logging.info(f"Topic '{topic_name}' créé avec succès.")
                else:
                    logging.info(f"Le topic '{topic_name}' existe déjà.")

                producer.send(topic_name, value=document)  # Envoyer le document au topic correspondant
                logging.info(f"Message envoyé au topic {topic_name} : {document}")
            else:
                logging.warning(f"Document ignoré (pas de NUM_POSTE) : {document}")
        except Exception as e:
            logging.error(f"Erreur lors de l'envoi du document : {e}")

    if document_count == 0:
        logging.warning("Aucun document trouvé dans la collection MongoDB.")

    logging.info("Transfert terminé.")
except Exception as e:
    logging.error(f"Erreur lors du transfert des données : {e}")
finally:
    # Fermer les connexions
    logging.info("Fermeture des connexions...")
    producer.close()
    client.close()
