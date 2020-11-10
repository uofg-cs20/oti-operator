import os, random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OperatorWebsite.settings')

import django
django.setup()

from django.contrib.auth.models import User
from OperatorApp.models import Mode, Operator

def populate():

    # delete if the database is already populated
    if User.objects.filter(username='superuser').exists():
        User.objects.all().delete()
    if Mode.objects.all():
        Mode.objects.all().delete
    if Operator.objects.all():
        Operator.objects.all().delete

    # superuser account - use this to log into the django admin page
    dev = User.objects.create_user(username='dev', password='1234', is_superuser=True, is_staff=True, email="dev@project.com", first_name='dev')

    # operator admin accounts
    admin1 = User.objects.create_user(username='scotrail', password='1234', email='admin@scotrail.co.uk.', first_name='Scotrail Admin')
    admin2 = User.objects.create_user(username='citylink', password='1234', email='admin@citylink.co.uk.', first_name='CityLink Admin')
    admin3 = User.objects.create_user(username='firstbus', password='1234', email='admin@firstbus.co.uk.', first_name='FirstBus Admin')
    
    # operator profiles
    scotrail = Operator.objects.get_or_create(admin=admin1, name='Scotrail', homepage='https://scotrail.co.uk', api_url='https://scotrail.opentransport.co.uk', phone='07083249084', email='support@scotrail.co.uk')[0]
    citylink = Operator.objects.get_or_create(admin=admin2, name='Citylink', homepage='https://citylink.co.uk', api_url='https://citylink.opentransport.co.uk', phone='117083249084', email='support@citylink.co.uk')[0]   
    firstbus = Operator.objects.get_or_create(admin=admin3, name='First Bus', homepage='https://firstbus.co.uk', api_url='https://firstbus.opentransport.co.uk', phone='087083249084', email='support@firstbus.co.uk')[0]   

    # modes
    on_foot = Mode.objects.get_or_create(short_desc='on foot', long_desc='for complete end-to-end journey mapping')
    cycle = Mode.objects.get_or_create(short_desc='cycle', long_desc='includes both human-powered pedal cycle and ebike, typically rented or shared but also possibly privately owned for complete end-to-end journey mapping')
    moped_motorbike = Mode.objects.get_or_create(short_desc='moped & motorbike', long_desc='shared & privately-owned self-powered vehicles, for complete end-to-end journey mapping')
    scooter = Mode.objects.get_or_create(short_desc='scooter', long_desc='includes human and electric/battery powered where passenger steps in/on')
    segway = Mode.objects.get_or_create(short_desc='segway', long_desc='includes any motorised self-balancing personal platform and also electric unicycles')
    car = Mode.objects.get_or_create(short_desc='car', long_desc='includes any vehicle where the driver is also a passenger, such as: car / van vehicle rental, car pool & car club')
    bus = Mode.objects.get_or_create(short_desc='bus', long_desc='includes any vehicle typically greater than 8 seats.. such as a mini bus')
    tram = Mode.objects.get_or_create(short_desc='tram', long_desc='includes any guided vehicle such as a streetcar and also trolleybuses that are limited by overhead power lines')
    metro_subway = Mode.objects.get_or_create(short_desc='metro & subway', long_desc='includes any light rail transit and their interconnecting systems')
    train = Mode.objects.get_or_create(short_desc='train', long_desc='includes intercity, Eurostar / TGV, etc.')
    water_bus = Mode.objects.get_or_create(short_desc='water bus', long_desc='includes river buses, typically just passenger service with multiple stops')
    water_ferry = Mode.objects.get_or_create(short_desc='water ferry', long_desc='includes passenger only and also passenger & vehicle')
    air = Mode.objects.get_or_create(short_desc='air', long_desc='aeroplane, helicopter, etc.')
    car_parking = Mode.objects.get_or_create(short_desc='car parking', long_desc='includes on-street & off-street (e.g. dedicated building or airport short & long stay)')
    taxi = Mode.objects.get_or_create(short_desc='taxi', long_desc='includes any vehicle where the driver is NOT a passenger')
    suspended_cable_car = Mode.objects.get_or_create(short_desc='suspended cable car', long_desc="includes any aerial cable cars, such as London 'Emirates Air Line', Barcelona Montjuïc & Port Cable Cars and New York Roosevelt Island Tramway")
    

    train = Mode.objects.get_or_create(short_desc='train')[0]
    bus = Mode.objects.get_or_create(short_desc='bus')[0]
    tram = Mode.objects.get_or_create(short_desc='tram')[0]

    # add modes to operators
    scotrail.modes.add(train.id)
    citylink.modes.add(bus.id)
    firstbus.modes.add(bus.id)


if __name__ == '__main__':
    print('Starting population script...', end="")
    populate()
    print('DONE')