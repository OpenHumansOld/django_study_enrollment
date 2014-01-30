from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from registration import signals
from registration.models import RegistrationProfile
from registration.backends.default.views import RegistrationView as BaseRegistrationView
from registration.backends.default.views import ActivationView

from users.forms import RegistrationForm

from study_enrollment.mixins import ReqsMetMixin
from study_enrollment.models import UserEnrollment

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


class EnrollmentRegistrationView(ReqsMetMixin, RegistrationView):
    """
    A customization of RegistrationView for use with study_enrollment

    In this implementation, study requirements must be met before
    the user is invited to create an account.

    """
    def register(self, request, **cleaned_data):
        new_user = super(EnrollmentRegistrationView, self).register(request, **cleaned_data)
        # Get or create a new UserEnrollment and add is_eligible = True
        user_enrollment, _ = UserEnrollment.objects.get_or_create(user=request.user)
        user_enrollment.is_eligible = True
        user_enrollment.save()
        del request.session[IS_ELIGIBLE_FLAG]
