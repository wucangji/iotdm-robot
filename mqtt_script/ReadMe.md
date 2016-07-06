1. install the paho-mqtt:  
`sudo pip install paho-mqtt`  
May need to upgrade pip  
`sudo pip install --upgrade pip`  

if already installed the old version of paho-mqtt, upgrade with  
`sudo pip install paho-mqtt --upgrade`

2. put the script under the vm that runs iotdm.
3. run the script file "mqtt_script.py" with  
`python mqtt_script.py`



The script will subscribe to the topic "/tdf/test" of "168.128.108.105",
if the topic update, the script will grab the json data "deviceName" from the message payload, then create the <container> under the local IOTDM CSE "InCSE" with the name same with "deviceName"(ignore this step if the container already exists), then create a <ContentInstance> with the "con" attribute contains the whole json payload from the MQTT topic(String format).

