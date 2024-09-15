from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from user.manager import MyUserManager


# Create your models here.
class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='images/user/', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_name(self):
        if self.username:
            return self.username
        return self.email.split('@')[0]

    def __str__(self):
        return self.email


class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='teacher')
    telegram_url = models.URLField(max_length=200)
    instagram_url = models.URLField(max_length=200)
    user_id = models.OneToOneField(User, on_delete=models.SET_NULL, related_name='teachers', null=True)

    def __str__(self):
        return self.first_name

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
