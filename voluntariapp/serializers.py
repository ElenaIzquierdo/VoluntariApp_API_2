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

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ("id", "content", "forumtheme",)

class ForumThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ForumTheme
        fields = ("id","title","finished","description","tasks")