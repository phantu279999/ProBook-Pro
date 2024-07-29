from django.urls import path
from . import views

app_name = 'news'


urlpatterns = [
	path('', views.home_news, name="home_news"),
	path("news/<str:url>/", views.detail_news, name='detail_news'),
	path("news-category/<int:pk>/", views.news_category, name='news_category')
]
