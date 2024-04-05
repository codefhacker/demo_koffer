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
        except:
            print("bestand niet gevonden of verkeerd ingesteld")
            print("Bestand wordt hersteld met orginele waardes.......")
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
            self.save_to_file()
            print("bestand hersteld")

            

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
                        'led_strip_pin': self.led_strip_pin
                    },
                    'analoge_pinnen': {
                        'potmeter_temperatuur': self.potmeter_temperatuur,
                        'potmeter_setpoint': self.potmeter_setpoint
                    }
                },
                'overige_instellingen': {
                    'tijd_vertraging_servo': self.tijd_vertraging_servo
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

    # Voorbeeld: config wijzigen en opslaan
    config.servo_pin = "D10"
    config.led_hoge_storing = "D11"
    config.save_to_file()

    # Controleren of wijzigingen zijn doorgevoerd
    config = Config()
    config.load_from_file()
    print("\nGewijzigde config opgeslagen:")
    print(config.__dict__)
    print(config.servo_pin)

