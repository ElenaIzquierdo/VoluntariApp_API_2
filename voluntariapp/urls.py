# voluntariapp/urls.py
from django.conf.urls import url
from django.urls import include, path
from . import views
from rest_framework.documentation import include_docs_urls

urlpatterns = [

    path('rest-auth/', include('rest_auth.urls')),
    path('user', views.UserListView.as_view()),

    path('event', views.EventListView.as_view()),
    path('event/<id_event>', views.EventDetailView.as_view(), name="comments-detail"),

    path('forum', views.ForumThemeListView.as_view(), name="forum"),
    path('forum/<id_forumtheme>', views.ForumThemeDetailView.as_view(), name="forumtheme-detail"),

    path('comment', views.ListCommentView.as_view(), name="comments-all"),
    path('comment/<id_rate>', views.CommentDetailView.as_view(), name="comments-detail"),
    path('comment/forum/<id_forumtheme>', views.CommentFromThemeView.as_view(), name="comments-from-theme"),

    path('rate', views.ListRateView.as_view(), name="rate-all"),
    path('rate/<id_rate>', views.RateDetailView.as_view(), name="rate-detail"),
    path('rate/event/<id_event>', views.RateFromEventView.as_view(), name="rate-from-event"),

    path('eventattendee', views.ListEventAttendeeView.as_view(), name="eventattendee-all"),
    path('event/<int:pk>/attendee', views.AttendeeView.as_view(), name="eventattendee-detail"),
]