import logging
import sys
if sys.version_info < (2, 7):
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict

from django.views.generic.detail import BaseDetailView
from django.views.generic.edit import BaseCreateView, BaseUpdateView,\
                                      ProcessFormView
from django.views.generic.list import BaseListView

from mixins import JSONResponseMixin, BaseListViewMixin, BaseUpdateViewMixin,\
    BaseCreateViewMixin, BaseDetailViewMixin, ProcessFormViewMixin

logger = logging.getLogger("ajaxmiddleware")


def get_hybridview(newcls):
    """lambda-like function to create a view inheriting our callback"""

    class HybridView(newcls, JSONResponseMixin):
        """Middleware class which add the JSONResponseMixin in the view to
        handle ajax requests"""

        def __init__(self, *args, **kwargs):
            """Our newcls can be an instance of several mixins working with the
            get and post functions.
            e.g : CreateView is instance of BaseCreateView and ProcessFormView
            Let's add our custom mixins that implement get and post without
            returning a render_to_response, and call """

            newcls.__init__(self, **kwargs)
            # The order matters for the get/post calls.
            self.mixins = OrderedDict()
            self.mixins[BaseListView] = BaseListViewMixin
            self.mixins[BaseCreateView] = BaseCreateViewMixin
            self.mixins[BaseUpdateView] = BaseUpdateViewMixin
            self.mixins[BaseDetailView] = BaseDetailViewMixin
            self.mixins[ProcessFormView] = ProcessFormViewMixin
            [self.mixins.pop(baseView) for baseView in self.mixins.iterkeys()
                if not isinstance(self, baseView)]

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
            call super is not an option, as they return a render_to_response

            To remedy this problem, Mixins have been written for each of these
            parents which contain a get or post funcfion, and return context
            instead of a response
            """
            for mixin in self.mixins.itervalues():
                self, kwargs = mixin().get(self, request, *args, **kwargs)

            context = getattr(self, ["get_context_data", "get_json_context",
                ][self.is_ajax])(**kwargs)
            return self.render_to_response(context)

        def post(self, request, *args, **kwargs):
            """Hybrid post to handle all parents post actions"""

            if isinstance(self, BaseUpdateView):
                self.object = self.get_object()

            if isinstance(self, ProcessFormView):
                form_class = self.get_form_class()
                kwargs.update({"form" : self.get_form(form_class)})
                # TODO form_valid or form_invalid for render_to_response

            # TODO return self.delete(*args, **kwargs)

            context = getattr(self, ["get_context_data", "get_json_context",
                ][self.is_ajax])(**kwargs)
            return self.render_to_response(context)


    return HybridView.as_view()
