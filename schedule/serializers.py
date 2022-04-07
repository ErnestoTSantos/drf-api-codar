import logging
import re
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers

from schedule.models import Address, Employee, Establishment, Scheduling
from schedule.utils import Verifications


class SchedulingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheduling
        fields = [
            "id",
            "provider",
            "date_time",
            "client_name",
            "client_email",
            "client_phone",
            "confirmed",
            "states",
        ]

    provider = serializers.CharField()

    def get_hour(self, value, hour, minutes):
        date = datetime(value.year, value.month, value.day, hour, minutes)
        return date.strftime("%H:%M")

    def validate_provider(self, value):
        try:
            provider_obj = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Username não existe!")

        # Podemos retornar apenas o objeto,
        # pois o django por baixo dos panos sabe resolver qual será o objeto.
        return provider_obj

    def validate_date_time(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                "O agendamento não pode ser realizado no passado!"
            )

        if value and datetime.date(value).weekday() == 6:
            raise serializers.ValidationError(
                "Infelizmente o estabelecimento não trabalha aos domingos!"
            )

        if value:
            time = datetime.strftime(value, "%H:%M")

            lunch_time = self.get_hour(value, 12, 0)

            return_interval = self.get_hour(value, 13, 0)

            open_time = self.get_hour(value, 9, 0)

            closing_time = self.get_hour(value, 18, 0)

            if datetime.date(value).weekday() == 5 and time >= return_interval:
                raise serializers.ValidationError(
                    "Infelizmente o estabelecimento só trabalha até as 13h no sábado!"
                )
            elif (
                return_interval > time >= lunch_time
                and datetime.date(value).weekday() != 5
            ):
                raise serializers.ValidationError(
                    "Os funcionários estão no horário de almoço!"
                )
            elif open_time > time:
                raise serializers.ValidationError(
                    "O estabelecimento abre apenas às 9h!"
                )
            elif closing_time <= time:
                raise serializers.ValidationError("O estabelecimento fehca às 18h!")

        qs = Scheduling.objects.filter(canceled=False, confirmed=True)

        delta = timedelta(minutes=30)

        if qs:
            for element in qs:
                date_element = datetime.date(element.date_time)
                date_request = datetime.date(value)

                if date_element == date_request:
                    if (
                        element.date_time + delta <= value
                        or value + delta <= element.date_time
                    ):
                        pass
                    else:
                        raise serializers.ValidationError(
                            "Infelizmente o horário selecionado está indisponível!"
                        )

        return value

    def validate_client_name(self, value):
        amount_characters_name = len(value)

        if amount_characters_name < 7:
            raise serializers.ValidationError(
                "O nome do cliente precisa ter 7 ou mais caracteres!"
            )

        if not " " in value:  # noqa:E713
            raise serializers.ValidationError("O cliente precisa ter um sobrenome!")

        return value

    def validate_client_phone(self, value):
        verification_numbers = re.sub(r"[^0-9+() -]", "", value)
        amount_characters_phone = len(value)

        if value and amount_characters_phone < 12:
            raise serializers.ValidationError(
                "O número de telefone precisa ter no mínimo 8 digitos!"
            )

        if value != verification_numbers:
            raise serializers.ValidationError(
                "O número pode ter apenas valores entre 0-9, parenteses, traços, espaço e o sinal de mais!"
            )

        return value

    def validate(self, attrs):
        provider = attrs.get("provider", "")
        date_time = attrs.get("date_time", "")
        client_email = attrs.get("client_email", "")
        client_phone = attrs.get("client_phone", "")

        if date_time and client_email:
            if Scheduling.objects.filter(
                provider__username=provider,
                client_email=client_email,
                canceled=False,
                date_time__date=date_time,
            ).exists():
                raise serializers.ValidationError(
                    "O(A) cliente não pode ter duas reservas no mesmo dia!"
                )

        if (
            client_email.endswith(".br")
            and client_phone.startswith("+")
            and not client_phone.startswith("+55")
        ):
            raise serializers.ValidationError(
                "E-mail brasileiro deve estar associado a um número do Brasil (+55)"
            )

        return attrs


class EstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establishment
        fields = "__all__"

    def validate_name(self, value):
        obj = Establishment.objects.filter(name=value)
        amount_characters_name = len(value)

        if amount_characters_name < 8:
            raise serializers.ValidationError(
                "Infelizmente o nome do estabelecimento precisa ter mais de 7 caracteres!"
            )

        if obj.exists():
            raise serializers.ValidationError("O estabelecimento em questão já existe!")

        return obj


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

    provider = serializers.CharField()
    establishment = serializers.CharField()

    def validate_provider(self, value):
        try:
            provider_obj = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Username não existe!")

        return provider_obj

    def validate_establishment(self, value):
        try:
            establishment_obj = Establishment.objects.get(name=value)
        except Establishment.DoesNotExist:
            raise serializers.ValidationError("Estabelecimento não encontrado!")

        return establishment_obj

    def validate_assignment(self, value):
        amount_characters = len(value)

        if amount_characters < 5:
            raise serializers.ValidationError(
                "A profissão precisa ter mais de 4 caracteres!"
            )

        return value

    def validate(self, attrs):
        provider = attrs.get("provider", None)
        establishment = attrs.get("establishment", None)
        assignment = attrs.get("assignment", None)

        if Employee.objects.filter(
            provider=provider, establishment=establishment, assignment=assignment
        ).exists():
            raise serializers.ValidationError(
                "O prestador de serviço já está cadastrado com essas caracteristicas nesse estabelecimento!"
            )

        return attrs


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"

    establishment = serializers.CharField()
    state = serializers.CharField(default="")
    city = serializers.CharField(default="")
    district = serializers.CharField(default="")
    street = serializers.CharField(default="")

    def validate_establishment(self, value):
        obj = Establishment.objects.filter(name=value)

        if not obj.exists():
            raise serializers.ValidationError(
                "Infelizmente o estabelecimento não existe!"
            )

        return obj.first()

    def validate_cep(self, value):
        verification_characters = re.sub(r"[^0-9-]", "", value)

        if value == "":
            raise serializers.ValidationError("O cep precisa ser passado!")

        if value != verification_characters:
            raise serializers.ValidationError("O cep foi passado de maneira inválida!")

        amount_characters = len(value)

        if amount_characters != 9:
            raise serializers.ValidationError("O cep precisa ter 9 digitos!")

        validation_cep = Verifications.verify_cep(value)

        if not validation_cep:
            raise serializers.ValidationError(
                "O cep passado é inválido! Verifique e envie novamente!"
            )

        return value

    def validate_state(self, value):
        if value == "":
            return value

        amount_characters = len(value)

        if amount_characters != 2:
            raise serializers.ValidationError(
                'O estado precisa ter seu nome abreviado para dois caracteres. Ex:"RS"!'
            )

        verify_characters = re.sub(r"[^A-Za-z]", "", value)

        if value != verify_characters:
            raise serializers.ValidationError(
                "O nome do estado precisa conter apenas letras!"
            )

        return value.upper()

    def validate_city(self, value):
        if value == "":
            return value

        verify_characters = re.sub(r"[^A-Z a-z]", "", value)

        if value != verify_characters:
            raise serializers.ValidationError(
                "O nome da cidade precisa conter apenas letras!"
            )

        amount_characters = len(value)

        if amount_characters < 5:
            raise serializers.ValidationError(
                "O nome da cidade precisa ter cinco ou mais caracteres!"
            )

        return value.title()

    def validate_district(self, value):
        if value == "":
            return value

        amount_characters = len(value)

        if amount_characters < 7:
            raise serializers.ValidationError(
                "O bairro precisa ter 7 caracteres ou mais!"
            )

        return value.title()

    def validate_street(self, value):
        if value == "":
            return value

        amount_characters = len(value)

        if amount_characters < 5:
            raise serializers.ValidationError(
                "A rua precisa ter cinco ou mais caracteres!"
            )

        return value.title()

    def validate_complement(self, value):
        return value

    def validate(self, attrs):
        cep = attrs.get("cep", None)
        state = attrs.get("state", None)
        city = attrs.get("city", None)
        district = attrs.get("district", None)
        street = attrs.get("street", None)

        validation_values = Verifications.verify_cep(cep)

        validation_state = validation_values["state"]
        validation_city = validation_values["city"]
        validation_neighborhood = validation_values["neighborhood"]
        validation_street = validation_values["street"]

        if cep and state and city and district and street:
            if state != validation_state:
                logging.warning("O estado passado é diferente do conferido!")
            if city != validation_city:
                logging.warning("A cidade passada é diferente da conferida!")
            if district != validation_neighborhood:
                logging.warning("O bairro passado é diferente do conferido!")
            if street != validation_street:
                logging.warning("A rua passada é diferente da conferida!")

        if not state and not city and not district and not street:
            attrs["state"] = validation_state
            attrs["city"] = validation_city
            attrs["district"] = validation_neighborhood
            attrs["street"] = validation_street

        return attrs


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "scheduling"]

    scheduling = SchedulingSerializer(many=True, read_only=True)


class EmployeeEstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "employee"]

    employee = EmployeeSerializer(many=True, read_only=True)


class AddressEstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establishment
        fields = ["id", "name", "address"]

    address = AddressSerializer(many=True, read_only=True)
