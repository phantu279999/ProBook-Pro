from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
	path('', include('myapp.urls')),
    path('admin/', admin.site.urls),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)