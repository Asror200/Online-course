import os
import json
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from config.settings import EMAIL_DEFAULT_SENDER, BASE_DIR
from user.models import User, Teacher
from datetime import datetime


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, **kwargs):
    if kwargs['created']:
        subject = 'User joined'
        message = f'{instance.username} joined.'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in User.objects.all()]
        send_mail(subject, message, from_email, recipient_list)


@receiver(pre_delete, sender=User)
def pre_delete_customer(sender, instance, **kwargs):
    user_data = {
        'id': instance.id,
        'email': instance.email,
        'username': instance.username,
        'image': str(instance.image),
        'date_of_birth': str(instance.date_of_birth),
        'is_active': str(instance.is_active),
        'is_stuff': str(instance.is_staff),
        'is_superuser': str(instance.is_superuser),
    }

    date = datetime.now().strftime("%Y,%b")

    file_path = os.path.join(BASE_DIR, 'user/deleted_data/deleted_users', f'{date}.json')

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        data = []

    data.append(user_data)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


@receiver(post_save, sender=Teacher)
def create_user_profile(sender, instance, **kwargs):
    if kwargs['created']:
        subject = 'Teacher joined'
        message = f'{instance.first_name} joined.'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in User.objects.all()]
        send_mail(subject, message, from_email, recipient_list)


@receiver(pre_delete, sender=Teacher)
def pre_delete_customer(sender, instance, **kwargs):
    user_data = {
        'id': instance.id,
        'first_name': instance.first_name,
        'last_name': instance.last_name,
        'image': str(instance.image),
        'telegram_url': str(instance.telegram_url),
        'instagram_url': str(instance.instagram_url),

    }

    date = datetime.now().strftime("%Y,%b")

    file_path = os.path.join(BASE_DIR, 'user/deleted_data/deleted_teachers', f'{date}.json')

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        data = []

    data.append(user_data)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
