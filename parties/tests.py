from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from rest_framework.test import APIRequestFactory

from rest_framework import status

from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your tests here.
class TestParty(APITestCase):

    def setUp(self):

        url = reverse('user_login')
        User = get_user_model()
        u = User.objects.create_user(first_name='user', last_name='user1', email='user@foo.com', password='pass')
        self.assertEqual(u.is_active, 1, 'Active User')
        u.save()

        resp = self.client.post(url, {'email':'user@foo.com', 'password':'pass'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.token = resp.data['data']['token']

        self.party_url = reverse('parties_create')
        self.party_data_one = {
            'name':'APC', 
            'hqAddress':'31, Ajayi Aina Street Ikeja', 
            'logoUrl':'www.apc.com'
        }
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        request = self.client.post(self.party_url, self.party_data_one, format='json')
        self.party_id = request.data['data']['id']
        self.party_name = request.data['data']['name']
        
        self.party_data = {
            'name':'DPPM', 
            'hqAddress':'20, Allen Avenue. Ikeja', 
            'logoUrl':'www.dppm.com'
        }

        self.invalid_party_data = {
            'hqAddress':'20, Allen Avenue. Ikeja', 
            'logoUrl':'www.dppm.com'
        }
    
    
    
    def test_create_party_with_valid_data_succeeds(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        resp = client.post(self.party_url, self.party_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_create_party_with_invalid_data_succeeds(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        resp = client.post(self.party_url, self.invalid_party_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_parties_succeeds(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        resp = client.get(self.party_url, data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['status'], 200)
        self.assertEqual(len(resp.data['data']), 1)

    def test_get_a_particular_party_succeeds(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        resp = self.client.get('/parties/'+str(self.party_id), data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['data']['id'], self.party_id)
        self.assertEqual(resp.data['data']['name'], self.party_name)

    def test_get_a_particular_party_fails(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        resp = self.client.get('/parties/109', data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_a_particular_party_succeeds(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        resp = self.client.put('/parties/'+str(self.party_id), self.party_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['data']['name'], self.party_data['name'])

    def test_update_a_particular_party_with_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        resp = self.client.put('/parties/'+str(self.party_id), self.invalid_party_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_a_particular_party_with_invalid_party_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        resp = self.client.put('/parties/109', self.invalid_party_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_a_particular_party_succeeds(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        resp = self.client.delete('/parties/'+str(self.party_id), data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['data'][0]['message'], "party successfully deleted")