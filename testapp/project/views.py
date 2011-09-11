from django.core.urlresolvers import reverse
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
    default_context = {"bodyclass": "detail"}

    def get_json_context(self, **kwargs):
        """We receive the object as kwargs, return the fields we're interested
        on"""
        context = kwargs.get("object").__dict__
        context.pop("_state")  # ModelState object
        context.update(self.default_context)
        return context

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context.update(self.default_context)
        return context


class SomeListView(ListView):
    template_name = "project/list.html"
    model = User
    context_object_name = "users"
    default_context = {"bodyclass": "list"}

    def get_json_context(self, **kwargs):
        """get User object, return its fields name and value"""
        user_list = kwargs.get("object_list")
        context = dict(("name", u.name) for u in user_list)
        context.update(self.default_context)
        return context

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context.update(self.default_context)
        return context


class SomeFormView(FormView):
    template_name = "project/user_form.html"
    form_class = SomeForm
    default_context = {"bodyclass": "form"}

    def get_json_context(self, **kwargs):
        """get User object, return its fields name and value"""
        return self.default_context

    def get_context_data(self, **kwargs):
        context = super(FormView, self).get_context_data(**kwargs)
        context.update(self.default_context)
        return context


class SomeCreateView(CreateView):
    model = User
    default_context = {"bodyclass": "create"}

    def get_json_context(self, **kwargs):
        """get User object, return its fields name and value"""
        return self.default_context

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context.update(self.default_context)
        return context


class SomeUpdateView(UpdateView):
    model = User
    default_context = {"bodyclass": "update"}

    def get_json_context(self, **kwargs):
        """get User object, return its fields name and value"""
        context = kwargs.get("object").__dict__
        context.pop("_state")  # ModelState object
        context.update(self.default_context)
        return context

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context.update(self.default_context)
        return context


class SomeDeleteView(DeleteView):
    model = User
    default_context = {"bodyclass": "delete"}

    def get_success_url(self):
        return reverse("template_view")

    def get_json_context(self, **kwargs):
        """get User object, return its fields name and value"""
        return self.default_context

    def get_context_data(self, **kwargs):
        context = super(DeleteView, self).get_context_data(**kwargs)
        context.update(self.default_context)
        return context
