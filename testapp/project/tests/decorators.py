import json

from django.template.response import TemplateResponse


def html_ajax_test(orig_test=None, url=None):
    """decorator used by tests to verify that http or json requests
    return the appropriate response"""
    def _decorated(test_func):
        def _test(self):
            # normal request
            response = self.client.get(url)
            self.assertRaises(ValueError, json.loads, response.content)
            self.assertIsInstance(response, TemplateResponse)
            # ajax request
            response = self.client.get(url, CONTENT_TYPE="application/json")
            self.assertNotIsInstance(response, TemplateResponse)
            self.assertIsInstance(json.loads(response.content), dict)
            print response.content
            # Execute the rest of the test
            return test_func(self)

        for attr in ["__name__", "__dict__", "__doc__"]:
            setattr(_test, attr, getattr(test_func, attr))
        return _test

    if orig_test is None:
        return _decorated
    else:
        return _decorated(orig_test)
