import json

from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.test import TestCase


class ViewsTestCase(TestCase):
    """
    Tests for django 1.3 generic class based views
    View ignored::

        View: Mother view, doesn't handle response
        RedirectView
    """

    def __ajaxtest(self, url, response):
        """private function used by tests"""
        # normal request
        self.assertRaises(ValueError, json.loads, response.content)
        self.assertIsInstance(response, TemplateResponse)
        # ajax request
        response = self.client.get(url, CONTENT_TYPE="application/json")
        self.assertNotIsInstance(response, TemplateResponse)
        self.assertIsInstance(json.loads(response.content), dict)
        print response.content

    def test_templateview(self):
        """Test that the generic TemplateView handle html and json responses"""
        url = reverse("template_view")
        response = self.client.get(url)
        self.__ajaxtest(url, response)

    def test_detailview(self):
        """Test that the generic DetailView handle html and json responses"""
        url = reverse("details_view", args=(1, ))
        response = self.client.get(url)
        self.__ajaxtest(url, response)
