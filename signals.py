from django.db.models.signals import post_save
from django.contrib.auth.models import User
from store.models import Customer

def create_customer(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'customer'):
        Customer.objects.create(user=instance, name=instance.username, email=instance.email)

post_save.connect(create_customer, sender=User)
