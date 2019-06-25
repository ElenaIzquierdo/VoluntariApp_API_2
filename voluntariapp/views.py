# voluntariapp/views.py
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, JSONParser
from .models import Event, CustomUser, Comment, ForumTheme
from .serializers import EventSerializer, UserSerializer, CommentSerializer, ForumThemeSerializer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone

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
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        try:
            queryset = Event.objects.all()
            serializer = EventSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)

        except Event.DoesNotExist:
            content = {'please move along': 'nothing to see here'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
    def post(self,request):
        data = {"creator":request.user.id,"created_date": timezone.now()}
        data.update(request.data.dict())
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForumThemeListView(generics.ListAPIView):
    queryset = ForumTheme.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = ForumThemeSerializer

    def get(self, request, *args, **kwargs):
        try:
            queryset = ForumTheme.objects.all()
            serializer = ForumThemeSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)

        except Event.DoesNotExist:
            content = {'please move along': 'nothing to see here'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
    def post(self,request):
        data = {"creator":request.user.id,"created_date": timezone.now()}
        data.update(request.data.dict())
        serializer = ForumThemeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListCommentView(generics.ListAPIView):
    queryset = Comment.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = CommentSerializer

    def post(self, request):
        data = {"author": request.user.id, "created_date": timezone.now()}
        data.update(request.data.dict())
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET comment/:id/
    PUT comment/:id/
    DELETE comment/:id/
    """
    queryset = Comment.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        try:
            a_comment = self.queryset.get(pk=kwargs["pk"])
            serializer = CommentSerializer(a_comment, context={'request': request})
            return Response(serializer.data)
        except Comment.DoesNotExist:
            return Response(
                data={
                    "message": "Comment with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            a_comment = self.queryset.get(pk=kwargs["pk"])
            serializer = CommentSerializer()
            if a_comment.author == request.user:
                data = request.data.dict()
                updated_comment = serializer.update(a_comment, data)
                return JsonResponse(CommentSerializer(updated_comment).data, status=status.HTTP_200_OK)
            else:
                return JsonResponse(
                    data={
                        "message": "You are not the author of comment {}!".format(kwargs["pk"])
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
        except Comment.DoesNotExist:
            return JsonResponse(
                data={
                    "message": "Comment with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_comment = self.queryset.get(pk=kwargs["pk"])
            if a_comment.author == request.user:
                a_comment.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    data = {
                        "message": "You are not the original author of comment {}!".format(kwargs["pk"])
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
        except Comment.DoesNotExist:
            return Response(
                data={
                    "message": "Comment with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )




