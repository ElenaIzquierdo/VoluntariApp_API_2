# users/models.py
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
from voluntariapp.choices import *
from django.conf import settings



class CustomUser(AbstractUser):
    name = models.CharField(blank=True, max_length=255)
    surname = models.CharField(blank=True, max_length=255)
    project = models.CharField(choices=PROJECT_CHOICES, default="Petits", max_length=100)

    def __str__(self):
        return self.email

class Event(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_creator',
                                null=True)
    name = models.CharField(blank=True, max_length=255)
    type = models.CharField(blank=True, max_length=255)
    created_date = models.DateField(default=timezone.now)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True,null=True)
    attendance = models.IntegerField(null=True)

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name
