from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from .settings import DEBUG


urlpatterns = [
    path('', include('weather.urls'))
]
if DEBUG:
     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()

