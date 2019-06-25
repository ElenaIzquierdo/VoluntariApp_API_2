# voluntariapp/serializers.py
from rest_framework import serializers
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ('email','name','surname','password','project')

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ('name','type','start_date','end_date','description','attendance',)