from views import JSONResponseMixin


class AjaxMiddleware(object):
    """
    Middleware to handle ajax requests and return a json response for each view
    implementing a get_json_context OriginalViewtion
    """

    #def __init__(self, *args, **kwargs):
    #def process_request(self, request):
        #pass

    def process_view(self, request, callback, callback_args, callback_kwargs):
        module = callback.func_closure[1].cell_contents.__module__
        func_name = callback.func_name
        #OriginalView = getattr(
            #__import__(module, globals(), locals(), [func_name, ], -1),
            #func_name,
        #)
        import imp
        funcm = imp.find_module(module.split(".")[0])
        module = imp.load_module(module, *funcm)
        OriginalView = getattr(module, func_name)

        if getattr(OriginalView, "get_json_context", False):
            class HybridView(OriginalView, JSONResponseMixin):

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


            new_callback = HybridView.as_view()
            return new_callback(request, *callback_args, **callback_kwargs)

        return None
