# MeecoCodingChallengePart2
Part 2 of the Meeco Coding Challenge. This task required us to create an API for a fictional Car Rental company with several requirements for the type of cars, customers and bookings.


## Getting Started

This API is built in Python using the Flask framework. The flask API has several endpoints that are described further. The details about the software used can be found in the 'Built With' section below.


### Prerequisites

This project requires the following software to be installed:

**1. Python**
Can be installed in Windows using [this](https://www.python.org/downloads/windows/) link. For Linux users, including Macintosh, it can be installed using [this](https://www.python.org/downloads/mac-osx/) link.

**2. Flask**
Flask library needs to be installed after python is installed on the machine. This can be done by writing the following code in the command prompt on windows or Terminal on Macintosh

```
pip install flask
```
(Hint: Try using --user if there are permission issues)

**3. Flask-API**
Flask-API library needs to be installed on top of the Flask framework on the machine. This can be done by writing the following code on the command prompt on windows or Terminal on Macintosh

```
pip install Flask-API
```
(Hint: Try using --user if there are permission issues)

### Execution

Please use the following steps to execute the program

**1. Open command prompt/Terminal**
**2. Traverse to the folder on the machine**
**3. Run the file**
Use the following code to run the Flask server
```
python main.py
```
This will ensure that the flask server is running. Once you see the following on your command prompt/terminal, the server should be up and running:

```
 * Serving Flask app "main" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5002/ (Press CTRL+C to quit)
```
**4. Access the server**
Use [this](http://127.0.0.1:5002/) link to access the API endpoints.


## Using the API Endpoints

There are several endpoints for using this API. These can primarily be divided into 3 major categories:

### Customer
The customer endpoint handles the details for customers. There are several mock customers already added to this file. 
To access this endpoint, you can use the link: 

```
http://127.0.0.1:5002/customers
```
Link - [Customers](http://127.0.0.1:5002/customers).

There are two types of HTTP requests handled by this endpoint: 

#### GET
The GET request returns the details of all customers in a JSON format. If there are no customers, it will return an empty JSON.

#### POST
The POST request adds a new customer to the already existing list of customers. It requires the following arguments:
- name: The customer's name
- mobile: The customer's mobile phone number

An example of adding a new customer is as follows:
```
http://127.0.0.1:5002/customers?name=Donna Paulsen&mobile=01111112345
```

**DUPLICATE CUSTOMERS CANNOT BE ADDED**

### Cars
The customer endpoint handles the details for cars. There are several mock cars already added from a test file. 
To access this endpoint, you can use the link: 

```
http://127.0.0.1:5002/cars
```
Link - [Cars](http://127.0.0.1:5002/cars).

There are two types of HTTP requests handled by this endpoint: 

#### GET
The GET request returns the details of all cars in a JSON format. If there are no cars, it will return an empty JSON.

#### POST
The POST request adds a new cars to the already existing list of cars. It requires the following arguments:
- model: The cars's model
- license_plate: The car's license plate
- type: The car's type (must be one of economic, standard, or premium)
- fee: The car's rental fee (has to be a positive integer)

An example of adding a new car is as follows:
```
http://127.0.0.1:5002/cars?model=Tesla Model X&license_plate=BELGIUM&type=premium&fee=90
```

**DUPLICATE CARS CANNOT BE ADDED**

### Booking
The booking endpoint handles the details of bookings made for the cars. 
To access this endpoint, you can use the link: 

```
http://127.0.0.1:5002/booking
```
Link - [Booking](http://127.0.0.1:5002/booking).

There are three types of HTTP requests handled by this endpoint: 

#### GET
The GET request returns the details of all bookings in a JSON format. If there are no bookings, it will return an empty JSON.

There are two sub-endpoints contained within the GET request:

**1. GET bookings by ID**
This endpoint returns the detail of the booking searched by the ID provided as an argument.
The link to access this endpoint is as follows:
```
http://127.0.0.1:5002/booking/searchbyid
```
An example of getting a booking by ID is as follows:
```
http://127.0.0.1:5002/booking/searchbyid/2706226014344
```
This will return the details for the booking ID = 2706226014344, if it exists, otherwise, it will return an empty JSON

**2. GET bookings by customer's name**
This endpoint returns the details of the bookings searched by the customer's name provided as an argument
The link to access this endpoint is as follows:

```
http://127.0.0.1:5002/booking/searchbycustomer
```
An example of getting bookings by Customer's name is as follows: 

```
http://127.0.0.1:5002/booking/searchbycustomer/Mike%20Ross
```
This will return the details of the bookings made by Mike Ross. If there are no bookings, it will return an empty JSON.

#### POST
The POST request for this endpoint will add a new booking to the list of bookings. This request requires the following arguments:

- car: The car's type to be booked (must be one of economic, standard, or premium)
- customer: The name of the customer related to the booking (must be a customer that exists in the customer list)
- start_date: The date when the booking starts (must be after today's date)
- end_date: The date when the booking ends (must be after the start date and today's date)

**Bookings cannot be made if no cars of that type are available in the specified date range**

#### PATCH
The PATCH request for this endpoint handles the pick-up and drop-off for the booking. It requires the following arguments:
- id: The ID for the booking being changed
- request: The type of request being made (must be one of pick_up or drop_off)

**Pick-up** <br />
The following conditions must be met to register a pick up:
1. Valid booking ID: The booking ID must exist 
2. Start date must be on the day the request is being made or have already passed
3. The status of the booking should be new

**Drop-off** <br />
The following conditions must be met to register a drop off:
1. Valid booking ID: The booking ID must exist
2. Today's date must be before or on the booking's end date
3. The status of the booking should be in_progress


## Deployment

Since this API is only built for a test server, there is currently no framework designed to implement it on a live system.

## Built With

* [PyCharm](https://www.jetbrains.com/pycharm/) - The Python IDE used
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - The web dev API used
* [Postman](https://www.postman.com/) - The API collaborator used


## Authors

* **Aditi Sharma** - [LinkedIn](https://www.linkedin.com/in/aditisharma25/) | [Github](https://github.com/aditisharma2512)

## Acknowledgments

* Thank you to the team at Meeco.me for presenting the opportunity to create this project, specially Yuri Leikind and Jan Vereecken for their help and guidance.
