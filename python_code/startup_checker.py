"""
startup checker

wat dit programma doet is dat het bij het opstarten van de demo koffer controleerd wat de stand is van de schakelaars.
Aan de hand van de schakelaars wordt het programma modbus, het testprogramma of het standalone programma aangestuurd.


Gemaakt door Fabian Boshoven

Versie 1

Datum laatst gewijzigd: 29-5-2024

"""


import os # module om systeem commando's uit te voeren
from hardware import *
import time
from app_config import * 

settings = Config()
settings.load_from_file()

hardware = Hardware()

#print(settings.test_pin)
hardware.setup_status_schakelaar(settings.modbus_pin,settings.test_pin)

#print(hardware.status_schakelaar_0.is_pressed)
#print(hardware.status_schakelaar_1.is_pressed)
time.sleep(1)

if hardware.status_schakelaar_0.is_pressed and not hardware.status_schakelaar_1.is_pressed:
    #print("running automatic")
    os.system("/home/demo_koffer/lbk_code/env/bin/python3 /home/demo_koffer/lbk_code/main_standalone.py")
if hardware.status_schakelaar_0.is_pressed and hardware.status_schakelaar_1.is_pressed:
    #print("running test")
    os.system("/home/demo_koffer/lbk_code/env/bin/python3 /home/demo_koffer/lbk_code/test_all.py")
if hardware.status_schakelaar_0.is_pressed == 0 and hardware.status_schakelaar_1.is_pressed == 0:
    #print("running modbus")
    os.system("/home/demo_koffer/lbk_code/env/bin/python3 /home/demo_koffer/lbk_code/main_modbus.py")

