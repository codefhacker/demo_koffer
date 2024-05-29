import paho.mqtt.client as mqtt
import time
from hardware import *
from app_config import *
from wiskunde import *
from logica import *
from lcd_controller import *
from get_ip import *

#laad instellingen
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
topic_fan_storing = "storing/fan"
topic_klep_storing = "storing/klep"
topic_filter_storing = "storing/filter"

topic_klep_stand = "servo/klep_stand"

# hardware instellingen 
hardware = Hardware()
hardware.setup_adc_0(settings.address_adc_0)
hardware.setup_neopixel(settings.num_leds,settings.licht_sterkte_neopixel)
hardware.setup_leds(settings.led_hoge_storing, settings.led_lage_storing, settings.led_in_bedrijf)
hardware.setup_schakelaars(settings.schakelaars)
hardware.setup_servo(settings.servo_pin)
hardware.setup_fan(settings.fan_pin)

hardware.ticker_servo = 0
hardware.servo_status = 0

#logica functies
logica = Logica()

analoog_0 = Wiskunde()
analoog_1 = Wiskunde()
analoog_2 = Wiskunde()
analoog_3 = Wiskunde()
# verbind op de topics

hardware.led_ticker = 0

hardware.koelen = 0
hardware.verwarmen = 0

hardware.storing_filter = 0
hardware.storing_klep = 0
hardware.storing_fan = 0
hardware.in_bedrijf = 0
lcd_init() # i2c display aanmaken

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
    client.subscribe(topic_prefix + topic_filter_storing)
    client.subscribe(topic_prefix + topic_klep_storing)
    client.subscribe(topic_prefix + topic_fan_storing)
    
# Callback function when a message is received from the subscribed topic
def on_message(client, userdata, msg):
    #print("Received message on topic:", msg.topic)
    #print("Message:", msg.payload.decode())
    # Here you can add your logic to process the received message
    
    topic = msg.topic
    if topic.startswith("demo_koffer/modbus/leds") or topic.startswith("demo_koffer/modbus/led_strip"):
        mqtt_topic = topic
        mqtt_topic = mqtt_topic.split("/")
        mqtt_topic = mqtt_topic[3]
        
        data = msg.payload.decode()
        if data == "true":
            data = 1
        if data == "false":
            data = 0
        data = int(data)
        
        if mqtt_topic == "warmte_vraag":
            if data >=1:
                hardware.led_strip_control(data, 1)
                hardware.led_strip_status = "verwarmen"
                hardware.led_strip_data = str(abs(data))
                hardware.verwarmen = 0
                
            if data == 0:
                hardware.verwarmen = 1
                if hardware.koelen == 1:
                    hardware.led_strip_status = ""
            
        if mqtt_topic == "koude_vraag":
            if data >= 1:
                hardware.led_strip_control(data, 0)
                hardware.led_strip_status = "koelen"
                hardware.led_strip_data = str(abs(data))
                hardware.koelen = 0
                
            if data == 0:
                hardware.koelen = 1
                if hardware.verwarmen == 1:
                    hardware.led_strip_status = ""
        
        if mqtt_topic == "led_in_bedrijf":
            if data == 1:
                hardware.led_in_bedrijf.value = 1
                hardware.in_bedrijf = 1
            
            if data == 0:
                hardware.led_in_bedrijf.value = 0
                hardware.in_bedrijf = 0
                hardware.led_ticker +=1
                if hardware.led_ticker >=100:
                    hardware.led_strip_control(data, 1)
                    hardware.led_ticker = 0
                    
                
        
    if topic == "demo_koffer/modbus/servo/klep":
        
        data = msg.payload.decode()
        
        if data == "true" and hardware.servo_status == 0:
            hardware.ticker_servo += settings.tijd_vertraging_servo 
            hardware.move_servo(hardware.ticker_servo)
            if hardware.ticker_servo == 100:
                hardware.servo_status = 1
                hardware.klep_stand = 1
                hardware.ticker_servo = 0
                
                
        if data == "false" and hardware.servo_status == 1:
            hardware.ticker_servo -= 5
           
            hardware.move_servo(0)
            if hardware.ticker_servo <= 0:
                hardware.servo_status = 0
                hardware.klep_stand = 0
                hardware.ticker_servo = 0
                
            
                
    if topic == "demo_koffer/modbus/fan":
        
        data = msg.payload.decode()
        if data == "true":
            hardware.control_fan(1)
        if data == "false":
            hardware.control_fan(0)
            
    
    
    if topic == topic_prefix + topic_klep_storing:
        data = msg.payload.decode()
        if data == "true":
            hardware.storing_klep = 1
            print("klep aan")
             
        if data == "false":
            hardware.storing_klep = 0
            print("klep uit")
    
    if topic == topic_prefix + topic_fan_storing:
        data = msg.payload.decode()
        if data == "true":
            hardware.storing_fan = 1
            print("fan aan")
             
        if data == "false":
            hardware.storing_fan = 0
            print("fan uit")
            
    
    if topic == topic_prefix + topic_filter_storing:
        data = msg.payload.decode()
        if data == "true":
            hardware.storing_filter = 1
            print("filter aan")
        if data == "false":
            hardware.storing_filter = 0
            print("filter uit")
            
        
     
    
    
# MQTT client initialization
client = mqtt.Client(username)
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

old_klep_stand = None
ticker_led_hoog = 0
lh_state = 1

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
        print("status schakelaar :" + str(hardware.schakelaar_3.is_pressed))
    
    if old_klep_stand != hardware.klep_stand:
        client.publish(topic_prefix + topic_klep_stand,int(hardware.klep_stand))
        old_klep_stand = hardware.klep_stand
        
    lcd_setpoint = "setpoint: " + str(analoog_0.temp) + " *C" 
    lcd_string(lcd_setpoint,LCD_LINE_1)
    lcd_temp = "temperatuur: " + str(analoog_1.temp) + " *C"
    lcd_string(lcd_temp,LCD_LINE_2)
    if hardware.led_strip_status == "koelen" or hardware.led_strip_status == "verwarmen":
        lcd_string_regel_3 = hardware.led_strip_status + ": " + hardware.led_strip_data + "%"
        lcd_string(lcd_string_regel_3,LCD_LINE_3)
   
    if hardware.koelen == 1 and hardware.verwarmen == 1:
        lcd_string("neutraal: 0%",LCD_LINE_3)   
    
    
    if hardware.storing_fan == 1 or hardware.storing_klep == 1:
        hardware.led_hoog_urgent.value = lh_state
    
    if hardware.storing_filter == 1:
        hardware.led_laag_urgent.value = lh_state
            
            
            
        print("test")
        
    if hardware.storing_fan == 0 and hardware.storing_klep == 0:
        hardware.led_hoog_urgent.value = 0
        print("test")
        
    if hardware.storing_filter == 0:
        hardware.led_laag_urgent.value = 0
        print("test")
        
    logica.bereken_status(hardware.in_bedrijf,hardware.storing_fan,hardware.storing_klep,hardware.storing_filter)
    lcd_string(logica.lcd_string,LCD_LINE_4)
    
    
    time.sleep(0.2)
    ticker_led_hoog +=1
    if ticker_led_hoog >=settings.knippertijd_storings_leds:
        lh_state = not lh_state
        ticker_led_hoog = 0
    
    

    
    
    


