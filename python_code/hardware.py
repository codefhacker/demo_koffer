import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import neopixel
from time import sleep
from gpiozero import Servo, Button , LED

class Hardware:
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.adc_0_channel_0 = None
        self.adc_0_channel_1 = None
        self.adc_0_channel_2 = None
        self.adc_0_channel_3 = None
        
        self.adc_1_channel_0 = None
        self.adc_2_channel_1 = None
        self.adc_3_channel_2 = None
        self.adc_4_channel_3 = None
        
        self.led_strip = None
        
        self.led_hoog_urgent = None
        self.led_laag_urgent = None
        self.led_in_bedrijf = None
        
        self.schakelaar_0 = None
        self.schakelaar_1 = None
        self.schakelaar_2 = None
        self.schakelaar_3 = None
        self.schakelaar_4 = None
        self.schakelaar_5 = None
        self.schakelaar_6 = None
        self.schakelaar_7 = None
        self.schakelaar_8 = None
        self.schakelaar_9 = None
        
        self.servo = None
        self.servo_status = None
        
    def setup_adc_0(self,i2c_address):
        adc_0 = ADS.ADS1015(self.i2c, address=i2c_address)
        self.adc_0_channel_0 = AnalogIn(adc_0, ADS.P0)
        self.adc_0_channel_1 = AnalogIn(adc_0, ADS.P1)
        self.adc_0_channel_2 = AnalogIn(adc_0, ADS.P2)
        self.adc_0_channel_3 = AnalogIn(adc_0, ADS.P3)
        
    def setup_adc_1(self,i2c_address):
        adc_1 = ADS.ADS1015(self.i2c, address=i2c_address)
        self.adc_1_channel_0 = AnalogIn(adc_1, ADS.P0)
        self.adc_2_channel_1 = AnalogIn(adc_2, ADS.P1)
        self.adc_3_channel_2 = AnalogIn(adc_3, ADS.P2)
        self.adc_4_channel_3 = AnalogIn(adc_4, ADS.P3)
        
    def setup_neopixel(self,num_leds):
        self.led_strip = neopixel.NeoPixel(board.D18, num_leds, brightness=0.1)
    
    def setup_leds(self,pin_hoog_urgent,pin_laag_urgent,pin_in_bedrijf):
        self.led_hoog_urgent= LED(pin_hoog_urgent)
        self.led_laag_urgent= LED(pin_laag_urgent)
        self.led_in_bedrijf = LED(pin_in_bedrijf)
        
    def control_leds(self,hoog,laag, in_bedrijf):
        self.led_hoog_urgent.value = hoog
        self.led_laag_urgent.value = laag
        self.led_in_bedrijf.value = in_bedrijf
        
        
        
    
    def setup_schakelaars(self,schakelaars):
        self.schakelaar_0 = Button(schakelaars[0], pull_up=False)
        self.schakelaar_1 = Button(schakelaars[1], pull_up=False)
        self.schakelaar_2 = Button(schakelaars[2], pull_up=False)
        self.schakelaar_3 = Button(schakelaars[3], pull_up=False)
        self.schakelaar_4 = Button(schakelaars[4], pull_up=False)
        self.schakelaar_5 = Button(schakelaars[5], pull_up=False)
        self.schakelaar_6 = Button(schakelaars[6], pull_up=False)
        self.schakelaar_7 = Button(schakelaars[7], pull_up=False)
        self.schakelaar_8 = Button(schakelaars[8], pull_up=False)
        self.schakelaar_9 = Button(schakelaars[9], pull_up=False)
    
    def setup_servo(self,servo_pin):
        myCorrection=0.45
        maxPW=(2.0+myCorrection)/1000
        minPW=(1.0-myCorrection)/1000
        
        self.servo = Servo(servo_pin,min_pulse_width=minPW,max_pulse_width=maxPW)
    def move_servo(self, ticker):
        min_input = 0
        max_input = 100
        min_output = -1
        max_output = 1

        geschaalde_waarde = (ticker - min_input) / (max_input - min_input) * (max_output - min_output) + min_output
        
        self.servo.value = geschaalde_waarde
        sleep(0.5)
        self.servo.detach()
    
    def led_strip_control(self, vraag, status_verwarmen):
        if vraag:
            if status_verwarmen == 1:
                # Kleurverloop van rood naar donkerrood met toegevoegd groen
                r = vraag + 155
                self.led_strip.fill((r, 0, 0))
            else:
                b = vraag + 155
                self.led_strip.fill((0, 0, b))
        else:
                # Als er geen vraag is, zet de LED-strip uit
            self.led_strip.fill((0, 0, 0))  # Uitgeschakeld






        
        
        
        
         

if __name__ == "__main__":
    hardware = Hardware()
    hardware.setup_adc_0(0x48)
    hardware.setup_neopixel(8)
    hardware.setup_leds(21,20,16)
    hardware.led_strip.fill((0,20,0))

    hardware.led_strip_control(80,0)
#     hardware.led_laag_urgent.on()
#     schakelaars = (26,19,13,6,5,0,11,9,10,22)
#     hardware.setup_schakelaars(schakelaars)
#     hardware.setup_servo(12)
#     hardware.servo.value = -1
#     print("min")
#     sleep(2)
#     hardware.servo.detach()
#     hardware.servo.value = 0
#     print("mid")
#     sleep(2)
#     hardware.servo.detach()
#     hardware.servo.value = 0.5
#     print("max")
#     sleep(2)
#     hardware.servo.detach()
#     hardware.servo.value = 1
#     sleep(2)
#     hardware.servo.detach()
    
    
   
    
    
#     while True:
#         try:
#             print(hardware.adc_0_channel_0.voltage)
#             print(hardware.schakelaar_0.is_pressed)
#             
#             sleep(0.1)
#         except KeyboardInterrupt:
#             hardware.led_strip.fill((0,0,0))
#             print("stopping")
#             exit()
#         except:
#             print("error")
            
    
    
    
        
        
    
