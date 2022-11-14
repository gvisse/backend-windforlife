from datetime import datetime, timedelta
from django.utils import timezone

from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient, force_authenticate

from .models import Wind
from anemometer.models import Anemometer
from tag.models import Tag


class TestWind(APITestCase):
    url = reverse_lazy('wind:wind-list')

    today_min = datetime.combine(timezone.now().date(), datetime.today().time().min)
    today_max = datetime.combine(timezone.now().date(), datetime.today().time().max)

    week_min = datetime.combine(timezone.now().date() - timedelta(weeks=1), (datetime.today()-timedelta(weeks=1)).time().min)

    client = APIClient()

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user('user-test', 'user@user.com', 'user-test')
        cls.tag1 = Tag.objects.create(name='france')
        cls.tag2 = Tag.objects.create(name='asia')

        cls.tags = Tag.objects.filter(name__in=['france', 'asia'])

        cls.anemometer = Anemometer.objects.create(name='Anémomètre test', latitude=45.1000000, longitude=8.2000000, altitude=1)
        cls.anemometer.tags.set(cls.tags)

        cls.anemometer_2 = Anemometer.objects.create(name='Anémomètre test 2', latitude=45.1000001, longitude=8.2000001, altitude=1)
        cls.anemometer_2.tags.set(Tag.objects.filter(name='france'))

        cls.wind_1_1 = Wind.objects.create(speed=11, time=datetime.now(timezone.utc) - timedelta(hours=2), anemometer=cls.anemometer)
        cls.wind_1_2 = Wind.objects.create(speed=12, time=datetime.now(timezone.utc) - timedelta(hours=1), anemometer=cls.anemometer)
        cls.wind_1_3 = Wind.objects.create(speed=13, time=datetime.now(timezone.utc), anemometer=cls.anemometer)
        cls.wind_2_1 = Wind.objects.create(speed=11, time=datetime.now(timezone.utc) - timedelta(hours=2), anemometer=cls.anemometer_2)
        cls.wind_2_2 = Wind.objects.create(speed=12, time=datetime.now(timezone.utc) - timedelta(hours=1), anemometer=cls.anemometer_2)
        cls.wind_2_3 = Wind.objects.create(speed=13, time=datetime.now(timezone.utc), anemometer=cls.anemometer_2)


    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def get_wind_list_data(self, winds):
        return [
                {
                    'anemometer' : wind.anemometer.pk,
                    'speed': wind.speed,
                    'time': self.format_datetime(wind.time)
                }
            for wind in winds]

    def test_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_wind_list_data(Wind.objects.all().order_by('id')), response.json()['results'])

    def test_create(self):
        wind_count = Wind.objects.count()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data={'speed': 15, 'time': datetime.now(timezone.utc), 'anemometer': self.anemometer.pk}, format='json')
        self.assertEqual(response.status_code, 201)
        response = self.client.post(self.url, data={'speed': 15, 'time': datetime.now(timezone.utc), 'anemometer': None}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Wind.objects.count(), wind_count + 1)

    def test_update(self):
        self.client.force_authenticate(user=self.user)
        data = {'speed' : 10.0}
        expected = {
            'speed' : 10.0,
            'time' : self.format_datetime(self.wind_1_1.time),
            'anemometer' : self.wind_1_1.anemometer.id
        }
        response = self.client.patch('http://testserver/api/wind/%d/' % self.wind_1_1.id, data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected, response.json())

    def test_delete(self):
        self.assertEqual(Wind.objects.count(), 6)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete('http://testserver/api/wind/%d/' % self.wind_1_1.id )
        self.assertEqual(response.status_code, 204)
        response = self.client.get('http://testserver/api/wind/%d/' % self.wind_1_1.id )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Wind.objects.count(), 5)

    def test_filter_on_anemometer(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('http://testserver/api/wind/', data={'anemometer_id': self.anemometer.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_wind_list_data([self.wind_1_1, self.wind_1_2, self.wind_1_3]), response.json()['results'])
