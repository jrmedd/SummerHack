import serial
import requests
import time

lookup_url = "https://summerhack.xyz/weather"

microbit = serial.Serial('/dev/tty.usbmodem1412', baudrate=115200)

while True:
    weather_request = requests.get(lookup_url)
    weather_json = weather_request.json()
    current_conditions = weather_json.get('current_conditions')+"\n"
    microbit.write(current_conditions.encode())
    time.sleep(3)
