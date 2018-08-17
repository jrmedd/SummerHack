import serial
import requests
import time

lookup_url = "https://summerhack.xyz/traffic"

microbit = serial.Serial('/dev/tty.usbmodem1412', baudrate=115200)

while True:
    traffic_request = requests.get(lookup_url)
    traffic_json = traffic_request.json()
    current_conditions = traffic_json.get('current_traffic')+"\n"
    microbit.write(current_conditions.encode())
    time.sleep(3)
