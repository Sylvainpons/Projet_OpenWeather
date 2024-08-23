import Projet_OpenWeather.streamlit as st
from kafka import KafkaConsumer
from pymongo import MongoClient
import json
import pandas as pd

# Configuration Kafka
KAFKA_TOPIC = 'weather_data'
KAFKA_SERVER = 'kafka:9092'

# Configuration MongoDB
MONGO_URI = 'https://localhost:27017'
MONGO_DB = 'weather_db'
MONGO_COLLECTION = 'weather_data'


# Connexion à Kafka
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    group_id='weather-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Connexion à MongoDB
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client[MONGO_DB]
mongo_collection = mongo_db[MONGO_COLLECTION]



# Streamlit App
st.title('Dashboard Météorologique')

# Section Temps Réel
st.subheader('Données en Temps Réel depuis Kafka')

# Fonction pour obtenir les derniers messages de Kafka
def get_kafka_data():
    messages = []
    for message in consumer:
        data = message.value
        messages.append(data)
        if len(messages) > 10:  # Limiter le nombre de messages affichés
            break
    return messages

# Afficher les messages Kafka en temps réel
kafka_data = get_kafka_data()
if kafka_data:
    st.write(pd.DataFrame(kafka_data))
else:
    st.write("Aucune donnée en temps réel disponible.")

# Section Historique
st.subheader('Données Historisées')

# Sélection de la base de données pour les données historiques
db_choice = st.radio("Choisissez la source des données historiques:", ("MongoDB", "Cassandra"))

if db_choice == "MongoDB":
    # Fonction pour obtenir les données historisées de MongoDB
    def get_mongo_data():
        return list(mongo_collection.find({}))
    
    mongo_data = get_mongo_data()
    if mongo_data:
        st.write(pd.DataFrame(mongo_data))
    else:
        st.write("Aucune donnée historique disponible dans MongoDB.")


