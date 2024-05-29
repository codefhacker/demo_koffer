from hardware import *
from app_config import *
from time import sleep
from lcd_controller import *
from wiskunde import *


settings = Config()
settings.load_from_file()

hardware = Hardware()
hardware.setup_adc_0(settings.address_adc_0)
from hardware import *
from app_config import *
from time import sleep
from lcd_controller import *
from wiskunde import *


settings = Config()
settings.load_from_file()

hardware = Hardware()
hardware.setup_adc_0(settings.address_adc_0)
hardware.setup_adc_1(settings.address_adc_1)
hardware.setup_neopixel(settings.num_leds,settings.licht_sterkte_neopixel)
hardware.setup_leds(settings.led_hoge_storing, settings.led_lage_storing, settings.led_in_bedrijf)
hardware.setup_schakelaars(settings.schakelaars)
hardware.setup_servo(settings.servo_pin)
hardware.setup_fan(settings.fan_pin)

analoog_0 = Wiskunde()
analoog_1 = Wiskunde()
analoog_2 = Wiskunde()
analoog_3 = Wiskunde()

lcd_init() # i2c display aanmaken

state = 0
x = 0
while True:
    analoog_0.volt2_temp(settings.max_temp, settings.min_temp, settings.max_volt, settings.min_volt, hardware.adc_0_channel_0.voltage)
    analoog_1.volt2_temp(settings.max_temp, settings.min_temp, settings.max_volt, settings.min_volt, hardware.adc_0_channel_1.voltage)
    analoog_3.volt2_temp(settings.max_temp, settings.min_temp, settings.max_volt, settings.min_volt, hardware.adc_1_channel_0.voltage)
    analoog_2.volt2_temp(settings.max_temp, settings.min_temp, settings.max_volt, settings.min_volt, hardware.adc_0_channel_3.voltage)
    
    hardware.control_leds(1,1,1)
    hardware.led_strip_control(x,state)
    hardware.move_servo(x)
    sleep(0.2)
    hardware.control_leds(0,0,0)
    sleep(0.2)
    x +=10
    if x >= 100:  
        x = 0
        state = not state
    hardware.control_fan(state)  
    lcd_string("testprogramma",LCD_LINE_1)
    schakelaar_string = "schakelaars: " + str(int(hardware.schakelaar_0.is_pressed)) + "," + str(int(hardware.schakelaar_1.is_pressed)) + "," + str(int(hardware.schakelaar_2.is_pressed)) +  "," + str(int(hardware.schakelaar_3.is_pressed))
    lcd_string(schakelaar_string,LCD_LINE_2)
    pot_string = "pot: " + str(int(analoog_0.temp)) + "," + str(int(analoog_1.temp)) + "," + str(int(analoog_2.temp)) + "," + str(int(analoog_3.temp))
    lcd_string(pot_string,LCD_LINE_3)
    
    



lcd_init() # i2c display aanmaken

state = 0
x = 0
while True:
    analoog_0.volt2_temp(settings.max_temp, settings.min_temp, settings.max_volt, settings.min_volt, hardware.adc_0_channel_0.voltage)
    analoog_1.volt2_temp(settings.max_temp, settings.min_temp, settings.max_volt, settings.min_volt, hardware.adc_0_channel_1.voltage)
    analoog_3.volt2_temp(settings.max_temp, settings.min_temp, settings.max_volt, settings.min_volt, hardware.adc_0_channel_2.voltage)
    analoog_2.volt2_temp(settings.max_temp, settings.min_temp, settings.max_volt, settings.min_volt, hardware.adc_0_channel_3.voltage)
    
    hardware.control_leds(1,1,1)
    hardware.led_strip_control(x,state)
    hardware.move_servo(x)
    sleep(0.2)
    hardware.control_leds(0,0,0)
    sleep(0.2)
    x +=10
    if x >= 100:
        x = 0
        state = not state
    hardware.control_fan(state)
    lcd_string("testprogramma",LCD_LINE_1)
    schakelaar_string = "schakelaars: " + str(int(hardware.schakelaar_0.is_pressed)) + "," + str(int(hardware.schakelaar_1.is_pressed)) + "," + str(int(hardware.schakelaar_2.is_pressed)) +  "," + str(int(hardware.schakelaar_3.is_pressed))
    lcd_string(schakelaar_string,LCD_LINE_2)
    pot_string = "pot: " + str(int(analoog_0.temp)) + "," + str(int(analoog_1.temp)) + "," + str(int(analoog_2.temp)) + "," + str(int(analoog_3.temp))
    lcd_string(pot_string,LCD_LINE_3)
    
    
