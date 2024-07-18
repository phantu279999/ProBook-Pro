from django.urls import path
from . import views


urlpatterns = [
	path("", views.index, name='index'),
	path("video-youtube/", views.crawl_video_youtube, name='video_youtube'),
]