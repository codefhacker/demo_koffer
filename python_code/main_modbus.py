import paho.mqtt.client as mqtt
import time
from hardware import *
from app_config import *
from wiskunde import *
from logica import *
from lcd_controller import *
from get_ip import *


settings = Config()
settings.load_from_file()

# MQTT instellingen
broker_address = get_ip_adress()
broker_port = settings.mqtt_internet_poort
topic_prefix = settings.mqtt_topic_modbus
username = settings.mqtt_gebruikers_naam
password = settings.mqtt_wachtwoord

#topic voor mqtt
topic_schakelaars = ["schakelaar_0", "schakelaar_1", "schakelaar_2", "schakelaar_3", "schakelaar_4", "schakelaar_5"]
topic_analoge_ingangen = ["analoog_0", "analoog_1", "analoog_2" , "analoog_3"]
topic_leds = ["led_hoog_urgent", "led_laag_urgent" , "led_in_bedrijf", "led_4" , "led_5" , "led_6"]
topic_led_strip = ["warmte_vraag" , "koude_vraag"]
topic_servo = "servo/klep"
topic_fan = "fan"

#laad isntellingen


hardware = Hardware()
hardware.setup_adc_0(settings.address_adc_0)
hardware.setup_neopixel(settings.num_leds,settings.licht_sterkte_neopixel)
hardware.setup_leds(settings.led_hoge_storing, settings.led_lage_storing, settings.led_in_bedrijf)
hardware.setup_schakelaars(settings.schakelaars)
logica = Logica()
hardware.setup_servo(settings.servo_pin)
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
client.username_pw_set(username, password)  # Set username and password
client.on_connect = on_connect  # Add the on_connect callback
client.on_message = on_message  # Add the on_message callback
client.connect(broker_address, broker_port)

# Start the network loop to process incoming and outgoing messages
client.loop_start()
ticker = 0 
# Initialiseer oude waarden voor de variabelen
old_analoog_0 = None
old_analoog_1 = None
old_analoog_2 = None
old_analoog_3 = None

old_schakelaar_0_state = None
old_schakelaar_1_state = None
old_schakelaar_2_state = None
old_schakelaar_3_state = None
# Voeg hier andere variabelen toe die je wilt bewaken

while True:
    analoog_0.volt2_temp(settings.max_temp, settings.min_temp, settings.max_volt, settings.min_volt, hardware.adc_0_channel_0.voltage)
    analoog_1.volt2_temp(settings.max_temp, settings.min_temp, settings.max_volt, settings.min_volt, hardware.adc_0_channel_1.voltage)
    analoog_3.volt2_temp(settings.max_temp, settings.min_temp, settings.max_volt, settings.min_volt, hardware.adc_0_channel_2.voltage)
    analoog_2.volt2_temp(settings.max_temp, settings.min_temp, settings.max_volt, settings.min_volt, hardware.adc_0_channel_3.voltage)
    

    # Controleren en publiceren van nieuwe waarden van max_temp
    if old_analoog_0 != analoog_0.temp:
        client.publish(topic_prefix + "analoge_ingangen", str([analoog_0.temp * 10 ,analoog_1.temp * 10 ,analoog_2.temp * 10 ,analoog_3.temp * 10]))
        old_analoog_0 = analoog_0.temp
        
    if old_analoog_1 != analoog_1.temp:
        client.publish(topic_prefix + "analoge_ingangen", str([analoog_0.temp * 10 ,analoog_1.temp * 10 ,analoog_2.temp * 10 ,analoog_3.temp * 10]))
        old_analoog_1 = analoog_1.temp
        
    if old_analoog_2 != analoog_2.temp:
        client.publish(topic_prefix + "analoge_ingangen", str([analoog_0.temp * 10 ,analoog_1.temp * 10 ,analoog_2.temp * 10 ,analoog_3.temp * 10]))
        old_analoog_2 = analoog_2.temp
        
    if old_analoog_3 != analoog_3.temp:
        client.publish(topic_prefix + "analoge_ingangen", str([analoog_0.temp * 10 ,analoog_1.temp * 10 ,analoog_2.temp * 10 ,analoog_3.temp * 10]))
        old_analoog_3 = analoog_3.temp

    # Controleren en publiceren van nieuwe waarden van schakelaar_0
    if old_schakelaar_0_state != hardware.schakelaar_0.is_pressed:
        client.publish(topic_prefix + "schakelaars", str([int(hardware.schakelaar_0.is_pressed), int(hardware.schakelaar_1.is_pressed), int(hardware.schakelaar_2.is_pressed), int(hardware.schakelaar_3.is_pressed)]))
        old_schakelaar_0_state = hardware.schakelaar_0.is_pressed

    # Controleren en publiceren van nieuwe waarden van schakelaar_1
    if old_schakelaar_1_state != hardware.schakelaar_1.is_pressed:
        client.publish(topic_prefix + "schakelaars", str([int(hardware.schakelaar_0.is_pressed), int(hardware.schakelaar_1.is_pressed), int(hardware.schakelaar_2.is_pressed), int(hardware.schakelaar_3.is_pressed)]))
        old_schakelaar_1_state = hardware.schakelaar_1.is_pressed

    # Controleren en publiceren van nieuwe waarden van schakelaar_2
    if old_schakelaar_2_state != hardware.schakelaar_2.is_pressed:
        client.publish(topic_prefix + "schakelaars", str([int(hardware.schakelaar_0.is_pressed), int(hardware.schakelaar_1.is_pressed), int(hardware.schakelaar_2.is_pressed), int(hardware.schakelaar_3.is_pressed)]))
        old_schakelaar_2_state = hardware.schakelaar_2.is_pressed

    # Controleren en publiceren van nieuwe waarden van schakelaar_3
    if old_schakelaar_3_state != hardware.schakelaar_3.is_pressed:
        client.publish(topic_prefix + "schakelaars", str([int(hardware.schakelaar_0.is_pressed), int(hardware.schakelaar_1.is_pressed), int(hardware.schakelaar_2.is_pressed), int(hardware.schakelaar_3.is_pressed)]))
        old_schakelaar_3_state = hardware.schakelaar_3.is_pressed
    
    time.sleep(0.2)

    
    
    


