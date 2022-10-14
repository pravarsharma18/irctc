import random
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Ticket


@receiver(pre_save, sender=Ticket)
def my_callback(sender, instance, *args, **kwargs):
    if not instance.pnr:
        instance.pnr = random.randint(10000000, 100000000)
