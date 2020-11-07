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
    scotrail = Operator.objects.get_or_create(admin=admin1, name='Scotrail', homepage='scotrail.co.uk', api_url='opentransportapi/scotrail', phone='07083249084', email='support@scotrail.co.uk')[0]
    citylink = Operator.objects.get_or_create(admin=admin2, name='Citylink', homepage='citylink.co.uk', api_url='opentransportapi/citylink', phone='117083249084', email='support@citylink.co.uk')[0]   
    firstbus = Operator.objects.get_or_create(admin=admin3, name='First Bus', homepage='firstbus.co.uk', api_url='opentransportapi/firstbus', phone='087083249084', email='support@firstbus.co.uk')[0]   

    # modes
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