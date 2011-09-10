from django import http
from django.utils.simplejson import dumps


class JSONResponseMixin(object):

    def render_to_response(self, context, *args, **kwargs):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content, content_type='application/json',
            **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        return dumps(context)


def get_hybridview(newcls):
    class HybridView(newcls, JSONResponseMixin):
        @property
        def is_ajax(self):
            return "json" in self.request.META.get("CONTENT_TYPE")

        def render_to_response(self, context):
            cls = type(self).__bases__[self.is_ajax]
            return cls.render_to_response(self, context)

        def get(self, request, *args, **kwargs):
            if self.is_ajax:
                context = self.get_json_context()
            else:
                # BaseCreateView.get or BaseUpdateView.get
                self.object = self.queryset and self.get_object()
                # ProcessFormView.get
                form_class = self.get_form_class()
                form = self.get_form(form_class)
                context = self.get_context_data(form=form)
            return self.render_to_response(context)

    return HybridView.as_view()
