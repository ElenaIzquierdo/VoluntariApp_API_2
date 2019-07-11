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
        fields = ('id','name','type','start_date','end_date','description','attendance',)

class EventGetSerializer(serializers.ModelSerializer):
    attending = serializers.SerializerMethodField()

    def get_attending(self, obj):
        attender = self.context['request'].user
        return models.EventAttendee.objects.filter(event=obj, eventattendee_user=attender).exists()
    class Meta:
        model = models.Event
        fields = ('id','name','type','start_date','end_date','description','attendance','attending',)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ("id", "content", "forumtheme",)

class ForumThemeGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ForumTheme
        fields = ("id","title","description","tasks","finished","created_date")

class ForumThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ForumTheme
        fields = ("id","title","description","tasks")

class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rate
        fields = ("id", "event", "rate","description")

class EventAttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventAttendee
        fields = ("id", "user", "event","attending")