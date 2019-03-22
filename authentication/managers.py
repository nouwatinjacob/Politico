
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_field):
        """
        Creates and saves a User with the given email and password.
        """
        
        if not email:
            raise ValueError('The given email must be set')
        
        email = self.normalize_email(email)
        user = self.model(emeil=email, **extra_field)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_field):
        """Create new superuser"""

        user = self.create_user(email, password, **extra_field)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user
