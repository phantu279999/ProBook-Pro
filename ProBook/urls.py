from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
	path('', include('myapp.urls')),
	path('news/', include('news.urls')),
	path('accounts/', include('accounts.urls')),
	path('admin/', admin.site.urls),
	path('api/v1/', include('news.api.urls'))
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
