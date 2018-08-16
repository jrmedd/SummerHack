import requests
import blinkt
import time


url = "https://summerhack.xyz/weather"

## ANIMATION FUNCTIONS ##
# fade in a block colour
def sun(r, g, b):
    i = 0.0
    while i <= 0.8:
        blinkt.set_all(r, g, b, i)
        blinkt.show()
        time.sleep(0.2)
        i += 0.1
        if i > 0.8:
            i = 0.8

# a block of 2 LEDs travelling down the stick
def rain(r, g, b):
    while True:
        for i in range(8):
            blinkt.set_pixel(i, r, g, b)
            blinkt.show()
            time.sleep(0.1)
            blinkt.set_pixel(i-1, 0, 0, 0)
            blinkt.show()
            if i == 6 or i == 7:
                blinkt.set_pixel(i, 0, 0, 0);
                blinkt.show()

        time.sleep(0.05)

# random sparkles - for white, use the same number in all RGB values. Higher numbers = brighter white
def fog(r, g, b):
    import random
    for i in range(150):
        pixels = random.sample(range(blinkt.NUM_PIXELS), random.randint(1, 5))
        for i in range(blinkt.NUM_PIXELS):
            if i in pixels:
                blinkt.set_pixel(i, r, g, b) # change colour in the last 3 digits here
            else:
                blinkt.set_pixel(i, 0, 0, 0)
        blinkt.show()
        time.sleep(0.05)
        blinkt.clear()
        blinkt.show()


def rainbow():
    import colorsys
    spacing = 360.0 / 16.0
    hue = 0

    for i in range(2000):
        hue = int(time.time() * 100) % 360
        for x in range(blinkt.NUM_PIXELS):
            offset = x * spacing
            h = ((hue + offset) % 360) / 360.0
            r, g, b = [int(c*255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
            blinkt.set_pixel(x, r, g, b)

        blinkt.show()
        time.sleep(0.001)
    blinkt.clear()
    blinkt.show()


while True:
    r = requests.get(url)
    data = r.json()


    live_weather = data['current_conditions']

    if live_weather == "mild rain":
        rain(0, 255, 255)

    elif live_weather == "heavy rain":
        rain(0, 255, 255)

    elif live_weather == "mild sun":
        sun(255, 255, 0)

    elif live_weather == "lots of sun":
        sun(255, 130, 0)

    elif live_weather == "mild fog":
        fog(100, 100, 100)

    elif live_weather == "heavy fog":
        fog(200, 200, 200)

    else:
        print("Function for " + live_weather + " not ready yet")
