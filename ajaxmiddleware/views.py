from django import http
from django.utils.simplejson import dumps
from django.utils.translation import ugettext as _
from django.views.generic.edit import BaseCreateView, BaseUpdateView,\
                                      ProcessFormView
from django.views.generic.list import BaseListView


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


def get_hybridview(newcls):
    """lambda-like function to create a view inheriting our callback"""

    class HybridView(newcls, JSONResponseMixin):
        """Middleware class which add the JSONResponseMixin in the view to
        handle ajax requests"""

        @property
        def is_ajax(self):
            """Check the META HTTP_X_REQUESTED_WITH and CONTENT_TYPE"""
            meta = self.request.META
            return meta.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'\
                or "json" in meta.get("CONTENT_TYPE")

        def render_to_response(self, context):
            cls = type(self).__bases__[self.is_ajax]
            return cls.render_to_response(self, context)

        def get(self, request, *args, **kwargs):
            """As we override the parents' get, we need to redo their job here.
            call super is not an option, as they return a render_to_response"""

            self.object = None
            if isinstance(self, BaseUpdateView):
                self.object = self.get_object()
            if isinstance(self, BaseListView):
                self.object_list = self.get_queryset()
                allow_empty = self.get_allow_empty()
                if not allow_empty and len(self.object_list) == 0:
                    raise http.Http404(
                        _(u"Empty list and '%(class_name)s.allow_empty' is "
                        "False.") % {'class_name': self.__class__.__name__},
                    )
                kwargs.update({"object_list": self.object_list})
            if isinstance(self, ProcessFormView):
                form_class = self.get_form_class()
                kwargs.update({"form" : self.get_form(form_class)})

            context = getattr(self, ["get_context_data", "get_json_context",
                ][self.is_ajax])(**kwargs)
            return self.render_to_response(context)

    return HybridView.as_view()
