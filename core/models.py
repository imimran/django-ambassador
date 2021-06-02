from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('email is requried')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.is_admin = False
        user.is_staff = False
        user.save(using=self._db)
        return user  

    def create_superuser(self, email, password=None):
        """
        Create and save a SuperUser with the given email and password.
        """
        if not email:
            raise ValueError('email is requried')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user  




class User(AbstractUser):
    """ Use this option if you are happy with the existing fields 
     on the User model and just want to remove the username field."""
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(_('email address'), unique=True)
    is_ambassador = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    def __str__(self):
        return self.email



# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     """Use this option if you want to start from scratch by 
#     creating your own, completely new User model."""
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     email = models.EmailField(_('email address'), unique=True)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     date_joined = models.DateTimeField(default=timezone.now)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     objects = UserManager()

#     def __str__(self):
#         return self.email        
