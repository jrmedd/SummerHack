# Requests is a simple way to interact with websites, APIs and databases using Python. Often, you'll need to include a password or 'API key' - today, we're using an open API so we just need a URL (or web address)

#import the Requests library
import requests

# add the data source URL here, in quotation marks
url = 'https://summerhack.xyz/buses/manchester'

# send a GET request to the URL, and save the response in a variable called 'r'
r = requests.get(url)

# convert the full response to json format, so we can work with it like a
data = r.json()


# The full response contains some values that we don't necessarily need. To make things simpler, we can isolate the values that we want to work with

#The main response is a dictionary, so we first we call the category we're looking for - ['next']

#The value of ['next'] is a list (as it contains square brackets), so to retrieve a single item we need to include its position in the list - [0], [1] or [2]

first_bus = data['next'][0]
second_bus = data['next'][1]
third_bus = data['next'][2]

# The same principle applies to each data source, although 'weather' and 'traffic' do not contain any lists - you'll just need to call the dictionary category for the value you want. For example: 

# r = requests.get('https://summerhack.xyz/weather')
# weather_data = r.json()
# live_weather = data['current_conditions']
