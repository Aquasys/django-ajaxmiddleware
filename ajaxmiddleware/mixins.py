from django import http
#from django.http import HttpResponseRedirect
from django.utils.simplejson import dumps
from django.utils.translation import ugettext as _


class JSONResponseMixin(object):
    """Response Mixin which takes care of dumping the context in json format,
    and return the correct HttpResponse"""

    def render_to_response(self, context, *args, **kwargs):
        """Returns a JSON response containing 'context' as payload"""
        post_actions = context.pop("post_actions", None)
        if post_actions:
            #if "success_url" in post_actions:
                #return HttpResponseRedirect(post_actions["success_url"])
            if "form_is_valid" in post_actions:
                #if post_actions["form_is_valid"]:
                    #return HttpResponseRedirect(self.get_success_url())
                if not post_actions["form_is_valid"]:
                    context.update({
                        "errors": context["form"].errors,
                    })
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

    def get(self, cls, **kwargs):
        cls.object_list = cls.get_queryset()
        allow_empty = cls.get_allow_empty()
        if not allow_empty and len(cls.object_list) == 0:
            raise http.Http404(
                _(u"Empty list and '%(class_name)s.allow_empty' is "
                "False.") % {'class_name': cls.__class__.__name__},
            )
        kwargs.update({"object_list": cls.object_list})
        return cls, kwargs


class BaseCreateViewMixin(object):
    """Override the django BaseCreateView's get and post functions"""

    def get(self, cls, **kwargs):
        cls.object = None
        kwargs.update({"object": cls.object})
        return cls, kwargs

    post = get


class BaseUpdateViewMixin(object):
    """Override the django BaseUpdateView's get and post functions"""

    def get(self, cls, **kwargs):
        cls.object = cls.get_object()
        kwargs.update({"object": cls.object})
        return cls, kwargs

    post = get


class ProcessFormViewMixin(object):
    """Override the django ProcessFormView's get and post functions"""

    def get(self, cls, **kwargs):
        form_class = cls.get_form_class()
        kwargs.update({"form": cls.get_form(form_class)})
        return cls, kwargs

    def post(self, cls, **kwargs):
        form_class = cls.get_form_class()
        form = cls.get_form(form_class)
        kwargs.update({"form": form})
        kwargs.update({"post_actions": {
            "form_is_valid": form.is_valid(),
        }})
        return cls, kwargs


class BaseDetailViewMixin(object):
    """Override the django BaseDetailView's get and post functions"""

    def get(self, cls, **kwargs):
        cls.object = cls.get_object()
        kwargs.update({"object": cls.object})
        return cls, kwargs


class BaseDeleteViewMixin(object):
    """Override the django BaseDeleteView's get and post functions"""

    def get(self, cls, **kwargs):
        return cls, kwargs

    def post(self, cls, **kwargs):
        cls.object = cls.get_object()
        cls.object.delete()
        kwargs.update({
            "post_actions": {
                "success_url": cls.get_success_url(),
            },
            "message": "Object delete !",
        })
        return cls, kwargs
