# voluntariapp/urls.py
from django.urls import include, path
from . import views

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('user', views.UserListView.as_view()),

    path('event', views.EventListView.as_view()),
    path('event/<int:pk>', views.EventDetailView.as_view(), name="comments-detail"),

    path('forum', views.ForumThemeListView.as_view(), name="forum"),
    path('forum/<int:pk>', views.ForumThemeDetailView.as_view(), name="forumtheme-detail"),

    path('comment', views.ListCommentView.as_view(), name="comments-all"),
    path('comment/<int:pk>', views.CommentDetailView.as_view(), name="comments-detail"),
    path('comment/forum/<int:pk>', views.CommentFromIssueView.as_view(), name="comments-from-issue"),
]