from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from .managers import UserManager


class EducationCentre(AbstractBaseUser, PermissionsMixin):
    ECemail = models.EmailField(unique=True)
    ECname = models.CharField(max_length=128)
    EClocation = models.CharField(max_length=128)
    ECphonenumber = models.CharField(max_length=16)
    # set Abstract User Defaults
    date_joined = models.DateTimeField(default=timezone.now)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'ECemail'

    def __str__(self):
        return self.ECname


