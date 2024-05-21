import datetime
import django
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=20)
    user_level = models.IntegerField(default=1)
    created_date = models.DateTimeField(default=django.utils.timezone.now)

    def set_username_email(self):
        self.username = self.email

class Company(models.Model):
    name = models.CharField(max_length=50)
    website = models.CharField(max_length=50)
    bankaccountno = models.CharField(max_length=20)

class Operator(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)

class Constants(models.Model):
    group_name = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    data_type = models.CharField(max_length=10)
    value = models.CharField(max_length=20)
    
    class Meta:
        unique_together = ('group_name', 'name')