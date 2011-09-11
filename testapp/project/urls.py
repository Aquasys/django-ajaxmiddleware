from django.conf.urls.defaults import patterns, url

from views import *  # NOQA


urlpatterns = patterns('',
    url(r'^templateview/$', AboutView.as_view(), name="template_view"),
)
