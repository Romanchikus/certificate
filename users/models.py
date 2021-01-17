from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_api_key.crypto import KeyGenerator

class CustomUser(AbstractUser):
    company_name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255, editable=False, unique=True)
    hashed_key = models.CharField(max_length=255, editable=False, unique=True)
    REQUIRED_FIELDS = ['company_name']

    def save(self, *args, **kwargs):
        if not self.hashed_key:
            self.api_key, _, self.hashed_key = KeyGenerator(prefix_length=8, secret_key_length=32).generate()
        super(CustomUser, self).save(*args, **kwargs)
