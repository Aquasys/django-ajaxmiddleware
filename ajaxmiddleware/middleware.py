from django.conf import settings

from views import get_hybridview


class AjaxMiddleware(object):
    """
    Middleware to handle ajax requests and return a json response for each view
    implementing a get_json_context function.
    """

    def process_request(self, request):
        if settings.DEBUG and "curl" in request.REQUEST:
            setattr(request, '_dont_enforce_csrf_checks', True)

    def process_view(self, request, callback, callback_args, callback_kwargs):
        """Check the type of the callback before processing it.
        A class-based view will at this step be a function (maybe I can
        improve this later from the process_request function).
        """
        OriginalView = callback
        if getattr(callback, "func_closure", None) and\
                len(callback.func_closure) == 2:
            """hasattr is not enough, as we can get an empty func_closure with
            the callback.
            If we get more than 2 arguments in the func_closure, then it's a
            redirection like a login for a permission_required decored view
            """
            module = callback.func_closure[1].cell_contents.__module__
            func_name = callback.func_name

            try:
                import imp
                funcm = imp.find_module(module.split(".")[0])
                module = imp.load_module(module, *funcm)
                OriginalView = getattr(module, func_name, None)
            except ImportError:
                OriginalView = getattr(
                    __import__(module, globals(), locals(), [func_name, ], -1),
                    func_name,
                )
        if hasattr(OriginalView, "get_json_context"):
            new_callback = get_hybridview(OriginalView)
            return new_callback(request, *callback_args, **callback_kwargs)

        return None
