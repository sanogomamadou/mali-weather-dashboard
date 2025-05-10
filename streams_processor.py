from kafka import KafkaConsumer, KafkaProducer
import json
import logging
from geo_data import CITY_COORDINATES

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("StreamProcessor")

INPUT_TOPIC = "meteo-stream"
OUTPUT_TOPIC = "meteo-enriched"

def enrich_with_geodata(weather_data):
    city = weather_data["city"]
    if city in CITY_COORDINATES:
        weather_data["location"] = CITY_COORDINATES[city]
    else:
        weather_data["location"] = {"lat": 0, "lon": 0}
    return weather_data

def process_stream():
    # Configuration du consumer
    consumer = KafkaConsumer(
        INPUT_TOPIC,
        bootstrap_servers="localhost:9092",
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    
    # Configuration du producer
    producer = KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    
    logger.info("Démarrage du stream processor...")
    
    try:
        for message in consumer:
            try:
                # Transformation des données
                enriched_data = enrich_with_geodata(message.value)
                
                # Envoi vers le topic enrichi
                producer.send(OUTPUT_TOPIC, value=enriched_data)
                logger.debug(f"Message enrichi envoyé pour {enriched_data['city']}")
                
            except Exception as e:
                logger.error(f"Erreur de traitement: {str(e)}")
                
    except KeyboardInterrupt:
        logger.info("Arrêt demandé")
    finally:
        consumer.close()
        producer.close()

if __name__ == "__main__":
    process_stream()