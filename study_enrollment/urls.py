from django.conf.urls import patterns, url

from study_enrollment import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)