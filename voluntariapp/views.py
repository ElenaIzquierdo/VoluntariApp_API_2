# voluntariapp/views.py
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from .models import Event, CustomUser, Comment, ForumTheme, Rate, EventAttendee
from .serializers import EventSerializer, UserSerializer, CommentSerializer, ForumThemeSerializer, RateSerializer, \
    EventAttendeeSerializer, EventGetSerializer, ForumThemeGetSerializer
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

    def get(self, request):
        queryset = Event.objects.all()
        serializer = EventGetSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = {"creator": request.user.id, "created_date": timezone.now()}
        data.update(request.data)
        serializer = EventSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
        GET event/:id/
        PUT event/:id/
        DELETE event/:id/
        """
    queryset = Event.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = EventSerializer

    def get(self, request, id_event):
        a_event = get_object_or_404(Event, pk=id_event)
        serializer = EventSerializer(a_event)
        return Response(data=serializer.data, status= status.HTTP_200_OK)


    def patch(self, request, id_event):
        a_event = get_object_or_404(Event, pk=id_event)
        serializer = EventSerializer(a_event, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status= status.HTTP_200_OK)

    def delete(self, request, id_event):
        a_event = get_object_or_404(Event, pk=id_event)
        if a_event.creator == request.user:
            a_event.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                data={
                    "message": "You are not the original author of the event {}!"
                },
                status=status.HTTP_403_FORBIDDEN
            )


class ForumThemeListView(generics.ListAPIView):
    queryset = ForumTheme.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = ForumThemeSerializer

    def get(self, request):
        queryset = ForumTheme.objects.all()
        sort_param = self.request.query_params.get('sort', None)
        possible_param = ["title", "created_date", "-title", "-created_date"]
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
        serializer = ForumThemeGetSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        data = {"creator": request.user.id, "created_date": timezone.now(), "finished": False}
        data.update(request.data)
        serializer = ForumThemeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


class ForumThemeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
        GET forumtheme/:id/
        PUT forumtheme/:id/
        DELETE forumtheme/:id/
        """
    queryset = ForumTheme.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = ForumThemeSerializer

    def get(self, request, id_forumtheme):
        a_theme = get_object_or_404(ForumTheme,pk=id_forumtheme)
        serializer = ForumThemeSerializer(a_theme)
        return Response(data=serializer.data,status=status.HTTP_200_OK)


    def patch(self, request, id_forumtheme):
        a_theme = get_object_or_404(ForumTheme,pk=id_forumtheme)
        serializer = ForumThemeSerializer(a_theme,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


    def delete(self, request, id_forumtheme):
        a_theme = get_object_or_404(ForumTheme,pk=id_forumtheme)
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

class ListCommentView(generics.ListAPIView):
    queryset = Comment.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        queryset = Comment.objects.all()
        serializer = CommentSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data,status=status.HTTP_200_OK)


    def post(self, request):
        data = {"author": request.user.id, "created_date": timezone.now()}
        data.update(request.data)
        serializer = CommentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET comment/:id/
    PUT comment/:id/
    DELETE comment/:id/
    """
    queryset = Comment.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = CommentSerializer

    def get(self, request, id_comment):
        a_comment = get_object_or_404(Comment,pk=id_comment)
        serializer = CommentSerializer(a_comment, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id_comment):
        a_comment = get_object_or_404(Comment, pk=id_comment)
        serializer = CommentSerializer(a_comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, id_comment):
        a_comment = get_object_or_404(Comment,pk=id_comment)
        if a_comment.author == request.user:
            a_comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                data={
                    "message": "You are not the original author of comment {}!".format(kwargs["pk"])
                },
                status=status.HTTP_403_FORBIDDEN
            )


class CommentFromThemeView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = CommentSerializer

    def get(self, request, id_forumtheme):
        comments = self.queryset.filter(forumtheme=id_forumtheme)
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)



class ListRateView(generics.ListAPIView):
    queryset = Rate.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = RateSerializer

    def get(self, request):
        queryset = Rate.objects.all()
        serializer = RateSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data,status=status.HTTP_200_OK)


    def post(self, request):
        serializer = RateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


class RateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET rate/:id/
    PUT rate/:id/
    DELETE rate/:id/
    """
    queryset = Rate.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = RateSerializer

    def get(self, request,id_rate):
        a_rate = get_object_or_404(Rate, pk=id_rate)
        serializer = RateSerializer(a_rate)
        return Response(data=serializer.data,status=status.HTTP_200_OK)


    def patch(self, request, id_rate):
        a_rate = get_object_or_404(Rate, pk=id_rate)
        serializer = RateSerializer(a_rate, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, id_rate):
        a_rate = get_object_or_404(pk=id_rate)
        a_rate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class RateFromEventView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = RateSerializer

    def get(self, request, id_event):
        rates = self.queryset.filter(event=id_event)
        serializer = RateSerializer(rates, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ListEventAttendeeView(generics.ListAPIView):
    queryset = EventAttendee.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = EventAttendeeSerializer

    def get(self, request):
        queryset = EventAttendee.objects.all()
        serializer = EventAttendeeSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AttendeeView(generics.ListAPIView):
    queryset = EventAttendee.objects.all()
    serializer_class = EventAttendeeSerializer

    def post(self, request, id_event):
        a_event = get_object_or_404(Event, pk=id_event)
        EventAttendee.objects.create(user=request.user, event=a_event)
        return Response(status=status.HTTP_201_CREATED)


    "UnAttend function"

    def delete(self, request, id_event):
        event = get_object_or_404(Event, pk=id_event)
        a_attendee = self.queryset.get(event=event, user=request.user)
        a_attendee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
