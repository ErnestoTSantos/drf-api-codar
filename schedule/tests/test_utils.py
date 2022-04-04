from datetime import date
from unittest import TestCase

from schedule.utils import Verifications


class TestVerification(TestCase):
    def test_is_holiday_return_false(self):
        date_verification = date(2022, 12, 20)
        holiday_verification = Verifications.is_holiday(date_verification)

        assert holiday_verification is False

    def test_is_holiday_return_true(self):
        date_verification = date(2022, 12, 25)
        holiday_verification = Verifications.is_holiday(date_verification)

        assert holiday_verification is True

    def test_verify_cep_return_false(self):
        cep_verification = '27998-981'
        verify_cep = Verifications.verify_cep(cep_verification)

        assert verify_cep is False

    def test_verify_cep_return_informations(self):
        cep_verification = '27998-971'
        verify_cep = Verifications.verify_cep(cep_verification)

        dict_returned = {
            'cep': '27998971',
            'state': 'RJ',
            'city': 'Carapebus',
            'neighborhood': 'Centro',
            'street': 'Rua Getúlio Vargas, 480',
            'service': 'correios'
        }

        assert verify_cep == dict_returned
