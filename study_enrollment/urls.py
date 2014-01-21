from django.conf.urls import patterns, url

from study_enrollment import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^requirements', views.RequirementsView.as_view(), name='requirements'),
    url(r'^start', views.StartView.as_view(), name='start'),
)
