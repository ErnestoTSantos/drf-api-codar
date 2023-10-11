import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "marked.settings.dev")

app = Celery("marked")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task
def soma(a, b):
    print("Somando")
    return a + b
