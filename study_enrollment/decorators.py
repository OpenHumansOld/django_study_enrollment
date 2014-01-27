from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from study_enrollment.models import ActiveEnrollmentSet, UserEnrollment

def is_eligible(f):

    @wraps(f)
    def wrapper(request, *args, **kwds):
        if request.user.is_authenticated():
            user_enrollment, _ = UserEnrollment.objects.get_or_create(user=request.user)
            if not user_enrollment.is_eligible:
                if request.session.get('study_enrollment_eligible'):
                    # If user has just created an account, transfer session data.
                    user_enrollment.is_eligible = True
                    user_enrollment.save()
                    del request.session['study_enrollment_eligible']
                else:
                    # Direct user to check requirements.
                    return HttpResponseRedirect(reverse('requirements'))
        else:
            if request.session.get('study_enrollment_eligible'):
                # Direct user to create an account.
                return HttpResponseRedirect(reverse('registration_register'))
            else:
                # Direct user to complete requirements.
                return HttpResponseRedirect(reverse('requirements'))

        # Users that are both logged in and eligible get here.
        return f(request, *args, **kwds)

    return wrapper
