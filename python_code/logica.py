class Logica:
    def __init__(self):
        self.status_hoog_urgente_storing = None
        self.status_laag_urgente_storing = None
        self.status_in_bedrijf = None
        self.status_fan = None
        self.status_klep = None
        self.status_led_strip = None
        self.list_heater = None  # Toevoeging: initialiseer list_heater
        self.status_verwarmen = None
        
    def bereken_status(self, tijd_status, fan_status, klep_status, filter_status):
        if tijd_status == 1 and fan_status == 0 and klep_status == 0:
            self.status_in_bedrijf = 1
            self.status_fan = 1
            self.status_klep = 1
            self.status_hoog_urgente_storing = 0
            self.status_laag_urgente_storing = 0
            if filter_status == 1:
                self.status_laag_urgente_storing = 1
            else:
                self.status_laag_urgente_storing = 0
                
        elif tijd_status == 1 and (fan_status == 1 or klep_status == 1):
            self.status_in_bedrijf = 0
            self.status_fan = 0
            self.status_klep = 0
            self.status_hoog_urgente_storing = 1
            self.status_laag_urgente_storing = 0
            if filter_status == 1:
                self.status_laag_urgente_storing = 1
            else:
                self.status_laag_urgente_storing = 0
            
        elif fan_status == 1 or klep_status == 1:
            self.status_in_bedrijf = 0
            self.status_fan = 0
            self.status_klep = 0
            self.status_hoog_urgente_storing = 1
            self.status_laag_urgente_storing = 0
            if filter_status == 1:
                self.status_laag_urgente_storing = 1
            else:
                self.status_laag_urgente_storing = 0
            
        else:
            self.status_in_bedrijf = 0
            self.status_fan = 0
            self.status_klep = 0
            self.status_hoog_urgente_storing = 0
            if filter_status == 1:
                self.status_laag_urgente_storing = 1
            else:
                self.status_laag_urgente_storing = 0
    
    # Toevoeging: functie om de heater output lijst te berekenen
    def bereken_vermogen(self, Kr, setpoint, initial_temperature):
        # Functie om proportionele controle uit te voeren en de verwarmingsoutput te retourneren
        def proportional_control(Kr, setpoint, current_temperature):
            error = setpoint - current_temperature
            output_percentage = Kr * error  # Inverted control
    
            # Ensure output is within valid range [0, 100]
            output_percentage = max(0, min(100, output_percentage))
    
            return output_percentage
    
        heater_output = 100
        self.list_heater = []
    
        while heater_output > 1:
            heater_output = proportional_control(Kr, setpoint, initial_temperature)
            output_2 = 100 - heater_output
            initial_temperature += heater_output * 0.01  # Simulate system response
            self.list_heater.append(int(output_2))
    
        return self.list_heater

if __name__ == "__main__":
    logica_instance = Logica()
    logica_instance.bereken_status(1, 0, 0, 1)  # Voorbeeld invoer
    
    print("Status In Bedrijf:", logica_instance.status_in_bedrijf)
    print("Status Fan:", logica_instance.status_fan)
    print("Status Klep:", logica_instance.status_klep)
    print("Status Hoog Urgente Storing:", logica_instance.status_hoog_urgente_storing)
    print("Status Laag Urgente Storing:", logica_instance.status_laag_urgente_storing)
    
    print(logica_instance.bereken_vermogen(22,19,15))

