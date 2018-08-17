import serial
import requests
import time

lookup_url = "https://summerhack.xyz/buses/leigh"

microbit = serial.Serial('/dev/tty.usbmodem1412', baudrate=115200)

while True:
    bus_request = requests.get(lookup_url)
    bus_json = bus_request.json()
    next_bus = bus_json.get('destination')+ bus_json.get('next')[0]+"\n"
    microbit.write(next_bus.encode())
    time.sleep(3)
