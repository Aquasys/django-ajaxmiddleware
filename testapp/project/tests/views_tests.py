
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
        """Tests for TemplateView with html and ajax requests"""
        pass

    @html_ajax_test(url=reverse("details_view", args=(1, )))
    def test_detailview(self):
        """Tests for DetailView with html and ajax requests"""
        pass

    @html_ajax_test(url=reverse("list_view"))
    def test_listview(self):
        """Tests for ListView with html and ajax requests"""
        pass

    @html_ajax_test(url=reverse("form_view"))
    def test_formview(self):
        """Tests for FormView with html and ajax requests"""
        pass
