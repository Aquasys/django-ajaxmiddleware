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

    $ pip install -e git+https://github.com/Fandekasp/django-ajaxmiddleware#egg=ajaxmiddleware

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


Limitations
===========

* Currently work only for django >= 1.3 with class-based views.

TODO
====

* allow a get_json_response or a convert_context_to_json
* write tests to cover all generic class-based views
