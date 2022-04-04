import json

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from schedule.models import Establishment


class TestSerializerScheduling(APITestCase):
    def test_validate_provider_return_error(self):
        Establishment.objects.create(name='Ruby barber shop')
        scheduling_request_data = {
            'provider': 'Ernesto',
            'date_time': '2022-04-28T14:30:00Z',
            'client_name': 'Ernesto Santos',
            'client_email': 'ernesto.terra2003@gmail.com',
            'client_phone': '(51) 98936-5022'
        }
        response = self.client.post('/api/scheduling/?establishment=Ruby barber shop', scheduling_request_data)  # noqa:E501
        data = json.loads(response.content)

        assert response.status_code == 400
        assert data == {'provider': ['Username não existe!']}

    def test_validate_date_time_when_day_is_sunday(self):
        User.objects.create(email='ernesto.terra2003@gmail.com', username='Ernesto', password='12345')  # noqa:E501
        Establishment.objects.create(name='Ruby barber shop')
        scheduling_request_data = {
            'provider': 'Ernesto',
            'date_time': '2022-12-18T14:30:00Z',
            'client_name': 'Ernesto Santos',
            'client_email': 'ernesto.terra2003@gmail.com',
            'client_phone': '(51) 98936-5022'
        }
        response = self.client.post('/api/scheduling/?establishment=Ruby barber shop', scheduling_request_data)  # noqa:E501
        data = json.loads(response.content)

        assert response.status_code == 400
        assert data == {'date_time': ['Infelizmente o estabelecimento não trabalha aos domingos!']}  # noqa:E501

    def test_validate_date_time_when_day_is_saturday(self):
        User.objects.create(email='ernesto.terra2003@gmail.com', username='Ernesto', password='12345')  # noqa:E501
        Establishment.objects.create(name='Ruby barber shop')
        scheduling_request_data = {
            'provider': 'Ernesto',
            'date_time': '2022-11-19T14:30:00Z',
            'client_name': 'Ernesto Santos',
            'client_email': 'ernesto.terra2003@gmail.com',
            'client_phone': '(51) 98936-5022'
        }
        response = self.client.post('/api/scheduling/?establishment=Ruby barber shop', scheduling_request_data)  # noqa:E501
        data = json.loads(response.content)

        assert response.status_code == 400
        assert data == {'date_time': ['Infelizmente o estabelecimento só trabalha até as 13h no sábado!']}  # noqa:E501

    def test_validate_date_time_when_is_lunch_time(self):
        User.objects.create(email='ernesto.terra2003@gmail.com', username='Ernesto', password='12345')  # noqa:E501
        Establishment.objects.create(name='Ruby barber shop')
        scheduling_request_data = {
            'provider': 'Ernesto',
            'date_time': '2022-11-17T12:30:00Z',
            'client_name': 'Ernesto Santos',
            'client_email': 'ernesto.terra2003@gmail.com',
            'client_phone': '(51) 98936-5022'
        }
        response = self.client.post('/api/scheduling/?establishment=Ruby barber shop', scheduling_request_data)  # noqa:E501
        data = json.loads(response.content)

        assert response.status_code == 400
        assert data == {'date_time': ['Os funcionários estão no horário de almoço!']}  # noqa:E501

    def test_validate_date_time_when_time_is_earlier_than_opening_time(self):
        User.objects.create(email='ernesto.terra2003@gmail.com', username='Ernesto', password='12345')  # noqa:E501
        Establishment.objects.create(name='Ruby barber shop')
        scheduling_request_data = {
            'provider': 'Ernesto',
            'date_time': '2022-10-10T8:30:00Z',
            'client_name': 'Ernesto Santos',
            'client_email': 'ernesto.terra2003@gmail.com',
            'client_phone': '(51) 98936-5022'
        }
        response = self.client.post('/api/scheduling/?establishment=Ruby barber shop', scheduling_request_data)  # noqa:E501
        data = json.loads(response.content)

        assert response.status_code == 400
        assert data == {'date_time': ['O estabelecimento abre apenas às 9h!']}  # noqa:E501

    def test_validate_date_time_when_time_is_more_latest_than_closing_time(self):  # noqa:E501
        User.objects.create(email='ernesto.terra2003@gmail.com', username='Ernesto', password='12345')  # noqa:E501
        Establishment.objects.create(name='Ruby barber shop')
        scheduling_request_data = {
            'provider': 'Ernesto',
            'date_time': '2022-11-25T18:00:00Z',
            'client_name': 'Ernesto Santos',
            'client_email': 'ernesto.terra2003@gmail.com',
            'client_phone': '(51) 98936-5022'
        }
        response = self.client.post('/api/scheduling/?establishment=Ruby barber shop', scheduling_request_data)  # noqa:E501
        data = json.loads(response.content)

        assert response.status_code == 400
        assert data == {'date_time': ['O estabelecimento fehca às 18h!']}  # noqa:E501

    def test_validate_client_name_characters(self):
        User.objects.create(email='ernesto.terra2003@gmail.com', username='Ernesto', password='12345')  # noqa:E501
        Establishment.objects.create(name='Ruby barber shop')
        scheduling_request_data = {
            'provider': 'Ernesto',
            'date_time': '2022-10-11T17:00:00Z',
            'client_name': 'Ana',
            'client_email': 'ernesto.terra2003@gmail.com',
            'client_phone': '(51) 98936-5022'
        }
        response = self.client.post('/api/scheduling/?establishment=Ruby barber shop', scheduling_request_data)  # noqa:E501
        data = json.loads(response.content)

        assert response.status_code == 400
        assert data == {'client_name': ['O nome do cliente precisa ter 7 ou mais caracteres!']}  # noqa:E501

    def test_validate_client_name_space_for_last_name(self):
        User.objects.create(email='ernesto.terra2003@gmail.com', username='Ernesto', password='12345')  # noqa:E501
        Establishment.objects.create(name='Ruby barber shop')
        scheduling_request_data = {
            'provider': 'Ernesto',
            'date_time': '2022-10-11T17:00:00Z',
            'client_name': 'Ernesto',
            'client_email': 'ernesto.terra2003@gmail.com',
            'client_phone': '(51) 98936-5022'
        }
        response = self.client.post('/api/scheduling/?establishment=Ruby barber shop', scheduling_request_data)  # noqa:E501
        data = json.loads(response.content)

        assert response.status_code == 400
        assert data == {'client_name': ['O cliente precisa ter um sobrenome!']}  # noqa:E501

    def test_validate_client_phone_characters(self):
        User.objects.create(email='ernesto.terra2003@gmail.com', username='Ernesto', password='12345')  # noqa:E501
        Establishment.objects.create(name='Ruby barber shop')
        scheduling_request_data = {
            'provider': 'Ernesto',
            'date_time': '2022-10-10T17:00:00Z',
            'client_name': 'Ernesto Santos',
            'client_email': 'ernesto.terra2003@gmail.com',
            'client_phone': '(51) 98936'
        }
        response = self.client.post('/api/scheduling/?establishment=Ruby barber shop', scheduling_request_data)  # noqa:E501
        data = json.loads(response.content)

        assert response.status_code == 400
        assert data == {'client_phone': ['O número de telefone precisa ter no mínimo 8 digitos!']}  # noqa:E501

    def test_validate_client_phone_valid_characters(self):
        User.objects.create(email='ernesto.terra2003@gmail.com', username='Ernesto', password='12345')  # noqa:E501
        Establishment.objects.create(name='Ruby barber shop')
        scheduling_request_data = {
            'provider': 'Ernesto',
            'date_time': '2022-10-10T17:00:00Z',
            'client_name': 'Ernesto Santos',
            'client_email': 'ernesto.terra2003@gmail.com',
            'client_phone': '(51) 98936-5022*'
        }
        response = self.client.post('/api/scheduling/?establishment=Ruby barber shop', scheduling_request_data)  # noqa:E501
        data = json.loads(response.content)

        assert response.status_code == 400
        assert data == {'client_phone': ['O número pode ter apenas valores entre 0-9, parenteses, traços, espaço e o sinal de mais!']}  # noqa:E501

    def test_validate_date_time_horary_is_invalid(self):
        user = User.objects.create(email='ernesto.terra2003@gmail.com', username='Ernesto', password='12345')  # noqa:E501
        Establishment.objects.create(name='Ruby barber shop')
        scheduling_request_data = {
            'provider': 'Ernesto',
            'date_time': '2022-10-11T17:00:00Z',
            'client_name': 'Ernesto Santos',
            'client_email': 'ernesto.terra2003@gmail.com',
            'client_phone': '(51) 98936-5022'
        }
        self.client.post('/api/scheduling/?establishment=Ruby barber shop', scheduling_request_data)  # noqa:E501
        self.client.force_authenticate(user)
        patch = self.client.patch('/api/scheduling/1/?confirmed=true')

        scheduling_request = {
            'provider': 'Ernesto',
            'date_time': '2022-10-11T17:00:00Z',
            'client_name': 'Ernesto Santos',
            'client_email': 'ernesto.terra2003@gmail.com',
            'client_phone': '(51) 98936-5022'
        }
        post_response = self.client.post('/api/scheduling/?establishment=Ruby barber shop', scheduling_request)  # noqa:E501
        data = json.loads(post_response.content)

        assert patch.status_code == 200
        assert data == {'date_time': ['Infelizmente o horário selecionado está indisponível!']}  # noqa:E501
