from django.urls import path
from .views import create_post, feed, like_post

urlpatterns = [
    path('create/', create_post, name='create_post'),
    path('feed/', feed, name='feed'),
    path('like/', like_post, name='like'),
]