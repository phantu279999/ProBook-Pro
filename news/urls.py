from django.urls import path
from . import views

app_name = 'news'


urlpatterns = [
	path('', views.home_news, name="home_news")
]
