from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('solomon_comm.views',
    url('^$', 'user'),
)
