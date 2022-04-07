import json
from unittest import mock

from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class TestGetHorary(APITestCase):
    @mock.patch("schedule.utils.Verifications.is_holiday", return_value=True)
    def test_when_date_is_holiday_return_empty(self, is_holiday_mock):
        User.objects.create(
            email="ernesto.terra2003@gmail.com", username="Ernesto", password="12345"
        )  # noqa:E501
        response = self.client.get("/api/horary/2022-12-25/?username=Ernesto")
        data = json.loads(response.content)

        self.assertEqual(data, [])  # noqa:E501

    @mock.patch("schedule.utils.Verifications.is_holiday", return_value=False)
    def test_when_date_is_common(self, is_holiday_mock):
        User.objects.create(
            email="ernesto.terra2003@gmail.com", username="Ernesto", password="12345"
        )  # noqa:E501
        response = self.client.get("/api/horary/2022-04-28/?username=Ernesto")
        data = json.loads(response.content)

        self.assertNotEqual(data, [])
        self.assertEqual(data[0], {"date_time": "2022-04-28T09:00:00"})
        self.assertEqual(data[-1], {"date_time": "2022-04-28T17:30:00"})
