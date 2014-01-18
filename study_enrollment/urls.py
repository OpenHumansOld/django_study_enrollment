from django.conf.urls import patterns, url

from study_enrollment import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^requirements', views.requirements, name='requirements'),
    url(r'^start', views.start, name='start'),
)
