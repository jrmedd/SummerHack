import requests
import blinkt
import time

blinkt.set_brightness(0.3)

url = "https://summerhack.xyz/weather"


# possible weather types
# very light rain, light rain, mild rain, lots of rain, very light sun, light sun, mild sun, lots of sun, light wind, mild wind, lots of wind, very light fog, light fog, mild fog, lots of fog


while True:
    r = requests.get(url)
    data = r.json()

    live_weather = data['current_conditions']
    print("Current weather: " + live_weather)

    # add more colours for each weather type
    if live_weather == "mild rain":
        blinkt.set_all(0, 255, 255)    # cyan
        blinkt.show()
    elif live_weather == "heavy rain":
        blinkt.set_all(0, 0, 255)    # blue
        blinkt.show()
    elif live_weather == "mild sun":
        blinkt.set_all(255, 255, 0)    # yellow
        blinkt.show()
    elif live_weather == "lots of sun":
        blinkt.set_all(255, 130, 0)    # orange
        blinkt.show()
    elif live_weather == "mild fog":
        blinkt.set_all(100, 100, 100) # medium white/grey
        blinkt.show()
    elif live_weather == "heavy fog":
        blinkt.set_all(200, 200, 200) # white/grey
        blinkt.show()
    else:
        print("Function for " + live_weather + " not ready yet") # this will allow the code to run before all possible weather types have been added

    time.sleep(90) #wait for 90 seconds
