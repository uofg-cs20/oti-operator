from django.test import TestCase, Client
from ..models import Operator, Mode
from django.contrib.auth.models import User
from ..forms import OperatorForm
import json
import sys, os
from django.core.serializers import serialize
from ..Hypercat import hypercat
from ..views import operator_login, edit_profile

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Hypercat"))


class OperatorTestCase(TestCase):


    def setUp(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        self.admin1 = User.objects.create_user(username='TestAdmin', password='1234', email='test@operator.co.uk.',
                                               first_name='Test Admin')
        self.operator1 = Operator.objects.create(admin=self.admin1, name='TestOperator',
                                                 homepage='https://operator.co.uk',
                                                 api_url='https://test.opentransport.co.uk', phone='07083249084',
                                                 email='test@operator.co.uk', miptaurl='mipta.operator.co.uk')

        self.on_foot = Mode.objects.get_or_create(short_desc='on foot', long_desc='for complete end-to-end journey mapping')
        self.on_foot = Mode.objects.get_or_create(short_desc='on foot')[0]
        self.operator1.modes.add(self.on_foot.id)

    def test_operator_api_displays_data(self):
        self.maxDiff = None
        openT = 'urn:X-opentransport:rels:'
        response = self.client.get('/api/operator/?filterString=1')
        content = json.loads(response.content)
        comparisonDict = hypercat.createOperatorHypercat(serialize('python', [self.operator1]), Mode.objects.all())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, comparisonDict)

    def test_mode_api_displays_data(self):
        response = self.client.get('/api/mode/?filterString=1')
        content = json.loads(response.content)
        comparisonDict = [{'id': 1, 'short_desc': 'on foot', 'long_desc': 'for complete end-to-end journey mapping'}]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, comparisonDict)
