
from django.core.urlresolvers import reverse
from django.test import TestCase

from decorators import html_ajax_test


class ViewsTestCase(TestCase):
    """
    Tests for django 1.3 generic class based views
    View ignored::

        View: Mother view, doesn't handle response
        RedirectView
    """

    @html_ajax_test(url=reverse("template_view"))
    def test_templateview(self):
        pass

    @html_ajax_test(url=reverse("details_view", args=(1, )))
    def test_detailview(self):
        pass

    @html_ajax_test(url=reverse("list_view"))
    def test_listview(self):
        pass
