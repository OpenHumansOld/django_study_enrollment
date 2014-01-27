from django.contrib.auth.models import User, check_password
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import View, TemplateView
from study_enrollment.models import ActiveEnrollmentSet, Requirement, UserEnrollment
from study_enrollment.decorators import is_eligible


class BaseEnrollmentView(View):
    def _admin_pwd_changed(self, default_account):
        # If the password matches "study_admin", it hasn't been changed.
        if check_password('study_admin', default_account.password):
            return False
        else:
            return True

    def _transfer_eligibility_info(self, request):
        if request.session.get('study_enrollment_eligible'):
            self.user_enrollment.is_eligible = True
            del request.session['study_enrollment_eligible']

    def dispatch(self, request, *args, **kwargs):
        """
        Wrapper that checks system set up and loads:
          -  self.enrollment_set (always)
          -  self.requirements (if self.enrollment_set.use_req_list is True)
          -  self.user_enrollment (if user.is_authenticated() is True)

        """
        try:
            default_account = User.objects.get(username='study_admin')
        except User.DoesNotExist:
            return HttpResponse("If you're seeing this message, it's because " +
                                "the study_admin account doesn't exist -- " +
                                "probably because the initialize_data.yaml " +
                                "fixture hasn't been loaded.")
        if not self._admin_pwd_changed(default_account):
            return render(request, 'study_enrollment/system_needs_set_up.html')
        active_enrollment_set = ActiveEnrollmentSet.objects.all()
        if len(active_enrollment_set) != 1:
            return HttpResponse("Problem with database! One and only one ActiveEnrollmentSet should exist.")
        self.enrollment_set = active_enrollment_set[0]
        if self.enrollment_set.use_req_list:
            self.requirements = Requirement.objects.filter(req_list=self.enrollment_set.req_list)
        if request.user.is_authenticated():
            self.user_enrollment, _ = UserEnrollment.objects.get_or_create(user=request.user)
            self._transfer_eligibility_info(request)
            self.user_enrollment.save()

        # Remainder as in django.views.generic.base
        return super(BaseEnrollmentView, self).dispatch(request, *args, **kwargs)


class IndexView(BaseEnrollmentView):
    def get(self, request, *args, **kwargs):
        reqs_needed = ((request.user.is_authenticated() and self.user_enrollment.is_eligible) or
                       request.session.get('study_enrollment_eligible'))
        print reqs_needed
        not_logged_in = not request.user.is_authenticated()
        return render(request, 'study_enrollment/index.html', {'reqs_needed': reqs_needed,
                                                               'not_logged_in': not_logged_in})


class EnrollmentTemplateView(BaseEnrollmentView, TemplateView):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class RequirementsView(BaseEnrollmentView):
    def get(self, request, *args, **kwargs):
        if not self.enrollment_set.use_req_list:
            return HttpResponseRedirect('/start')
        if not self.requirements:
            return render(request, 'study_enrollment/requirements_need_set_up.html')
        requirement_choices = [req.requirementchoice_set.all() for req in self.requirements]
        req_items = [ {'requirement': self.requirements[x],
                       'req_choices': requirement_choices[x]}
                      for x in range(len(self.requirements)) ]
        return render(request, 'study_enrollment/requirements.html',
                      { 'req_items': req_items } )

    def post(self, request, *args, **kwargs):
        if not self.enrollment_set.use_req_list:
            return HttpResponseRedirect('/start')
        failed_questions = []
        for req in self.requirements:
            req_choices = req.requirementchoice_set.all()
            choice = req.requirementchoice_set.get(answer=request.POST[req.question])
            if not choice.is_eligible:
                failed_questions.append({'requirement': req, 'choice': choice})
        if failed_questions:
            return render(request, 'study_enrollment/not_eligible.html', { 'reqs_failed': failed_questions })
        else:
            if request.user.is_authenticated():
                user_enrollment, _ = UserEnrollment.objects.get_or_create(user=request.user)
                user_enrollment.is_eligible = True
                user_enrollment.save()
            else:
                request.session['study_enrollment_eligible'] = True
            return HttpResponseRedirect(reverse('requirements_passed'))


class StartView(BaseEnrollmentView):

    @method_decorator(is_eligible)
    def dispatch(self, request, *args, **kwargs):
        return super(StartView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponse("Page for starting enrollment exam.")
