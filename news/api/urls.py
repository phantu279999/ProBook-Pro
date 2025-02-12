from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from news.api.views import NewsViewSet, CategoryViewSet



router = DefaultRouter()
router.register('news', NewsViewSet)
router.register('category', CategoryViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    path("token-auth/", views.obtain_auth_token),
]
