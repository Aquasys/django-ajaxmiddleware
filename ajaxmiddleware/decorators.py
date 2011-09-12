import json
import logging

from django.template.response import TemplateResponse

logger = logging.getLogger(__name__.split(".")[0])


def html_ajax_test(orig_test=None, url=None):
    """
    Decorator used by tests to verify that http or json requests
    return the appropriate response
    Works for get requests only, post requests are too particular
    """
    def _decorated(test_func):
        def _test_html_get(self, url):
            response = self.client.get(url, follow=True)
            self.assertRaises(ValueError, json.loads, response.content)
            self.assertIsInstance(response, TemplateResponse)
            logger.info("\nhtml get:\t%s" % ", ".join(response.template_name))

        def _test_ajax_get(self, url):
            response = self.client.get(url, follow=True,\
                CONTENT_TYPE="application/json")
            self.assertNotIsInstance(response, TemplateResponse)
            self.assertIsInstance(json.loads(response.content), dict)
            logger.info("\najax get:\t%s" % response.content)

        def _set_url(self, url):
            """
            An url argument is mandatory for the html_ajax_test decorator
            You can give a hard-coded url, or a much nicer reverse with a
            lambda. e.g: url=lambda: reverse("some_url")
            """
            if not url:
                raise AttributeError("html_ajax_test requires an 'url' "
                    "argument, string or lambda")
            if not isinstance(url, str):
                return url()
            return url

        def _test(self):
            """Call the 4 tests, then run the normal tests"""
            processed_url = _set_url(self, url)
            _test_html_get(self, processed_url)
            _test_ajax_get(self, processed_url)
            # Execute the rest of the test
            return test_func(self)

        for attr in ["__name__", "__dict__", "__doc__"]:
            setattr(_test, attr, getattr(test_func, attr))
        return _test

    if orig_test is None:
        return _decorated
    else:
        return _decorated(orig_test)
