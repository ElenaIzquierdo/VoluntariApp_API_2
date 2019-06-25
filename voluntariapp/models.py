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

class EventAttendee(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='eventattendee_user',
                                null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attending = models.BooleanField(default=False)


class ForumTheme(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='forumtheme_creator',
                                null=True)
    title = models.CharField(blank=True, max_length=255)
    created_date = models.DateField(default=timezone.now)
    finished = models.BooleanField(blank=True)
    description = models.TextField(blank=True, null=True)
    tasks = models.TextField(blank=True, null=True)

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    content = models.CharField(max_length=400)
    forumtheme = models.ForeignKey(ForumTheme, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

class Rate(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rate = models.IntegerField(blank=True,null=True)
    description = models.TextField(blank=True, null=True)

class CentreInteres(models.Model):
    objectius = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)

