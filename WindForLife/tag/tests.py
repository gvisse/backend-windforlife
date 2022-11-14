from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient, force_authenticate

from .models import Tag
from anemometer.models import Anemometer

class TestTag(APITestCase):
    url = reverse_lazy('tag:tag-list')

    client = APIClient()

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user('user-test', 'user@user.com', 'user-test')
        cls.tag = Tag.objects.create(name='europe')
        cls.tag_2 = Tag.objects.create(name='lake')
        cls.tag_3 = Tag.objects.create(name='north america')
        cls.tag_4 = Tag.objects.create(name='south-america')
        cls.tag_5 = Tag.objects.create(name='united states of america')
        cls.tag_6 = Tag.objects.create(name='africa')
        cls.tag_7 = Tag.objects.create(name='mountain')
        cls.tag_8 = Tag.objects.create(name='beach')
        cls.tag_9 = Tag.objects.create(name='forest')
        cls.tag_10 = Tag.objects.create(name='desert')
        cls.tag_11 = Tag.objects.create(name='france')
        cls.tag_12 = Tag.objects.create(name='asia')

        cls.tags_list_page2 = Tag.objects.filter(name__in=['france', 'asia'])
        cls.tags_list_page1 = Tag.objects.exclude(name__in=['france', 'asia'])

        cls.anemometer = Anemometer.objects.create(name='Anémomètre test', latitude=45.1000000, longitude=8.2000000, altitude=1)
        cls.anemometer.tags.set(cls.tags_list_page2)

    def get_tag_list_data(self, tags):
        return [{'id': tag.pk, 'name': tag.name} for tag in tags]

    def test_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_tag_list_data(self.tags_list_page1), response.json()['results'])

    def test_create(self):
        tag_count = Tag.objects.count()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data={'name': 'New tag'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tag.objects.count(), tag_count + 1 )

    def test_go_to_page2(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('http://testserver/api/tag/?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_tag_list_data(self.tags_list_page2), response.json()['results'])

    def test_update(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch('http://testserver/api/tag/%d/' % self.tag_3.pk, data={'name': 'north-america'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual({'id': self.tag_3.pk, 'name': 'north-america'}, response.json())

    def test_delete(self):
        self.assertEqual(self.anemometer.tags.count(), 2)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete('http://testserver/api/tag/%d/' % self.tag_12.pk)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Tag.objects.count(), 11)
        self.assertEqual(self.anemometer.tags.count(), 1)
