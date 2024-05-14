"""
App config lader

Gemaakt door Fabian Boshoven

Versie 1

Dit programma laad het instellingen bestand en controleerd of deze goed is ingeladen.
De instellingen kan je na het laden gemakkelijk opvragen.

Mocht het laden van het instellingen bestand niet lukken dan wordt het bestand opnieuw aangemaakt met de basis instellingen.

Versie 1

"""





import json
from time import sleep

class Config:
    def __init__(self):
        self.servo_pin = None
        self.led_hoge_storing = None
        self.led_lage_storing = None
        self.led_in_bedrijf = None
        self.fan_pin = None
        self.led_strip_pin = None
        self.potmeter_temperatuur = None
        self.potmeter_setpoint = None
        self.tijd_vertraging_servo = None
        self.Kr_factor_verwarmen = None
        self.Kr_factor_koelen = None
        self.max_volt = None
        self.min_volt = None
        self.max_temp = None
        self.min_temp = None
        self.address_adc_0 = None
        self.address_adc_1 = None
        self.num_leds = None
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
        self.schakelaars = {str(i): None for i in range(10)}
        self.mqtt_gebruikers_naam = None
        self.mqtt_wachtwoord = None
        self.mqtt_internet_poort = None
        self.max_procent_regelaar = None
        self.min_procent_regelaar = None
        self.licht_sterkte_neopixel = None
        self.mqtt_topic_modbus = None
        self.mqtt_topic_normaal = None

    def load_from_file(self, filename='config.json'):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.servo_pin = data['demo_koffer']['hardware']['digitale_pinnen']['servo_pin']
                
                self.led_hoge_storing = data['demo_koffer']['hardware']['digitale_pinnen']['led_hoge_storing']
                self.led_lage_storing = data['demo_koffer']['hardware']['digitale_pinnen']['led_lage_storing']
                self.led_in_bedrijf = data['demo_koffer']['hardware']['digitale_pinnen']['led_in_bedrijf']
                
                self.fan_pin = data['demo_koffer']['hardware']['digitale_pinnen']['fan_pin']
                self.led_strip_pin = data['demo_koffer']['hardware']['digitale_pinnen']['led_strip_pin']
                self.potmeter_temperatuur = data['demo_koffer']['hardware']['analoge_pinnen']['potmeter_temperatuur']
                self.potmeter_setpoint = data['demo_koffer']['hardware']['analoge_pinnen']['potmeter_setpoint']
                self.tijd_vertraging_servo = data['demo_koffer']['overige_instellingen']['tijd_vertraging_servo']
                
                self.Kr_factor_verwarmen = data['demo_koffer']['overige_instellingen']['Kr_factor_verwarmen']
                self.Kr_factor_koelen = data['demo_koffer']['overige_instellingen']['Kr_factor_koelen']
                
                self.max_volt = data['demo_koffer']['overige_instellingen']['maximale_voltage']
                self.min_volt = data['demo_koffer']['overige_instellingen']['minimale_voltage']
                self.max_temp = data['demo_koffer']['overige_instellingen']['maximale_temperatuur']
                self.min_temp = data['demo_koffer']['overige_instellingen']['minimale_temperatuur']
                
                self.address_adc_0 = data['demo_koffer']['overige_instellingen']['i2c_address_adc_0']
                self.address_adc_1 = data['demo_koffer']['overige_instellingen']['i2c_address_adc_1']
                
                self.num_leds = data['demo_koffer']['overige_instellingen']['aantal_neopixel_leds']
                
                self.mqtt_gebruikers_naam = data['demo_koffer']['overige_instellingen']['mqtt_gebruikers_naam']
                self.mqtt_wachtwoord = data['demo_koffer']['overige_instellingen']['mqtt_wachtwoord']
                self.mqtt_internet_poort = data['demo_koffer']['overige_instellingen']['mqtt_internet_poort']
                self.mqtt_topic_normaal = data['demo_koffer']['overige_instellingen']['mqtt_topic_normaal']
                self.mqtt_topic_modbus = data['demo_koffer']['overige_instellingen']['mqtt_topic_modbus']
                
                self.max_procent_regelaar = data['demo_koffer']['overige_instellingen']['max_procent_regelaar']
                self.min_procent_regelaar = data['demo_koffer']['overige_instellingen']['min_procent_regelaar']
                
                self.schakelaar_0 = data['demo_koffer']['hardware']['digitale_pinnen']['schakelaars']['0']
                self.schakelaar_1 = data['demo_koffer']['hardware']['digitale_pinnen']['schakelaars']['1']
                self.schakelaar_2 = data['demo_koffer']['hardware']['digitale_pinnen']['schakelaars']['2']
                self.schakelaar_3 = data['demo_koffer']['hardware']['digitale_pinnen']['schakelaars']['3']
                self.licht_sterkte_neopixel = data['demo_koffer']['overige_instellingen']['licht_sterkte_neopixel']

                self.schakelaars = tuple(data['demo_koffer']['hardware']['digitale_pinnen']['schakelaars'][str(i)] for i in range(4))   # zet voor i in range 10 mochten er in de toekomst 10 schakelaars zijn.

                
                self.address_adc_0 = int(self.address_adc_0, 16) # omzetten van string naar nummer anders doet module voor adc het niet 
                self.address_adc_1 = int(self.address_adc_1, 16) # omzetten van string naar nummer anders doet module voor adc het niet
                
        except Exception as e:
            print(e)
            sleep(10)
            print("Bestand niet gevonden of verkeerd ingesteld")
            print("Bestand wordt hersteld met originele waarden.......")
            sleep(1)
            self.servo_pin = 12
            self.led_hoge_storing = 22
            self.led_lage_storing = 27
            self.led_in_bedrijf = 17
            self.fan_pin = 23
            self.led_strip_pin = 18
            self.potmeter_temperatuur = None
            self.potmeter_setpoint = None
            self.tijd_vertraging_servo = 10
            self.Kr_factor_verwarmen = 20
            self.Kr_factor_koelen = 10
            self.max_volt = 3.3
            self.min_volt = 0
            self.max_temp = 30
            self.min_temp = 10
            self.address_adc_0 = "0x48"
            self.address_adc_1 = "0x49"
            self.num_leds = 8
            self.schakelaar_0 = 24
            self.schakelaar_1 = 25
            self.schakelaar_2 = 5
            self.schakelaar_3 = 6
            self.licht_sterkte_neopixel = 1
#             self.schakelaar_4 = 21
#             self.schakelaar_5 = 20
#             self.schakelaar_6 = None
#             self.schakelaar_7 = None
#             self.schakelaar_8 = None
#             self.schakelaar_9 = None
            self.mqtt_gebruikers_naam = "demo_koffer"
            self.mqtt_wachtwoord = "coneco2024"
            self.mqtt_internet_poort = 1883
            self.mqtt_topic_normaal = "demo_koffer/"
            self.mqtt_topic_modbus = "demo_koffer/modbus/"
            
            self.max_procent_regelaar = 100
            self.min_procent_regelaar = 0
            
            self.save_to_file()
            print("Bestand hersteld")

    def save_to_file(self, filename='config.json'):
        config_data = {
            'demo_koffer': {
                'hardware': {
                    'digitale_pinnen': {
                        'servo_pin': self.servo_pin,
                        'led_hoge_storing': self.led_hoge_storing,
                        'led_lage_storing': self.led_lage_storing,
                        'led_in_bedrijf' : self.led_in_bedrijf,
                        'fan_pin' : self.fan_pin,
                        'led_strip_pin': self.led_strip_pin,
                        'schakelaars': {
                            '0' : self.schakelaar_0,
                            '1' : self.schakelaar_1,
                            '2' : self.schakelaar_2,
                            '3' : self.schakelaar_3,
                            '4' : self.schakelaar_4,
                            '5' : self.schakelaar_5,
                            '6' : self.schakelaar_6,
                            '7' : self.schakelaar_7,
                            '8' : self.schakelaar_8,
                            '9' : self.schakelaar_9
                        }
                    },
                    'analoge_pinnen': {
                        'potmeter_temperatuur': self.potmeter_temperatuur,
                        'potmeter_setpoint': self.potmeter_setpoint
                    }
                },
                'overige_instellingen': {
                    'tijd_vertraging_servo': self.tijd_vertraging_servo,
                    'Kr_factor_verwarmen': self.Kr_factor_verewarmen,
                    'Kr_factor_koelen': self.Kr_factor_koelen,
                    'maximale_voltage': self.max_volt,
                    'minimale_voltage': self.min_volt,
                    'maximale_temperatuur': self.max_temp,
                    'minimale_temperatuur': self.min_temp,
                    'i2c_address_adc_0': self.address_adc_0,
                    'i2c_address_adc_1': self.address_adc_1,
                    'aantal_neopixel_leds': self.num_leds,
                    'mqtt_gebruikers_naam' : self.mqtt_gebruikers_naam,
                    'mqtt_wachtwoord' : self.mqtt_wachtwoord,
                    'mqtt_internet_poort' : self.mqtt_internet_poort,
                    'mqtt_topic_normaal' : self.mqtt_topic_normaal,
                    'mqtt_topic_modbus' : self.mqtt_topic_modbus,
                    'max_procent_regelaar' : self.max_procent_regelaar,
                    'min_procent_regelaar' : self.min_procent_regelaar,
                    'licht_sterkte_neopixel' : self.licht_sterkte_neopixel
                }
            }
        }

        with open(filename, 'w') as f:
            json.dump(config_data, f, indent=4)

if __name__ == "__main__":
    config = Config()
    config.load_from_file()
    print("Config geladen:")
    print(config.__dict__)

#     # Voorbeeld: config wijzigen en opslaan
#     config.servo_pin = "D10"
#     config.led_hoge_storing = "D11"
#     config.schakelaar_0 = "D12"  # Voorbeeld van schakelaar 0
#     config.save_to_file()
# 
#     # Controleren of wijzigingen zijn doorgevoerd
#     config = Config()
#     config.load_from_file()
#     print("\nGewijzigde config opgeslagen:")
#     print(config.__dict__)
#     print(config.servo_pin)


