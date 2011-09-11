from django import forms

from models import User


class SomeForm(forms.ModelForm):

    class Meta:
        model = User
