import json

from django.test import TestCase
from django.urls import reverse

from user_module.models import User
# Create your tests here.
class Test_Login(TestCase):
    def setUp(self):
        user=User(email='test@test.com',username='user1',activation_code='sdsds',is_active=True)
        user.set_password('1234')
        user.save()
        content=json.loads(self.client.post(reverse('login'),data={'email_username':'test@test.com','password':'1234'}).content)
        access_token=content.get('access_token')
        self.who_am_i__result=self.client.get(reverse('who_am_i'),headers={'Authorization':f'Bearer {access_token}'}).status_code
    def test(self):
        self.assertEqual(self.who_am_i__result,200,msg='failed to authenticate with valid access token')

