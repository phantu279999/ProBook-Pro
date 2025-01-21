from django.urls import path, include
from rest_framework.authtoken import views

from news.api.views import NewsListView, NewsDetailView

urlpatterns = [
    path('news/', NewsListView.as_view(), name='api_list_news'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='api_detail_news')
]

urlpatterns += [
    path('auth/', include('rest_framework.urls')),
    path("token-auth/", views.obtain_auth_token),
]