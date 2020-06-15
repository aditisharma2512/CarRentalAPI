"""
This file contains the classes for the RentAPI. The API uses GET, POST and PATCH requests to
retrieve/add/manipulate data. The data gets stored in python dictionaries and NOT a database, as
requested in the Coding Challenge Sheet.
The return statements are used to inform about any errors that may exist in the data
being sent
"""

__author__ = "Aditi Sharma"
__modified__ = "15.06.2020"

from flask import Flask, request
from flask_restful import Resource, Api
import json
from datetime import datetime

app = Flask(__name__)
api = Api(app)


# The home page of the API
@app.route('/')
def api_root():
    return '<h1>Welcome to EURent</h1><br /> <hr>' \
           '<h3>EURent is a company which has as its main activity the renting of cars to its customers. The' \
           'company has many fleet locations with many parking lots all over the country, where these cars' \
           'can be picked up and dropped off. </h3>'


class Cars(Resource):
    """
    This class creates Cars to be added to the EURent system. The class handles get and post requests.
    """
    TYPES = ['economic', 'standard', 'premium']  # A class of a car can only belong to one of these car type values
    cars = []
    with open('cars.csv', encoding='utf-8') as fn:
        lines = fn.readlines()
    count = 0
    for line in lines:
        if count == 0:
            pass
        else:
            vals = line.lstrip(' ').rstrip(' ').strip('\n').split(',')
            cars.append({'model': vals[0].strip(' '), 'license_plate': vals[1].strip(' '), 'type': vals[2].strip(' '),
                         'fee': vals[3].strip(' ')})
        count += 1

    def get(self):
        """
        GET for the class.
        :return: Returns all the cars in a JSON format
        """
        return json.dumps(self.cars)
    
    def post(self):
        """
        POST for the class. Adds a new car to the cars list according to the values sent as args
        :return: Message
        """
        model = request.args.get('model')
        license_plate = request.args.get('license_plate')
        type = request.args.get('type')
        if type not in self.TYPES:
            return "Incorrect car type. Type must belong to " + str(self.TYPES)
        fee = request.args.get('fee')
        try:
            fee = int(fee)
        except TypeError:
            return "Fee must be int value"

        car_dict = {'model': model, 'license_plate': license_plate, 'type': type, 'fee': fee}
        self.cars.append(car_dict)
        return "Added Car Successfully"

    @staticmethod
    @app.route('/cars/<model>')
    def get_car_by_model(model):
        """
        GET method for the car class, but with model being passed as a parameter
        :param model: Model of the car being searched
        :return: Details of the car in a JSON format
        """
        to_return = []
        for entry in Cars.cars:
            if entry['model'] == model:
                to_return.append(entry)
        return json.dumps(to_return)


class Customer(Resource):
    """
    This class contains the information about all the customers for EURent. This class handles
    GET and POST requests
    """
    customers = [{'ID': 1, 'name': 'Harvey Specter', 'mobile': '0123456789', 'bookings': 0},
                 {'ID': 2, 'name': 'Mike Ross', 'mobile': '0112345678', 'bookings': 0},
                 {'ID': 3, 'name': 'Louis Litt', 'mobile': '0111234567', 'bookings': 0},
                 {'ID': 4, 'name': 'Jessica Pearson', 'mobile': '0111123456', 'bookings': 0},
                 {'ID': 5, 'name': 'Robert Zane', 'mobile': '0111112345', 'bookings': 0}]

    def get(self):
        """
        GET method for the class.
        :return: returns all the customers in a JSON format
        """
        return json.dumps(self.customers)

    @staticmethod
    @app.route('/customers/<name>')
    def get_customer_by_name(name):
        """
        GET method for the class but by customer name as an argument
        :param name: name of the customer being searched
        :return: the records of the customers in a JSON format
        """
        to_return = []
        for entry in Customer.customers:
            if entry['name'] == name:
                to_return.append(entry)
        return json.dumps(to_return)

    def post(self):
        """
        POST method for the class. Adds a new customer to the list according to the values provided
        :return: Message
        """
        max_id = 0
        for entry in self.customers:
            if entry['ID'] > max_id:
                max_id = entry['ID']
        name = request.args.get('name')
        mobile = request.args.get('mobile')
        bookings = 0
        for customer in self.customers:
            if customer['name'] == name and customer['mobile'] == mobile:
                return "Customer already exists"
        cust_dict = {'ID': max_id+1, 'name': name, 'mobile': mobile, 'bookings': bookings}
        self.customers.append(cust_dict)
        return "Added Customer Successfully"


class Booking(Resource):
    """
    This class handles all the bookings. This class handles the GET, POST and PATCH methods.
    """
    bookings = []

    def get(self):
        """
        GET method for the class.
        :return: Returns a list of all bookings in a JSON format
        """
        return json.dumps(self.bookings, default=str)

    @staticmethod
    @app.route('/booking/searchbyid/<id>')
    def get_booking_by_id(id):
        """
        GET method for the class but with ID given as a parameter
        :param id: ID to be searched
        :return: booking, if found. Otherwise, return a message
        """
        for booking in Booking.bookings:
            if booking['booking_id'] == int(id):
                return booking
        return "No booking found for this id"

    @staticmethod
    @app.route('/booking/searchbycustomer/<name>')
    def get_bookings_by_customer_name(name):
        """
        GET method for the class but with customer name given as a parameter
        :param name: Name to be searched
        :return: bookings for the customer in a JSON format
        """
        customer_bookings = []
        for booking in Booking.bookings:
            customer = booking['customer']
            if customer['name'] == name:
                customer_bookings.append(booking)

        if len(customer_bookings) <= 0:
            return "No bookings found for customer " + name
        else:
            return json.dumps(customer_bookings)

    # TODO: Try modularising
    def post(self):
        """
        POST method for the class. Adds a new booking to the bookings list
        :return: Message
        """
        booking_id = id(self)
        selected_car = None
        car_type = request.args.get('car')
        date_format = '%d-%m-%Y'
        today = datetime.now().date()
        try:
            start_date = datetime.strptime(request.args.get('start_date'), date_format).date()
            end_date = datetime.strptime(request.args.get('end_date'), date_format).date()
            if start_date < today or end_date < start_date:
                raise ValueError
        except TypeError:
            return 'Invalid date format please use dd-mm-yyyy'
        except ValueError:
            return 'Invalid dates provided'
        if car_type not in Cars.TYPES:
            return 'Invalid car type, please enter one from ' + str(Cars.TYPES)
        car_list = []
        for one_car in Cars.cars:
            if one_car['type'] == car_type:
                car_list.append(one_car)
        for booking in self.bookings:
            if booking['start_date'] <= start_date <= booking['end_date'] or \
                    booking['start_date'] <= end_date <= booking['end_date']:
                for car in car_list:
                    if booking['car'] == car:
                        car_list.remove(car)
        if len(car_list) <= 0:
            return 'No ' + str(car_type) + " cars available for this date range"
        else:
            selected_car = car_list[0]
        selected_customer = None
        customer = request.args.get('customer')
        for one_cust in Customer.customers:
            if one_cust['name'] == customer:
                selected_customer = one_cust
                one_cust['bookings'] += 1
        if not selected_customer:
            return 'Customer not found'
        if end_date < start_date:
            return 'End date cannot be before start date'
        status = 'new'
        Booking.bookings.append({'booking_id': booking_id, 'customer': selected_customer, 'car': selected_car,
                                 'start_date': start_date, 'end_date': end_date, 'status': status})
        return "Booking " + str(booking_id) + " Added Successfully"

    # TODO: Try modularising
    def patch(self):
        booking_id = request.args.get('id')
        request_type = request.args.get('request')
        if request_type == 'pick_up':
            found = False
            today = datetime.now().date()
            for booking in Booking.bookings:
                if booking['booking_id'] == int(booking_id):
                    if booking['status'] == 'completed':
                        return 'Booking has already been completed'
                    start_date = booking['start_date']
                    found = True
                    if today <= start_date:
                        return 'Booking has not yet started, you can pickup on or after ' + str(start_date)
                    if booking['status'] != 'new':
                        return 'Booking has already been picked up/completed'
                    else:
                        booking['status'] = 'in_progress'
            if not found:
                return 'Booking ' + str(booking_id) + ' not found'
            return 'Booking ' + str(booking_id) + ' successfully registered for pick up'
        elif request_type == 'drop_off':
            found = False
            today = datetime.now().date()
            for booking in Booking.bookings:
                if booking['booking_id'] == int(booking_id):
                    end_date = booking['end_date']
                    start_date = booking['start_date']
                    found = True
                    if booking['status'] != 'in_progress':
                        return 'Booking has not yet been picked up or completed'
                    else:
                        booking['status'] = 'completed'
                    if today >= end_date:
                        return 'Drop off date passed, you had to drop off on or before ' + str(end_date)
                    elif today <= start_date:
                        return 'Drop off date cannot be before start date'
            if not found:
                return 'Booking ' + str(booking_id) + ' not found'
            return 'Booking ' + str(booking_id) + ' successfully registered for drop off'
        else:
            return 'Invalid request type'


api.add_resource(Customer, '/customers')
api.add_resource(Cars, '/cars')
api.add_resource(Booking, '/booking')

if __name__ == '__main__':
    app.run(port='5002', debug=True)
