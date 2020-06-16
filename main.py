"""
This file contains the classes for the RentAPI. The API uses GET, POST and PATCH requests to
retrieve/add/manipulate data. The data gets stored in python dictionaries and NOT a database, as
requested in the Coding Challenge Sheet.
The return statements are used to inform about any errors that may exist in the data
being sent
"""

__author__ = "Aditi Sharma"
__modified__ = "15.06.2020"

from flask import Flask
from flask_restful import Api
from Cars import Cars, CarByModel
from Customers import Customer, CustomerByName
from Booking import Booking, BookingById, BookingByCustomer

app = Flask(__name__)
api = Api(app)


# The home page of the API
@app.route('/')
def api_root():
    return '<h1>Welcome to EURent</h1><br /> <hr>' \
           '<h3>EURent is a company which has as its main activity the renting of cars to its customers. The' \
           'company has many fleet locations with many parking lots all over the country, where these cars' \
           'can be picked up and dropped off. </h3>'


def add_resources():
    api.add_resource(Customer, '/customers')
    api.add_resource(CustomerByName, '/customers/<name>')
    api.add_resource(Cars, '/cars')
    api.add_resource(CarByModel, '/cars/<model>')
    api.add_resource(Booking, '/booking')
    api.add_resource(BookingById, '/booking/searchbyid/<id>')
    api.add_resource(BookingByCustomer, '/booking/searchbycustomer/<name>')


if __name__ == '__main__':
    add_resources()
    app.run(port='5002', debug=True)
