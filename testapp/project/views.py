from django.views.generic import *  # NOQA


class AboutView(TemplateView):
    template_name = "project/about.html"
    default_context = {
        "bodyclass": "about",
        "object": {
            "name": "Bob the Sponge",
            "description": "Some anime character",
        },
    }

    def get_json_context(self, **kwargs):
        return self.default_context

    def get_context_data(self, **kwargs):
        return self.default_context
