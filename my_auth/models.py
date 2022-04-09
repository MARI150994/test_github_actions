from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager


class Employee(AbstractUser):
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female')
    )

    username = None
    email = models.EmailField('email address', max_length=50, unique=True)
    birthday = models.DateField('Birthday data', blank=True, null=True)
    position = models.ForeignKey('task.Role', on_delete=models.PROTECT,
                                 verbose_name='User position',
                                 related_name='employees',
                                 blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER, null=True)
    phone = models.CharField(max_length=30, blank=True, unique=True, db_index=True, null=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
