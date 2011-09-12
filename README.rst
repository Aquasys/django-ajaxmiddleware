=====================
django-ajaxmiddleware
=====================


To develop a website with progressive enhancement means being able to return a
basic page for non-js clients, and ajax responses to enhance the design when
javascript is enabled on the client.

Your views have to render html or json depending if the request is text/html or
application/json.

Today, tons of solutions exist, and every developer cook its own way to handle
that.

This application remove the pain to handle this.

Installation
============

First, install the application::

    $ pip install django-ajaxmiddleware

.. alert:: while it's in a early stage, I'd recommend to pull from github instead::

    $ pip install -e git+https://Fandekasp@github.com/Fandekasp/django-ajaxmiddleware.git#egg=ajaxmiddleware

Then, add the new middleware in your settings::

    from django.conf.global_settings import MIDDLEWARE_CLASSES
    MIDDLEWARE_CLASSES += ('ajaxmiddleware.middleware.AjaxMiddleware',)

Finally, add in your view a get_json_context function::

    from django.views.generic import CreateView

    class FoobarCreateView(CreateView):
        def get_json_context(self, **kwargs):
            return {
                "foo": "bar",
            }

Your view is now able to return the json context if called from a ajax request.

For the url::

    url(r'foobar/create/', FoobarCreateView.as_view())

You can verify the json response with curl::

    $ curl -X GET -H 'Content-type: application/json' http://uri/foobar/create/
    {"foo": "bar"}
    $

.. TIP:: If you test a view which requires login, you can add a "**curl**" value
    in your post data, and the middleware will disable the csrf check for you::

    $ curl -d "username=bobthesponge&password=test123&curl" -L -H 'Content-type: application/json' http://127.0.0.1:8000/accounts/login/\?next\=/testview/


Limitations
===========

* Currently work only for django >= 1.3 with class-based views.


TODO
====

* allow a get_json_response or a convert_context_to_json
* write tests to cover Date-based views


BONUS
=====

You can use the decorator ajaxmiddleware.decorators.html_ajax_test for your own
tests to insure html and ajax requests are covered correctly::

    from django.core.urlresolvers import reverse
    from django.test import TestCase
    from ajaxmiddleware.decorators import html_ajax_test


    class ViewsTestCase(TestCase):

        @html_ajax_test(url="/some/url/"))
        def test_templateview(self):
            """Tests for TemplateView with html and ajax requests"""
            pass

        @html_ajax_test(url=lambda: reverse("another_url"))
        def test_detailview(self):
            """Isn't it nicer to give a reverse url to the decorator ?"""
            pass

.. note:: This will only test GET requests

You can also add the *ajaxmiddleware* logger to get a verbose output while
running these tests (see ``testapp.settings.LOGGING``)
