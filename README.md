## CS20 Team Project Overview

**University of Glasgow - School of Computing Science - Third Year Team Project**

This project was to implement the Open Transport API and create a proof of concept of data sharing between two public transport operators. To do this we made two websites: Operator and Customer, both implementing their respective APIs. A user can log in to one instance of the Customer site, and link their account from another instance of the Customer site. This works by querying the Operator site to get the details of the second Customer instance, and then querying that Customer instance to retrieve the ticket data.

## Main Functionality

This repository contains the Operator website, which implements the Operator API (https://app.swaggerhub.com/apis/open-transport/operator-info/1.1.0). It can be populated with dummy operator data, to illustrate the purpose of the website - i.e. a transport operator lookup. Once logged in, there are 2 main pages:
- Operators - for viewing a complete list of transport operators, and their details
- Edit Profile - for updating your details

## Installation  

Install requirements:  
`cd cs20-operator`  
`pip install -r requirements.txt`  

Ensure database structure is up to date:  
`cd Website`  
`python manage.py makemigrations`  
`python manage.py migrate`  

## Viewing the Website

Run the population script:  
`python populate.py`  

Run the server:  
`python manage.py runserver`

Run the tests:  
`python manage.py test`

Log in as an operator (homepage):  
username: scotrail / firstbus / citylink (see population script)  
password: 1234  

Log in as website admin (/admin):  
username: dev  
password: 1234  

To view the API visit   
Operators: `http://127.0.0.1:8000/api/operator`   
Mode: `http://127.0.0.1:8000/api/mode`
