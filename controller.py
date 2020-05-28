from ibath_master_client import IBathMasterClient
from constants import MQTT_BROKER, MQTT_PORT
import time

# Inicializamos el cliente con las constantes de broker y puerto
ibath_master_client = IBathMasterClient(mqtt_broker=MQTT_BROKER, mqtt_port=MQTT_PORT)
# Lanzamos el cliente
ibath_master_client.start()

while(1):
    pass

