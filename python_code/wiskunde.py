import time

class Wiskunde:
    def __init__(self):
        self.test = None
        self.versterkingsfactor = None
        self.temp = None
        self.procent_regelaar = None
        
    def volt2_temp(self,Max_temp,Min_temp,Max_volt,Min_volt,huidig_voltage):
        self.versterkingsfactor = (Max_temp - Min_temp) / (Max_volt - Min_volt)
        self.temp = (huidig_voltage * self.versterkingsfactor) + Min_temp
        self.temp = round(self.temp,1)
        
    def offset2_procent(self,Max_procent,Min_procent,Max_offset,Min_offset,huidig_offset):
        versterkingsfactor = (Max_procent - Min_procent) / (Max_offset - Min_offset)
        self.procent_regelaar = (huidig_offset * versterkingsfactor) + Min_offset
        
        
        self.procent_regelaar = self.procent_regelaar
        self.procent_regelaar = round(self.procent_regelaar,1)
        
        
            
            
ticker = 0
        
if __name__ == "__main__":
    for i in range(100):
        
        wiskunde = Wiskunde()
        ticker += 0.5
        wiskunde.offset2_procent(-100,100,20,0,ticker)
        print(wiskunde.procent_regelaar)
        time.sleep(0.2)
        wiskunde.offset2_procent(-100,100,20,0,ticker)
        print(wiskunde.procent_regelaar)
            
        if ticker >=10:
            ticker = 0
                
     
        
    
    
