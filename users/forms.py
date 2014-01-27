from django import forms
from registration.forms import RegistrationForm
from django.contrib.auth.models import User
from django.core.validators import validate_email

class RegistrationForm(forms.Form):
    """
    Form for registering a new user account for an email address.
    
    Validates that the requested email is not already in use, and
    requires the password to be entered twice to catch typos.

    """
    email = forms.EmailField(widget=forms.EmailInput,
                             label="E-mail")
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label="Password (confirm)")
    
    def clean_email(self):
        """
        Validate that the email is not already in use.

        """
        existing = User.objects.filter(username__iexact=self.cleaned_data['email'])
        if existing.exists():
            raise forms.ValidationError("A user with that email already exists.")
        else:
            return self.cleaned_data['email']

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("The two password fields didn't match.")
        return self.cleaned_data
