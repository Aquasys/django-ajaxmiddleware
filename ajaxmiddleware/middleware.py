from views import get_hybridview


class AjaxMiddleware(object):
    """
    Middleware to handle ajax requests and return a json response for each view
    implementing a get_json_context function.
    """

    def process_view(self, request, callback, callback_args, callback_kwargs):
        module = callback.func_closure[1].cell_contents.__module__
        func_name = callback.func_name

        try:
            import imp
            funcm = imp.find_module(module.split(".")[0])
            module = imp.load_module(module, *funcm)
            OriginalView = getattr(module, func_name)
        except ImportError:
            OriginalView = getattr(
                __import__(module, globals(), locals(), [func_name, ], -1),
                func_name,
            )

        if getattr(OriginalView, "get_json_context", False):

            new_callback = get_hybridview(OriginalView)
            return new_callback(request, *callback_args, **callback_kwargs)

        return None
