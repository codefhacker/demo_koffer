class Wiskunde:
    def __init__(self):
        self.test = None
        self.versterkingsfactor = None
        self.temp = None
        
    def volt2_temp(self,Max_temp,Min_temp,Max_volt,Min_volt,huidig_voltage):
        self.versterkingsfactor = (Max_temp - Min_temp) / (Max_volt - Min_volt)
        self.temp = (huidig_voltage * self.versterkingsfactor) + Min_temp
        self.temp = round(self.temp,1)
        
if __name__ == "__main__":
    wiskunde = Wiskunde()
    wiskunde.volt2_temp(30,10,3.3,0,0.75)
    print(wiskunde.temp)
    
