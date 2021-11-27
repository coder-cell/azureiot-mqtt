import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import datetime
import keyboard
import time
import random
import json
import ssl

iot_hub_name = "IoTrpiHub"
device_id = "rpi-device"
path_to_root_cert = "digital.cer"
sas_token = "SharedAccessSignature sr=IoTrpiHub.azure-devices.net%2Fdevices%2Frpi-device&sig=t2A6X70RvAk8YiMs71MH6OEDiPfU6cNQfVTOlbFtjm8%3D&se=1638023592"

username = "{}.azure-devices.net/{}/api-version=2018-06-30".format(iot_hub_name, device_id)



MQTT_SERVER = iot_hub_name+".azure-devices.net"
MQTT_PATH = "channel"
SUBPATH = ["Temp", "Vol", "Visc"]


def append_datetime(msgs):
    now = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")    
    for topic in msgs:
        
        if type(topic["payload"]) is str:
            topic["payload"] = json.loads(topic["payload"])        
        topic["payload"]["datetime"] = now
        topic["payload"] = json.dumps(topic["payload"])                
    return msgs


def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK Returned code=",rc)
    else:
        print("Bad connection Returned code=",rc)
        
def on_log(client, userdata, level, buf):
    print("log: ",buf)

client = mqtt.Client(client_id=device_id, protocol=mqtt.MQTTv311, clean_session=False)

client.on_log = on_log
client.on_connect=on_connect 

client.username_pw_set(username=username,
                       password=sas_token)
client.tls_set(ca_certs=path_to_root_cert, certfile=None, keyfile=None,
               cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
client.tls_insecure_set(False)


print(client.connect(MQTT_SERVER, 8883, keepalive=60))
client.loop_start()  #Start loop 
print("In Main Loop")
t_temp = "devices/{}/messages/events/".format(device_id)
msgs= [{"topic":t_temp, "payload": {"data": "Temperature is {}".format(random.randrange(0, 100)), "datetime": None}}, ]


      
while True:
    append_datetime(msgs)  
    print(client.publish(msgs[0]["topic"], payload=msgs[0]["payload"] ))
    time.sleep(10) # Wait for connection setup to complete

client.loop_stop() 
client.disconnect()

# while True:
#     # msgs= [{"topic": "channel/Temp", "payload": {"data": "Temperature is {}".format(random.randrange(0, 100)), "datetime": None}},
#     #     {"topic": "channel/Vol", "payload": {"data": "Volume is {}".format(random.randrange(0, 100)),"datetime": None}},
#     #     {"topic": "channel/Visc", "payload": {"data": "Viscosity is {}".format(random.randrange(0, 100)), "datetime": None}} ]
    
#     t_temp = "devices/{}/messages/events/".format(device_id)
#     msgs= [{"topic":t_temp, "payload": {"data": "Temperature is {}".format(random.randrange(0, 100)), "datetime": None}}, ]
    
#     append_datetime(msgs)        
#     print(client.publish(msgs[0]["topic"], payload=msgs[0]["payload"] ))
#     print(msgs)
#     time.sleep(3)
#     if keyboard.is_pressed("q"):
#         exit(0)
