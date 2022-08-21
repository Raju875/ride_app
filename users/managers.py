from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, username, email, password):
        user = self.model(email=self.normalize_email(email))
        user.username = username
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.user_type = 1 #1=Admin; 2=Customer; 3=Driver
        user.save()

        return user


    def create_superuser(self, username, email, password):
        if email is None:
            raise TypeError('Users must have an email address.')
        if password is None:
            raise TypeError('Superusers must have a password.')

        return self.create_user(username, email, password)
