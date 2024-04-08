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
                self.schakelaar_0 = data['demo_koffer']['hardware']['digitale_pinnen']['schakelaars']['0']
                self.schakelaar_1 = data['demo_koffer']['hardware']['digitale_pinnen']['schakelaars']['1']
                self.schakelaar_2 = data['demo_koffer']['hardware']['digitale_pinnen']['schakelaars']['2']
                self.schakelaar_3 = data['demo_koffer']['hardware']['digitale_pinnen']['schakelaars']['3']
                self.schakelaar_4 = data['demo_koffer']['hardware']['digitale_pinnen']['schakelaars']['4']
                self.schakelaar_5 = data['demo_koffer']['hardware']['digitale_pinnen']['schakelaars']['5']
                self.schakelaar_6 = data['demo_koffer']['hardware']['digitale_pinnen']['schakelaars']['6']
                self.schakelaar_7 = data['demo_koffer']['hardware']['digitale_pinnen']['schakelaars']['7']
                self.schakelaar_8 = data['demo_koffer']['hardware']['digitale_pinnen']['schakelaars']['8']
                self.schakelaar_9 = data['demo_koffer']['hardware']['digitale_pinnen']['schakelaars']['9']
                self.schakelaars = tuple(data['demo_koffer']['hardware']['digitale_pinnen']['schakelaars'][str(i)] for i in range(10))

                
                self.address_adc_0 = int(self.address_adc_0, 16)
                
        except Exception as e:
            print(e)
            sleep(100)
            print("Bestand niet gevonden of verkeerd ingesteld")
            print("Bestand wordt hersteld met originele waarden.......")
            sleep(1)
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
                    'Kr_factor_verwarmen': self.Kr_factor_verwarmen,
                    'Kr_factor_koelen': self.Kr_factor_koelen,
                    'maximale_voltage': self.max_volt,
                    'minimale_voltage': self.min_volt,
                    'maximale_temperatuur': self.max_temp,
                    'minimale_temperatuur': self.min_temp,
                    'i2c_address_adc_0': self.address_adc_0,
                    'i2c_address_adc_1': self.address_adc_1,
                    'aantal_neopixel_leds': self.num_leds
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

