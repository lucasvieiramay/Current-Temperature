from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^api/', include('searches.urls')),
    url(r'^admin/', admin.site.urls),
]
