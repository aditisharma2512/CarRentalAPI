"""
This class handles all the booking data. There are three classes in this file:
Booking : Handles the booking data, it stores the records of the bookings being made.
It handles three requests: GET, POST, PATCH
BookingById: Searches the bookings by the Id given by the user
BookingByCustomer: Searches the bookings by the customer name given by the user
"""

__author__ = "Aditi Sharma"
__modified__ = "16-06-2020"

from flask import request
from flask_restful import Resource
from flask_api import status
import json
from datetime import datetime
from Cars import Cars
from Customers import Customer


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

    def fix_date(self, date_str):
        """
        Method to convert date string to date format
        :param date_str: The string of date to be converted
        :return: the fixed date, if successful, otherwise none
        """
        try:
            fixed_date = datetime.strptime(date_str, self.date_format).date()
        except TypeError or ValueError:
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
        try:
            start_date = self.fix_date(request.args.get('start_date'))
            end_date = self.fix_date(request.args.get('end_date'))
        except ValueError:
            return {"message": "Invalid Dates Provided, please use dd-mm-yyyy"}, status.HTTP_400_BAD_REQUEST
        if start_date < self.today or end_date < start_date:
            return {"message": 'Invalid date range provided'}, status.HTTP_400_BAD_REQUEST
        if car_type not in Cars.TYPES:
            return {"message": 'Invalid car type, please enter one from ' + str(Cars.TYPES)}, \
                   status.HTTP_400_BAD_REQUEST

        # To get the available cars, we follow the steps below:
        # 1. Get a list of all cars of the type specified by the user
        # 2. Check if there are any bookings for these cars in the date range specified
        # 3. Remove the cars identified in step 2 that are booked
        # 4. Book the first available car in the list
        car_list = []
        cars = Cars.cars
        for one_car in cars:
            if one_car['type'] == car_type:
                car_list.append(one_car)
        for booking in self.bookings:
            if booking['start_date'] <= start_date <= booking['end_date'] or \
                    booking['start_date'] <= end_date <= booking['end_date']:
                for car in car_list:
                    if booking['car'] == car:
                        car_list.remove(car)

        # If there are no cars of this type left, return response
        if len(car_list) <= 0:
            return {"message": 'No ' + str(car_type) + " cars available for this date range"}, status.HTTP_200_OK
        else:
            selected_car = car_list[0]

        # Find the customer from the customer list
        selected_customer = None
        customers = Customer.customers
        customer = request.args.get('customer')
        for one_cust in customers:
            if one_cust['name'] == customer:
                selected_customer = one_cust
                one_cust['bookings'] += 1

        # If the customer doesn't exist, return an error message
        if not selected_customer:
            return {"message": 'Customer not found'}, status.HTTP_400_BAD_REQUEST

        # If the end date is BEFORE start date, return an error message
        if end_date < start_date:
            return {"message": 'End date cannot be before start date'}, status.HTTP_400_BAD_REQUEST

        # Since the post method adds a new booking, the status is always new
        booking_status = 'new'

        Booking.bookings.append({'booking_id': booking_id, 'customer': selected_customer, 'car': selected_car,
                                 'start_date': start_date, 'end_date': end_date, 'status': booking_status})
        return {"message": "Booking " + str(booking_id) + " Added Successfully"}, status.HTTP_200_OK

    def patch(self):
        """
        Patch method for updating the fields for the booking. This method expects two arguments:
        :arg: id: The booking ID
        :arg: request: The type of request (pick_up, drop_off)
        :return: Message once the operation is complete
        """
        booking_id = request.args.get('id')
        request_type = request.args.get('request')

        # If the request is to pick_up a car, run the code below
        if request_type == 'pick_up':
            found = False
            for booking in Booking.bookings:
                if booking['booking_id'] == int(booking_id):
                    if booking['status'] == 'completed':
                        return {"message": 'Booking has already been completed'}, status.HTTP_400_BAD_REQUEST
                    start_date = booking['start_date']
                    end_date = booking['end_date']
                    found = True
                    if self.today < start_date and self.today < end_date:
                        return {"message": 'Booking has not yet started, you can pickup on or after ' +
                                           str(start_date)}, status.HTTP_400_BAD_REQUEST
                    # If the booking is not new, it is unavailable for pick up
                    if booking['status'] != 'new':
                        return {"message": 'Booking has already been picked up/completed'}, status.HTTP_400_BAD_REQUEST
                    else:
                        booking['status'] = 'in_progress'
            if not found:
                return {"message": 'Booking ' + str(booking_id) + ' not found'}, status.HTTP_200_OK
            return {"message": 'Booking ' + str(booking_id) + ' successfully registered for pick up'}, \
                status.HTTP_200_OK

        # If the request is to drop off, run the code below
        elif request_type == 'drop_off':
            found = False
            for booking in Booking.bookings:
                if booking['booking_id'] == int(booking_id):
                    end_date = booking['end_date']
                    start_date = booking['start_date']
                    found = True
                    # If a booking is not in progress, it is unable to be dropped off
                    if booking['status'] != 'in_progress':
                        return {"message": 'Booking has not yet been picked up or completed'}, \
                               status.HTTP_400_BAD_REQUEST
                    else:
                        booking['status'] = 'completed'

                    # If the end date has passed, the booking is unable to be dropped off
                    if self.today > end_date:
                        return {"message": 'Drop off date passed, you had to drop off on or before ' + str(end_date)}, \
                               status.HTTP_400_BAD_REQUEST

                    # Cannot drop off if the drop off date is before the start date
                    elif self.today < start_date:
                        return {"message": 'Drop off date cannot be before start date'}, \
                               status.HTTP_400_BAD_REQUEST
            if not found:
                return {"message": 'Booking ' + str(booking_id) + ' not found'}, status.HTTP_200_OK
            return {"message": 'Booking ' + str(booking_id) + ' successfully registered for drop off'}, \
                status.HTTP_200_OK
        else:
            return {"message": 'Invalid request type'}, status.HTTP_400_BAD_REQUEST


class BookingById(Resource):
    """
    This class searches the bookings by the Id given by the user
    """
    def get(self, id):
        """
        GET method for the class but with ID given as a parameter
        :param id: ID to be searched
        :return: booking, if found. Otherwise, return a message
        """
        for booking in Booking.bookings:
            if booking['booking_id'] == int(id):
                return json.dumps(booking, default=str), status.HTTP_200_OK
        return {"message": "No booking found for this id"}, status.HTTP_200_OK


class BookingByCustomer(Resource):
    """
    This class searches the Bookings by the customer name given by the user
    """
    def get(self, name):
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
            return json.dumps(customer_bookings, default=str), status.HTTP_200_OK

