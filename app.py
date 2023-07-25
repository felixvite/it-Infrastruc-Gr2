from apiflask import APIFlask, Schema
from flask import request, redirect
from marshmallow import Schema, fields, validates, ValidationError

app = APIFlask(__name__, title='Insurance price calculation API', version='1.0')


class PriceQuery(Schema):
    location = fields.Str(required=True)
    date = fields.Str(required=True)

    @validates('location')
    def validate_location(self, value):
        if value not in ['NewYork', 'Boston']:
            raise ValidationError('Invalid location.')

    @validates('date')
    def validate_date(self, value):
        if value not in ['today', 'tomorrow']:
            raise ValidationError('Invalid date.')


class PriceOut(Schema):
    price = fields.Float(required=True)


# Can cause problems with the APIFlask decorator --> First to uncomment and check if codes not working when problems
class FlightDataSchema(Schema):
    flightNo = fields.Str()
    airline = fields.Str()
    planeNo = fields.Str()
    departure = fields.Str()
    arrival = fields.Str()
    time = fields.Str()
    distance = fields.Str()


@app.route('/')
def root():
    return redirect('/docs')


@app.route('/price/', methods=['GET'])
@app.input(PriceQuery, location='query')
@app.output(PriceOut, 200)
@app.doc(summary='Return insurance price',
         description='Return price calculation based on location and date.',
         responses=[204, 400, 404])
def get_price(query: PriceQuery):
    location = request.args.get('location')
    date = request.args.get('date')
    # Validate input parameters
    if not location or not date:
        return {'error': 'Both location and date parameters are required.'}, 400

    # Perform price calculation logic based on location and date
    price = price_calculation(location, date)

    if price['price'] is None:
        return {'error': 'Invalid location or date.'}, 400

    return price, 200


def price_calculation(location, date):
    # @Todo Felix Vité - bring location and date in right format
    price = 0

    # @Todo Felix Vité - remove dummy data and put price calculation logic here
    if location == 'NewYork':
        price = 100
    elif location == 'Boston':
        price = 200

    if date == 'today':
        price += 50
    elif date == 'tomorrow':
        price += 50

    else:
        price = None

    price_dict = {'price': price}

    return price_dict


@app.route('/get_flight_data/', methods=['GET'])
@app.output(FlightDataSchema, 200)
@app.doc(summary='Returns actual flight data',
         description='Returns actual flight data from imaginary API landing location, time and distance.',
         responses=[204, 400, 404])
def get_flight_data():
    flightdata_dict = {'flightNo': "#99999",
                       'Airline': "TestAirline",
                       'planeNo': "12345TEA",
                       'Departure': "Berlin",
                       'Arrival': "London",
                       'time': "12:00",
                       'distance': "932,08 km"}
    return flightdata_dict, 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)