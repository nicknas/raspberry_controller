from ibath_master_client import IBathMasterClient
from constants import MQTT_BROKER, MQTT_PORT
import time



# Main program loop
ibath_master_client = IBathMasterClient(mqtt_broker=MQTT_BROKER, mqtt_port=MQTT_PORT)
ibath_master_client.start()


while(1):
    pass

