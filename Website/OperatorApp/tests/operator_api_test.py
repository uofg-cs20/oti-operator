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
                                                 email='test@operator.co.uk', miptaurl='mipta.operator.co.uk')

        on_foot = Mode.objects.get_or_create(short_desc='on foot', long_desc='for complete end-to-end journey mapping')
        on_foot = Mode.objects.get_or_create(short_desc='on foot')[0]
        self.operator1.modes.add(on_foot.id)

    def test_operator_api(self):
        self.maxDiff = None
        print('Operator API Test')
        openT = 'urn:X-opentransport:rels:'
        response = self.client.get('/api/operator/?filterString=1')
        content = json.loads(response.content)
        comparisonDict = [{'catalogue-metadata': [
            {'rel': 'urn:X-hypercat:rels:isContentType', 'val': 'application/vnd.hypercat.catalogue+json'},
            {'rel': 'urn:X-hypercat:rels:hasDescription:en', 'val': 'OpenTransport Operator Catalogue'},
            {'rel': 'urn:X-hypercat:rels:supportsSearch', 'val': 'urn:X-hypercat:search:simple'}], 'items': [
            {'href': 'https://test.opentransport.co.uk', 'item-metadata': [
                {'rel': 'urn:X-hypercat:rels:isContentType', 'val': 'application/vnd.hypercat.catalogue+json'},
                {'rel': 'urn:X-hypercat:rels:hasDescription:en', 'val': 'TestOperator'},
                {'rel': 'urn:X-hypercat:rels:hasHomepage', 'val': 'https://operator.co.uk'}, {'rel': openT+'hasID', 'val': 1},
                {'rel': openT+'hasEmail', 'val': 'test@operator.co.uk'}, {'rel': openT+'hasPhone', 'val': '07083249084'},
                {'rel': openT+'hasDefaultLanguage', 'val': 'English'}, {'rel': openT+'hasNumberModes', 'val': 1},
                {'rel': openT+'hasNumberMode1#Code', 'val': 1}, {'rel': openT+'hasNumberMode1#Description', 'val': 'on foot'},
                {'rel': openT+'hasNumberMIPTAURLs', 'val': 1}, {'rel': openT+'hasMIPTAURL', 'val': 'mipta.operator.co.uk'}
                ]}]}]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, comparisonDict)

    def test_mode_api(self):
        print('Mode API Test')
        response = self.client.get('/api/mode/?filterString=1')
        content = json.loads(response.content)
        comparisonDict = [{'id': 1, 'short_desc': 'on foot', 'long_desc': 'for complete end-to-end journey mapping'}]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, comparisonDict)
