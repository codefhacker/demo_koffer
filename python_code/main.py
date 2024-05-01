import paho.mqtt.client as mqtt
from time import time, sleep
from hardware import *
from app_config import *
from wiskunde import *
from logica import *
from lcd_controller import *
from get_ip import *
# MQTT broker instellingen
broker_address = get_ip_adress()
broker_port = 1883
topic_prefix = "demo_koffer/"
username = "demo_koffer"
password = "coneco2024"

# Functie om bericht te publiceren
def publish_message(topic, message):
    client.publish(topic, message)

# Callback functie wanneer de client verbinding maakt met de broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# MQTT client initialisatie
client = mqtt.Client("demo_koffer")
client.username_pw_set(username, password)  # instellen gebruikersnaam en wachtwoord
client.on_connect = on_connect  # toevoegen van de on_connect callback
client.connect(broker_address, broker_port)

settings = Config()
settings.load_from_file() # laad config vanuit json bestand

hardware = Hardware()
hardware.setup_adc_0(settings.address_adc_0)
hardware.setup_neopixel(settings.num_leds)
hardware.setup_leds(settings.led_hoge_storing, settings.led_lage_storing, settings.led_in_bedrijf)

hardware.setup_schakelaars(settings.schakelaars)
logica = Logica()
hardware.setup_servo(settings.servo_pin)
# print(settings.schakelaars)
setpoint_temperatuur = Wiskunde()
huidige_temperatuur = Wiskunde()
ticker = 0
ticker_servo = 0
hardware.servo_status = 0
ticker_led = 0

last_led_time = time()  # Houd de tijd bij van de laatste LED-aanpassing
last_heater_list = []  # Houd de laatst bekende lijst met heaters bij
led_index = 0  # Definieer de variabele voor de LED-index
led_list_completed = False  # Vlag om aan te geven of de lijst met heaters is doorlopen


lcd_init() # i2c display aanmaken


while True:
    # Controleer of hardware.schakelaar_4.is_pressed waar is
    if hardware.schakelaar_4.is_pressed:
        mqtt_processing = True
    else:
        mqtt_processing = False
        
    if mqtt_processing:
        # Logica berekenen via MQTT
        client.loop()
    else:
        # Logica berekenen via hardware schakelaars
        logica.bereken_status(hardware.schakelaar_0.is_pressed, hardware.schakelaar_1.is_pressed, hardware.schakelaar_2.is_pressed, hardware.schakelaar_3.is_pressed)
    
    if ticker >= 10:
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
        
        # Controleer of de lijst met heaters is gewijzigd sinds de laatste keer dat deze is gebruikt
        if logica.list_heater != last_heater_list:
            last_heater_list = logica.list_heater
            led_list_completed = False  # Reset de vlag voor lijst voltooid
            last_led_time = time()  # Reset de tijd van de laatste LED-aanpassing
            print("New heater list detected. Resetting LED list completion flag.")
            led_index = 0
        print(logica.list_heater, last_heater_list)
        
        # Als de lijst met heaters is doorlopen, stel de vlag in en voer de LED-aanpassing uit
        if not led_list_completed and time() - last_led_time >= 0.5:
            if last_heater_list:  # Controleer of de lijst niet leeg is
                led_index %= len(last_heater_list)  # Zorg ervoor dat de index binnen de grenzen van de lijst blijft
                if setpoint_temperatuur.temp < huidige_temperatuur.temp:
                    hardware.led_strip_control(last_heater_list[led_index], 0)
                    publish_message(topic_prefix + "koel_factor", str(last_heater_list[led_index] + 1))
                    publish_message(topic_prefix + "verwarm_factor", "0")
                    print("Cooling LED index:", led_index)
                    lcd_cool = "regelaar klep : " + str(last_heater_list[led_index] +1) + "%"
                    lcd_string(lcd_cool,LCD_LINE_4)
                elif setpoint_temperatuur.temp > huidige_temperatuur.temp:
                    hardware.led_strip_control(last_heater_list[led_index], 1)
                    publish_message(topic_prefix + "verwarm_factor", str(last_heater_list[led_index] + 1))
                    publish_message(topic_prefix + "koel_factor", "0")
                    print("Heating LED index:", led_index)
                    lcd_warm = "regelaar klep : " + str(last_heater_list[led_index] + 1) + "%"
                    lcd_string(lcd_warm,LCD_LINE_4)
                led_index += 1  # Ga naar de volgende LED in de lijst
                last_led_time = time()  # Update de tijd van de laatste LED-aanpassing
                if led_index >= len(last_heater_list):
                    led_list_completed = True  # Alle LEDs in de lijst zijn doorlopen
                    print("LED list completed.")
            
        ticker = 0
        
    sleep(0.01)
    ticker += 1
    
    
    if logica.status_in_bedrijf == 1 and hardware.servo_status == 0:
        ticker_servo += 5
        hardware.move_servo(ticker_servo)
        if ticker_servo == 100:
            hardware.servo_status = 1
            ticker_servo = 0
    
    if logica.status_hoog_urgente_storing == 1 and hardware.servo_status == 1:
        ticker -= 5
        hardware.move_servo(ticker_servo)
        print("in loop")
        print(ticker)
        if ticker_servo <= 0:
            hardware.servo_status = 0
            ticker_servo = 0
                
    setpoint_temperatuur.volt2_temp(settings.max_temp,settings.min_temp,settings.max_volt,settings.min_volt,hardware.adc_0_channel_0.voltage)
    huidige_temperatuur.volt2_temp(settings.max_temp,settings.min_temp,settings.max_volt,settings.min_volt,hardware.adc_0_channel_1.voltage)
    publish_message(topic_prefix + "status_in_bedrijf", str(logica.status_in_bedrijf))
    publish_message(topic_prefix + "status_fan", str(logica.status_fan))
    publish_message(topic_prefix + "status_klep", str(logica.status_klep))
    publish_message(topic_prefix + "status_hoog_urgente_storing", str(logica.status_hoog_urgente_storing))
    publish_message(topic_prefix + "status_laag_urgente_storing", str(logica.status_laag_urgente_storing))
    publish_message(topic_prefix + "adc_0", str(setpoint_temperatuur.temp))
    publish_message(topic_prefix + "adc_1", str(huidige_temperatuur.temp))
    
    lcd_setpoint = "setpoint : " + str(setpoint_temperatuur.temp)
    lcd_string(lcd_setpoint,LCD_LINE_1)
    lcd_temp = "huidig : " + str(huidige_temperatuur.temp)
    lcd_string(lcd_temp,LCD_LINE_2)
        
    if setpoint_temperatuur.temp > huidige_temperatuur.temp:
        logica.bereken_vermogen(settings.Kr_factor_verwarmen,setpoint_temperatuur.temp,huidige_temperatuur.temp)
        #print("verwarmen")
        publish_message(topic_prefix + "status_regelaar", "verwarmen")
        lcd_status = "status : verwarmen"
        lcd_string(lcd_status,LCD_LINE_3)
    if setpoint_temperatuur.temp < huidige_temperatuur.temp:
        #print("koelen")
        publish_message(topic_prefix + "status_regelaar", "koelen")
        logica.bereken_vermogen(settings.Kr_factor_koelen,huidige_temperatuur.temp,setpoint_temperatuur.temp)
        lcd_status = "status : koelen"
        lcd_string(lcd_status,LCD_LINE_3)

# Detach the servo outside the while loop
hardware.servo.detach()

