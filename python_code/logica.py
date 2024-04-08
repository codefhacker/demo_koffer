class Logica:
    def __init__(self):
        self.status_hoog_urgente_storing = None
        self.status_laag_urgente_storing = None
        self.status_in_bedrijf = None
        self.status_fan = None
        self.status_klep = None
        self.status_led_strip = None
       
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
            self.status_laag_urgente_storing = 0



if __name__ == "__main__":
    logica_instance = Logica()
    logica_instance.bereken_status(1, 0, 0, 1)  # Voorbeeld invoer 
    print("Status In Bedrijf:", logica_instance.status_in_bedrijf)
    print("Status Fan:", logica_instance.status_fan)
    print("Status Klep:", logica_instance.status_klep)
    print("Status Hoog Urgente Storing:", logica_instance.status_hoog_urgente_storing)
    print("Status Laag Urgente Storing:", logica_instance.status_laag_urgente_storing)

