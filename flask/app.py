
import json
from flask import Flask, render_template, request
from flask_mqtt import Mqtt
import datetime

#constant inputs
iot_hub_name = "IoTrapi"
sas_token = ""
device_id = "manipi"

username = "{}.azure-devices.net/{}/api-version=2018-06-30".format(iot_hub_name, device_id)

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = iot_hub_name+".azure-devices.net"
app.config['MQTT_BROKER_PORT'] = 8883
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_USERNAME'] = username
app.config['MQTT_PASSWORD'] = sas_token

mqtt = Mqtt()
mqtt.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")
    

@app.route("/", methods= ['POST', 'GET'])
def read():
    if  request.method == 'POST':
        if not request.form.get("reset"):        
            temp = request.form.get("Temp")
            vol = request.form.get("Vol")
            visc = request.form.get("Visc")        
        else:
            temp = vol = visc = 50
        print(request.form)        
    else:
        print(request.args)
    
    t_temp = "devices/{}/messages/events/".format(device_id)
    t_vol = "devices/{}/messages/events/Vol".format(device_id)
    t_visc = "devices/{}/messages/events/Visc".format(device_id)
    
    
    msgs= [{"topic": t_temp, "payload": {"data": "Temperature is {}".format(temp), "datetime": datetime.datetime.now().strftime("%Y-%b-%d %H:%M:%S")}},
    {"topic": t_vol, "payload": {"data": "Volume is {}".format(vol),"datetime": datetime.datetime.now().strftime("%Y-%b-%d %H:%M:%S")}},
    {"topic": t_visc, "payload": {"data": "Viscosity is {}".format(visc), "datetime": datetime.datetime.now().strftime("%Y-%b-%d %H:%M:%S")}} ]
    
    print(mqtt.connected)
    for msg in msgs:        
        mqtt.publish(msg["topic"], json.dumps(msg["payload"]))
    
    return render_template('index.html', pTemp=temp, pVol=vol, pVisc=visc)

   
if __name__ == '__main__':
    app.run(debug=True)