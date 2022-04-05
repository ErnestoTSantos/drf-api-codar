from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import generics, permissions, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from schedule.models import (Address, Employee, Establishment, Faithfulness,
                             Scheduling)
from schedule.serializers import (AddressEstablishmentSerializer,
                                  AddressSerializer,
                                  EmployeeEstablishmentSerializer,
                                  EmployeeSerializer, EstablishmentSerializer,
                                  ProviderSerializer, SchedulingSerializer)
from schedule.utils import Verifications


class IsOwnerOrCreateOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True

        username = request.query_params.get('username', None)
        if request.user.username == username:
            return True
        return False


class IsProvider(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.provider == request.user:
            return True
        return False


class SchedulingList(generics.ListCreateAPIView):  # noqa:E501

    serializer_class = SchedulingSerializer
    permission_classes = [IsOwnerOrCreateOnly]

    def post(self, request, *args, **kwargs):
        data = request.data
        provider_user = data['provider']
        provider = User.objects.filter(username=provider_user).first()
        client_name = data['client_name']
        date = data['date_time']
        date = datetime.strptime(date[:10], '%Y-%m-%d').date()
        establishment = request.query_params.get('establishment', None)

        holiday = Verifications.is_holiday(date)

        if holiday:
            raise serializers.ValidationError('Infelizmente agendamentos não podem ser realizados em feriados!')  # noqa:E501

        establishment_obj = Establishment.objects.filter(name=establishment)

        obj = Faithfulness.objects.filter(provider__username=provider_user, client=client_name)  # noqa:E501

        if establishment_obj.exists():
            if Employee.objects.filter(provider__username=provider_user, establishment=establishment_obj.first()).exists():  # noqa:E501
                if obj.exists():
                    obj = obj.first()
                    if obj.level < 11:
                        obj.level += 1
                        obj.save()
                else:
                    Faithfulness.objects.create(provider=provider, client=client_name)   # noqa:E501
        else:
            raise serializers.ValidationError('O estabelecimento não foi encontrado!')   # noqa:E501

        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        confirmed = self.request.query_params.get('confirmed', None)
        if confirmed == 'True' or confirmed == 'true':
            username = self.request.query_params.get('username', None)
            queryset = Scheduling.objects.filter(provider__username=username, canceled=False, confirmed=True).order_by('date_time__time')  # noqa:E501
        elif confirmed == 'False' or confirmed == 'false':
            username = self.request.query_params.get('username', None)
            queryset = Scheduling.objects.filter(provider__username=username, canceled=False, confirmed=False).order_by('date_time__time')  # noqa:E501
        else:
            username = self.request.query_params.get('username', None)
            queryset = Scheduling.objects.filter(provider__username=username, canceled=False).order_by('date_time__time')  # noqa:E501

        return queryset


class SchedulingDetail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsProvider]
    queryset = Scheduling.objects.filter(canceled=False)
    serializer_class = SchedulingSerializer
    lookup_field = 'id'

    def patch(self, request, id, *args, **kwargs):
        username = request.user.username
        confirmed = request.query_params.get('confirmed', None)
        data = request.data

        if confirmed == 'True' or confirmed == 'true':
            obj = Scheduling.objects.filter(provider__username=username, id=id).first()  # noqa:E501
            comparison_obj = Scheduling.objects.filter(provider__username=username, date_time=obj.date_time, canceled=False, confirmed=True).first()  # noqa:E501
            if comparison_obj:
                raise serializers.ValidationError('Infelizmente o horário em questão já foi confirmado para outro cliente!')  # noqa:E501
            obj.confirmed = True
            obj.states = 'CONF'
            obj.save()
        else:
            if data == {}:
                raise serializers.ValidationError('É necessário passar algum elemento para ser atualizado!')  # noqa:E501

        return super().patch(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.confirmed = False
        instance.canceled = True
        instance.states = 'CANC'
        instance.save()

        faithfulness = Faithfulness.objects.filter(provider__username=instance.provider, client=instance.client_name)  # noqa:E501
        if faithfulness.exists():
            faithfulness.first()
            if faithfulness.level > 0:
                faithfulness.level -= 1
                faithfulness.save()

        return Response(status=204)


class ProviderList(generics.ListAPIView):  # noqa:E501

    serializer_class = ProviderSerializer
    queryset = User.objects.all()

    permission_classes = [permissions.IsAdminUser]


class EmployeeEstablishmentList(generics.ListAPIView):

    serializer_class = EmployeeEstablishmentSerializer
    queryset = User.objects.all()

    permission_classes = [permissions.IsAdminUser]


class EstablishmentAddressList(generics.ListAPIView):

    serializer_class = AddressEstablishmentSerializer
    queryset = Establishment.objects.all()

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class EmployeeList(generics.ListCreateAPIView):

    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [permissions.IsAdminUser]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'id'


class EstablishmentList(generics.ListCreateAPIView):

    serializer_class = EstablishmentSerializer
    queryset = Establishment.objects.all()

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class EstablishmentDetail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentSerializer
    lookup_field = 'id'


class AddressList(generics.ListCreateAPIView):

    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AddressDetail(generics.RetrieveUpdateAPIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_field = 'id'


class HoraryList(APIView):
    def get(self, request, date):
        username = request.query_params.get('username', None)
        obj = User.objects.filter(username=username)
        if obj:
            date = datetime.strptime(date, '%Y-%m-%d').date()

            appointment_list = []

            holiday = Verifications.is_holiday(date)

            if holiday:
                return JsonResponse(appointment_list, safe=False)

            qs = Scheduling.objects.filter(canceled=False, date_time__date=date, provider__username=username, confirmed=True).order_by('date_time__time')  # noqa:E501
            serializer = SchedulingSerializer(qs, many=True)

            dt_start = datetime(date.year, date.month, date.day, 9)  # noqa:E501
            dt_end_saturday = datetime(date.year, date.month, date.day, 13)
            dt_end = datetime(date.year, date.month, date.day, 18)  # noqa:E501
            delta = timedelta(minutes=30)  # noqa:E501

            if date.weekday() != 5 and date.weekday() != 6:
                while dt_start != dt_end:
                    appointment_list.append({
                        'date_time': dt_start
                    })

                    dt_start += delta

            if date.weekday() == 5:
                while dt_start != dt_end_saturday:
                    appointment_list.append({
                        'date_time': dt_start
                    })

                    dt_start += delta

            if date.weekday() == 6:
                appointment_list.append({
                    'Information': 'Infelizmente o estabelecimento não trabalha aos domingos!'  # noqa:E501
                })

            for element in serializer.data:
                element = element.get('date_time')
                time_element = element[11:16]
                for time in appointment_list:
                    date_time = time.get('date_time')
                    time_list = datetime.strftime(date_time, '%H:%M')
                    if time_element == time_list:
                        appointment_list.remove(time)

            return JsonResponse(appointment_list, safe=False)
        return Response(status=404)


@api_view(http_method_names=['GET', 'POST'])
def user_functions(request):
    if request.method == 'GET':
        qs = User.objects.all()
        users_list = []

        for user in qs:
            users_list.append({
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'e-mail': user.email,
                'is_staff': user.is_staff,
                'is_active': user.is_active
            })

        return JsonResponse(users_list, safe=False)

    if request.method == 'POST':
        data = request.data
        username = data['username']
        password = data['password']
        email = data['email']

        if not username:
            raise serializers.ValidationError('É necessário ter um nome de usuário!')  # noqa:E501

        if not password:
            raise serializers.ValidationError('É necessário ter uma senha para o usuário!')  # noqa:E501

        if not email:
            raise serializers.ValidationError('É necessário ter um e-mail para o usuário!')  # noqa:E501

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('O nome de usuário enviado já existe!')  # noqa:E501

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('O e-mail enviado já está em uso!')  # noqa:E501

        obj = User.objects.create_user(username=username, password=password, email=email, is_staff=False)  # noqa:E501

        dict_obj = {
            'id': obj.id,
            'username': obj.username,
            'first_name': obj.first_name,
            'last_name': obj.last_name,
            'e-mail': obj.email,
            'is_staff': obj.is_staff,
            'is_active': obj.is_active
        }

        return JsonResponse(dict_obj, safe=False)


@api_view(http_method_names=['GET'])
def healthcheck(request):
    return Response({'status': 'OK'}, status=200)
