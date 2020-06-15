from flask import Flask, request
from flask_restful import Resource, Api
import json
from datetime import datetime

app = Flask(__name__)
api = Api(app)


@app.route('/')
def api_root():
    return '<h1>Welcome to EURent</h1>'


class Cars(Resource):
    TYPES = ['economic', 'standard', 'premium']
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
        return json.dumps(self.cars)
    
    def post(self):
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
        to_return = []
        for entry in Cars.cars:
            if entry['model'] == model:
                to_return.append(entry)
        return json.dumps(to_return)


class Customer(Resource):
    customers = [{'ID': 1, 'name': 'Harvey Specter', 'mobile': '0123456789', 'bookings': 0},
                 {'ID': 2, 'name': 'Mike Ross', 'mobile': '0112345678', 'bookings': 0},
                 {'ID': 3, 'name': 'Louis Litt', 'mobile': '0111234567', 'bookings': 0},
                 {'ID': 4, 'name': 'Jessica Pearson', 'mobile': '0111123456', 'bookings': 0},
                 {'ID': 5, 'name': 'Robert Zane', 'mobile': '0111112345', 'bookings': 0}]
    def get(self):
        return json.dumps(self.customers)

    @staticmethod
    @app.route('/customers/<name>')
    def get_customer_by_name(name):
        to_return = []
        for entry in Customer.customers:
            if entry['name'] == name:
                to_return.append(entry)
        return json.dumps(to_return)

    def post(self):
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
    bookings = []

    def get(self):
        return json.dumps(self.bookings, default=str)

    @staticmethod
    @app.route('/booking/searchbyid/<id>')
    def get_booking_by_id(id):
        for booking in Booking.bookings:
            if booking['booking_id'] == int(id):
                return booking
        return "No booking found for this id"

    @staticmethod
    @app.route('/booking/searchbycustomer/<name>')
    def get_bookings_by_customer_name(name):
        customer_bookings = []
        for booking in Booking.bookings:
            customer = booking['customer']
            if customer['name'] == name:
                customer_bookings.append(booking)

        if len(customer_bookings) <= 0:
            return "No bookings found for customer " + name
        else:
            return json.dumps(customer_bookings)

    def post(self):
        booking_id = id(self)
        selected_car = None
        car_type = request.args.get('car')
        date_format = '%d-%m-%Y'
        try:
            start_date = datetime.strptime(request.args.get('start_date'), date_format)
            end_date = datetime.strptime(request.args.get('end_date'), date_format)
        except ValueError:
            return 'Invalid date format please use dd-mm-yyyy'
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

    def patch(self):
        today = datetime.now()
        return str(today)


api.add_resource(Customer, '/customers')
api.add_resource(Cars, '/cars')
api.add_resource(Booking, '/booking')

if __name__ == '__main__':
    app.run(port='5002', debug=True)
