"""
This file contains the Car class and the CarByModel class. The car class is used to store information about the cars
added to the application and the CarByModel class is used to retrieve a car according to the name given by the user.
"""

__author__ = "Aditi Sharma"
__modified__ = "16-06-2020"

from flask import request
from flask_restful import Resource
from flask_api import status
import json


class Cars(Resource):
    """
    This class creates Cars to be added to the EURent system. The class handles get and post requests.
    """
    TYPES = ['economic', 'standard', 'premium']  # A class of a car can only belong to one of these car type values

    def __init__(self):
        self.cars = []
        with open('cars.csv', encoding='utf-8') as fn:
            lines = fn.readlines()
        count = 0
        for line in lines:
            if count == 0:
                pass
            else:
                vals = line.lstrip(' ').rstrip(' ').strip('\n').split(',')
                self.cars.append({'model': vals[0].strip(' '), 'license_plate': vals[1].strip(' '), 'type': vals[2].strip(' '),
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
        if not model:
            return {"message": "Car model cannot be blank"}, status.HTTP_400_BAD_REQUEST
        license_plate = request.args.get('license_plate')
        type = request.args.get('type')
        if type not in self.TYPES:
            return {"message": "Incorrect car type. Must belong to " + str(self.TYPES)}, status.HTTP_400_BAD_REQUEST
        fee = request.args.get('fee')
        try:
            fee = int(fee)
            if fee < 0:
                raise ValueError
        except ValueError:
            return {"message": "Fee must be a positive int value "}, status.HTTP_400_BAD_REQUEST

        car_dict = {'model': model, 'license_plate': license_plate, 'type': type, 'fee': fee}
        if car_dict in self.cars:
            return {"message": "This car already exists"}, status.HTTP_400_BAD_REQUEST
        else:
            self.cars.append(car_dict)
            return {"message": "Added Car Successfully"}, status.HTTP_200_OK


class CarByModel(Resource):
    """
    This class searches the cars by the model given by the user
    """
    def get(self, model):
        """
        GET method for the car class, but with model being passed as a parameter
        :return: Details of the car in a JSON format
        """
        cars = Cars()
        cars = cars.cars
        to_return = []
        for entry in cars:
            if entry['model'] == model:
                to_return.append(entry)
        return json.dumps(to_return), status.HTTP_200_OK
