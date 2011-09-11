import json
import logging

from django.template.response import TemplateResponse

logger = logging.getLogger(__name__.split(".")[0])


def html_ajax_test(orig_test=None, url=None):
    """decorator used by tests to verify that http or json requests
    return the appropriate response"""
    def _decorated(test_func):
        def _test_html_get(self):
            response = self.client.get(url)
            self.assertRaises(ValueError, json.loads, response.content)
            self.assertIsInstance(response, TemplateResponse)
            logger.info("\nhtml:\t%s" % ", ".join(response.template_name))

        def _test_html_post(self):
            pass

        def _test_ajax_get(self):
            response = self.client.get(url, CONTENT_TYPE="application/json")
            self.assertNotIsInstance(response, TemplateResponse)
            self.assertIsInstance(json.loads(response.content), dict)
            logger.info("\njson:\t%s" % response.content)
            # Execute the rest of the test
            return test_func(self)

        def _test_ajax_post(self):
            pass

        def _test(self):
            _test_html_get(self)
            _test_html_post(self)
            _test_ajax_get(self)
            _test_ajax_post(self)

        for attr in ["__name__", "__dict__", "__doc__"]:
            setattr(_test, attr, getattr(test_func, attr))
        return _test

    if orig_test is None:
        return _decorated
    else:
        return _decorated(orig_test)
