from kafka import KafkaProducer
import requests
import json
import time
from datetime import datetime
import logging

# Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MeteoProducer")

# OpenWeatherMap Config
API_KEY = "520f6307ae14de11f0d946c52ff9252c"  # Remplacez par votre clé
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
CITIES = [
    {"name": "Bamako", "country": "ML"},
    {"name": "Sikasso", "country": "ML"},
    {"name": "Mopti", "country": "ML"},
    {"name": "Koutiala", "country": "ML"},
    {"name": "Ségou", "country": "ML"},
    {"name": "Gao", "country": "ML"},
    {"name": "Kayes", "country": "ML"},
    {"name": "Tombouctou", "country": "ML"}
]

# Kafka Config
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"  # Change if needed
TOPIC_NAME = "meteo-stream"

def get_weather_data(city_name, country_code):
    """Récupère les données météo depuis l'API OpenWeatherMap"""
    try:
        params = {
            'q': f"{city_name},{country_code}",
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'fr'
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Erreur lors de la récupération pour {city_name}: {str(e)}")
        return None

def transform_weather_data(raw_data):
    """Transforme les données brutes en format simplifié"""
    if not raw_data or 'main' not in raw_data:
        return None
        
    return {
        "city": raw_data['name'],
        "country": raw_data['sys']['country'],
        "timestamp": datetime.utcnow().isoformat(),
        "temperature": raw_data['main']['temp'],
        "feels_like": raw_data['main']['feels_like'],
        "temp_min": raw_data['main']['temp_min'],
        "temp_max": raw_data['main']['temp_max'],
        "humidity": raw_data['main']['humidity'],
        "pressure": raw_data['main']['pressure'],
        "wind_speed": raw_data['wind']['speed'],
        "wind_deg": raw_data['wind'].get('deg', 0),
        "clouds": raw_data['clouds']['all'],
        "weather": raw_data['weather'][0]['main'],
        "weather_desc": raw_data['weather'][0]['description'],
        "rain": raw_data.get('rain', {}).get('1h', 0),
        "snow": raw_data.get('snow', {}).get('1h', 0),
        "sunrise": datetime.utcfromtimestamp(raw_data['sys']['sunrise']).isoformat(),
        "sunset": datetime.utcfromtimestamp(raw_data['sys']['sunset']).isoformat()
    }

def create_kafka_producer():
    """Crée et retourne un producteur Kafka"""
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',
            retries=3
        )
        logger.info("Connecté à Kafka")
        return producer
    except Exception as e:
        logger.error(f"Erreur de connexion à Kafka: {str(e)}")
        raise

def main():
    producer = create_kafka_producer()
    
    while True:
        for city_info in CITIES:
            try:
                # Récupération des données
                raw_data = get_weather_data(city_info["name"], city_info["country"])
                if not raw_data:
                    continue
                
                # Transformation
                weather_data = transform_weather_data(raw_data)
                if not weather_data:
                    continue
                
                # Envoi à Kafka
                producer.send(TOPIC_NAME, value=weather_data)
                logger.info(f"Données envoyées pour {city_info['name']}: {weather_data['temperature']}°C")
                
            except Exception as e:
                logger.error(f"Erreur pour {city_info['name']}: {str(e)}")
        
        # Attente avant le prochain cycle
        time.sleep(60)  # 5 minutes entre chaque requête

if __name__ == "__main__":
    main()