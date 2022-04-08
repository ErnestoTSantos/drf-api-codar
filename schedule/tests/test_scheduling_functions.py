import json
from datetime import datetime, timezone

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from schedule.models import Establishment, Scheduling


class TestListingScheduling(APITestCase):
    def test_listing_empty(self):
        user = User.objects.create(
            email="ernesto.terra2003@gmail.com", username="Ernesto", password="12345"
        )  # noqa:E501
        self.client.force_authenticate(user)
        response = self.client.get("/api/scheduling/?username=Ernesto")
        data = json.loads(response.content)
        self.assertEqual(data, [])

    def test_listing_schedulings(self):
        user = User.objects.create(
            email="ernesto.terra2003@gmail.com", username="Ernesto", password="12345"
        )  # noqa:E501
        Scheduling.objects.create(
            provider=user,
            date_time="2022-04-28T17:30:00Z",
            client_name="Ernesto Santos",
            client_email="ernesto.terra2003@gmail.com",
            client_phone="(51) 98936-5022",
        )  # noqa:E501
        self.client.force_authenticate(user)
        response = self.client.get("/api/scheduling/?username=Ernesto")
        data = json.loads(response.content)
        scheduling_serialized = {
            "id": 1,
            "provider": "Ernesto",
            "date_time": "2022-04-28T17:30:00Z",
            "client_name": "Ernesto Santos",
            "client_email": "ernesto.terra2003@gmail.com",
            "client_phone": "(51) 98936-5022",
            "confirmed": False,
            "states": "NCNF",
        }
        self.assertEqual(data[0], scheduling_serialized)


class TestCreateScheduling(APITestCase):
    def test_create_scheduling(self):
        user = User.objects.create(
            email="ernesto.terra2003@gmail.com", username="Ernesto", password="12345"
        )  # noqa:E501
        Establishment.objects.create(name="Ruby barber shop")
        scheduling_request_data = {
            "provider": "Ernesto",
            "date_time": "2022-04-28T14:30:00-00:00",
            "client_name": "Ernesto Santos",
            "client_email": "ernesto.terra2003@gmail.com",
            "client_phone": "(51) 98936-5022",
        }
        self.client.force_authenticate(user)
        response = self.client.post(
            "/api/scheduling/?establishment=Ruby barber shop", scheduling_request_data
        )  # noqa:E501
        scheduling_create = Scheduling.objects.get()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(scheduling_create.provider, user)
        self.assertEqual(
            scheduling_create.date_time,
            datetime(2022, 4, 28, 14, 30, tzinfo=timezone.utc),
        )  # noqa:E501
        self.assertEqual(scheduling_create.client_name, "Ernesto Santos")  # noqa:E501
        self.assertEqual(
            scheduling_create.client_email, "ernesto.terra2003@gmail.com"
        )  # noqa:E501
        self.assertEqual(scheduling_create.client_phone, "(51) 98936-5022")  # noqa:E501

    def test_create_scheduling_in_past(self):
        User.objects.create(
            email="ernesto.terra2003@gmail.com", username="Ernesto", password="12345"
        )  # noqa:E501
        Establishment.objects.create(name="Ruby barber shop")
        scheduling_request_data = {
            "provider": "Ernesto",
            "date_time": "2020-04-28T14:30:00-00:00",
            "client_name": "Ernesto Santos",
            "client_email": "ernesto.terra2003@gmail.com",
            "client_phone": "(51) 98936-5022",
        }
        response = self.client.post(
            "/api/scheduling/?establishment=Ruby barber shop", scheduling_request_data
        )  # noqa:E501

        self.assertEqual(response.status_code, 400)

    def test_create_scheduling_with_get(self):
        user = User.objects.create(
            email="ernesto.terra2003@gmail.com", username="Ernesto", password="12345"
        )  # noqa:E501
        Establishment.objects.create(name="Ruby barber shop")
        scheduling_request_data = {
            "provider": "Ernesto",
            "date_time": "2022-04-28T14:30:00Z",
            "client_name": "Ernesto Santos",
            "client_email": "ernesto.terra2003@gmail.com",
            "client_phone": "(51) 98936-5022",
        }
        url = "/api/scheduling/?establishment=Ruby barber shop"
        self.client.force_authenticate(user)
        response = self.client.post(url, scheduling_request_data)  # noqa:E501
        response_get = self.client.get("/api/scheduling/?username=Ernesto")
        data = json.loads(response_get.content)
        scheduling_element = data[0]

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            scheduling_element["date_time"], scheduling_request_data["date_time"]
        )  # noqa:E501
        self.assertEqual(
            scheduling_element["client_name"], scheduling_request_data["client_name"]
        )  # noqa:E501
        self.assertEqual(
            scheduling_element["client_email"], scheduling_request_data["client_email"]
        )  # noqa:E501
        self.assertEqual(
            scheduling_element["client_phone"], scheduling_request_data["client_phone"]
        )  # noqa:E501

    def test_return_400_when_invalid(self):
        user = User.objects.create(
            email="ernesto.terra2003@gmail.com", username="Ernesto", password="12345"
        )  # noqa:E501
        Establishment.objects.create(name="Ruby barber shop")
        scheduling_request_data = {
            "provider": "Ernesto",
            "date_time": "2022-04-28T17:30:00Z",
            "client_name": "Ernesto Santos",
            "client_email": "ernesto.terra2003",
            "client_phone": "(51) 98936-5022",
        }
        self.client.force_authenticate(user)
        response = self.client.post(
            "/api/scheduling/?establishment=Ruby barber shop", scheduling_request_data
        )  # noqa:E501

        self.assertEqual(response.status_code, 400)


class TestDetailScheduling(APITestCase):
    def test_get_object(self):
        user = User.objects.create(
            email="ernesto.terra2003@gmail.com", username="Ernesto", password="12345"
        )  # noqa:E501
        Establishment.objects.create(name="Ruby barber shop")
        scheduling_request_data = {
            "provider": "Ernesto",
            "date_time": "2022-04-28T14:30:00Z",
            "client_name": "Ernesto Santos",
            "client_email": "ernesto.terra2003@gmail.com",
            "client_phone": "(51) 98936-5022",
        }
        response = self.client.post(
            "/api/scheduling/?establishment=Ruby barber shop", scheduling_request_data
        )  # noqa:E501
        self.client.force_authenticate(user)
        url = "/api/scheduling/1/?username=Ernesto"
        response_get = self.client.get(url)
        data = json.loads(response_get.content)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            data["date_time"], scheduling_request_data["date_time"]
        )  # noqa:E501
        self.assertEqual(
            data["client_name"], scheduling_request_data["client_name"]
        )  # noqa:E501
        self.assertEqual(
            data["client_email"], scheduling_request_data["client_email"]
        )  # noqa:E501
        self.assertEqual(
            data["client_phone"], scheduling_request_data["client_phone"]
        )  # noqa:E501

    def test_patch_object(self):
        user = User.objects.create(
            email="ernesto.terra2003@gmail.com", username="Ernesto", password="12345"
        )  # noqa:E501
        Establishment.objects.create(name="Ruby barber shop")
        scheduling_request_data = {
            "provider": "Ernesto",
            "date_time": "2022-04-28T14:30:00Z",
            "client_name": "Ernesto Santos",
            "client_email": "ernesto.terra2003@gmail.com",
            "client_phone": "(51) 98936-5022",
        }
        self.client.post(
            "/api/scheduling/?establishment=Ruby barber shop", scheduling_request_data
        )  # noqa:E501]
        url = "/api/scheduling/1/"
        self.client.force_authenticate(user)
        response_patch = self.client.patch(
            url, {"client_name": "Ernesto Terra dos Santos"}
        )  # noqa:E501
        response_get = self.client.get(url + "?username=Ernesto")
        data = json.loads(response_get.content)

        self.assertEqual(response_patch.status_code, 200)
        self.assertEqual(data["client_name"], "Ernesto Terra dos Santos")

    def test_delete_object(self):
        user = User.objects.create(
            email="ernesto.terra2003@gmail.com", username="Ernesto", password="12345"
        )  # noqa:E501
        Establishment.objects.create(name="Ruby barber shop")
        scheduling_request_data = {
            "provider": "Ernesto",
            "date_time": "2022-04-28T14:30:00Z",
            "client_name": "Ernesto Santos",
            "client_email": "ernesto.terra2003@gmail.com",
            "client_phone": "(51) 98936-5022",
        }
        self.client.post(
            "/api/scheduling/?establishment=Ruby barber shop", scheduling_request_data
        )  # noqa:E501
        self.client.force_authenticate(user)
        url = "/api/scheduling/1/"
        response_delete = self.client.delete(url)

        self.assertEqual(response_delete.status_code, 204)
