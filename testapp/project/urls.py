from django.conf.urls.defaults import patterns, url

from views import *  # NOQA


urlpatterns = patterns('',
    url(r'^about/$', AboutView.as_view(), name="template_view"),
    url(r'^details/(?P<pk>\d+)/$', DetailView.as_view(), name="details_view"),
    url(r'^list/$', ListView.as_view(), name="list_view"),
)
