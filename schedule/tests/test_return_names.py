from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from schedule.models import Address, Employee, Establishment, Faithfulness, Scheduling


class TestingReturnedName(APITestCase):
    def test_returned_name_in_scheduling(self):
        user = User.objects.create(
            email="ernesto.terra2003@gmail.com", username="Ernesto", password="12345"
        )  # noqa:E501
        scheduling = Scheduling.objects.create(
            provider=user,
            date_time="2022-04-28T15:00Z",
            client_name="Matheus Silva",
            client_phone="(51) 93920-0394",
        )  # noqa:E501

        assert str(scheduling) == "Matheus Silva"

    def test_returned_name_in_faithfulness(self):
        user = User.objects.create(
            email="ernesto.terra2003@gmail.com", username="Ernesto", password="12345"
        )  # noqa:E501
        faithfulness = Faithfulness.objects.create(
            provider=user, client="Matheus Silva"
        )

        assert str(faithfulness) == "Matheus Silva = 0"

    def test_returned_name_in_establishment(self):
        establishment = Establishment.objects.create(name="Python Barber shop")

        assert str(establishment) == "Python Barber shop"

    def test_returned_name_in_employee(self):
        user = User.objects.create(
            email="ernesto.terra2003@gmail.com", username="Ernesto", password="12345"
        )  # noqa:E501
        establishment = Establishment.objects.create(name="Python Barber shop")
        employee = Employee.objects.create(
            provider=user, establishment=establishment, assignment="Cortar cabelo"
        )  # noqa:E501

        assert str(employee) == "Ernesto -> Python Barber shop"

    def test_returned_name_in_address(self):
        establishment = Establishment.objects.create(name="Python Barber shop")
        address = Address.objects.create(
            establishment=establishment,
            cep="88901-104",
            city="Araranguá",
            district="Cidade Alta",
            street="Alameda Antônio Alves da Silva",
        )  # noqa:E501

        assert (
            str(address) == "Python Barber shop -> Alameda Antônio Alves da Silva"
        )  # noqa:E501
