import time
import sys
# import board
# import neopixel
# pixels = neopixel.NeoPixel(board.D18, 12)

Kr = float(sys.argv[1])
setpoint = float(sys.argv[2])
huidige_temperatuur = float(sys.argv[3])
inverted = True
sleep_time = 0.1
heater_output = 10
color_red = 0
color_green = 0
color_blue = 0

# Functie om de heateroutput te berekenen
def proportionele_regeling(setpoint, huidige_temperatuur):
    fout = setpoint - huidige_temperatuur
    output_percentage = Kr * (fout)  # Omgekeerde regeling

    # Zorg ervoor dat de output binnen het geldige bereik [0, 100] ligt
    output_percentage = max(0, min(100, output_percentage))
    
    return output_percentage

# Simuleren van de regellus
while heater_output > 1:  # Simuleer 50 iteraties
    heater_output = proportionele_regeling(setpoint, huidige_temperatuur)
    output_2 = 100 - heater_output
    #print(output_2)
    huidige_temperatuur += heater_output * 0.01  # Simuleer systeemrespons
    
    #print("Temp:",round(huidige_temperatuur,2) ," °C, output: ",int(output_2))
    print(round(huidige_temperatuur,2),int(output_2))
#     color_red = int(output_2) + 155
#     color_blue = 100 - int(output_2)
#     color_green = 100 - int(output_2)
#     print(f"red : {color_red}")
#     pixels.fill((color_red, color_green, color_blue))
#     pixels.show()
#     time.sleep(0.5)
    


