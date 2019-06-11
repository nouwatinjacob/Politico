from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from rest_framework.test import APIRequestFactory

from rest_framework import status

from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your tests here.
class TestOffice(APITestCase):

    def setUp(self):

        url = reverse('user_login')
        User = get_user_model()
        u = User.objects.create_user(first_name='user', last_name='user1', email='user@foo.com', password='pass')
        self.assertEqual(u.is_active, 1, 'Active User')
        u.save()

        resp = self.client.post(url, {'email':'user@foo.com', 'password':'pass'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.token = resp.data['data']['token']

        self.office_url = reverse('office_create')
        self.office_data_one = {
                'name':'Governor',
                'type':'State'
            }
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        request = self.client.post(self.office_url, self.office_data_one, format='json')
        self.office_id = request.data['data']['id']
        self.office_name = request.data['data']['name']
        
        self.office_data = {
            'name':'President', 
            'type':'Federal'
        }

        self.invalid_office_data = {
            'name':'President'
        }
    
    
    
    def test_create_office_with_valid_data_succeeds(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        resp = client.post(self.office_url, self.office_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_create_office_with_invalid_data_succeeds(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        resp = client.post(self.office_url, self.invalid_office_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_parties_succeeds(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        resp = client.get(self.office_url, data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['status'], 200)
        self.assertEqual(len(resp.data['data']), 1)

    def test_get_a_particular_office_succeeds(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        resp = self.client.get('/offices/'+str(self.office_id), data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['data']['id'], self.office_id)
        self.assertEqual(resp.data['data']['name'], self.office_name)

    def test_get_a_particular_office_fails(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        resp = self.client.get('/offices/109', data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_a_particular_office_succeeds(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        resp = self.client.patch('/offices/'+str(self.office_id), self.office_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['data']['name'], self.office_data['name'])

    def test_update_a_particular_office_with_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        resp = self.client.patch('/offices/'+str(self.office_id), self.invalid_office_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_a_particular_office_with_invalid_party_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        resp = self.client.patch('/offices/109', self.invalid_office_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_a_particular_party_succeeds(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        resp = self.client.delete('/offices/'+str(self.office_id), data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['data'][0]['message'], "office successfully deleted")

    def test_register_candidate_succeds(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        resp = self.client.post('/office/register',{'office':self.office_id}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_register_candidate_with_invalid_data_fails(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        resp = self.client.post('/office/register',{'office':'here'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_candidate_when_the_office_as_been_applied_for_by_same_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        resp = self.client.post('/office/register',{'office':self.office_id}, format='json')
        resp1 = self.client.post('/office/register',{'office':self.office_id}, format='json')
        self.assertEqual(resp1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp1.data['error'], "You have either applied for this office or another office")