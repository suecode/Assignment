from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^travels$', views.index),
    url(r'^add$', views.add),
    url(r'^process$', views.process),
    url(r'^logout$', views.logout),
    url(r'^destination/(?P<trip_id>\d+)$', views.destination),
    url(r'^destination/join/(?P<trip_id>\d+)$', views.join),
]
