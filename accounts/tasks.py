from celery import shared_task
from django.utils import timezone


@shared_task
def add(a, b):
    return a + b


@shared_task
def print_time():
    print(f'{timezone.now()} hozirgi vaqt')
