import csv
from io import StringIO

from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from marked.celery import app

from schedule.serializers import ProviderSerializer


def write_file(writer):
    providers = User.objects.all()
    serializer = ProviderSerializer(providers, many=True)

    for provider in serializer.data:
        schedulings = provider["scheduling"]
        for scheduling in schedulings:
            writer.writerow(
                [
                    scheduling["provider"],
                    scheduling["client_name"],
                    scheduling["client_email"],
                    scheduling["client_phone"],
                    scheduling["confirmed"],
                    scheduling["states"],
                ]
            )


def generate_file(output):
    writer = csv.writer(output)
    writer.writerow(
        [
            "provider",
            "client_name",
            "client_email",
            "client_phone",
            "confirmed",
            "states",
        ]
    )
    write_file(writer)


@app.task
def generate_report_provider():
    output = StringIO()
    generate_file(output)

    email = EmailMessage(
        subject="Marked -> Provider report",
        body="Em anexo relatório solicitado.",
        from_email="ernesto.terra2003@gmail.com",
        to=["ernesto.terra2003@gmail.com"],
    )

    # Mine é o formato que estamos dizendo o tipo de arquivo que estamos enviando.
    # Estamos adicionando o arquivo, dando o tipo e nomeando ele.
    email.attach("report.csv", output.getvalue(), "text/csv")
    email.send()
