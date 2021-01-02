from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import resolute


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]

        def save(self, commit=True):
            user = super(RegistrationForm, self).save(commit=False)

            if commit:
                user.save()
            return user


class ResolutionForm(forms.ModelForm):
    class Meta:
        model = resolute
        fields = ['title', 'body', 'expires']

class ResolutionGetForm(forms.Form):
    offset = forms.IntegerField(min_value=0)
    limit = forms.IntegerField(min_value=1)
