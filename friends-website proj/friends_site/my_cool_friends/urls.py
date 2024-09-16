from django.urls import path

from . import views


urlpatterns = [

    path("", views.home_page),
    path("<str:friendName>", views.friend_page, name='friend_page'),

]