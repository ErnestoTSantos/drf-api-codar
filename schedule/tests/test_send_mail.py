from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from schedule.models import Scheduling
from schedule.tasks import generate_file, write_file


class EmailTest(TestCase):
    def test_send_email(self):
        user = User.objects.create(
            email="ernesto.terra2003@gmail.com", username="Ernesto", password="12345"
        )
        Scheduling.objects.create(
            provider=user,
            date_time="2022-04-28T17:30:00Z",
            client_name="Ernesto Santos",
            client_email="ernesto.terra2003@gmail.com",
            client_phone="(51) 98936-5022",
        )
