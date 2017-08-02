from django.http import HttpResponse


def index(request): return HttpResponse("Hello, world. You're at the polls index.")`


add new polls / urls.py with content: `from django.conf.urls import url
from . import views

urlpatterns = [url(r'^$', views.index, name='index'), ]
