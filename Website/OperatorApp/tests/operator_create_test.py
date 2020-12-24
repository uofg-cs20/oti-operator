from django.test import TestCase
from ..models import Operator, Mode
from django.contrib.auth.models import User


class OperatorTestCase(TestCase):
    def setUp(self):
        admin1 = User.objects.create_user(username='TestAdmin', password='1234', email='test@operator.co.uk.',
                                          first_name='Test Admin')
        operator1 = Operator.objects.create(admin=admin1, name='TestOperator', homepage='https://operator.co.uk',
                                            api_url='https://test.opentransport.co.uk', phone='07083249084',
                                            email='test@operator.co.uk')

        on_foot = Mode.objects.get_or_create(short_desc='on foot', long_desc='for complete end-to-end journey mapping')
        cycle = Mode.objects.get_or_create(short_desc='cycle',
                                           long_desc='includes both human-powered pedal cycle and ebike, typically '
                                                     'rented or shared but also possibly privately owned for complete '
                                                     'end-to-end journey mapping')
        moped_motorbike = Mode.objects.get_or_create(short_desc='moped & motorbike',
                                                     long_desc='shared & privately-owned self-powered vehicles, '
                                                               'for complete end-to-end journey mapping')

        on_foot = Mode.objects.get_or_create(short_desc='on foot')[0]
        cycle = Mode.objects.get_or_create(short_desc='cycle')[0]
        moped_motorbike = Mode.objects.get_or_create(short_desc='moped & motorbike')[0]

        operator1.modes.add(on_foot.id)
        operator1.modes.add(cycle.id)
        operator1.modes.add(moped_motorbike.id)

    def test_operator_exists(self):
        """Operator details are checked"""
        print("Operator Exists Test")
        operator = Operator.objects.get(name="TestOperator")
        
        self.assertEqual(operator.name, 'TestOperator')
        self.assertEqual(operator.modes.get(id='1').short_desc, 'on foot')
        self.assertEqual(operator.modes.get(id='2').short_desc, 'cycle')
        self.assertEqual(operator.modes.get(id='3').short_desc, 'moped & motorbike')
