import paho.mqtt.client as mqtt
from datetime import datetime

class IBathMasterClient:

    def __init__(self, mqtt_broker, mqtt_port):
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.client = mqtt.Client("ibath_master_client")

    def process_control_light(self, payload: str):
        print('Recogido input para controlar la luz')
        time = datetime.strptime(payload, "%H:%M").time()
        if (time.hour == 20 and time.minute >= 30) or time.hour > 20 or time.hour < 6:
            print('Enviado calid light a slave')
            self.client.publish('iBath-slave/control_light', 'calid light')
        else:
            print('Enviado light a slave')
            self.client.publish('iBath-slave/control_light', 'light')

    def process_control_temperature(self, payload: str):
        print('Recogido input para controlar la temperatura')
        temperature = float(payload)
        if temperature > 20.0:
            print('Enviado on a slave')
            self.client.publish('iBath-slave/control_temperature', 'on')
        else:
            print('Enviado off a slave')
            self.client.publish('iBath-slave/control_temperature', 'off')

    def process_control_humidity_co2(self, payload: str):
        print('Recogido input para controlar la humedad y co2')
        parameters = payload.split(',')
        humidity = float(parameters[0])
        co2 = float(parameters[1])
        alert = str()
        if co2 > 1000.0:
            alert += 'co2 alert'
        
        if humidity > 30.0:
            if len(alert) == 0:
                alert += 'humidity alert'
            else:
                alert += ' and humidity alert'
        
        if len(alert) > 0:
            print('Enviado ' + alert + ' a slave')
            self.client.publish('iBath-slave/control_humidity_co2', alert)

        else:
            print('Enviado no alert a slave')
            self.client.publish('iBath-slave/control_humidity_co2', 'no alert')

    def receive_slave_inputs(self, client, userdata, message):
        if str(message.topic) == 'iBath-master/control_light':
            self.process_control_light(str(message.payload.decode("utf-8")))
            
        if str(message.topic) == 'iBath-master/control_temperature':
            self.process_control_temperature(str(message.payload.decode("utf-8")))

        if str(message.topic) == 'iBath-master/control_humidity_co2':
            self.process_control_humidity_co2(str(message.payload.decode("utf-8"))) 

    def start(self):
        self.client.connect(self.mqtt_broker, self.mqtt_port)
        self.client.subscribe("iBath-master/control_light") # Subscribe to the topic AC_unit
        self.client.subscribe("iBath-master/control_temperature")
        self.client.subscribe("iBath-master/control_humidity_co2")
        self.client.on_message = self.receive_slave_inputs # Attach the messageFunction to subscription
        self.client.loop_start() # Start the MQTT client
        

