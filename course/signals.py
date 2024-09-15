import os
import json
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from course.models import Course, Video, Customer, Blog, Comment
from config.settings import EMAIL_DEFAULT_SENDER, BASE_DIR
from user.models import User
from datetime import datetime


@receiver(post_save, sender=Course)
def post_save_customers(sender, created, instance, **kwargs):
    if created:
        subject = 'Course added'
        message = f'{instance.title} added a new course.'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in User.objects.all()]
        send_mail(subject, message, from_email, recipient_list)


@receiver(pre_delete, sender=Course)
def pre_delete_customer(sender, instance, **kwargs):
    customer_data = {
        'id': instance.id,
        'title': instance.title,
        'description': instance.description,
        'image': instance.image,
        'price': instance.price,
        'category_id': instance.category_id,
        'teacher_id': instance.teacher_id,
        'slug': instance.slug,
    }

    date = datetime.now().strftime("%Y,%b")

    file_path = os.path.join(BASE_DIR, 'course/deleted_data/deleted_course', f'{date}.json')

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        data = []

    data.append(customer_data)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


@receiver(post_save, sender=Video)
def post_save_customers(sender, created, instance, **kwargs):
    if created:
        subject = 'Video added'
        message = f'{instance.title} added a new video.'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in User.objects.all()]
        send_mail(subject, message, from_email, recipient_list)


@receiver(pre_delete, sender=Video)
def pre_delete_customer(sender, instance, **kwargs):
    customer_data = {
        'id': instance.id,
        'title': instance.title,
        'duration': instance.duration,
        'file': instance.file,
        'course_id': instance.course_id,

    }

    date = datetime.now().strftime("%Y,%b")

    file_path = os.path.join(BASE_DIR, 'course/deleted_data/deleted_videos', f'{date}.json')

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        data = []

    data.append(customer_data)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


@receiver(post_save, sender=Comment)
def post_save_customers(sender, created, instance, **kwargs):
    if created:
        subject = 'Comment added'
        message = f'{instance.content} added a new comment.'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in User.objects.all()]
        send_mail(subject, message, from_email, recipient_list)


@receiver(pre_delete, sender=Comment)
def pre_delete_customer(sender, instance, **kwargs):
    customer_data = {
        'id': instance.id,
        'rating': instance.rating,
        'content': instance.content,
        'user_id': instance.user_id,
        'video_id': instance.video_id,

    }

    date = datetime.now().strftime("%Y,%b")

    file_path = os.path.join(BASE_DIR, 'course/deleted_data/deleted_comments', f'{date}.json')

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        data = []

    data.append(customer_data)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


@receiver(post_save, sender=Customer)
def post_save_customers(sender, created, instance, **kwargs):
    if created:
        subject = 'Customer bought'
        message = f"Customer's number : {instance.phone} bought a new course."
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in User.objects.all()]
        send_mail(subject, message, from_email, recipient_list)


@receiver(pre_delete, sender=Customer)
def pre_delete_customer(sender, instance, **kwargs):
    customer_data = {
        'id': instance.id,
        'phone': instance.phone,
        'user_id': instance.user_id,
        'course_id': instance.course_id,

    }

    date = datetime.now().strftime("%Y,%b")

    file_path = os.path.join(BASE_DIR, 'course/deleted_data/deleted_customers', f'{date}.json')

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        data = []

    data.append(customer_data)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


@receiver(post_save, sender=Blog)
def post_save_customers(sender, instance, **kwargs):
    if kwargs['created']:
        subject = 'Blog was created'
        message = f"Blog's title : {instance.title} created a new blog."
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in User.objects.all()]
        send_mail(subject, message, from_email, recipient_list)


@receiver(pre_delete, sender=Blog)
def pre_delete_customer(sender, instance, **kwargs):
    customer_data = {
        'id': instance.id,
        'title': instance.title,
        'content': instance.body,
        'image': str(instance.image.url),
        'category_id': instance.category_id,

    }

    date = datetime.now().strftime("%Y,%b")

    file_path = os.path.join(BASE_DIR, 'course/deleted_data/deleted_blogs', f'{date}.json')

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        data = []

    data.append(customer_data)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
