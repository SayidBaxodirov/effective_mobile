from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from .models import Ads, ExchangeProposal
from .serializers import ProposalSerializer, AdSerializer
from django.urls import reverse

User = get_user_model()


class AdsTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass', first_name='user1',
                                              last_name='user1')
        self.user2 = User.objects.create_user(username='user2', password='testpass', first_name='user2',
                                              last_name='user2')

        self.ad1 = Ads.objects.create(title='user1 Ad 1', description="some description1", category="Category1",
                                      condition="good", user=self.user1)
        self.ad2 = Ads.objects.create(title='user1 Ad 2', description="another description2", category="Category2",
                                      condition="bad", user=self.user1)
        self.ad3 = Ads.objects.create(title='user2 awesome Ad 1', description="another description1",
                                      category="Category2",
                                      condition="norm", user=self.user2)
        self.ad4 = Ads.objects.create(title='user2 Ad 2', description="some description2", category="Category3",
                                      condition="good", user=self.user2)

        self.client.login(username='user1', password='testpass')

    def test_create_ad(self):
        url = '/api/ads/'
        data = {'title': 'user1 Ad 1', 'description': 'some ads description',
                'image_url': "http://image.com/123", 'category': 'Category1',
                'condition': 'good'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'user1 Ad 1')
        self.assertEqual(response.data['description'], 'some ads description')
        self.assertEqual(response.data['image_url'], 'http://image.com/123')
        self.assertEqual(response.data['category'], 'Category1')
        self.assertEqual(response.data['condition'], 'good')
        self.assertEqual(response.data['user'], 1)

    def test_update_ad(self):
        # self.client.login(username='user2', password='testpass')
        url = f'/api/ads/{self.ad1.id}/'
        data = {'condition': 'good', 'category': 'Category3'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ad1.refresh_from_db()
        self.assertEqual(self.ad1.condition, 'good')
        self.assertEqual(self.ad1.category, 'Category3')

    def test_update_forbidden(self):
        self.client.login(username='user2', password='testpass')
        url = f'/api/ads/{self.ad1.id}/'
        data = {'condition': 'bad'}
        response = self.client.patch(url, data, format='json')
        # second user cannot update 1st user's ad
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.ad1.refresh_from_db()
        self.assertEqual(self.ad1.condition, 'good')  # update shouldn't happen

    def test_delete_ad(self):
        self.client.login(username='user2', password='testpass')
        url = f'/api/ads/{self.ad3.id}/'
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_not_found(self):
        self.client.login(username='user2', password='testpass')
        url = f'/api/ads/10/'
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_search(self):
        url = f'/api/ads/?search=another'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        results = response.json().get('results', [])
        contains_word = any('another' in item['description'].lower() for item in results)
        self.assertTrue(contains_word, msg="At least one description should have word 'another'")

    def test_filter_category(self):
        # check filter by category
        url = f'/api/ads/?category=Category2'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        expected_data = AdSerializer([self.ad3, self.ad2], many=True).data
        response_data = response.json()['results']
        self.assertEqual(response_data, expected_data)

    def test_filter_condition(self):
        # check filter by condition
        url = '/api/ads/?condition=good'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        expected_data = AdSerializer([self.ad4, self.ad1], many=True).data
        response_data = response.json()['results']
        self.assertEqual(response_data, expected_data)


class ProposalTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass', first_name='user1',
                                              last_name='user1')
        self.user2 = User.objects.create_user(username='user2', password='testpass', first_name='user2',
                                              last_name='user2')

        self.ad1 = Ads.objects.create(title='User1 Ad 1', description="some description1", category="Category1",
                                      condition="good", user=self.user1)
        self.ad2 = Ads.objects.create(title='User2 Ad 1', description="some description2", category="Category1",
                                      condition="bad", user=self.user2)
        self.ad3 = Ads.objects.create(title='User1 Ad 2', description="some description1", category="Category2",
                                      condition="good", user=self.user1)
        self.ad4 = Ads.objects.create(title='User2 Ad 2', description="some description2", category="Category2",
                                      condition="normal", user=self.user2)
        # needed to check if the objects were created with all required
        # fields, needed for SQLite database, for PostgreSQL it is automatic and not needed
        # self.ad1.full_clean()
        # self.ad1.save()
        # self.ad2.full_clean()
        # self.ad2.save()
        self.client.login(username='user1', password='testpass')

    def test_create_proposal(self):
        url = '/api/proposals/'
        data = {
            "ad_sender": self.ad1.id,
            "ad_receiver": self.ad2.id,
            "comment": "I want to exchange this."
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExchangeProposal.objects.count(), 1)
        self.assertEqual(ExchangeProposal.objects.first().comment, "I want to exchange this.")

    def test_update_proposal_status_only(self):
        proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment="Initial proposal"
        )

        url = f"/api/proposals/{proposal.id}/"
        patch_data = {
            "status": "accept",
        }
        response = self.client.patch(url, patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        proposal.refresh_from_db()
        self.assertEqual(proposal.status, "accept")

    def test_invalid_comment(self):
        url = '/api/proposals/'
        data = {
            "ad_sender": self.ad1.id,
            "ad_receiver": self.ad2.id,
            "comment": "bad"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("comment", response.data)

    def test_proposal_filter(self):
        proposal1 = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment="Proposal 1-2"
        )
        proposal2 = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad3,
            comment="Proposal 1-3"
        )
        proposal3 = ExchangeProposal.objects.create(
            ad_sender=self.ad2,
            ad_receiver=self.ad3,
            comment="Proposal 2-3",
            status="accept"
        )
        proposal4 = ExchangeProposal.objects.create(
            ad_sender=self.ad3,
            ad_receiver=self.ad4,
            comment="Proposal 3-4",
            status='accept'
        )
        # test ad sender filtering
        url = '/api/proposals/?ad_sender=1'
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 2)
        expected_data = ProposalSerializer([proposal2, proposal1], many=True).data
        response_data = response.json()['results']
        self.assertEqual(response_data, expected_data)
        # test ad receiver filtering
        url = '/api/proposals/?ad_receiver=3'
        response2 = self.client.get(url, format='json')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.json()['count'], 2)
        expected_data2 = ProposalSerializer([proposal3, proposal2], many=True).data
        response_data2 = response2.json()['results']
        self.assertEqual(response_data2, expected_data2)
        # test status filtering
        url = '/api/proposals/?status=accept'
        response3 = self.client.get(url, format='json')
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.json()['count'], 2)
        expected_data3 = ProposalSerializer([proposal4, proposal3], many=True).data
        response_data3 = response3.json()['results']
        self.assertEqual(response_data3, expected_data3)

    def test_proposal_delete(self):
        proposal = ExchangeProposal.objects.create(ad_sender=self.ad3,
                                                   ad_receiver=self.ad4,
                                                   comment="Proposal 3-4",
                                                   status='reject')
        url = f'/api/proposals/{proposal.id}/'
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
