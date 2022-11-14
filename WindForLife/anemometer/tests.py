from datetime import datetime, timedelta

from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.db.models import Q, Avg
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient, force_authenticate

from .models import Anemometer
from tag.models import Tag
from wind.models import Wind

class TestAnemometer(APITestCase):

    url = reverse_lazy('anemometer:anemometer-list')

    today_min = datetime.combine(timezone.now().date(), datetime.today().time().min)
    today_max = datetime.combine(timezone.now().date(), datetime.today().time().max)

    week_min = datetime.combine(timezone.now().date() - timedelta(weeks=1), (datetime.today()-timedelta(weeks=1)).time().min)

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

        cls.anemometer_2 = Anemometer.objects.create(name='Anémomètre test 2', latitude=45.1000001, longitude=8.2000001, altitude=1)
        cls.anemometer_2.tags.set(Tag.objects.filter(name='france'))

        cls.anemometer_without_tag = Anemometer.objects.create(name='Anémomètre test 0 tag', latitude=43.1000560, longitude=8.2688590, altitude=1)

        cls.wind_1_1 = Wind.objects.create(speed=11, time=datetime.now(timezone.utc) - timedelta(hours=2), anemometer=cls.anemometer)
        cls.wind_1_2 = Wind.objects.create(speed=12, time=datetime.now(timezone.utc) - timedelta(hours=1), anemometer=cls.anemometer)
        cls.wind_1_3 = Wind.objects.create(speed=13, time=datetime.now(timezone.utc), anemometer=cls.anemometer)
        cls.wind_2_1 = Wind.objects.create(speed=11, time=datetime.now(timezone.utc) - timedelta(hours=2), anemometer=cls.anemometer_2)
        cls.wind_2_2 = Wind.objects.create(speed=12, time=datetime.now(timezone.utc) - timedelta(hours=1), anemometer=cls.anemometer_2)
        cls.wind_2_3 = Wind.objects.create(speed=13, time=datetime.now(timezone.utc), anemometer=cls.anemometer_2)

    def get_tag_list_data(self, tags):
        return [{'id': tag.pk, 'name': tag.name} for tag in tags]

    def get_anemometer_list_data(self, anemometers):
        mean_speed_today = Avg('winds__speed', filter=Q(winds__time__range=(self.today_min, self.today_max)))
        mean_speed_week = Avg('winds__speed', filter=Q(winds__time__range=(self.week_min, self.today_max)))
        anemometers = anemometers.annotate(mean_speed_today=mean_speed_today, mean_speed_week=mean_speed_week)
        return [
                {
                    'id': anemometer.pk,
                    'name': anemometer.name,
                    'latitude': format(anemometer.latitude, '.7f'),
                    'longitude': format(anemometer.longitude, '.7f'),
                    'altitude': anemometer.altitude,
                    'mean_speed_today': anemometer.mean_speed_today,
                    'mean_speed_week': anemometer.mean_speed_week,
                    'tags': self.get_tag_list_data(anemometer.tags.all())
                }
            
            for anemometer in anemometers]

    def test_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_anemometer_list_data(Anemometer.objects.all().order_by('id')), response.json()['results'])

    def test_create(self):
        self.client.force_authenticate(user=self.user)
        anemo_count = Anemometer.objects.count()
        response = self.client.post(self.url, data={'name': 'Anémomètre test create', 'latitude': 18.1745, 'longitude': 52.4769, 'altitude': 5, 'tags': []}, format='json')
        # check status code of the creation without tags
        self.assertEqual(response.status_code, 201)
        response = self.client.post(self.url, data={'name': 'Anémomètre test create 2', 'latitude': 18.1785, 'longitude': 52.4769, 'altitude': 5, 'tags': [{'name': 'tag test'}, {'name': self.tag_2.name}]}, format='json')
        self.assertEqual(response.status_code, 201)
        # check status code of the creation with tags (existing or not)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tag.objects.count(), 13)
        self.assertEqual(Anemometer.objects.count(), anemo_count + 2 )

    def test_update(self):
        self.client.force_authenticate(user=self.user)
        expected = {
            'id': self.anemometer_without_tag.pk,
            'name': 'Test Update Anemometre',
            'latitude': format(self.anemometer_without_tag.latitude, '.7f'),
            'longitude': format(self.anemometer_without_tag.longitude, '.7f'),
            'altitude': self.anemometer_without_tag.altitude,
            'mean_speed_today': None,
            'mean_speed_week': None,
            'tags': [
                {'id':self.tag_11.pk, 'name': self.tag_11.name},
                {'id': 14 , 'name': 'tag test created on update'}
            ]
        }
        data = {
            'name': 'Test Update Anemometre',
            'tags': [
                {'name': self.tag_11.name},
                {'name': 'tag test created on update'}
            ]
        }
        response = self.client.patch('http://testserver/api/anemometer/%d/' % self.anemometer_without_tag.pk, data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected, response.json())

    def test_go_to_page2(self):
        tags = Tag.objects.all().values_list('name')
        for i in range(len(tags)-3):
            anemometer = Anemometer.objects.create(name=tags[i], latitude=i, longitude=i, altitude=1)
            anemometer.tags.set(Tag.objects.filter(name=tags[i]))
            anemometer.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.get('http://testserver/api/anemometer/?page=2')
        self.assertEqual(response.status_code, 200)
        anemometers = Anemometer.objects.filter(id__in=[anemometer.pk -1, anemometer.pk])
        self.assertEqual(self.get_anemometer_list_data(anemometers), response.json()['results'])

    def test_delete(self):
        self.assertEqual(self.anemometer.winds.count(), 3)
        self.assertEqual(Wind.objects.count(), 6)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete('http://testserver/api/anemometer/%d/' % self.anemometer.pk)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Tag.objects.count(), 12)
        self.assertEqual(Anemometer.objects.count(), 2)
        self.assertEqual(Wind.objects.count(), 3)

    def test_filter_with_tags(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('http://testserver/api/anemometer/', data={'tags': 'france'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_anemometer_list_data(Anemometer.objects.filter(id__in=[self.anemometer.id, self.anemometer_2.id])), response.json()['results'])
        response = self.client.get('http://testserver/api/anemometer/', data={'tags': 'asia'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_anemometer_list_data(Anemometer.objects.filter(id__in=[self.anemometer.id])), response.json()['results'])