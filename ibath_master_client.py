import paho.mqtt.client as mqtt
from datetime import datetime

class IBathMasterClient:

    def __init__(self, mqtt_broker, mqtt_port):
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.client = mqtt.Client("ibath_master_client")

    # Función que decide qué tipo de luz usar en el baño
    # Entre las 20:30 hasta las 6 de la mañana se emitirá luz cálida
    # Por el contrario, se emite luz fría
    def process_control_light(self, payload: str):
        print('Recogido input para controlar la luz')
        time = datetime.strptime(payload, "%H:%M").time()
        if (time.hour == 20 and time.minute >= 30) or time.hour > 20 or time.hour < 6:
            print('Enviado calid light a slave')
            self.client.publish('iBath-slave/control_light', 'calid light')
        else:
            print('Enviado light a slave')
            self.client.publish('iBath-slave/control_light', 'light')

    # Función que decide si el ventilador tiene que estar encendido
    # Solo se activará si la temperatura es mayor a 25ºC
    def process_control_temperature(self, payload: str):
        print('Recogido input para controlar la temperatura')
        temperature = float(payload)
        if temperature > 25.0:
            print('Enviado on a slave')
            self.client.publish('iBath-slave/control_temperature', 'on')
        else:
            print('Enviado off a slave')
            self.client.publish('iBath-slave/control_temperature', 'off')

    # Función que decide qué alarmas emitir en el baño
    # Para el CO2, a partir de 1000 ppm el usuario puede tener dolores de cabeza y sensación de asfixia
    # Por lo que emitiría una alarma de CO2 a partir de esta cantidad.
    # A partir de una cantidad superior a un 60% de humedad, el usuario puede sentir asfixia,
    # Por lo que emitiría una alarma de humedad.
    # Si no hay riesgos, el controlador responde que no hay alarmas
    def process_control_humidity_co2(self, payload: str):
        print('Recogido input para controlar la humedad y co2')
        parameters = payload.split(',')
        humidity = float(parameters[0])
        co2 = float(parameters[1])
        alert = str()
        if co2 > 1000.0:
            alert += 'co2 alert'
        
        if humidity > 60.0:
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

    # Función listener que escucha los mensajes del slave
    def receive_slave_inputs(self, client, userdata, message):
        if str(message.topic) == 'iBath-master/control_light':
            self.process_control_light(str(message.payload.decode("utf-8")))
            
        if str(message.topic) == 'iBath-master/control_temperature':
            self.process_control_temperature(str(message.payload.decode("utf-8")))

        if str(message.topic) == 'iBath-master/control_humidity_co2':
            self.process_control_humidity_co2(str(message.payload.decode("utf-8"))) 

    # Inicializamos todas las subscripciones y listeners
    def start(self):
        self.client.connect(self.mqtt_broker, self.mqtt_port)
        self.client.subscribe("iBath-master/control_light")
        self.client.subscribe("iBath-master/control_temperature")
        self.client.subscribe("iBath-master/control_humidity_co2")
        self.client.on_message = self.receive_slave_inputs
        self.client.loop_start()
        

