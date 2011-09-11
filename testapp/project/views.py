from django.views.generic import *  # NOQA

from forms import SomeForm
from models import User


class SomeTemplateView(TemplateView):
    template_name = "project/about.html"
    default_context = {
        "bodyclass": "about",
        "object": {
            "name": "About",
            "description": "Life is harsh",
        },
    }

    def get_json_context(self, **kwargs):
        return self.default_context

    def get_context_data(self, **kwargs):
        return self.default_context


class SomeDetailView(DetailView):
    template_name = "project/about.html"
    model = User

    def get_json_context(self, **kwargs):
        """get User object, return its fields name and value"""
        userdict = self.model.objects.get(**kwargs).__dict__
        userdict.pop("_state")  # can't dump a django.db.models.base.ModelState
        return userdict

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context.update({
            "bodyclass": "details",
        })
        return context


class SomeListView(ListView):
    template_name = "project/list.html"
    model = User
    context_object_name = "users"

    def get_json_context(self, **kwargs):
        """get User object, return its fields name and value"""
        return {}

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context.update({
            "bodyclass": "lists",
        })
        return context


class SomeFormView(FormView):
    template_name = "project/user_form.html"
    form_class = SomeForm

    def get_json_context(self, **kwargs):
        """get User object, return its fields name and value"""
        return {}

    def get_context_data(self, **kwargs):
        context = super(FormView, self).get_context_data(**kwargs)
        context.update({
            "bodyclass": "form",
        })
        return context


class SomeCreateView(CreateView):
    model = User

    def get_json_context(self, **kwargs):
        """get User object, return its fields name and value"""
        return {}

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context.update({
            "bodyclass": "create",
        })
        return context
