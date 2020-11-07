import os, random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OperatorWebsite.settings')

import django
django.setup()

from OperatorApp.models import Mode, Operator

def populate():

    # delete if the database is already populated
    if Mode.objects.all():
        Mode.objects.all().delete
    if Operator.objects.all():
        Operator.objects.all().delete

    scotrail = Operator.objects.get_or_create(name='Scotrail', homepage='scotrail.co.uk', api_url='opentransportapi/scotrail', phone='07083249084', email='support@scotrail.co.uk')[0]

    citylink = Operator.objects.get_or_create(name='Citylink', homepage='citylink.co.uk', api_url='opentransportapi/citylink', phone='117083249084', email='support@citylink.co.uk')[0]   

    firstbus = Operator.objects.get_or_create(name='First Bus', homepage='firstbus.co.uk', api_url='opentransportapi/firstbus', phone='087083249084', email='support@firstbus.co.uk')[0]   

    train = Mode.objects.get_or_create(short_desc='train')[0]
    bus = Mode.objects.get_or_create(short_desc='bus')[0]
    tram = Mode.objects.get_or_create(short_desc='tram')[0]

    scotrail.modes.add(train.id)
    citylink.modes.add(bus.id)
    firstbus.modes.add(bus.id)


if __name__ == '__main__':
    print('Starting population script...', end="")
    populate()
    print('DONE')