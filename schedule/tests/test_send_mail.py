from django.core import mail
from django.test import TestCase


class EmailTest(TestCase):
    def test_send_email(self):
        mail.send_mail(
            "Subject here",
            "Here is the message.",
            "from@example.com",
            ["to@example.com"],
            fail_silently=False,
        )

        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == "Subject here"

    def test_sender_email(self):
        mail.send_mail(
            "Subject here",
            "Here is the message.",
            "from@example.com",
            ["to@example.com"],
            fail_silently=False,
        )

        assert mail.outbox[0].from_email == "from@example.com"

    def test_receiver_email(self):
        mail.send_mail(
            "Subject here",
            "Here is the message.",
            "from@example.com",
            ["to@example.com"],
            fail_silently=False,
        )

        assert mail.outbox[0].to[0] == "to@example.com"

    def test_have_attachment(self):
        mail.send_mail(
            "Subject here",
            "Here is the message.",
            "from@example.com",
            ["to@example.com"],
            fail_silently=False,
        )

        assert mail.outbox[0].attachments == []
