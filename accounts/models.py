from django.db import models
from django.contrib.auth.models import AbstractUser
from  phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ["email", "phone_number"]

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = "accounts"
