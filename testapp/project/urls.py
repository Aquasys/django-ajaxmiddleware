# flake8: noqa
from django.conf.urls.defaults import patterns, url

from views import *


urlpatterns = patterns('',
    url(r'^about/$', SomeTemplateView.as_view(), name="template_view"),
    url(r'^details/(?P<pk>\d+)/$', SomeDetailView.as_view(), name="details_view"),
    url(r'^list/$', SomeListView.as_view(), name="list_view"),
    url(r'^form/$', SomeFormView.as_view(), name="form_view"),
    url(r'^create/$', SomeCreateView.as_view(), name="create_view"),
    url(r'^update/(?P<pk>\d+)/$', SomeUpdateView.as_view(), name="update_view"),
    url(r'^delete/(?P<pk>\d+)/$', SomeDeleteView.as_view(), name="delete_view"),
)
