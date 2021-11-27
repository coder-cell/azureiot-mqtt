import paho.mqtt.client as mqtt #import library
import json
 
# MQTT_SERVER = "localhost" #specify the broker address, it can be IP of raspberry pi or simply localhost
# MQTT_PATH = "channel/Temp" #this is the name of topic, like temp



iot_hub_name = "IoTrpiHub"
device_id = "rpi-device"

MQTT_SERVER = iot_hub_name+".azure-devices.net"
username = "{}.azure-devices.net/{}/api-version=2018-06-30".format(iot_hub_name, device_id)
sas_token = "SharedAccessSignature sr=IoTrpiHub.azure-devices.net%2Fdevices%2Frpi-device&sig=NJ3VyIip3Xz3lxpbIRvfjeHiLJJ5bzMh3aV5PGZuPmQ%3D&se=1638009801"


t_temp = "devices/{}/messages/events/Temp".format(device_id)

req_list = [t_temp]
 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    for topic in req_list:
        client.subscribe(topic)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    print("Recevied: " + msg.topic +" "+ str(payload["datetime"]) + " " + str(payload["data"]))    
    # more callbacks, etc
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username=username,
                       password=sas_token)
client.connect(MQTT_SERVER, 8883)
client.loop_forever()# use this line if you don't want to write any further code. It blocks the code forever to check for data
#client.loop_start()  #use this line if you want to write any more code here