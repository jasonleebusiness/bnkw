from django.db.models.signals import post_save, pre_save
# from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Userprofile, Transactions
from django.contrib.auth import get_user_model


User = get_user_model()


# @receiver(post_save, sender=Transactions)
def create_qrcode(sender, instance, **kwargs):
    print('instance pk -', instance.pk)
    Transactions.objects.get(pk=instance.pk)
    ('na soooooo')


post_save.connect(create_qrcode, sender=Transactions)




