# voluntariapp/views.py
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, JSONParser
from .models import Event, CustomUser
from .serializers import EventSerializer, UserSerializer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response

class UserListView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        try:
            queryset = CustomUser.objects.all()
            serializer = UserSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            content = {'please move along': 'nothing to see here'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)


class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)

    def get(self, request, *args, **kwargs):
        try:
            queryset = Event.objects.all()
            serializer = EventSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)

        except Event.DoesNotExist:
            content = {'please move along': 'nothing to see here'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)


