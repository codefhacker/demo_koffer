import paho.mqtt.client as mqtt
import time
from hardware import *
from app_config import *
from wiskunde import *
from logica import *
#from lcd_controller import *
from get_ip import *

# MQTT instellingen
broker_address = get_ip_adress()
broker_port = 1883
topic_prefix = "demo_koffer/modbus/"
username = "demo_koffer"
password = "coneco2024"

#topic voor mqtt
topic_schakelaars = ["schakelaar_0", "schakelaar_1", "schakelaar_2", "schakelaar_3", "schakelaar_4", "schakelaar_5"]
topic_analoge_ingangen = ["analoog_0", "analoog_1", "analoog_2" , "analoog_3"]
topic_leds = ["led_hoog_urgent", "led_laag_urgent" , "led_in_bedrijf", "led_4" , "led_5" , "led_6"]
topic_led_strip = ["warmte_vraag" , "koude_vraag"]
topic_servo = "servo/klep"
topic_fan = "fan"

#laad isntellingen

settings = Config()
settings.load_from_file()
hardware = Hardware()
hardware.setup_adc_0(settings.address_adc_0)
hardware.setup_neopixel(settings.num_leds)
hardware.setup_leds(settings.led_hoge_storing, settings.led_lage_storing, settings.led_in_bedrijf)
hardware.setup_schakelaars(settings.schakelaars)
logica = Logica()
hardware.setup_servo(12)
print(settings.schakelaars)
analoog_0 = Wiskunde()
analoog_1 = Wiskunde()
analoog_2 = Wiskunde()
analoog_3 = Wiskunde()
# verbind op de topics
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribe to a topic upon successful connection
    client.subscribe(topic_prefix + "modbus")
    for schakelaar in topic_schakelaars:
        client.subscribe(topic_prefix + "schakelaars/" + schakelaar)
    for analoge_ingang in topic_analoge_ingangen:
        client.subscribe(topic_prefix + "analoge_ingangen/" + analoge_ingang)
    for led_strip in topic_led_strip:
        client.subscribe(topic_prefix + "led_strip/" + led_strip)
    for leds in topic_leds:
        client.subscribe(topic_prefix + "leds/" + leds)
    client.subscribe(topic_prefix + topic_servo)
    client.subscribe(topic_prefix + topic_fan)
    
    
    

        
    
        

# Callback function when a message is received from the subscribed topic
def on_message(client, userdata, msg):
    #print("Received message on topic:", msg.topic)
    #print("Message:", msg.payload.decode())
    # Here you can add your logic to process the received message
    
    topic = msg.topic
    if topic.startswith("demo_koffer/modbus/leds") or topic.startswith("demo_koffer/modbus/led_strip"):
        test = topic
        test = test.split("/")
        test = test[3]
        print(test)
        print(msg.payload.decode())
    if topic == "demo_koffer/modbus/servo/klep":
        print("servo/klep")
        print(msg.payload.decode())
    if topic == "demo_koffer/modbus/fan":
        print("fan")
        print(msg.payload.decode())
        
    
    
    
        
    
    
    

# MQTT client initialization
client = mqtt.Client("demo_koffer")
#client.username_pw_set(username, password)  # Set username and password
client.on_connect = on_connect  # Add the on_connect callback
client.on_message = on_message  # Add the on_message callback
client.connect(broker_address, broker_port)

# Start the network loop to process incoming and outgoing messages
client.loop_start()
ticker = 0
while True:
    ticker +=1
    #print(settings.max_temp)
   # print(hardware.adc_0_channel_0.voltage)
    analoog_0.volt2_temp(settings.max_temp,settings.min_temp,settings.max_volt,settings.min_volt,hardware.adc_0_channel_0.voltage)
    #print(analoog_0.temp)
    analoog_1.volt2_temp(settings.max_temp,settings.min_temp,settings.max_volt,settings.min_volt,hardware.adc_0_channel_1.voltage)
    #print(analoog_1.temp)
    analoog_2.volt2_temp(settings.max_temp,settings.min_temp,settings.max_volt,settings.min_volt,hardware.adc_0_channel_2.voltage)
    #print(analoog_2.temp)
    analoog_3.volt2_temp(settings.max_temp,settings.min_temp,settings.max_volt,settings.min_volt,hardware.adc_0_channel_3.voltage)
    #print(analoog_3.temp)
    
    client.publish(topic_prefix + "analoge_ingangen/analoog_0", analoog_0.temp)
    client.publish(topic_prefix + "analoge_ingangen/analoog_1", analoog_1.temp)
    client.publish(topic_prefix + "analoge_ingangen/analoog_2", analoog_2.temp)
    client.publish(topic_prefix + "analoge_ingangen/analoog_3", analoog_3.temp)
#     client.publish(topic_prefix + "analoge_ingangen/analoog_1", ticker)
#     client.publish(topic_prefix + "analoge_ingangen/analoog_2", ticker)
#     client.publish(topic_prefix + "analoge_ingangen/analoog_3", ticker)
#     print(ticker)
    #print("Published message:", message)
    time.sleep(0.05)
    


