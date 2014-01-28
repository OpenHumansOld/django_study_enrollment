from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from study_enrollment.utils import requirements_needed

class ReqsMetMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not requirements_needed(request):
            return super(ReqsMetMixin, self).dispatch(request, *args, **kwargs)
        messages.add_message(
            request, messages.ERROR, 
            'Please first complete our study requirements ' +
            'questionnaire to see if you qualify.')
        return HttpResponseRedirect(reverse('requirements'))


class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
        messages.add_message(
            request, messages.ERROR, 
            'Please create an account or log in to continue')
        return HttpResponseRedirect(reverse('registration_register'))
