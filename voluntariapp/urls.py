# voluntariapp/urls.py
from django.urls import include, path
from . import views

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('user', views.UserListView.as_view()),
    path('event', views.EventListView.as_view()),
]