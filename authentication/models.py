from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser

from django.utils.translation import ugettext_lazy as _

from parties.models import Party

from .managers import UserManager
# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    party_id = models.ForeignKey(Party, on_delete=models.CASCADE, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('customuser')
        verbose_name_plural = _('customusers')

    def get_full_name(self):
        """Return the fullname of the user"""

        full_name = '{} {}'.format(self.first_name,self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name of the user"""
         
        return self.first_name
