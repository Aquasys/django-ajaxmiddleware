from django import http
from django.utils.simplejson import dumps
from django.utils.translation import ugettext as _


class JSONResponseMixin(object):
    """Response Mixin which takes care of dumping the context in json format,
    and return the correct HttpResponse"""

    def render_to_response(self, context, *args, **kwargs):
        """Returns a JSON response containing 'context' as payload"""
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        """Construct an `HttpResponse` object."""
        return http.HttpResponse(content, content_type='application/json',
            **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        """If the context hasn't been dumped in the get_json_context,
        Convert the context dictionary into a JSON object"""
        if type(context) == str:
            """context has already been dumped"""
            return context
        return dumps(context)


class BaseListViewMixin(object):
    """Override the django BaseListView's get and post functions"""

    def get(self, cls, request, *args, **kwargs):
        cls.object_list = cls.get_queryset()
        allow_empty = cls.get_allow_empty()
        if not allow_empty and len(cls.object_list) == 0: raise http.Http404(
                _(u"Empty list and '%(class_name)s.allow_empty' is "
                "False.") % {'class_name': cls.__class__.__name__},
            )
        kwargs.update({"object_list": cls.object_list})
        return cls, kwargs


class BaseCreateViewMixin(object):
    """Override the django BaseCreateView's get and post functions"""

    def get(self, cls, request, *args, **kwargs):
        cls.object = None
        kwargs.update({"object" : cls.object})
        return cls, kwargs


class BaseUpdateViewMixin(object):
    """Override the django BaseUpdateView's get and post functions"""

    def get(self, cls, request, *args, **kwargs):
        cls.object = cls.get_object()
        kwargs.update({"object" : cls.object})
        return cls, kwargs


class ProcessFormViewMixin(object):
    """Override the django ProcessFormView's get and post functions"""

    def get(self, cls, request, *args, **kwargs):
        form_class = cls.get_form_class()
        kwargs.update({"form" : cls.get_form(form_class)})
        return cls, kwargs


class BaseDetailViewMixin(object):
    """Override the django BaseDetailView's get and post functions"""

    def get(self, cls, request, *args, **kwargs):
        cls.object = cls.get_object()
        kwargs.update({"object" : cls.object})
        return cls, kwargs
