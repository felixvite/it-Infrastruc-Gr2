from apiflask import APIFlask, Schema
from flask import request
from marshmallow import Schema, fields, validates, ValidationError
import pandas as pd
from FlightData import FlightData
import joblib
from datetime import datetime
import sqlite3
import os
from dotenv import load_dotenv
import math


# Load environment variables from .env file
load_dotenv()

# Load the model from the joblib file
LOADED_MODEL = joblib.load('Modell/catboost_model.joblib')

app = APIFlask(__name__, title='Insurance price calculation API', version='1.0')

class PriceQuery(Schema):
    date = fields.Str(required=True, metadata={"format": "%Y-%m-%d", "example": "2023-08-15", "description": "The date where the flight takes place"})
    location_origin = fields.Str(required=True, metadata={"example": "GNV", "description": "The shortcut of the origin location"})
    location_dest = fields.Str(required=True, metadata={"example": "ATL", "description": "The shortcut of the destination location"})
    carrier = fields.Str(required=True, metadata={"example": "9E", "description": "The shortcut of the air carrier"})
    time = fields.Str(required=True, metadata={"format": "%H:%M", "example": "00:00", "description": "The time where the flight takes place"})

    @validates('location_origin')
    def validate_location(self, value):
        if len(value) != 3:
            raise ValidationError('Make sure to use the shortcut for the airport. For example, use ATL for Atlanta')

    @validates('location_dest')
    def validate_location(self, value):
        if len(value) != 3:
            raise ValidationError('Make sure to use the shortcut for the airport. For example, use ATL for Atlanta')

class PriceOut(Schema):
    price = fields.Float(required=True)

@app.route('/price', methods=['GET'])
@app.input(PriceQuery, location='query')
@app.output(PriceOut, 200)
@app.doc(summary='Return insurance price',
         description='Return price calculation based on date, location, time and carrier',
         responses=[400, 404])

def get_price(query: PriceQuery):
    date = request.args.get('date')
    time = request.args.get('time')
    location_origin = request.args.get('location_origin')
    location_dest = request.args.get('location_dest')
    carrier = request.args.get('carrier')

    # Perform price calculation logic based on location and date
    price = price_calculation(date, location_origin, location_dest, time, carrier)

    if price['price'] is None:
        return {'error': 'Invalid location or date.'}, 400

    return price, 200


def get_day_of_month_and_week(date_str):
    # Convert the date string to a datetime object
    date_object = datetime.strptime(date_str, '%Y-%m-%d')

    # Get the day of the month and day of the week (Monday is 0 and Sunday is 6)
    day_of_month = date_object.day
    day_of_week = date_object.weekday() + 1

    return day_of_month, day_of_week


def convert_to_block(user_time):
    # Convert user_time to an integer representing total minutes
    hours, minutes = map(int, user_time.split(':'))
    total_minutes = hours * 60 + minutes

    # Define time blocks in the same format as in the database
    time_blocks = ['0000-0559', '0600-0659', '0700-0759', '0800-0859', '0900-0959', '1000-1059', '1100-1159',
                    '1200-1259', '1300-1359', '1400-1459', '1500-1559', '1600-1659', '1700-1759', '1800-1859',
                    '1900-1959', '2000-2059', '2100-2159', '2200-2259', '2300-2359']

    # Loop through time_blocks to find the block that contains user_time
    for block in time_blocks:
        start, end = block.split('-')
        start_hours, start_minutes = int(start[:2]), int(start[2:])
        end_hours, end_minutes = int(end[:2]), (int(end[2:]) + 1)

        # Convert block start and end times to total minutes
        start_total = start_hours * 60 + start_minutes
        end_total = end_hours * 60 + end_minutes
        # Check if user_time falls within this block
        if start_total <= total_minutes < end_total:
            return block


def get_distance(origin, destination):
    # Create a connection to the SQLite database
    conn = sqlite3.connect('FlightData.db')
    # Create a cursor
    cur = conn.cursor()
    # Execute a query
    cur.execute('SELECT DISTANCE FROM flight_data WHERE ORIGIN = ? AND DEST = ?', (origin, destination))
    # Fetch the results
    data = cur.fetchone()
    # Close the connection
    conn.close()

    if data is not None:
        return data[0]
    else:
        return 'No data found for route from {origin} to {destination}.'.format(origin=origin, destination=destination)

def price_calculation(date, location_origin, location_dest, time, carrier):
    day_of_month, day_of_week = get_day_of_month_and_week(date)
    origin = location_origin
    destination = location_dest
    dep_time_blk = convert_to_block(time)
    distance = get_distance(origin, destination)

    # flight_data = FlightData(21, 1, 'DL', 'THL', 'ATL', '1500-1559', 223.0)
    flight_data = FlightData(day_of_month, day_of_week, origin, destination, carrier,  dep_time_blk, distance)
    new_data = pd.DataFrame(flight_data.get_data())

    # Get the values from the environment
    ticket_price = float(os.getenv("TICKET_PRICE"))
    compensation = float(os.getenv("SERVICE_CHARGE"))

    # Make predictions on the new data
    new_data_probabilities = LOADED_MODEL.predict_proba(new_data)
    # Display the predicted probabilities
    print("Predicted Probabilities:")
    print(new_data_probabilities)
    insurance_price = new_data_probabilities[0][1] * ticket_price + compensation
    insurance_price = math.ceil(insurance_price * 100) / 100
    print("Insurance Price")
    print(insurance_price)
    # Config File --> Für Probability 0 und 1 ?
    # --> Confile --> Wahrscheinlichkeiten dotenv --> Environment Variablen --> cost = 350, base = 5

    price_dict = {'price': insurance_price}

    return price_dict

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)