import paho.mqtt.client as mqtt #import library
import json
import ssl
# MQTT_SERVER = "localhost" #specify the broker address, it can be IP of raspberry pi or simply localhost
# MQTT_PATH = "channel/Temp" #this is the name of topic, like temp



iot_hub_name = "IoTrpiHub"
device_id = "rpi-device"
path_to_root_cert = "digital.cer"

MQTT_SERVER = iot_hub_name+".azure-devices.net"
username = "{}.azure-devices.net/{}/api-version=2018-06-30".format(iot_hub_name, device_id)
sas_token = "SharedAccessSignature sr=IoTrpiHub.azure-devices.net%2Fdevices%2Frpi-device&sig=t2A6X70RvAk8YiMs71MH6OEDiPfU6cNQfVTOlbFtjm8%3D&se=1638023592"


t_temp = "devices/{device_id}/messages/devicebound/#".format(device_id=device_id)

req_list = [t_temp]
 
def on_subscribe(client, userdata, mid, granted_qos):
    print('Subscribed for m' + str(mid))

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


def on_log(client, userdata, level, buf):
    print("log: ",buf)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    print("Recevied: " + msg.topic +" "+ str(payload["datetime"]) + " " + str(payload["data"] + "with Qos:" + str(msg.qos)))    
    # more callbacks, etc
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username=username,
                       password=sas_token)
client.tls_set(ca_certs=path_to_root_cert, certfile=None, keyfile=None,
               cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
client.tls_insecure_set(False)

client.connect(MQTT_SERVER, 8883)
print("connected")
client.subscribe("devices/{device_id}/messages/devicebound/".format(device_id=device_id))
client.loop_forever()# use this line if you don't want to write any further code. It blocks the code forever to check for data
#client.loop_start()  #use this line if you want to write any more code here