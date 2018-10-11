import datetime

import pytz

import os

from flask import Flask, render_template, request, session, redirect, jsonify, url_for, flash

from pymongo import MongoClient

import logging
logging.basicConfig(filename='errors.log',level=logging.DEBUG)

MONGO_URL = os.environ.get('MONGO_URL')
CLIENT = MongoClient(MONGO_URL)
print("Connected to MongoDB")

MANCHESTER_TZ = pytz.timezone("Europe/London")

DB = CLIENT['SummerHack']

BUSES = DB['buses']

APP = Flask(__name__)

APP.secret_key = os.environ.get('SECRET_KEY')

LETS_ENCRYPT_CHALLENGE = os.environ.get('LETS_ENCRYPT_CHALLENGE')
LETS_ENCRYPT_RESPONSE = os.environ.get('LETS_ENCRYPT_RESPONSE')

CONDITION_ADJECTIVES = ['lots of', 'mild', 'light', 'very light']

WEATHER_CONDITIONS = ['rain', 'sun', 'wind', 'fog']

TRAFFIC_CONDITIONS = ['clear', 'congestion']


@APP.route('/buses/<destination>', methods=['GET'])
def bus_time(destination):
    time_now = int(datetime.datetime.now(MANCHESTER_TZ).strftime("%H%M"))
    lookup = destination.title()
    results = list(BUSES.find({'destination':lookup, 'departing':{'$gte':time_now}},{'_id':0,'destination':0}).sort('departing', 1).limit(3))
    if results:
        times = [str(result.get('departing')).zfill(4) for result in results]
        times = ["%s:%s" % (time[:-2], time[-2:]) for time in times]

    else:
        times = []
    return jsonify(destination=lookup, next=times)

@APP.route('/weather', methods=['GET'])
def weather():
    time_now = int(datetime.datetime.now(MANCHESTER_TZ).strftime("%M"))
    conditions = "%s %s" % (CONDITION_ADJECTIVES[int(time_now/3)%4], WEATHER_CONDITIONS[int(time_now/15)])
    return jsonify(current_conditions=conditions)

@APP.route('/traffic', methods=['GET'])
def traffic():
    time_now = int(datetime.datetime.now(MANCHESTER_TZ).strftime("%M"))
    traffic_state = TRAFFIC_CONDITIONS[int(time_now/15)%2]
    if traffic_state != 'clear':
        traffic_state = "%s %s" % (CONDITION_ADJECTIVES[(int(time_now/3)%4)-2], traffic_state)
    return jsonify(current_traffic=traffic_state)

@APP.route('/code')
def code():
    return redirect('https://github.com/jrmedd/SummerHack/tree/master/python_examples')

@APP.route('/.well-known/challenge/<challenge_string>')
def acme_challenge(challenge_string):
    if challenge_string == LETS_ENCRYPT_CHALLENGE:
        return LETS_ENCRYPT_RESPONSE
    else:
        return "Doesn't match"

@APP.errorhandler(404)
def page_not_found(e):
    return "This page doesn't exist!"

if __name__ == '__main__':
    print("Starting application")
    APP.run()
