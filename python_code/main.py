from hardware import *
from app_config import *
from wiskunde import *
from logica import *
settings = Config()
settings.load_from_file() # laad config vanuit json bestand




hardware = Hardware()
hardware.setup_adc_0(settings.address_adc_0)
hardware.setup_neopixel(settings.num_leds)
hardware.setup_leds(settings.led_hoge_storing, settings.led_lage_storing, settings.led_in_bedrijf)
hardware.led_strip.fill((0, 255, 0))
hardware.setup_schakelaars(settings.schakelaars)
logica = Logica()

print(settings.schakelaars)
wiskunde_0 = Wiskunde()
wiskunde_1 = Wiskunde()
ticker = 0
while True:
    logica.bereken_status(hardware.schakelaar_0.is_pressed, hardware.schakelaar_1.is_pressed, hardware.schakelaar_2.is_pressed, hardware.schakelaar_3.is_pressed)
    #print(hardware.schakelaar_0.is_pressed)
    if ticker >= 1:
        print(" ")
        print("Status In Bedrijf:", logica.status_in_bedrijf)
        print("Status Fan:", logica.status_fan)
        print("Status Klep:", logica.status_klep)
        print("Status Hoog Urgente Storing:", logica.status_hoog_urgente_storing)
        print("Status Laag Urgente Storing:", logica.status_laag_urgente_storing)
        print("ADC_0:", wiskunde_0.temp)
        print("ADC_1:", wiskunde_1.temp)
        print(" ")
        hardware.control_leds(logica.status_hoog_urgente_storing,logica.status_laag_urgente_storing,logica.status_in_bedrijf)
        ticker = 0
    sleep(0.1)
    ticker += 0.1
    
    
    wiskunde_0.volt2_temp(settings.max_temp,settings.min_temp,settings.max_volt,settings.min_volt,hardware.adc_0_channel_0.voltage)
    wiskunde_1.volt2_temp(settings.max_temp,settings.min_temp,settings.max_volt,settings.min_volt,hardware.adc_0_channel_1.voltage)



