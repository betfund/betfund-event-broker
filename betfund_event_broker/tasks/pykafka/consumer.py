"""ONLY FOR TESTING PURPOSES"""
import json

from kafka import KafkaConsumer

CONSUMER = KafkaConsumer(
    'upcomingEvents',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in CONSUMER:
    print(message)
