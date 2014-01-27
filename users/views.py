from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from registration import signals
from registration.models import RegistrationProfile
from registration.backends.default.views import RegistrationView as BaseRegistrationView
from registration.backends.default.views import ActivationView

from users.forms import RegistrationForm

class RegistrationView(BaseRegistrationView):
    """
    A registration view with the following workflow:
    1. User signs up with email as username, inactive account is created.
    2. Email is sent to user with activation link.
    3. User clicks activation link, account is now active.
    """
    def register(self, request, **cleaned_data):
        """
        Adapted from the django-registration default backend.
        """
        email, password = cleaned_data['email'], cleaned_data['password1']
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = RegistrationProfile.objects.create_inactive_user(email, email,
                                                                    password, site)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user
