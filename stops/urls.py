from django.conf.urls import url
from stops import views

urlpatterns = [
    url(r'^',  views.map_show, name='stops'),
]