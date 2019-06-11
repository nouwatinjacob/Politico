from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from rest_framework.test import APIRequestFactory

from rest_framework import status

from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your tests here.
class TestVote(APITestCase):
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


        self.candidate_url = reverse('register_candidate')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        candidate = self.client.post(self.candidate_url,{'office':self.office_id}, format='json')
        self.candidate_id = candidate.data['data']['id']

    def test_vote_with_valid_data_succeeds(self):
        self.vote_data = {
            'office': self.office_id,
            'candidate': self.candidate_id
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        resp = client.post('/votes/', self.vote_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_vote_with_invalid_data_fails(self):
        self.vote_data = {
            'candidate': self.candidate_id
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        resp = client.post('/votes/', self.vote_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_vote_if_user_already_vote_succeeds(self):
        self.vote_data = {
            'office': self.office_id,
            'candidate': self.candidate_id
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        resp = client.post('/votes/', self.vote_data, format='json')
        resp1 = client.post('/votes/', self.vote_data, format='json')
        self.assertEqual(resp1.data['status'], status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp1.data['error'], "You have voted this office, please vote another pollitical office")