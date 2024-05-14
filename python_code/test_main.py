import paho.mqtt.client as mqtt
from time import time, sleep
from hardware import *
from app_config import *
from wiskunde import *
from logica import *
from lcd_controller import *
from get_ip import *
from simple_pid import PID
from pid_controller import *
settings = Config()
settings.load_from_file() # laad config vanuit json bestand

# MQTT broker instellingen
broker_address = get_ip_adress()
broker_port = settings.mqtt_internet_poort
topic_prefix = settings.mqtt_topic_normaal
username = settings.mqtt_gebruikers_naam
password = settings.mqtt_wachtwoord

# Functie om bericht te publiceren
def publish_message(topic, message):
    client.publish(topic, message)

# Callback functie wanneer de client verbinding maakt met de broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# MQTT client initialisatie
client = mqtt.Client(username)
client.username_pw_set(username, password)  # instellen gebruikersnaam en wachtwoord
client.on_connect = on_connect  # toevoegen van de on_connect callback
client.connect(broker_address, broker_port)



hardware = Hardware()
hardware.setup_adc_0(settings.address_adc_0)
print(settings.licht_sterkte_neopixel)
hardware.setup_neopixel(settings.num_leds,settings.licht_sterkte_neopixel)
hardware.setup_leds(settings.led_hoge_storing, settings.led_lage_storing, settings.led_in_bedrijf)
hardware.setup_fan(settings.fan_pin)
hardware.setup_schakelaars(settings.schakelaars)
logica = Logica()
hardware.setup_servo(settings.servo_pin)
hardware.setup_status_leds(16)
hardware.control_status_leds(1)
heater_controller = HeaterController(10, 1, 0, 0.25)


print(settings.schakelaars)
setpoint_temperatuur = Wiskunde()
huidige_temperatuur = Wiskunde()
ticker = 0
ticker_servo = 0
hardware.servo_status = 0
ticker_led = 0





lcd_init() # i2c display aanmaken


while True:
    
    
    logica.bereken_status(hardware.schakelaar_0.is_pressed, hardware.schakelaar_1.is_pressed, hardware.schakelaar_2.is_pressed, hardware.schakelaar_3.is_pressed)
    
    if ticker >= 5:
        # Logica-informatie publiceren
        
        print(" ")
        print("Status In Bedrijf:", logica.status_in_bedrijf)
        print("Status Fan:", logica.status_fan)
        print("Status Klep:", logica.status_klep)
        print("Status Hoog Urgente Storing:", logica.status_hoog_urgente_storing)
        print("Status Laag Urgente Storing:", logica.status_laag_urgente_storing)
        print("ADC_0:", setpoint_temperatuur.temp)
        print(" ")
        hardware.control_leds(logica.status_hoog_urgente_storing,logica.status_laag_urgente_storing,logica.status_in_bedrijf)
        ticker = 0
        
    sleep(0.01)
    ticker += 1
    
    if logica.status_in_bedrijf == 1 and hardware.servo_status == 0:
        ticker_servo += 5
        hardware.move_servo(ticker_servo)
        if ticker_servo == 100:
            hardware.servo_status = 1
            hardware.control_fan(1)
            ticker_servo = 0
    
    if logica.status_hoog_urgente_storing == 1 and hardware.servo_status == 1:
        ticker -= 5
        hardware.move_servo(ticker_servo)
        print("in loop")
        print(ticker)
        if ticker_servo <= 0:
            hardware.servo_status = 0
            hardware.control_fan(0)
            hardware.led_strip_control(0, 0) 
            ticker_servo = 0
    
    lcd_string(logica.lcd_string,LCD_LINE_4)
                
    setpoint_temperatuur.volt2_temp(settings.max_temp,settings.min_temp,settings.max_volt,settings.min_volt,hardware.adc_0_channel_0.voltage)
    huidige_temperatuur.volt2_temp(settings.max_temp,settings.min_temp,settings.max_volt,settings.min_volt,hardware.adc_0_channel_1.voltage)
    publish_message(topic_prefix + "status_in_bedrijf", str(logica.status_in_bedrijf))
    publish_message(topic_prefix + "status_fan", str(logica.status_fan))
    publish_message(topic_prefix + "status_klep", str(logica.status_klep))
    publish_message(topic_prefix + "status_hoog_urgente_storing", str(logica.status_hoog_urgente_storing))
    publish_message(topic_prefix + "status_laag_urgente_storing", str(logica.status_laag_urgente_storing))
    publish_message(topic_prefix + "adc_0", str(setpoint_temperatuur.temp))
    publish_message(topic_prefix + "adc_1", str(huidige_temperatuur.temp))
    
    lcd_setpoint = "setpoint: " + str(setpoint_temperatuur.temp) + " Gr"
    lcd_string(lcd_setpoint,LCD_LINE_1)
    lcd_temp = "temperatuur: " + str(huidige_temperatuur.temp) + " Gr"
    lcd_string(lcd_temp,LCD_LINE_2)
        
    
    heater_percentage = heater_controller.bereken_vermogen(setpoint_temperatuur.temp, huidige_temperatuur.temp)
    heater_percentage = int(heater_percentage)
    
    if heater_percentage >=1:
        #print("verwarmen")
        publish_message(topic_prefix + "status_regelaar", "verwarmen")
        publish_message(topic_prefix + "verwarm_factor", int(heater_percentage))
        publish_message(topic_prefix + "koel_factor", 0)
        lcd_status = "verwarmen " + str(heater_percentage) + "%"
        lcd_string(lcd_status,LCD_LINE_3)
        if logica.status_in_bedrijf == 1 and hardware.servo_status == 1:
            hardware.led_strip_control(heater_percentage, 1) 
        
    if heater_percentage <=-1:
        #print("koelen")
        publish_message(topic_prefix + "status_regelaar", "koelen")
        publish_message(topic_prefix + "koel_factor", int(-heater_percentage))
        publish_message(topic_prefix + "verwarm_factor", 0)
        lcd_status = "koelen " + str(abs(heater_percentage)) + "%"
        lcd_string(lcd_status,LCD_LINE_3)
        if logica.status_in_bedrijf == 1 and hardware.servo_status == 1:
            hardware.led_strip_control(abs(heater_percentage), 0)
                
    
        



