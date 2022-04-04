from django.db import models


class Scheduling(models.Model):
    ACTION_STATES = [
        ('NCNF', 'Not confirmed'),
        ('CONF', 'Confirmed'),
        ('EXEC', 'Executed'),
        ('CANC', 'Canceled')
    ]

    provider = models.ForeignKey('auth.User', related_name='scheduling', on_delete=models.CASCADE, verbose_name='Prestador do serviço')  # noqa:E501
    date_time = models.DateTimeField('Data e hora')
    client_name = models.CharField('Nome do cliente', max_length=200)
    client_email = models.EmailField('E-mail do cliente')
    client_phone = models.CharField('Número do cliente', max_length=20)
    states = models.CharField('Estados do elemento', max_length=4, choices=ACTION_STATES, default='NCNF')  # noqa:E501
    confirmed = models.BooleanField('Horário confirmado', default=False)
    canceled = models.BooleanField('Horário cancelado', default=False)

    def __str__(self):
        return self.client_name


class Faithfulness(models.Model):
    provider = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='faithfulness', verbose_name='Prestador do serviço')  # noqa:E501
    client = models.CharField('Nome do cliente', max_length=200)
    level = models.IntegerField('Fidelidade', default=0)

    def __str__(self):
        return f'{self.client} = {self.level}'


class Establishment(models.Model):
    name = models.CharField('Nome do estabelecimento', max_length=100, unique=True)  # noqa:E501

    def __str__(self):
        return self.name


class Employee(models.Model):
    provider = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='employee', verbose_name='Prestador do serviço')  # noqa:E501
    establishment = models.ForeignKey('Establishment', on_delete=models.CASCADE, related_name='employee', verbose_name='Nome do estabelecimento')  # noqa:E501
    assignment = models.CharField('Atribuição', max_length=50)

    def __str__(self):
        return f'{self.provider} -> {self.establishment}'


class Address(models.Model):
    establishment = models.ForeignKey('Establishment', on_delete=models.CASCADE, related_name='address', verbose_name='Estabelecimento')  # noqa:E501
    cep = models.CharField(max_length=9)
    state = models.CharField('Estado', max_length=2)
    city = models.CharField('Cidade', max_length=50)
    district = models.CharField('Bairro', max_length=50)
    street = models.CharField('Rua', max_length=50)
    complement = models.CharField('Complement', max_length=50, blank=True, null=True)  # noqa:E501

    def __str__(self):
        return f'{self.establishment} -> {self.street}'
