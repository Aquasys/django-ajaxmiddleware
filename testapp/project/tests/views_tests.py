import json
import logging

from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.test import TestCase

from ajaxmiddleware.decorators import html_ajax_test
from project.models import User

logger = logging.getLogger("ajaxmiddleware")


class ViewsTestCase(TestCase):
    """
    Tests for django 1.3 generic class based views
    View ignored::

        View: Mother view, doesn't handle response
        RedirectView
    """

    @html_ajax_test(url=lambda: reverse("template_view"))
    def test_templateview(self):
        """Tests for TemplateView with html and ajax requests"""
        pass

    @html_ajax_test(url=lambda: reverse("details_view", args=(1, )))
    def test_detailview(self):
        """Tests for DetailView with html and ajax requests"""
        pass

    @html_ajax_test(url=lambda: reverse("list_view"))
    def test_listview(self):
        """Tests for ListView with html and ajax requests"""
        pass

    @html_ajax_test(url=lambda: reverse("form_view"))
    def test_formview(self):
        """Tests for FormView with html and ajax requests"""
        pass

    @html_ajax_test(url=lambda: reverse("create_view"))
    def test_createview(self):
        """Tests for CreateView with html and ajax requests"""
        pass

    # give hard-coded url to the decorator
    @html_ajax_test(url=reverse("update_view", args=(1, )))
    def test_updateview(self):
        """Tests for UpdateView with html and ajax requests"""
        pass

    @html_ajax_test(url=reverse("delete_view", args=(1, )))
    def test_deleteview(self):
        """Tests for DeleteView with html and ajax requests"""
        self.assertEqual(User.objects.count(), 2)
        # http post
        url = reverse("delete_view", args=(1, ))
        response = self.client.post(url, follow=True)
        self.assertRaises(ValueError, json.loads, response.content)
        self.assertIsInstance(response, TemplateResponse)
        self.assertEqual(User.objects.count(), 1)
        logger.info("\nhtml post:\t%s" % ", ".join(response.template_name))
        # ajax post
        url = reverse("delete_view", args=(2, ))
        response = self.client.post(url, follow=True,\
            CONTENT_TYPE="application/json")
        self.assertNotIsInstance(response, TemplateResponse)
        self.assertIsInstance(json.loads(response.content), dict)
        #self.assertContains(response, "message")
        self.assertEqual(User.objects.count(), 0)
        logger.info("\najax post:\t%s" % response.content)
