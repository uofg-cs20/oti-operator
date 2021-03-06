import os, random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OperatorWebsite.settings')

import django
django.setup()

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from OperatorApp.models import Mode, Operator


def choice(all_modes):
    return random.choice(all_modes)

def populate():
    # delete if the database is already populated
    if User.objects.filter(username='dev').exists():
        User.objects.all().delete()
    if Mode.objects.all():
        Mode.objects.all().delete()
    if Operator.objects.all():
        Operator.objects.all().delete()

    # create superuser account - use this to log into the django admin page
    dev = User.objects.create_user(username='dev', password='1234', is_superuser=True, is_staff=True, email="dev@project.com", first_name='dev')

    # create modes
    on_foot = Mode.objects.get_or_create(short_desc='on foot', long_desc='for complete end-to-end journey mapping')[0]
    cycle = Mode.objects.get_or_create(short_desc='cycle', long_desc='includes both human-powered pedal cycle and ebike, typically rented or shared but also possibly privately owned for complete end-to-end journey mapping')[0]
    moped_motorbike = Mode.objects.get_or_create(short_desc='moped & motorbike', long_desc='shared & privately-owned self-powered vehicles, for complete end-to-end journey mapping')[0]
    scooter = Mode.objects.get_or_create(short_desc='scooter', long_desc='includes human and electric/battery powered where passenger steps in/on')[0]
    segway = Mode.objects.get_or_create(short_desc='segway', long_desc='includes any motorised self-balancing personal platform and also electric unicycles')[0]
    car = Mode.objects.get_or_create(short_desc='car', long_desc='includes any vehicle where the driver is also a passenger, such as: car / van vehicle rental, car pool & car club')[0]
    bus = Mode.objects.get_or_create(short_desc='bus', long_desc='includes any vehicle typically greater than 8 seats.. such as a mini bus')[0]
    tram = Mode.objects.get_or_create(short_desc='tram', long_desc='includes any guided vehicle such as a streetcar and also trolleybuses that are limited by overhead power lines')[0]
    metro_subway = Mode.objects.get_or_create(short_desc='metro & subway', long_desc='includes any light rail transit and their interconnecting systems')[0]
    train = Mode.objects.get_or_create(short_desc='train', long_desc='includes intercity, Eurostar / TGV, etc.')[0]
    water_bus = Mode.objects.get_or_create(short_desc='water bus', long_desc='includes river buses, typically just passenger service with multiple stops')[0]
    water_ferry = Mode.objects.get_or_create(short_desc='water ferry', long_desc='includes passenger only and also passenger & vehicle')[0]
    air = Mode.objects.get_or_create(short_desc='air', long_desc='aeroplane, helicopter, etc.')[0]
    car_parking = Mode.objects.get_or_create(short_desc='car parking', long_desc='includes on-street & off-street (e.g. dedicated building or airport short & long stay)')[0]
    taxi = Mode.objects.get_or_create(short_desc='taxi', long_desc='includes any vehicle where the driver is NOT a passenger')[0]
    suspended_cable_car = Mode.objects.get_or_create(short_desc='suspended cable car', long_desc="includes any aerial cable cars, such as London 'Emirates Air Line', Barcelona Montju??c & Port Cable Cars and New York Roosevelt Island Tramway")[0]
    all_modes = [on_foot, cycle, moped_motorbike, scooter, segway, car, bus, tram, metro_subway, train, water_bus, water_ferry, air, car_parking, taxi, suspended_cable_car]

    # create users
    num = 30
    User.objects.bulk_create([User(username='user'+str(i), password=make_password('1234', None, 'md5'), email='test@test.co.uk', first_name="Admin " +str(i)) for i in range(num)])
    
    # create operators
    Operator.objects.bulk_create([Operator(admin=User.objects.filter(username="user"+str(j))[0], name="Operator "+str(j), homepage='https://operator'+str(j)+'.co.uk', api_url='https://opentransport.operator'+str(j)+'.co.uk', phone='07123456789', email='support@operator'+str(j)+'.co.uk', miptaurl="https://mipta.operator"+str(j)+".co.uk") for j in range(num)])
    ops = Operator.objects.all()
    for op in ops:
        mod = []
        for j in range(random.randint(1, 3)):
            mod.append(random.choice(all_modes))
        op.modes.set(mod)
        
    # Edit Operator 0 to point to Zebras
    zebrasobj = Operator.objects.get(name="Operator 0")
    zebrasobj.name = "Zebras"
    zebrasobj.homepage = "https://cs20customer.herokuapp.com/"
    zebrasobj.api_url = "https://cs20customer.herokuapp.com/api/"
    zebrasobj.miptaurl = "https://mipta.zebras.co.uk"
    zebrasobj.modes.set([cycle, scooter])
    Operator.save(zebrasobj)
    
    # Edit Operator 1 to point to CS21's customer site
    cstwentyoneobj = Operator.objects.get(name="Operator 1")
    cstwentyoneobj.name = "PSD Buses"
    cstwentyoneobj.homepage = "https://cs21customerproject.pythonanywhere.com/"
    cstwentyoneobj.api_url = "https://psdbuses.pythonanywhere.com/"
    cstwentyoneobj.miptaurl = "https://mipta.cs21.co.uk"
    cstwentyoneobj.modes.set([bus])
    Operator.save(cstwentyoneobj)
    
    # Edit Operator 2 to point to Cheetahs
    cheetahsobj = Operator.objects.get(name="Operator 2")
    cheetahsobj.name = "Cheetahs"
    cheetahsobj.homepage = "https://cs20team.pythonanywhere.com/"
    cheetahsobj.api_url = "https://cs20team.pythonanywhere.com/api/"
    cheetahsobj.miptaurl = "https://mipta.cheetahs.co.uk"
    cheetahsobj.modes.set([bus, tram, train])
    Operator.save(cheetahsobj)
    
    # Edit Operator 3 to point to Sharks
    sharksobj = Operator.objects.get(name="Operator 3")
    sharksobj.name = "Sharks"
    sharksobj.homepage = "http://127.0.0.1:8000/"
    sharksobj.api_url = "http://127.0.0.1:8000/api/"
    sharksobj.miptaurl = "https://mipta.sharks.co.uk"
    sharksobj.modes.set([water_ferry, water_bus])
    Operator.save(sharksobj)



if __name__ == '__main__':
    print('Starting population script...', end="")
    populate()
    print('DONE')