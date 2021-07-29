from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models.base import Model


# Create your models here.

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_farmer = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

class Farmer(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_regex = RegexValidator(
		regex=r'^\+?1?\d{9,15}$',
		message="Phone number must be entered in the format: '+254700000000'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, unique=True) # validators should be a list
    date_of_birth = models.CharField(max_length = 20)

class Farmers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_regex = RegexValidator(
		regex=r'^\+?1?\d{9,15}$',
		message="Phone number must be entered in the format: '+254700000000'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, unique=True) # validators should be a list
    date_of_birth = models.CharField(max_length = 20)

class CityWeather(models.Model):
    city = models.CharField(max_length=100)    
    date = models.CharField(max_length=100)
