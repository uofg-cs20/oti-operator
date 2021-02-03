# CS20 Operator  

This repository contains the Operator website, while the main repository contains the Customer website  

## Installation  

Install requirements:  
`cd cs20-operator`  
`pip install -r requirements.txt`  

Ensure database structure is up to date:  
`cd Website`  
`python manage.py makemigrations`  
`python manage.py migrate`  

Run the population script:  
`python populate.py`  

Run the server:  
`python manage.py runserver`

Run the tests:  
`python manage.py test --pattern="*_test.py"`

Log in as an operator (homepage):  
username: scotrail / firstbus / citylink (see population script)  
password: 1234  

Log in as website admin (/admin):  
username: dev  
password: 1234  

To view the API visit   
Operators: `http://127.0.0.1:8000/api/?operator=<pk>`   
Mode: `http://127.0.0.1:8000/api/?mode=<pk>`

Coverage Test Report
`coverage run --source 'OperatorApp' manage.py test OperatorApp --pattern="*_test.py"`
`coverage report`