from flask import request
from flask_restful import Resource
from flask_api import status
import json


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

    # @staticmethod
    # @app.route('/customers/<name>')
    # def get_customer_by_name(name):
    #     """
    #     GET method for the class but by customer name as an argument
    #     :param name: name of the customer being searched
    #     :return: the records of the customers in a JSON format
    #     """
    #     to_return = []
    #     for entry in Customer.customers:
    #         if entry['name'] == name:
    #             to_return.append(entry)
    #     return json.dumps(to_return), status.HTTP_200_OK

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
            # A customer is uniquely identified by their name AND mobile number
            if customer['name'] == name and customer['mobile'] == mobile:
                # Cannot add duplicate customers
                return {"message":"Customer already exists"}, status.HTTP_400_BAD_REQUEST
        cust_dict = {'ID': max_id+1, 'name': name, 'mobile': mobile, 'bookings': bookings}
        self.customers.append(cust_dict)
        return {"message": "Added Customer Successfully"}, status.HTTP_200_OK


class CustomerByName(Resource):
    """
    This class searches the customers by the name given by the user
    """
    def get(self, name):
        """
        GET method for the class but by customer name as an argument
        :param name: name of the customer being searched
        :return: the records of the customers in a JSON format
        """
        customer = Customer()
        customers = customer.customers
        to_return = []
        for entry in customers:
            if entry['name'] == name:
                to_return.append(entry)
        return json.dumps(to_return), status.HTTP_200_OK
