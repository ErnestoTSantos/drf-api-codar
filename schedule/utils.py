import logging
import os
from datetime import date, datetime

import requests
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()


class Verifications:
    @staticmethod
    def is_holiday(date: date):
        logging.info(
            f"Fazendo requisição para BrasilAPI com a data: {date.isoformat()}"
        )  # noqa:E501
        if settings.TESTING is True:
            logging.info(
                "Requisição não está sendo feita pois o TESTING = True"
            )  # noqa:E501
            if date.day == 25 and date.month == 12:
                return True
            return False

        api_request_os = os.environ.get(
            "URL_API_HOLIDAYS", "https://brasilapi.com.br/"
        )  # noqa:E501
        request_api = requests.get(
            api_request_os + f"api/feriados/v1/{date.year}"
        )  # noqa:E501

        if request_api.status_code != 200:
            logging.error("Algum erro aconteceu na BrasilAPI!")
            return False
            # raise ValueError('Infelizmente não foi possível consultar os feriados!')  # noqa:E501

        holidays = request_api.json()

        for holiday in holidays:
            date_holiday = holiday["date"]
            if datetime.strptime(date_holiday, "%Y-%m-%d").date() == date:
                return True

        return False

    @staticmethod
    def verify_cep(cep: str):
        logging.info(f"Fazendo requisição para BrasilAPI com o cep: {cep}")  # noqa:E501

        api_request_os = os.environ.get(
            "URL_API_HOLIDAYS", "https://brasilapi.com.br/"
        )  # noqa:E501
        resquest_api = requests.get(api_request_os + f"api/cep/v1/{cep}")

        if resquest_api.status_code != 200:
            logging.error("Algo aconteceu na BrasilAPI")
            return False

        informations = resquest_api.json()
        return informations
