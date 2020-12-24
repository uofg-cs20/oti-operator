from django.test import TestCase, Client
from ..models import Operator, Mode
from django.contrib.auth.models import User
from ..forms import OperatorForm
import json

from ..views import operator_login, edit_profile


class OperatorTestCase(TestCase):
    def setUp(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        self.admin1 = User.objects.create_user(username='TestAdmin', password='1234', email='test@operator.co.uk.',
                                               first_name='Test Admin')
        self.operator1 = Operator.objects.create(admin=self.admin1, name='TestOperator',
                                                 homepage='https://operator.co.uk',
                                                 api_url='https://test.opentransport.co.uk', phone='07083249084',
                                                 email='test@operator.co.uk')

        on_foot = Mode.objects.get_or_create(short_desc='on foot', long_desc='for complete end-to-end journey mapping')
        on_foot = Mode.objects.get_or_create(short_desc='on foot')[0]
        self.operator1.modes.add(on_foot.id)

    def test_operator_api(self):
        print("Operator API Test")
        response = self.client.get('/api/?operator=1')
        content = json.loads(response.content)
        comparisonDict = {"model": "OperatorApp.operator",
                          "pk": 1, "fields": {"admin": 1, "name": "TestOperator",
                                              "homepage": "https://operator.co.uk",
                                              "api_url": "https://test.opentransport.co.uk",
                                              "default_language": "English", "phone": "07083249084",
                                              "email": "test@operator.co.uk", "active": True, "modes": [1]}}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, comparisonDict)

    def test_mode_api(self):
        print("Mode API Test")
        response = self.client.get('/api/?mode=1')
        content = json.loads(response.content)
        comparisonDict = {'model': 'OperatorApp.mode', 'pk': 1,
                          'fields': {'short_desc': 'on foot', 'long_desc': 'for complete end-to-end journey mapping'}}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, comparisonDict)
