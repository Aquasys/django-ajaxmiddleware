import logging
import sys
if sys.version_info < (2, 7):
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict

from django.views.generic.detail import BaseDetailView
from django.views.generic.edit import BaseCreateView, BaseUpdateView,\
                                      ProcessFormView, BaseDeleteView
from django.views.generic.list import BaseListView

from mixins import JSONResponseMixin, BaseListViewMixin, BaseUpdateViewMixin,\
            BaseCreateViewMixin, BaseDetailViewMixin, ProcessFormViewMixin,\
            BaseDeleteViewMixin

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
            self.mixins[BaseDeleteView] = BaseDeleteViewMixin
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

        def get(self, request, **kwargs):
            if not self.is_ajax:
                "If it's not ajax, return the inherited get"
                return super(HybridView, self).get(self, **kwargs)

            for mixin in self.mixins.itervalues():
                self, kwargs = mixin().get(self, **kwargs)

            context = kwargs
            context.update(self.get_json_context(**kwargs))
            context.pop("form", None)
            context.pop("object", None)
            context.pop("object_list", None)
            return self.render_to_response(context)

        def post(self, request, **kwargs):
            """Hybrid post to handle all parents post actions"""
            if not self.is_ajax:
                "If it's not ajax, return the inherited get"
                return super(HybridView, self).post(self, **kwargs)

            for mixin in self.mixins.itervalues():
                try:
                    self, kwargs = mixin().post(self, **kwargs)
                except AttributeError:
                    """The inherited view doesn't handle post"""
                    pass

            context = kwargs
            context.update(self.get_json_context(**kwargs))
            context.pop("form", None)
            return self.render_to_response(context)

    return HybridView.as_view()
