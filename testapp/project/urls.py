from django.conf.urls.defaults import patterns, url

from views import *  # NOQA


urlpatterns = patterns('',
    url(r'^about/$', SomeTemplateView.as_view(), name="template_view"),
    url(r'^details/(?P<pk>\d+)/$', SomeDetailView.as_view(), name="details_view"),
    url(r'^list/$', SomeListView.as_view(), name="list_view"),
    url(r'^form/$', SomeFormView.as_view(), name="form_view"),
)
