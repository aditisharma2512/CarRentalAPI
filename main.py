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
from flask_api import status

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
        return json.dumps(self.cars), status.HTTP_200_OK

    def post(self):
        """
        POST for the class. Adds a new car to the cars list according to the values sent as args
        :return: Message
        """
        model = request.args.get('model')
        license_plate = request.args.get('license_plate')
        type = request.args.get('type')
        if type not in self.TYPES:
            return {"message": "Incorrect car type. Must belong to " + str(self.TYPES)}, status.HTTP_400_BAD_REQUEST
        fee = request.args.get('fee')
        try:
            fee = int(fee)
        except TypeError:
            return {"message": "Fee must be int value"}, status.HTTP_400_BAD_REQUEST

        car_dict = {'model': model, 'license_plate': license_plate, 'type': type, 'fee': fee}
        self.cars.append(car_dict)
        return {"message": "Added Car Successfully"}, status.HTTP_200_OK

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
        return json.dumps(to_return), status.HTTP_200_OK


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
        return json.dumps(self.customers), status.HTTP_200_OK

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
        return json.dumps(to_return), status.HTTP_200_OK

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
                return {"message":"Customer already exists"}, status.HTTP_400_BAD_REQUEST
        cust_dict = {'ID': max_id+1, 'name': name, 'mobile': mobile, 'bookings': bookings}
        self.customers.append(cust_dict)
        return {"message": "Added Customer Successfully"}, status.HTTP_200_OK


class Booking(Resource):
    """
    This class handles all the bookings. This class handles the GET, POST and PATCH methods.
    """
    bookings = []
    date_format = '%d-%m-%Y'
    today = datetime.now().date()

    def get(self):
        """
        GET method for the class.
        :return: Returns a list of all bookings in a JSON format
        """
        return json.dumps(self.bookings, default=str), status.HTTP_200_OK

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
        return {"message": "No booking found for this id"}, status.HTTP_200_OK

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
            return {"message": "No bookings found for customer " + name}, status.HTTP_200_OK
        else:
            return json.dumps(customer_bookings), status.HTTP_200_OK

    def fix_date(self, date_str):
        try:
            fixed_date = datetime.strptime(date_str, self.date_format).date()
        except TypeError:
            return None
        else:
            return fixed_date

    def post(self):
        """
        POST method for the class. Adds a new booking to the bookings list
        :return: Message
        """
        booking_id = id(self)
        car_type = request.args.get('car')
        start_date = self.fix_date(request.args.get('start_date'))
        end_date = self.fix_date(request.args.get('end_date'))
        if not start_date or not end_date:
            return {"message": "Invalid Dates Provided, please use dd-mm-yyyy"}, status.HTTP_400_BAD_REQUEST
        elif start_date < self.today or end_date < start_date:
            return {"message": 'Invalid date range provided'}, status.HTTP_400_BAD_REQUEST
        if car_type not in Cars.TYPES:
            return {"message": 'Invalid car type, please enter one from ' + str(Cars.TYPES)}, \
                   status.HTTP_400_BAD_REQUEST
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
            return {"message": 'No ' + str(car_type) + " cars available for this date range"}, status.HTTP_200_OK
        else:
            selected_car = car_list[0]
        selected_customer = None
        customer = request.args.get('customer')
        for one_cust in Customer.customers:
            if one_cust['name'] == customer:
                selected_customer = one_cust
                one_cust['bookings'] += 1
        if not selected_customer:
            return {"message": 'Customer not found'}, status.HTTP_200_OK
        if end_date < start_date:
            return {"message": 'End date cannot be before start date'}, status.HTTP_400_BAD_REQUEST
        booking_status = 'new'
        Booking.bookings.append({'booking_id': booking_id, 'customer': selected_customer, 'car': selected_car,
                                 'start_date': start_date, 'end_date': end_date, 'status': booking_status})
        return {"message": "Booking " + str(booking_id) + " Added Successfully"}, status.HTTP_200_OK

    def patch(self):
        booking_id = request.args.get('id')
        request_type = request.args.get('request')

        if request_type == 'pick_up':
            found = False
            for booking in Booking.bookings:
                if booking['booking_id'] == int(booking_id):
                    if booking['status'] == 'completed':
                        return {"message": 'Booking has already been completed'}, status.HTTP_400_BAD_REQUEST
                    start_date = booking['start_date']
                    found = True
                    if self.today <= start_date:
                        return {"message": 'Booking has not yet started, you can pickup on or after ' +
                                           str(start_date)}, status.HTTP_400_BAD_REQUEST
                    if booking['status'] != 'new':
                        return {"message": 'Booking has already been picked up/completed'}, status.HTTP_400_BAD_REQUEST
                    else:
                        booking['status'] = 'in_progress'
            if not found:
                return {"message": 'Booking ' + str(booking_id) + ' not found'}, status.HTTP_200_OK
            return {"message": 'Booking ' + str(booking_id) + ' successfully registered for pick up'}, \
                status.HTTP_200_OK

        elif request_type == 'drop_off':
            found = False
            for booking in Booking.bookings:
                if booking['booking_id'] == int(booking_id):
                    end_date = booking['end_date']
                    start_date = booking['start_date']
                    found = True
                    if booking['status'] != 'in_progress':
                        return {"message": 'Booking has not yet been picked up or completed'}, \
                               status.HTTP_400_BAD_REQUEST
                    else:
                        booking['status'] = 'completed'
                    if self.today >= end_date:
                        return {"message": 'Drop off date passed, you had to drop off on or before ' + str(end_date)}, \
                               status.HTTP_400_BAD_REQUEST
                    elif self.today <= start_date:
                        return {"message": 'Drop off date cannot be before start date'}, \
                               status.HTTP_400_BAD_REQUEST
            if not found:
                return {"message": 'Booking ' + str(booking_id) + ' not found'}, status.HTTP_200_OK
            return {"message": 'Booking ' + str(booking_id) + ' successfully registered for drop off'}, \
                status.HTTP_200_OK
        else:
            return {"message": 'Invalid request type'}, status.HTTP_400_BAD_REQUEST


api.add_resource(Customer, '/customers')
api.add_resource(Cars, '/cars')
api.add_resource(Booking, '/booking')

if __name__ == '__main__':
    app.run(port='5002', debug=True)
