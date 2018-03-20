from django.conf.urls import url
from searches import views

urlpatterns = [
    url(r'^$', views.search_zip),
    url(r'list-logs', views.list_logs),
]
