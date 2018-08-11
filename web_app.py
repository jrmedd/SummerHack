import datetime

import os

from flask import Flask, render_template, request, session, redirect, jsonify, url_for, flash

from pymongo import MongoClient

MONGO_URL = os.environ.get('MONGO_URL')

CLIENT = MongoClient(MONGO_URL)

DB = CLIENT['SummerHack']

BUSES = DB['buses']

APP = Flask(__name__)

APP.secret_key = os.environ.get('SECRET_KEY')

CONDITION_ADJECTIVES = ['lots of', 'mild', 'light', 'very light']

WEATHER_CONDITIONS = ['rain', 'sun', 'wind', 'fog']

TRAFFIC_CONDITIONS = ['clear', 'congestion']

@APP.route('/buses/<destination>', methods=['GET'])
def bus_time(destination):
    time_now = int(datetime.datetime.now().strftime("%H%M"))
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
    time_now = int(datetime.datetime.now().strftime("%M"))
    conditions = "%s %s" % (CONDITION_ADJECTIVES[int(time_now/3)%4], WEATHER_CONDITIONS[int(time_now/15)])
    return jsonify(current_conditions=conditions)

@APP.route('/traffic', methods=['GET'])
def traffic():
    time_now = int(datetime.datetime.now().strftime("%M"))
    traffic_state = TRAFFIC_CONDITIONS[int(time_now/15)%2]
    if traffic_state != 'clear':
        traffic_state = "%s %s" % (CONDITION_ADJECTIVES[(int(time_now/3)%4)-2], traffic_state)
    return jsonify(current_traffic=traffic_state)

@APP.errorhandler(404)
def page_not_found(e):
    return "This page doesn't exist!"

if __name__ == '__main__':
    APP.run(host="0.0.0.0", debug=True)
