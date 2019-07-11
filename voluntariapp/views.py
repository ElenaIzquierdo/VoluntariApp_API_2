# voluntariapp/views.py
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, JSONParser
from .models import Event, CustomUser, Comment, ForumTheme, Rate, EventAttendee
from .serializers import EventSerializer, UserSerializer, CommentSerializer, ForumThemeSerializer, RateSerializer, \
                        EventAttendeeSerializer, EventGetSerializer
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
            serializer = EventGetSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)

        except Event.DoesNotExist:
            content = {'please move along': 'nothing to see here'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
    def post(self,request):
        data = {"creator":request.user.id,"created_date": timezone.now()}
        data.update(request.data)
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
        GET event/:id/
        PUT event/:id/
        DELETE event/:id/
        """
    queryset = Event.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        try:
            a_event = self.queryset.get(pk=kwargs["pk"])
            serializer = EventSerializer(a_event, context={'request': request})
            return Response(serializer.data)
        except Event.DoesNotExist:
            return Response(
                data={
                    "message": "Event with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            a_event = self.queryset.get(pk=kwargs["pk"])
            serializer = EventSerializer()
            if a_event.creator == request.user:
                data = request.data.dict()
                updated_event = serializer.update(a_event, data)
                return JsonResponse(EventSerializer(updated_event).data, status=status.HTTP_200_OK)
            else:
                return JsonResponse(
                    data={
                        "message": "You are not the author of the event {}!".format(kwargs["pk"])
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
        except Event.DoesNotExist:
            return JsonResponse(
                data={
                    "message": "Event with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_event = self.queryset.get(pk=kwargs["pk"])
            if a_event.creator == request.user:
                a_event.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    data={
                        "message": "You are not the original author of the event {}!".format(kwargs["pk"])
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
        except Event.DoesNotExist:
            return Response(
                data={
                    "message": "Event with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

class ForumThemeListView(generics.ListAPIView):
    queryset = ForumTheme.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = ForumThemeSerializer

    def get(self, request, *args, **kwargs):
        try:
            queryset = ForumTheme.objects.all()
            sort_param = self.request.query_params.get('sort', None)
            possible_param = ["title","created_date","-title","-created_date"]
            if sort_param is not None:
                if sort_param in possible_param:
                    queryset = queryset.order_by(sort_param)
                else:
                    status_code = 400
                    message = "The request is not valid."
                    explanation = "The parameter to sort is not correct, possible values: title,created_date"
                    return Response({'message': message, 'explanation': explanation}, status=status_code)

            filter_status = self.request.query_params.get('status', None)
            if filter_status is not None:
                possible_status = ["open", "closed"]
                if filter_status in possible_status:
                    if filter_status == "open":
                        queryset = queryset.filter(finished=False)
                    elif filter_status == "closed":
                        queryset = queryset.filter(finished=True)
                else:
                    status_code = 400
                    message = "The request is not valid."
                    explanation = "The parameter to filter status is not correct, possible values: open, closed"
                    return Response({'message': message, 'explanation': explanation}, status=status_code)
            serializer = ForumThemeSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)

        except Event.DoesNotExist:
            content = {'please move along': 'nothing to see here'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
    def post(self,request):
        data = {"creator":request.user.id,"created_date": timezone.now()}
        data.update(request.data)
        serializer = ForumThemeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForumThemeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
        GET forumtheme/:id/
        PUT forumtheme/:id/
        DELETE forumtheme/:id/
        """
    queryset = ForumTheme.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = ForumThemeSerializer

    def get(self, request, *args, **kwargs):
        try:
            a_theme = self.queryset.get(pk=kwargs["pk"])
            serializer = ForumThemeSerializer(a_theme, context={'request': request})
            return Response(serializer.data)
        except ForumTheme.DoesNotExist:
            return Response(
                data={
                    "message": "Forum Theme with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            a_theme = self.queryset.get(pk=kwargs["pk"])
            serializer = ForumThemeSerializer()
            if a_theme.creator == request.user:
                data = request.data.dict()
                updated_theme = serializer.update(a_theme, data)
                return JsonResponse(ForumThemeSerializer(updated_theme).data, status=status.HTTP_200_OK)
            else:
                return JsonResponse(
                    data={
                        "message": "You are not the author of the theme {}!".format(kwargs["pk"])
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
        except ForumTheme.DoesNotExist:
            return JsonResponse(
                data={
                    "message": "Theme with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_theme = self.queryset.get(pk=kwargs["pk"])
            if a_theme.creator == request.user:
                a_theme.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    data={
                        "message": "You are not the original author of theme {}!".format(kwargs["pk"])
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
        except ForumTheme.DoesNotExist:
            return Response(
                data={
                    "message": "Theme with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class ListCommentView(generics.ListAPIView):
    queryset = Comment.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        try:
            queryset = Comment.objects.all()
            serializer = CommentSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)

        except Comment.DoesNotExist:
            content = {'please move along': 'nothing to see here'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        data = {"author": request.user.id, "created_date": timezone.now()}
        data.update(request.data)
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

class CommentFromThemeView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        try:
            comments = self.queryset.filter(forumtheme=kwargs["pk"])
            serializer = CommentSerializer(comments, many=True, context={'request': request})
            return Response(serializer.data)
        except ForumTheme.DoesNotExist:
            return Response(
                data={
                    "message": "Theme with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

class ListRateView(generics.ListAPIView):
    queryset = Rate.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = RateSerializer

    def get(self, request, *args, **kwargs):
        try:
            queryset = Rate.objects.all()
            serializer = RateSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)

        except Rate.DoesNotExist:
            content = {'please move along': 'nothing to see here'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = RateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET rate/:id/
    PUT rate/:id/
    DELETE rate/:id/
    """
    queryset = Rate.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = RateSerializer

    def get(self, request, *args, **kwargs):
        try:
            a_rate = self.queryset.get(pk=kwargs["pk"])
            serializer = RateSerializer(a_rate, context={'request': request})
            return Response(serializer.data)
        except Rate.DoesNotExist:
            return Response(
                data={
                    "message": "Rate with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            a_rate = self.queryset.get(pk=kwargs["pk"])
            serializer = RateSerializer()
            data = request.data.dict()
            updated_rate = serializer.update(a_rate, data)
            return JsonResponse(RateSerializer(updated_rate).data, status=status.HTTP_200_OK)

        except Comment.DoesNotExist:
            return JsonResponse(
                data={
                    "message": "Rate with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_rate = self.queryset.get(pk=kwargs["pk"])
            a_rate.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Comment.DoesNotExist:
            return Response(
                data={
                    "message": "Rate with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

class RateFromEventView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = RateSerializer

    def get(self, request, *args, **kwargs):
        try:
            a_rate = Event.objects.get(pk=kwargs["pk"])
            rates = self.queryset.filter(event=kwargs["pk"])
            serializer = RateSerializer(rates, many=True, context={'request': request})
            return Response(serializer.data)
        except Event.DoesNotExist:
            return Response(
                data={
                    "message": "Event with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

class ListEventAttendeeView(generics.ListAPIView):
    queryset = EventAttendee.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = EventAttendeeSerializer

    def get(self, request, *args, **kwargs):
        try:
            queryset = EventAttendee.objects.all()
            serializer = EventAttendeeSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)

        except EventAttendee.DoesNotExist:
            content = {'please move along': 'nothing to see here'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

class AttendeeView(generics.ListAPIView):
    queryset = EventAttendee.objects.all()
    serializer_class = EventAttendeeSerializer

    def post(self, request, *args, **kwargs):
        try:
            a_event = Event.objects.get(pk=kwargs["pk"])
            EventAttendee.objects.create(user=request.user, event=a_event)
            return Response(status=status.HTTP_201_CREATED)
        except Event.DoesNotExist:
            return Response(
                data={
                    "message": "Event with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    "UnAttend function"

    def delete(self, request, *args, **kwargs):
        try:
            event = Event.objects.get(pk=kwargs["pk"])
            a_attendee = self.queryset.get(event=event, user=request.user)
            a_attendee.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except (Event.DoesNotExist, EventAttendee.DoesNotExist) as e:
            return Response(
                data={
                    "message": "Event with id: {} does not exist or EventAttendee from user: {} does not exist".format(
                        kwargs["pk"], request.user)
                },
                status=status.HTTP_404_NOT_FOUND
            )





