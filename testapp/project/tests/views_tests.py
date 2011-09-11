import json

from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.test import TestCase


class ViewsTestCase(TestCase):
    """tests for django 1.3 generic class based views"""

    def test_templateview(self):
        """Test that django.views.generic.View return a json"""
        url = reverse("template_view")
        response = self.client.get(url)
        # normal request
        self.assertRaises(ValueError,json.loads, response.content)
        self.assertIsInstance(response, TemplateResponse)
        # ajax request
        response = self.client.get(url, CONTENT_TYPE="application/json")
        self.assertNotIsInstance(response, TemplateResponse)
        self.assertIsInstance(json.loads(response.content), dict)
