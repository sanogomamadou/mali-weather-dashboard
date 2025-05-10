from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json
import logging
from datetime import datetime

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MeteoConsumer")

# Configuration Kafka
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC_NAME = "meteo-enriched"
GROUP_ID = "meteo-es-group"

# Configuration Elasticsearch (version corrigée)
ES_HOST = "localhost"
ES_PORT = 9200
ES_SCHEME = "http"  # ou "https" si vous utilisez SSL
ES_INDEX = "meteo-data-correct"

def create_es_index(es_client):
    """Crée l'index Elasticsearch avec le mapping approprié"""
    if not es_client.indices.exists(index=ES_INDEX):
        mapping = {
            "mappings": {
                "properties": {
                    "timestamp": {"type": "date"},
                    "city": {"type": "keyword"},
                    "country": {"type": "keyword"},
                    "temperature": {"type": "float"},
                    "feels_like": {"type": "float"},
                    "temp_min": {"type": "float"},
                    "temp_max": {"type": "float"},
                    "humidity": {"type": "integer"},
                    "pressure": {"type": "integer"},
                    "wind_speed": {"type": "float"},
                    "wind_deg": {"type": "integer"},
                    "clouds": {"type": "integer"},
                    "weather": {"type": "keyword"},
                    "weather_desc": {"type": "text"},
                    "rain": {"type": "float"},
                    "snow": {"type": "float"},
                    "sunrise": {"type": "date"},
                    "sunset": {"type": "date"},
                    "location": {"type": "geo_point"}
                }
            }
        }
        es_client.indices.create(index=ES_INDEX, body=mapping)
        logger.info(f"Index {ES_INDEX} créé avec le mapping")

def create_kafka_consumer():
    """Crée et retourne un consommateur Kafka"""
    try:
        consumer = KafkaConsumer(
            TOPIC_NAME,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=GROUP_ID,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        logger.info("Connecté à Kafka")
        return consumer
    except Exception as e:
        logger.error(f"Erreur de connexion à Kafka: {str(e)}")
        raise

def create_es_client():
    """Crée et retourne un client Elasticsearch (version corrigée)"""
    try:
        # Nouvelle configuration avec le schéma
        es = Elasticsearch(
            [{'host': ES_HOST, 'port': ES_PORT, 'scheme': ES_SCHEME}],
            # Alternative moderne:
            # hosts=[f"{ES_SCHEME}://{ES_HOST}:{ES_PORT}"]
        )
        if es.ping():
            logger.info("Connecté à Elasticsearch")
            return es
        else:
            raise ConnectionError("Impossible de se connecter à Elasticsearch")
    except Exception as e:
        logger.error(f"Erreur de connexion à Elasticsearch: {str(e)}")
        raise

def transform_to_es_action(message):
    """Transforme le message Kafka en action bulk pour ES"""
    try:
        value = message.value
        location = value.get("location", {})
        lat = location.get("lat", 0)  # 0 par défaut si absent
        lon = location.get("lon", 0)
        action = {
            "_index": ES_INDEX,
            "_source": {
                **value,
                "location": {
                    "lat": lat, 
                    "lon": lon
                }
            }
        }
        return action
    except Exception as e:
        logger.error(f"Erreur de transformation du message: {str(e)}")
        return None

def main():
    # Initialisation des clients
    es = create_es_client()
    consumer = create_kafka_consumer()
    
    # Création de l'index ES si nécessaire
    create_es_index(es)
    
    # Traitement des messages
    batch_size = 10
    batch = []
    
    try:
        for message in consumer:
            try:
                action = transform_to_es_action(message)
                if action:
                    batch.append(action)
                    logger.debug(f"Message ajouté au batch: {message.value['city']}")
                
                if len(batch) >= batch_size:
                    bulk(es, batch)
                    logger.info(f"{len(batch)} documents envoyés à Elasticsearch")
                    batch = []
                    
            except Exception as e:
                logger.error(f"Erreur de traitement du message: {str(e)}")
                
    except KeyboardInterrupt:
        logger.info("Arrêt demandé par l'utilisateur")
    finally:
        if batch:
            bulk(es, batch)
            logger.info(f"{len(batch)} derniers documents envoyés")
        
        consumer.close()
        es.close()
        logger.info("Connexions fermées")

if __name__ == "__main__":
    main()