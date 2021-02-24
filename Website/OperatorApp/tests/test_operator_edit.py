from django.test import TestCase, Client
from ..models import Operator, Mode
from django.contrib.auth.models import User
from ..forms import OperatorForm
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

    def test_edit_operator_details(self):
        response = self.client.post('/', {"username": 'TestAdmin', "password": "1234"})
        response = self.client.get('/edit/')

        data = response.context['form'].initial
        opform = ({
            "name": data['name'],
            "modes": 1,
            "homepage": "https://test.com/",
            "api_url": data['api_url'],
            "default_language": data["default_language"],
            "phone": "07712345678",
            "email": data['email'],
            "active": data["active"]
        })
        response = self.client.post('/edit/', opform, follow=True)

        self.operator1 = Operator.objects.get(id=self.operator1.id)
        self.assertEqual(self.operator1.phone, '07712345678')
        self.assertEqual(self.operator1.homepage, 'https://test.com/')
        self.assertEqual(response.context['form'].initial['phone'], '07712345678')